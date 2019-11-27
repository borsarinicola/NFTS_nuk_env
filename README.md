# NFTS NUKE ENVIONMENT


This repository contains the custom tools and default gizmos for Nuke, Nuke Studio and Hiero at the National Film and TV School.

This repo is meant to be copyed to a network shared drive and all machines that need access to it must have the environment variables <b>NUKE_PATH</b> and <b>HIERO_PLUGIN_PATH</b> pointing to the shared volume. 
</br>Third party code is often implemented by explicitely defining paths. Locally the NFTS Envirnoment can be reached at <i>//digitalfxserver/CompEnvironment/</i> on Windows Machines and at <i>/Volumes/CompEnvironment</i> on MacOS.

OS specific plugins such as 3DEqualizer and that KeenTools suite are loaded differently based on the os. 
</br>Check the init.py, menu.py and the plugins own folders.

General practises.
Gizmos should not be loaded as "true gizmos" but rather as groups. This allows for the student to be able to move nuke scripts to outside the school without having to copy those as well. Furthermore this means that any uptade to the available plugin will not affect old scripts, ensurig that backwards compatibility is always retained.

<h2>Custom Pipeline</h2>

All the defintions that I'm about to mention will act only if both the nuke script is saved and a version numeber is present in the fine name

<h4>INCREMENTAL SAVE</h4>

The default behaviour of the Incremental Save has been overwritten by the new function <code>incrementalSave()</code>. This not only increases the version of the script, but also increment every Write and DeepWrite node in the script, to ensure that the render version always matches the scrip version.

<h4>WRITE NODES</h4>

When rendering form this customized version of Nuke the software automatically creates a copy of the script in the same location adding <i>_artifact</i> at the end of the file name. This ensures that it's always possible to restore the script that rendered a specific output.
To further ensure that script are not overwritten after a render, Nuke will also ask whether to save an incremetal of the script after the render has been executed.
These extra functionalities are implemented by changind the default values of the Python Knobs Before Render <code>writeBeforePipeline()</code> and After Render <code>writeAfterPipeline()</code>.
These definitions contain further commands.

<h4>NUKESTUDIO WRITE NODES</h4>
When Write nodes have been generated either with NukeStudio or in a Nuke setup where the pipeline is not available, the Before and After Render behaviours are not in place.
To ensure that standard write nodes are converted in "pipeline write nodes" the <code>incrementalSave()</code> function mentioned above has also been implemented to change the necessary Python Knobs. 

<h4>CUSTOM PIPELINE WITH DEADLINE</h4>

<h2>Custom Tools</h2>

<h4>NFTS COPY PASTE</h4>

The NFTS Copy paste is a quick way to copy data between different scrips on different machines.
It is possible to initialize the share the selected nodes by navigating to <b>NFTS Share/Share Selected Nodes</b> (Alt+Shift+C).
</br>Nodes are then easy to paste by selecting <b>NFTS Share/Paste Shared Nodes</b> (Alt+Shift+V).
The shared data is stored on a file located at %NUKE_PATH%/NFTS_CopyPaste_Data.nk that get's overwritten ever time that a user copies soemthing new.

<h4>SHARED TOOLS</h4>

User do not have permissions to modify the data on the Envirnomnet. Therfore to allow for easy publish of simple toolsets and gizmos "Shared Tools" can be used. 
This allows user to select some node or groups into the nodgraph and publish them for everyone to use using the create, modify and delete options in the SharedTools Menu.
Data is stored on %NUKE_PATH%/SharedToolSets. The permissions of that folder have been modified to allow users write access this specific folder.
All data contained in here is editable, exeption made for the preloaded lens distortion toolsets. This nodes are crucial for efficient lens distortion workflows and should not be removed or modified.

<h4>CUSTOM SHORTCUTS</h4>
<ul>
<li>Keymix          v</li>
<li>Expression      e</li>
<li>Invert          alt+ctrl+i</li>
<li>Premult         alt+shift+p</li>
<li>Unpremult       alt+shift+u</li>
<li>ChannelMerge    shift+m</li>
<li>TransformMasked  Shift+t</li>
<li>Backdrops       alt+b</li>
<li>Read from Write       shift+r</li>
<li>Reveal file in Browser      alt+shift+r</li>
<li>Lable Shortcut       shift+l</li>
<li>Cycle Between Operations       alt+x and alt+shift+x</li>
</ul>
