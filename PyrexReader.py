"""
###############################
@author: zhenwei.shi, Maastro##
###############################
Usage:
import PyrexReader
	
img_path = '.\CTscan'
rtstruct_path = '.\RTstruct'
ROI = Region Of Interest
Img,Mask = PyrexReader.Img_Bimask(img_path,rtstruct_path,ROI)

"""

import pydicom,os
import numpy as np
from skimage import draw
import SimpleITK as sitk
import re
import glob


# module PyrexReader:
def match_ROIid(rtstruct_path,ROI_name): # Match ROI id in RTSTURCT to a given ROI name in the parameter file
    mask_vol = Read_RTSTRUCT(rtstruct_path)
    M= mask_vol[0]
    for i in range(len(M.StructureSetROISequence)):
        if str(ROI_name)==M.StructureSetROISequence[i].ROIName:
            ROI_number = M.StructureSetROISequence[i].ROINumber
#            print(ROI_number)
            break
    for ROI_id in range(len(M.StructureSetROISequence)):
        if ROI_number == M.ROIContourSequence[ROI_id].ReferencedROINumber:
#            print(ROI_number)
            break
    return ROI_id

def ROI_match(ROI,rtstruct_path): # Literal match ROI
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
        print('Input ROI is: ')
        ROI_name = raw_input()
        target.append(ROI_name)
    print '------------------------------------'
    return target

def Read_scan(path): # Read scans under the specified path 
    scan = [pydicom.dcmread(s, force=True) for s in glob.glob(os.path.join(path,'*.dcm'))]
    try:
        scan.sort(key = lambda x: int(x.ImagePositionPatient[2])) # sort slices based on Z coordinate
    except:
        print('AttributeError: Cannot read scans')
    return scan

def Read_RTSTRUCT(path): # Read RTSTRUCT under the specified path
    try:
        rt = [pydicom.dcmread(s, force=True) for s in glob.glob(os.path.join(path,'*.dcm'))]
    except:
        print('AttributeError: Cannot read RTSTRUCT')
    return rt


def poly2mask(vertex_row_coords, vertex_col_coords, shape): # Mask interpolation
    fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
    mask = np.zeros(shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask

def get_pixels_hu(scans): # Units to Hounsfield Unit (HU) by multiplying rescale slope and add intercept
    image = np.stack([s.pixel_array for s in scans])
    image = image.astype(np.int16) #convert to int16
    # the code below checks if the image has slope and intercept
    # since MRI images often do not provide these
    try:
        intercept = scans[0].RescaleIntercept
        slope = scans[0].RescaleSlope
    except AttributeError:
        pass
    else:
        if slope != 1:
            image = slope * image.astype(np.float64)
            image = image.astype(np.int16)        
        image += np.int16(intercept)    
    return np.array(image, dtype=np.int16)

def Img_Bimask(img_path,rtstruct_path,ROI_name): # generating image array and binary mask
    print('Generating binary mask from RTSTRUCT...')
    img_vol = Read_scan(img_path)
    mask_vol=Read_RTSTRUCT(rtstruct_path)

    IM=img_vol[0] # Slices usually have the same basic information including slice size, patient position, etc.
    IM_P=get_pixels_hu(img_vol)
    M=mask_vol[0]
    num_slice=len(img_vol)
    mask=np.zeros([num_slice, IM.Rows, IM.Columns],dtype=np.uint8)
    xres=np.array(IM.PixelSpacing[0])
    yres=np.array(IM.PixelSpacing[1])
    ROI_id = match_ROIid(rtstruct_path,ROI_name)
    #Check DICOM file Modality
    if IM.Modality == 'CT' or 'PT':
		for k in range(len(M.ROIContourSequence[ROI_id].ContourSequence)):    
			Cpostion_rt = M.ROIContourSequence[ROI_id].ContourSequence[k].ContourData[2]
#			print(Cpostion_rt)
            
			for i in range(num_slice):
				if Cpostion_rt == img_vol[i].ImagePositionPatient[2]: # match the binary mask and the corresponding slice
					sliceOK = i
					break
#			print('Slice:',sliceOK)
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
#			print('point-2')
			x-= IM.ImagePositionPatient[1]
			y-= IM.ImagePositionPatient[0]
			z-= IM.ImagePositionPatient[2]
			pts = np.zeros([len(x),3])  
			pts[:,0] = x
			pts[:,1] = y
			pts[:,2] = z
			a=0
			b=1
			p1 = xres
			p2 = yres
			m=np.zeros([2,2])             
			m[0,0]=img_vol[sliceOK].ImageOrientationPatient[a]*p1 
			m[0,1]=img_vol[sliceOK].ImageOrientationPatient[a+3]*p2
			m[1,0]=img_vol[sliceOK].ImageOrientationPatient[b]*p1
			m[1,1]=img_vol[sliceOK].ImageOrientationPatient[b+3]*p2
#			print('point-3') 
         # Transform points from reference frame to image coordinates
			m_inv=np.linalg.inv(m)
			pts = (np.matmul((m_inv),(pts[:,[a,b]]).T)).T
			mask[sliceOK,:,:] = np.logical_or(mask[sliceOK,:,:],poly2mask(pts[:,0],pts[:,1],[IM_P.shape[1],IM_P.shape[2]]))
         
    elif IM.Modality == 'MR':
        slice_0 = img_vol[0]
        slice_n = img_vol[-1]

		 # the screen coordinates, including the slice number can then be computed 
		  # using the inverse of this matrix
        transform_matrix = np.r_[slice_0.ImageOrientationPatient[3:], 0, slice_0.ImageOrientationPatient[:3], 0, 0, 0, 0, 0, 1, 1, 1, 1].reshape(4, 4).T # yeah that's ugly but I didn't have enough time to make anything nicer
        T_0 = np.array(slice_0.ImagePositionPatient)
        T_n = np.array(slice_n.ImagePositionPatient)
        col_2 = (T_0 - T_n) / (1 - len(img_vol))
        pix_s = slice_0.PixelSpacing
        transform_matrix[:, -1] = np.r_[T_0, 1] 
        transform_matrix[:, 2] = np.r_[col_2, 0] 
        transform_matrix[:, 0] *= pix_s[1]
        transform_matrix[:, 1] *= pix_s[0]
        
        transform_matrix = np.linalg.inv(transform_matrix)
#        print('point-1')
        for s in M.ROIContourSequence[ROI_id].ContourSequence:    
			Cpostion_rt = np.r_[s.ContourData[:3], 1] # the ROI point to get slice number from
													  # in homogenous coordinates

			roi_slice_nb = int(transform_matrix.dot(Cpostion_rt)[2]) # the slice number according to the 
																	 # inverse transform
			for i in range(num_slice):
				print(roi_slice_nb, i)
				if roi_slice_nb == i:
					sliceOK = i
					break
			x=[]
			y=[]
			z=[]			                            
			m=s.ContourData
			for i in range(0,len(m),3):
				x.append(m[i+1])
				y.append(m[i+0])
				z.append(m[i+2])
    	
			x=np.array(x)
			y=np.array(y)
			z=np.array(z)
#			print('point-2')
			x-= IM.ImagePositionPatient[1]
			y-= IM.ImagePositionPatient[0]
			z-= IM.ImagePositionPatient[2]
			pts = np.zeros([len(x),3])	
			pts[:,0] = x
			pts[:,1] = y
			pts[:,2] = z
			a=0
			b=1
			p1 = xres
			p2 = yres
			m=np.zeros([2,2])             
			m[0,0]=img_vol[sliceOK].ImageOrientationPatient[a]*p1 
			m[0,1]=img_vol[sliceOK].ImageOrientationPatient[a+3]*p2
			m[1,0]=img_vol[sliceOK].ImageOrientationPatient[b]*p1
			m[1,1]=img_vol[sliceOK].ImageOrientationPatient[b+3]*p2
#			print('point-3') 
			# Transform points from reference frame to image coordinates
			m_inv=np.linalg.inv(m)
			pts = (np.matmul((m_inv),(pts[:,[a,b]]).T)).T
			mask[sliceOK,:,:] = np.logical_or(mask[sliceOK,:,:],poly2mask(pts[:,0],pts[:,1],[IM_P.shape[1],IM_P.shape[2]]))

    IM_P-=np.min(IM_P)
    IM_P=IM_P.astype(np.float32)
    IM_P/=np.max(IM_P)
    IM_P*=255
        
    Img=sitk.GetImageFromArray(IM_P.astype(np.float32)) # convert image_array to image
    Mask=sitk.GetImageFromArray(mask)
    
#    image_file_name='pyrex_image.nrrd'
#    mask_file_name='pyrex_mask.nrrd' 
#        
#    sitk.WriteImage(Img,image_file_name) # save image and binary mask locally
#    sitk.WriteImage(Mask,mask_file_name)
    return Img, Mask      
