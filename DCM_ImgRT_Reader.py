"""
@author: zhenwei.shi, Maastro

eg:
import DCM_ImgRT_Reader
	
path1=r'c:\ABC\FolderContainingDicomOfLungCTscan'
path2=r'c:\ABC\FolderContainingDicomOfRTstruct'
DCM_ImgRT_Reader(img_path=path1,rtstruct_path=path2,ROI)

"""

import dicom,os
import numpy as np
from skimage import draw
import SimpleITK as sitk
import re


#class DcmRTstruct_Reader:
def ROI_ref(rtstruct_path,ROI_name):
    mask_vol = Read_RTSTRUCT(rtstruct_path)
    M= mask_vol[0]
    for i in range(len(M.StructureSetROISequence)):
        if str(ROI_name)==M.StructureSetROISequence[i].ROIName:
            ROI_number = M.StructureSetROISequence[i].ROINumber
            break
    return int(ROI_number)

def match_ROIid(rtstruct_path,ROI_number): 
    mask_vol = Read_RTSTRUCT(rtstruct_path)
    M= mask_vol[0]                                           
    for j in range(len(M.StructureSetROISequence)):
		if ROI_number == M.ROIContourSequence[j].RefdROINumber:
			break
    return j
	
def ROI_match(ROI,rtstruct_path):
    mask_vol=Read_RTSTRUCT(rtstruct_path)
    M=mask_vol[0]
    target = []
    for i in range(0,len(M.StructureSetROISequence)):
        if re.search(ROI,M.StructureSetROISequence[i].ROIName):
            target.append(M.StructureSetROISequence[i].ROIName)		
    if len(target)==0:
        for j in range(0,len(M.StructureSetROISequence)):
            print M.StructureSetROISequence[j].ROIName
            break
        print 'Input ROI is: '
        ROI_name = raw_input()
        target.append(ROI_name)
    print '------------------------------------'
    return target

def Read_scan(path):
    scan = [dicom.read_file(path + '\\' + s) for s in os.listdir(path)]
    scan.sort(key = lambda x: int(x.InstanceNumber))  
    return scan

def Read_RTSTRUCT(path):
    scan = [dicom.read_file(path + '\\' + s) for s in os.listdir(path)] 
    return scan

def Read_CTscan(json_CT):
    img_list = []
    for i in range(len(json_CT)):
        img_list.append(str(json_CT[i]['location']))
    Imgs = [dicom.read_file(s) for s in img_list]
    Imgs.sort(key = lambda x: int(x.InstanceNumber))  
    return Imgs

def poly2mask(vertex_row_coords, vertex_col_coords, shape):
    fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
    mask = np.zeros(shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask

def get_pixels(scan):
    image = np.stack([s.pixel_array for s in scan])
    image = image.astype(np.int16)
#    image[image == -2000] = 0   
    intercept = scan[0].RescaleIntercept
    slope = scan[0].RescaleSlope
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)        
    image += np.int16(intercept)    
    return np.array(image, dtype=np.int16)

def Img_Bimask(img_path,rtstruct_path,ROI_name):
	# Volume of DICOM files and RTstruct files
    print 'Loading scans and RTstruct ......'

    img_vol = Read_scan(img_path)
    mask_vol=Read_RTSTRUCT(rtstruct_path)
	# Slices all have the same basic information including slice size, patient position, etc.
    L=img_vol[0]
    LP=get_pixels(img_vol)
    M=mask_vol[0]
    num_slice=len(img_vol)
    
    print 'Creating binary mask ......'

    mask=np.zeros([num_slice, L.Rows, L.Columns],dtype=np.uint8)
    
    xres=np.array(L.PixelSpacing[0])
    yres=np.array(L.PixelSpacing[1])
	
    ROI_number = ROI_ref(rtstruct_path,ROI_name)
    ROI_id = match_ROIid(rtstruct_path,ROI_number)

    for k in range(len(M.ROIContourSequence[ROI_id].ContourSequence)):
        UIDrt=''        

        UIDrt = M.ROIContourSequence[ROI_id].ContourSequence[k].ContourImageSequence[0].ReferencedSOPInstanceUID
        
        for i in range(num_slice):
            UIDslice = img_vol[i].SOPInstanceUID
            
            if UIDrt==UIDslice:
                sliceOK = i
                break
				
        x=[]
        y=[]
        z=[]
        
        m=M.ROIContourSequence[ROI_id].ContourSequence[k].ContourData
                              
        for i in range(0,len(m),3):
            x.append(m[i+1])
            y.append(m[i+0])
            z.append(m[i+2])
        
        x=np.array(x)
        y=np.array(y)
        z=np.array(z)
    
        x-= L.ImagePositionPatient[1]
        y-= L.ImagePositionPatient[0]
        z-= L.ImagePositionPatient[2]

        pts = np.zeros([len(x),3])	
        pts[:,0] = x
        pts[:,1] = y
        pts[:,2] = z
        a=0
        b=1
        p1 = xres;
        p2 = yres;
          
        m=np.zeros([2,2])             
        m[0,0]=img_vol[sliceOK].ImageOrientationPatient[a]*p1 
        m[0,1]=img_vol[sliceOK].ImageOrientationPatient[a+3]*p2
        m[1,0]=img_vol[sliceOK].ImageOrientationPatient[b]*p1
        m[1,1]=img_vol[sliceOK].ImageOrientationPatient[b+3]*p2
    
        # Transform points from reference frame to image coordinates
        m_inv=np.linalg.inv(m)
        pts = (np.matmul((m_inv),(pts[:,[a,b]]).T)).T
        mask[sliceOK,:,:] = np.logical_or(mask[sliceOK,:,:],poly2mask(pts[:,0],pts[:,1],[LP.shape[1],LP.shape[2]]))
          
        LP-=np.min(LP)
        LP=LP.astype(np.float32)
        LP/=np.max(LP)
        LP*=255
        
        Img=sitk.GetImageFromArray(LP.astype(np.float32))
        Mask=sitk.GetImageFromArray(mask)
        
    return Img, Mask