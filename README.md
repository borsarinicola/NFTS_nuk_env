# NFTS NUKE ENVIONMENT

<h2>General Infromations</h2>

This repository contains the custom tools, pipelines and default gizmos for Nuke, Nuke Studio and Hiero at the National Film and TV School, DFX Department.

This repo can be copyed to a network shared drive and all machines that need access to it must have the environment variables <code>NUKE_PATH</code> and <code>HIERO_PLUGIN_PATH</code> pointing to the shared volume.

Locally the NFTS Envirnoment can be reached at <code>//digitalfxserver/CompEnvironment/</code> on Windows Machines and mounted <code>/Volumes/CompEnvironment</code> on MacOS. Paths in third party code is often implemented explicitely.

OS sensitive plugins such as 3DEqualizer and KeenTools are loaded using conditional statements and attention should be paid to run the same versions on every OS.

<h4>BEST PRACTISES</h4>
Due to the nature of the work Gizmos should not be installed as groups. This allows to be able to easely move nuke scripts to outside the shool. This also means that any uptade to the available plugin will not affect old scripts, ensurig that backwards compatibility is always retained.

<h2>Custom Pipeline</h2>

All the defintions that I'm about to mention will act only if both the nuke script is saved and a version numeber is present in the file name.

<h4>INCREMENTAL SAVE</h4>

The default behaviour of the Incremental Save has been overwritten by the new function called <code>incrementalSave()</code>. This not only increases the version of the script, but also increments every Write and DeepWrite node in the script, ensuring that the render versions always match the script versions.

<h4>WRITE NODES</h4>

To ensure that script are not overwritten after a render, Nuke will also ask whether to save an incremetal of the script after the render has been executed. Artifacts will also be created upon render.
These extra functionalities are implemented by changing the default values of the Python Knobs <b>Before Render</b><code>writeBeforePipeline()</code> and <b>After Render</b> <code>writeAfterPipeline()</code>.

<h4>ARTIFACTS</h4>

When rendering form this customized version of Nuke the software automatically creates a copy of the script in the location where it's saved, adding <i>_artifact</i> at the end of the file name. This ensures that it's always possible to restore the script that rendered a specific output. Aritifacts are created only during GUI sessions. This is done using the <code>nuke.GUI</code> variable.

<h4>EXTERNAL WRITE NODES ISSUE</h4>
When Write nodes have been generated either with NukeStudio or in a Nuke setup where the pipeline is not available, the Before and After Render behaviours will not be in place.
To ensure that "standard rite nodes" are converted in "pipeline write nodes", the function <code>incrementalSave()</code> has also been implemented to change the necessary python knobs on script save. 

<h4>CUSTOM PIPELINE WITH DEADLINE</h4>
Deadline renders run in the non-GUI version of Nuke. Therfore artifacts must be created at submission time.
This is achieved with the <code>advencedSubmission()</code> function. This will first run a script save <code>nuke.scriptsave()</code>, folowed by the standard Deadline Submission function <code>DealineNukeClient.main()</code> and upon succes of the last step the <code>createArtifact()</code>. 
This also ensures that artifacts are generated only once and not evey time that a Deadline render task is initialized.

<h2>Custom Tools</h2>

<h4>NFTS COPY PASTE</h4>

The NFTS Copy paste is a quick way to copy data between different scrips on different machines.
It is possible to initialize the share the selected nodes by navigating to <b>NFTS Share/Share Selected Nodes</b> (Alt+Shift+C).
</br>Nodes are then easy to paste by selecting <b>NFTS Share/Paste Shared Nodes</b> (Alt+Shift+V).
The shared data is stored on a file located at <code>%NUKE_PATH%/NFTS_CopyPaste_Data.nk</code> that get's overwritten ever time that a user copies soemthing new.

<h4>SHARED TOOLS</h4>

User do not have permissions to modify the data on the Environment. Therfore to allow for easy publication of simple toolsets and gizmos "Shared Tools" can be used. 
This allows users to select some nodes or groups from the nodegraph and publish them for everyone to use, modify and eventualy delete; using the relative options in the SharedTools Menu.
Data is stored on <code>%NUKE_PATH%/SharedToolSets</code>. Permissions for this folder have been modified to allow users read and write access. All data contained in here is editable, exeption made for the preloaded lens distortion toolsets. This nodes are crucial for efficient lens distortion workflows and users should not atempt to remove or modify them.

<h4>CUSTOM SHORTCUTS</h4>

<table>
  <tr>
    <td width="50%">
      <ul>
        <li>Keymix          V</li>
        <li>Expression      E</li>
        <li>Invert          Alt+Ctrl+I</li>
        <li>Premult         Alt+Shift+P</li>
        <li>Unpremult       Alt+Shift+U</li>
        <li>ChannelMerge    Shift+M</li>
        <li>TransformMasked  Shift+T</li>
      </ul>
    </td>
    <td width="50%">
      <ul>
        <li>Backdrops       Alt+B</li>
        <li>Read from Write       Shift+R</li>
        <li>Reveal file in Browser      Alt+Shift+R</li>
        <li>Lable Shortcut       Shift+L</li>
        <li>Cycle Between Operations       Alt+X and Alt+Shift+X</li>
        <li>Sumbit to Deadline      Alt+R</li>
      </ul>
    </td>
  </tr>
</table>

<h2>SCRIPTS</h2>

To allow fast setup of direcories and Environment Variables, bat and bash scripts have been created.

<h4>ENVIRONMENT VARIABLES</h4>

There are two scripts available, one for Windows and one for MacOS.
<code>set_hiero_env_win.bat</code> (WIN) creates the permanent user variable <code>HIERO_PLUGIN_PATH</code> adn directs it to the environment while <code>set_nuke_hiero_env_mac.command</code> (MAC) creates the temporary <code>HIERO_PLUGIN_PATH</code> nad <code>NUKE_PATH</code> variables. The MAC script needs to be runned at startup to ensure a working setup. At the NFTS the variable <code>NUKE_PATH</code> should be already set by default.

<h4>DOCUMENTATION</h4>

Documentation is often available. The Deadline guidelines for priorities and submission are stored in <code>documentation/deadline10_guidelines</code> and can also be accesed by navigating to the <code>Thinkbox/Documentation</code> within Nuke's interface.

<h2>EXTRA NON-NUKE CONFIGURATIONS</h2>

The Environment safely stores some important scripts and executables to quickly set up other bits of software.

<h4>HOUDINI</h4>

In the <code>scripts/houdini</code> folder, a the script <code>set_houdini_renderers.bat</code> is stored. When executed the script created a houdini17.0 folder in the user's Documents and populates it with a precompile <code>houdini.env</code> file. This contains the necessary text to allow Houdini 17 to run Redshift and Arnold. Note that if the file already exists, it will be replaced. 

To install the Deadline submission tool for Houdini please run the <code>Houdini-submitter-windows-installer.exe</code> contained in the same folder. This will add extra lines to the <code>houdini.env</code> so make sure to run the Arnold and Redshift script first.

<h4>DEADLINE</h4>
