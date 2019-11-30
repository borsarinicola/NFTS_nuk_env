# NFTS NUKE ENVIRONMENT

<h2>General Infromations</h2>

This repository contains the custom tools, pipelines and default gizmos for Nuke, Nuke Studio and Hiero at the National Film and TV School, DFX Department. It contains both oringal and third party scripts that have been implemented to suite the school needs. (These are marked with a * in the description's title).

This repo can be copied to a network shared drive and all machines that need access to it must have the environment variables <code>NUKE_PATH</code> and <code>HIERO_PLUGIN_PATH</code> pointing to the shared volume.

Locally the NFTS Envirnoment can be reached at <code>//digitalfxserver/CompEnvironment/</code> on Windows Machines and mounted <code>/Volumes/CompEnvironment</code> on MacOS. Paths in third party code is often implemented explicitely.

OS sensitive plugins such as 3DEqualizer and KeenTools are loaded using conditional statements and attention should be paid to run the same versions on every OS.

<h4>BEST PRACTISES</h4>
Due to the nature of the work Gizmos should not be installed as groups. This allows being able to easily move nuke scripts to outside the school. This also means that any update to the available plugin will not affect old scripts, ensuring that backwards compatibility is always retained.

<h2>Custom Pipeline</h2>

All the definitions that I'm about to mention will act only if both the nuke script is saved and a version number is present in the file name.

<h4>INCREMENTAL SAVE</h4>

The default behaviour of the Incremental Save has been overwritten by the new function called <code>incrementalSave()</code>. This not only increases the version of the script, but also increments every Write and DeepWrite node in the script, ensuring that the render versions always match the script versions.

<h4>WRITE NODES</h4>

To ensure that scripts are not overwritten after a render, Nuke will also ask whether to save an incremental of the script after the render has been executed. Artifacts will also be created upon render.
These extra functionalities are implemented by changing the default values of the Python Knobs adding <code>writeBeforePipeline()</code> to <b>Before Render</b>and <code>writeAfterPipeline()</code> to <b>After Render</b>.

<h4>ARTIFACTS</h4>

When rendering form this customized version of Nuke the software automatically creates a copy of the script in the location where it's saved, adding <i>_artifact</i> at the end of the file name. This ensures that it's always possible to restore the script that rendered a specific output. Aritifacts are created only during GUI sessions. This is done using the <code>nuke.GUI</code> variable.

<h4>EXTERNAL WRITE NODES CONVERSION</h4>
When Write nodes have been generated either with NukeStudio or in a Nuke setup where the pipeline is not available, the Before and After Render behaviours will not be in place.
To ensure that "standard rite nodes" are converted in "pipeline write nodes", the function <code>incrementalSave()</code> has also been implemented to change the necessary python knobs on script save. 

<h4>CUSTOM PIPELINE WITH DEADLINE</h4>
Deadline renders run in the non-GUI version of Nuke. Therefore artifacts must be created at submission time.
This is achieved with the <code>advencedSubmission()</code> function. This will first run a script save <code>nuke.scriptsave()</code>, folowed by the standard Deadline Submission function <code>DealineNukeClient.main()</code> and upon succes of the last step the <code>createArtifact()</code>. 
This also ensures that artifacts are generated only once and not every time that a Deadline render task is initialized.

<h4>NETWORK DRIVE REMAPPING</h4>
Often it is necessary to access nuke scritps form a diffrerent OS. To nesure that all the schoold servers and ISIS volumes are available indipendently form the OS file paths can be handled from the file <code>network_drive_remapping.py</code>.

<h2>Custom Tools and Shortcuts</h2>

<h4>NFTS COPY PASTE</h4>

The NFTS Copy paste is a quick way to copy data between different scrips on different machines.
It is possible to initialize the share the selected nodes by navigating to <b>NFTS Share/Share Selected Nodes</b> (Alt+Shift+C).
</br>Nodes are then easy to paste by selecting <b>NFTS Share/Paste Shared Nodes</b> (Alt+Shift+V).
The shared data is stored on a file located at <code>%NUKE_PATH%/NFTS_CopyPaste_Data.nk</code> that gets overwritten every time that a user copies something new.
This is done through the functions <code>nftsCopy()</code> and <code>nftsPaste()</code>.

<h4>SHARED TOOLSETS*</h4>

User do not have permissions to modify the data on the Environment. Therefore to allow for easy publication of simple toolsets and gizmos "Shared Toolsets" can be used. 
This allows users to select some nodes or groups from the nodegraph and publish them for everyone to use, modify and eventually delete; using the relative options in the SharedToolsets Menu.
Data is stored in <code>%NUKE_PATH%/SharedToolSets</code>. Permissions for this folder have been modified to allow users read and write access. All data contained in here is editable, exception made for the preloaded lens distortion toolsets. These nodes are crucial for efficient lens distortion workflows and users should not attempt to remove or modify them. Only groups should be published, Gizmos are not supported.

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
        <li>Submit to Deadline <i>Alt+R</i></li>
        <li>Toggle $Gui in the Disable Knob <i>Alt+D</i></li>
      </ul>
    </td>
  </tr>
</table>

<h2>SCRIPTS</h2>

To allow the fast setup of directories and Environment Variables, bat and bash scripts have been created.

<h4>ENVIRONMENT VARIABLES</h4>

There are two scripts available, one for Windows and one for MacOS.
<code>set_hiero_env_win.bat</code> (WIN) creates the permanent user variable <code>HIERO_PLUGIN_PATH</code> and directs it to the environment while <code>set_nuke_hiero_env_mac.command</code> (MAC) creates temporary <code>HIERO_PLUGIN_PATH</code> and <code>NUKE_PATH</code> variables. The MAC script needs to be runned at startup to ensure a working setup or otherwise variables need to be defined in the <code>.plist</code> file. At the NFTS the variable <code>NUKE_PATH</code> should be already set by default on Windows machines.

<h2>HELP AND DOCUMENTATION</h2>

Documentation is often available. The Deadline guidelines for priorities and submission are stored in <code>%NUKE_PATH%/documentation/deadline10_guidelines</code> and can also be accesed by navigating to the <code>Help/Deadline Guidelines</code> within Nuke's interface.
</br>This GitHub page is also accessable by accessing the <code>Help/NFTS Environment Help</code> menu in the Nuke menu bar.
All the Nuke customizations are imported form <code>NFTShelp.py</code> and furhter instructions should be handled through that file.

<h2>THIRD PARTY SCRIPTS AND PLUGINS</h2>

In this repository third party scritps have been implemented, this is a list of them with links to the relative documentation.

<ul>
  <li>WrapItUp <a href="https://maxvanleeuwen.com/project/collect-nuke-scripts-wrapitup/">official page</a></li>
  <li>Switch to NukeX <a href="https://github.com/franklinvfx/NukeSwitch-Script-for-Nuke">official page</a></li>
  <li>Give me Python Selection for Hiero <a href="http://www.nukepedia.com/hiero/give-me-python-selection">official page</a></li>
  <li>Thumbnail Exporter <a href="http://www.nukepedia.com/hiero/python/thumbnail-exporter">official page</a></li>
</ul>

<h2>EXTRA NON-NUKE CONFIGURATIONS</h2>

The Environment safely stores some important scripts and executables to quickly set up other bits of software. Most of the department's machine run Windows so most of the following information (specifically Houdini's and Deadline's) is Windows-specific.

<h4>HOUDINI</h4>

In the script <code>%NUKE_PATH%/scripts/houdini/set_houdini_renderers.bat</code>, when executed, creates a houdini17.0 folder in the user's Documents and populates it with a pre-prepared <code>houdini.env</code> file. This contains the necessary instructions that allow Houdini 17 to run Redshift and Arnold. Note that if the file already exists, it will be replaced. 

To install the Deadline submission tool for Houdini run the <code>Houdini-submitter-windows-installer.exe</code> contained in the same location. This will add extra lines to the <code>houdini.env</code> so make sure to install the renderers before this.

<h4>DEADLINE</h4>
The <code>deadline_config</code> folder contains INI files that store the minimisation preferences for the Deadline Client GUI. The TXT files contain the necessary code to copy those files on remote machines using the deadline remote control.
</br>The <code>deadline_no_gui.bat</code> script, permanently hides the Deadline Client form the GUI interface making it run in the background. 


<h2>LICENSE AND COPYRIGHT</h2>

By downloading a file from this repository you agree to the general license terms below.
</br>Copyright (c) 2010 till present. All rights reserved. Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
</br>
</br>THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOO/ OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
