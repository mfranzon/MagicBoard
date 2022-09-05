# Magic Board
Magic Board is a PoC using stable diffusion.

Dashboard to draw or upload an image and modify with the power of stable diffusion.
Select the number of steps and the strength to generate the final image. 

![Screen dashboard](./magic.png)


The final result is : 
<p style="text-align:center;"><img src="./result.png" width="200"/></p>


NOTE:

This implementation use a `torch.float16` due to low VRAM available. Strongly suggest to set it `torch.float32` to speed up the computation. [Here](./utils.py)