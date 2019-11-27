
####################################

'''
NFTS - National Film and Television School.
latest update: 2019-11-07
'''

####################################

import nuke, os, sys

# Make all filepaths load without errors regardless of OS (No Linux support and no C: support)


def myFilenameFilter(filename):
	

	#conversions form win to macos

    if nuke.env['MACOS']:


        filename = filename.replace( 'Z:/','/Volumes/2018-2019/' ) # dfx server
        filename = filename.replace( '//digitalfxservers/2018-2019/','/Volumes/2018-2019/' ) # dfx server
        filename = filename.replace( 'Y:/','/Volumes/2019-2020/' ) # dfx server
        filename = filename.replace( '//digitalfxservers/2019-2020/','/Volumes/2019-2020/' ) # dfx server
        filename = filename.replace( '//digitalfxserver/DEFX/','/Volumes/DEFX/' ) # old dfx server
        filename = filename.replace( '//digitalfxserver/StockFootageLibrary/','/Volumes/StockFootageLibrary/' ) # stock footage lib   
        filename = filename.replace( '//digitalfxserver/CompEnvironment/','/Volumes/CompEnvironment/' ) # comp env



    #conversions form macos to win

    if nuke.env['WIN32']:


        filename = filename.replace( '/Volumes/2018-2019/','Z:/' ) # dfx server
        filename = filename.replace( '/Volumes/2019-2020/','Y:/' ) # dfx server
        filename = filename.replace( '/Volumes/DEFX/','//digitalfxserver/DEFX/' ) # old dfx server
        filename = filename.replace( '/Volumes/StockFootageLibrary/','//digitalfxserver/StockFootageLibrary/' ) # stock footage lib   
        filename = filename.replace( '/Volumes/CompEnvironment/','//digitalfxserver/CompEnvironment/' ) # comp env

        filename = filename.replace( '/Volumes/GraAnim19-TheUnknown/','//AvidISIS/GraAnim19-TheUnknown/' ) # gran anim
        filename = filename.replace( '/Volumes/GraAnim19-Daniel/','//AvidISIS/GraAnim19-Daniel/' ) # gran anim
        filename = filename.replace( '/Volumes/GraFic19-Voce/','//AvidISIS/GraFic19-Voce/' ) # gran fic

        



    return filename



nuke.addFilenameFilter(myFilenameFilter)


