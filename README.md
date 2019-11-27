# NFTS NUKE ENVIONMENT


This repository contains the custom tools and default gizmos for Nuke, Nuke Studio and Hiero at the National Film and TV School.

This repo is meant to be copyed to a network shared drive and all machines that need access to it must have the environment variables <b>NUKE_PATH</b> and <b>HIERO_PLUGIN_PATH</b> pointing to the shared volume. 
</br>Third party code is often implemented by explicitely defining paths. Locally the NFTS Envirnoment can be reached at <i>//digitalfxserver/CompEnvironment/</i> on Windows Machines and at <i>/Volumes/CompEnvironment</i> on MacOS.

OS specific plugins such as 3DEqualizer and that KeenTools suite are loaded differently based on the os. 
</br>Check the init.py, menu.py and the plugins own folders.

General practises.
Gizmos should not be loaded as "true gizmos" but rather as groups. This allows for the student to be able to move nuke scripts to outside the school without having to copy those as well. Furthermore this means that any uptade to the available plugin will not affect old scripts, ensurig that backwards compatibility is always retained.

<h2>Custom Pipleines</h2>

<h4>WRITE NODES</h4>




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
