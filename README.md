# NFTS NUKE ENVIRONMENT

<h2>General Information</h2>

This repository contains the custom tools, pipelines and default gizmos for Nuke, Nuke Studio and Hiero that I have created for the National Film and TV School, DFX Department. It contains both original scripts that I have written and third party scripts, modified and implemented to suite the school needs. (These are marked with a * in the description's title). 

This repo can be copied to a network shared drive and all machines that need access to it must have the environment variables <code>NUKE_PATH</code> and <code>HIERO_PLUGIN_PATH</code> pointing to the shared volume.

The root to the NFTS Environment is also saved in the <code>NFTS_COMP_ENV_ROOT</code> session  environment variable, to be used withing the configurations. Please use this variable rather than hard-coding the path.

Locally the NFTS Environment can be reached at <code>\\\\digitalfxserver\VFX\Shared\NFTS_nuk_env</code> on Windows Machines and mounted <code>/Volumes/VFX/Shared/NFTS_nuk_env</code> on MacOS.

OS sensitive plugins such as 3DEqualizer and KeenTools are installed using helper scripts and attention should be paid to run the same versions on every OS. If a new version needs to be installed, please follow the convention set by the currently installed tools.

<h4>BEST PRACTICES</h4>
Due to the nature of the work Gizmos should be installed as groups. This allows being able to easily move nuke scripts to outside the school. This also means that any update to the available plugin will not affect old scripts, ensuring that backwards compatibility is always retained.

<h2>Custom Pipeline</h2>

Most of the custom pipeline is designed to work on fully set-up shots. Meaning it will kick in if both the nuke script is saved and a version number is present in a write node's file name.

<h4>CODE STRUCTURE</h4>
The core pipeline tools are stored the <code>$NUKE_PATH/NFTS_pipe</code> folder. Any code added to this root will be added to the NukePluginPath.
It's divided ina few helper scripts, their functions is documented inside the relative docstring:

<ul>
  <li>init.py</li>
  <li>menu.py</li>
  <li>artifacting.py</li>
  <li>callback_manager.py</li>
  <li>post_processing.py</li>
  <li>tools_loader.py</li>
  <li>versioning.py</li>
</ul>

<h4>INCREMENTAL SAVE</h4>

Callbacks have been installed at <code>OnScriptSave</code>. This ensures that every Write and DeepWrite node's version number, will always match the script's, ensuring that it's always possible to re-generate the output by re-rendering script with matching version.

<h4>WRITE NODES AND ARTIFACTS</h4>

To ensure that scripts are not overwritten after a render, Nuke will also prompt the user to save an incremental of the script. Artifacts will also be created upon render.
This is implemented by adding <code>AfterRender</code> callbacks via the <i>callback_manager</i> tool. </br></br>
When rendering form within a fully setup shot, Nuke will automatically create a copy of the script in the location where it's saved, adding the <i>_artifact</i> suffix the file name. This ensures that it's always possible to restore the script that rendered a specific output.</br>
Artifacts are not meant to be used to continue with the work. For that reason a prompt will ask if you are sure to continue when opening one. Selecting NO will close the artifact script.
This is implemented by adding <code>AfterRender</code> callbacks via the <i>callback_manager</i> tool.

<h4>MAKE JPEGS FROM READ NODE</h4>

It's often useful to convert plates/assets to a JPEG sequence for for reference purposed/passing on to CG.
A shortcut has been added to top menubar, under <code>NFTS/Make JPEGs from selected Reads</code> to automate the process. </br>
This will auto-create JPEG sequence in the same folder as the source data of the read node, in a <code>/jpegs</code> subfolder. The script will attempt to assign one of the following colourspaces (if available) based on the order of preference.
<ol>
  <li>review (OCIO role)</li>
  <li>Output - Rec.709</li>
  <li>BT1886</li>
  <li>default (OCIO role)</li>
</ol>
Note that the main assumption is that OCIO has  been configured, and it works best in an ACES configuration. In case some issue with setting up the JPEGs write node, the script will skip the automatic nodes cleanup operations and move on to the next in the selection.
This tool bypasses <code>AfterRender</code> callbacks.

<h4>CENTRALLY INSTALLING NEW GIZMOS</h4>
Installing new gizmos should not be taken lightly. They should be thoroughly tested before pushing them centrally.
To reduce the potential issue crated by editing the configuration files, the <i>Tool Loader</i> will scan specific folders and automatic mirror the structure of the tools in the nuke menu. </br>The tools expects files ending in <i>.gizmo</i> or <i>.nk</i> for gizmos, and <i>.png</i> for the relative icons. It will try to assign to every gizmo the icon with a matching name (if found in the same folder).
</br>The <code>$NUKE_PATH/NFTS_tools</code> folder is already set-up for auto loading.

<h2>Custom Tools and Shortcuts</h2>

<h4>NFTS COPY PASTE</h4>

The NFTS Copy paste is a quick way to copy data between different scrips on different machines.
It is possible to initialize the share the selected nodes by navigating to <b>NFTS Share/Share Selected Nodes</b> (Alt+Shift+C). Nodes are then easy to paste by selecting <b>NFTS Share/Paste Shared Nodes</b> (Alt+Shift+V). </br>
The shared data is stored on a file located at <code>$NUKE_PATH/NFTS_CopyPaste_Data.nk</code> that gets overwritten every time that a user copies something new.
This is done through the functions <code>nftsCopy()</code> and <code>nftsPaste()</code>.

<h4>SHARED TOOLSETS*</h4>

It's best to touch the central configuration as little as possible. Therefore to allow for easy publication of simple toolsets and even groups, "Shared Toolsets" can be used. 
This allows users to select some nodes or groups from the nodegraph and publish them for everyone to use, modify and eventually delete; using the relative options in the SharedToolsets Menu.
Data is stored in <code>$NUKE_PATH/SharedToolSets</code>.

<h4>NUKE STUDIO / HIERO TOOLS</h4>

There's a small collection of Hiero tools available.
Safe for custom tokens or Export Presets they are all available in the <code>NFTS/NFTS Hiero Tools</code> menu.
<ul>
  <li><strong>Presets/Reset Environment Presets</strong> - Replaces the centrally installed presets for the current hiero version with <code>NFTS_Safe_TaskPresets</code></li>
    <li><strong>Presets/Remove All User Presets</strong> - Removes the TaskPresets stored in <code>~/.nuke/TaskPresets</code></li>
  <li><strong>Change Clip FPS</strong> - Reinterprets the framerate of the selected clip(s) in the media bin</li>
  <li><strong>Custom <i>{project_code}</i> token</strong> - A three letter project code auto-generated using the hiero project name</li>
  <li><strong>Custom Tokens for <i>{width}</i>, <i>{height}</i> and <i>{rez}</i></strong> - Returning respectively 1920, 1080 and 1920x1080 for a FullHD Clip</li>
</ul>

<h4>SHORTCUTS</h4>

<table>
  <tr>
    <td width="50%">
      <ul>
        <li>Keymix<i>V</i></li>
        <li>Expression <i>E</i></li>
        <li>Invert <i>Alt+Ctrl+I</i></li>
        <li>Premult <i>Alt+Shift+P</i></li>
        <li>Unpremult <i>Alt+Shift+U</i></li>
        <li>ChannelMerge <i>Shift+M</i></li>
        <li>TransformMasked <i>Shift+T</i></li>
      </ul>
    </td>
    <td width="50%">
      <ul>
        <li>Backdrops <i>Alt+B</i></li>
        <li>Read from Write <i>Shift+R</i></li>
        <li>Reveal file in Browser <i>Alt+Shift+R</i></li>
        <li>Label Shortcut <i>Shift+L</i></li>
        <li>Cycle Operations <i>Alt+X</i> and <i>Alt+Shift+X</i></li>
        <li>Toggle <code>nuke.executing()</code> in the Disable Knob <i>Alt+D</i></li>
      </ul>
    </td>
  </tr>
</table>

<h2>Scripts</h2>

To allow the fast setup of directories and Environment Variables, bat and bash scripts have been created.

<h4>ENVIRONMENT VARIABLES</h4>

There are two scripts available, one for Windows and one for MacOS.
<code>set_hiero_env_win.bat</code> (WIN) creates the permanent user variable <code>HIERO_PLUGIN_PATH</code> and directs it to the environment while <code>set_nuke_hiero_env_mac.command</code> (MAC) creates temporary <code>HIERO_PLUGIN_PATH</code> and <code>NUKE_PATH</code> variables. The MAC script needs to be executed at startup to ensure a working setup or otherwise variables need to be defined in the <code>.plist</code> file. At the NFTS the variable <code>NUKE_PATH</code> should be already set by default on Windows machines.

<h2>Help and Documentation</h2>

Documentation is often available.
</br>This GitHub page is also accessible by accessing the <code>NFTS/Help/NFTS Environment Help</code> menu in the Nuke menu bar.
All the Nuke customizations are imported form <code>NFTShelp.py</code> and further instructions should be handled through that file.

<h2>Third Party Scripts and Plugins</h2>

In this repository third party scripts have been implemented, this is a list of them with links to the relative documentation.

<ul>
  <li>KeenTools <a href="https://keentools.io/download/plugins-for-nuke">official page</a></li>
  <li>3DEqualizer <a href="https://www.3dequalizer.com/?site=tech_docs">official page</a></li>
  <li>SharedToolsets <a href="http://www.nukepedia.com/python/ui/sharedtoolsets">official page</a></li>
  <li>NukeSurvivalToolkit <a href="https://github.com/CreativeLyons/NukeSurvivalToolkit_publicRelease">official page</a></li>
  <li>WrapItUp <a href="https://maxvanleeuwen.com/project/collect-nuke-scripts-wrapitup/">official page</a></li>
  <li>Switch to NukeX <a href="https://github.com/franklinvfx/NukeSwitch-Script-for-Nuke">official page</a></li>
  <li>AnimationMaker <a href="http://www.nukepedia.com/python/ui/animation-maker">official page</a></li>
  <li>Give me Python Selection for Hiero <a href="http://www.nukepedia.com/hiero/give-me-python-selection">official page</a></li>
  <li>Thumbnail Exporter <a href="http://www.nukepedia.com/hiero/python/thumbnail-exporter">official page</a></li>
</ul>


<h2>License and Copyright</h2>

By downloading a file from this repository you agree to the general license terms below.
</br>Copyright (c) 2010 till present. All rights reserved. Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
</br>
</br>THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOO/ OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
