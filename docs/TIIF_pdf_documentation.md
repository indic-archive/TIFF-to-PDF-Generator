# TIFF PDF Converter Documentation

## Install Setup

1. Run Installer

![](pics/Pictures/100000000000021E000001A59D9B2F85C496A382.png)

Click Install.

2. Install Ghostscript when new window appears.

![](pics/Pictures/1000000000000220000001A595DA6A46C1271E37.png)


3. Finish Ghostscript installation. Make sure “Generate cidfmap for
Windows CJK TrueType fonts” clicked.

![](pics/Pictures/10000001000001FE00000192855156B278BE2C93.png)
  
  

![](pics/Pictures/10000000000002110000019581B26443A89AF153.png)


4.Finish Installation and open TIFF PDF Generator.

## Usage

![](pics/Pictures/10000000000001A4000001F7FC3CF4B584D7BCB0.png")



1. Select the folder in which TIFF files exist using **Select Image
Folder **option. (Sometimes the folder looks empty. TIFF files won’t be
shown.)

![](pics/Pictures/100000000000041A0000021ACB7A7BDB13A24739.png)


2. When the folder is chosen, the folder path appears in the UI and
also number of files in the folder will be listed there (as shown in
rectangle).

![](pics/Pictures/10000001000001BC000001F4A6BA49A00FD575B0.png)
  
  
  
3. Select **Custom DPI **from **Select Resize
Option**.

![](pics/Pictures/10000000000001D1000002155EBB5BCCC849D18E.png)
   
 
  
4. Enter required DPI (prefered DPI is
250).

![](pics/Pictures/10000000000001B6000001F89E578F2353323AED.png)


5. Choose proper Print Option (Use *default* for usual cases). For
higher quality, use *prepress*. For very low quality, use *ebook*.

![](pics/Pictures/10000000000001AD000001DE019E4CCCF996FD8F.png)
  
   

6. Now click **Convert.**

The progressbar will show 50% when *img2pdf* run successfully. It will
show 100% when completed conversion and status bar will show
successfully converted message with file path.

![](pics/Pictures/10000000000001B2000001E999097A98EAB28389.png)
![](pics/Pictures/10000000000001B60000021D95483EC84E05DD15.png)
![](pics/Pictures/10000000000001B5000001F256A25F22B3BDCB04.png)


You can see two outputs in the TIFF folder – output.pdf, which is a
combined pdf with large size and resized_output.pdf, which is resized to
specified DPI.  

![](pics/Pictures/10000000000002A90000012A8A34155530F9B480.png)
   

# Troubleshooting

### Check Ghostscript installation

Open cmd (command prompt). Run **gswin64c.**

![](pics/Pictures/10000001000004070000022EC2FE4D35D5600B65.png)
  
  
  
Output will show **GS\> ** along with version of Ghostscript.

If this command is not recognized, check ghostscipt installation path in
`C:\\Program Files\\gs\\gs10.0.40`.

If this folder is present and gswin64c is present inside bin folder in
above path, add path to environmental variable.

![](pics/Pictures/100000010000034F000000E9272DC8CC3CE946B3.png)
  
  
  
Steps:

Right click **This PC**. Open **Properties**. Window on right side will
show up.

![](pics/Pictures/100000010000048100000292EFFB6FD28931E105.png)
![](pics/Pictures/100000000000013B000001484D94AF9A3882A942.png)


Alternatively, open this from Settings/Control Panel \> System.

From there, open **Advanced System Settings** as shown in screenshot
above.

![](pics/Pictures/10000001000001AA000001F0DF48806290DEA243.png)



From **Advanced** Tab, choose **Environment Variables**. Now click on
**path** and click **Edit**.

![](pics/Pictures/10000001000002770000026A8D9AB217C53D22CA.png)
  
   

![](pics/Pictures/100000010000029700000281A91F2A9502608B7E.png)

Now click **New** and add path to
ghsotscript bin folder there (`C:\\Program Files\\gs\\gs10.0.40/bin`) and
click **OK**. The path will appear like below. Now check ghostscript
installation again from command prompt again. It will show the version
details.
