# import gmplot package 
import gmplot 
  
# GoogleMapPlotter return Map object 
# Pass the center latitude and 
# center longitude 
gmap1 = gmplot.GoogleMapPlotter(-15.80423, 
                                -47.9526007, 17, 'AIzaSyDK_hPqU0_GSURBCDQ-KoSadNzSfVCg9PM' ) 
  
# Pass the absolute path 
gmap1.draw( "C:\\tmp\\Python\\proj\\mapas\\map11.html" ) 
