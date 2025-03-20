import tifffile
from cellstitch_cuda.pipeline import cellstitch_cuda, correction

# img = r"Z:\Rheenen\tvl_jr\SP8\2025Mar6_2516017_DiLiCre-4mg-2d_2W_Ileum\2025Mar6_2516017_DiLiCre-4mg-2d_2W_Ileum-2\output.tif"
#
# cellstitch_cuda(
#     img,
#     output_masks=True,
#     verbose=True,
#     seg_mode="nuclei_cells",
#     interpolation=False,
#     n_jobs=1,
#     # z_step=3.5,
#     # pixel_size=1/2.2,
#     bleach_correct=True,
# )

masks = tifffile.imread(r"Z:\Rheenen\tvl_jr\SP8\2025Mar6_2516017_DiLiCre-4mg-2d_2W_Ileum\2025Mar6_2516017_DiLiCre-4mg-2d_2W_Ileum-2\cellstitch_masks_pre-correction.tif")

masks = correction(masks, outpath=r"E:\Tom", n_jobs=-1)

tifffile.imwrite(r"Z:\Rheenen\tvl_jr\SP8\2025Mar6_2516017_DiLiCre-4mg-2d_2W_Ileum\2025Mar6_2516017_DiLiCre-4mg-2d_2W_Ileum-2\cellstitch_masks.tif", masks)
