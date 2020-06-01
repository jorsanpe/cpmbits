## Installation

<pre><code class="language-bash">pip3 install cpm-cli
</code></pre>

CPM depends on [CMake](https://cmake.org/) and [ninja](https://ninja-build.org/) for the build process.

## Create a Project

<pre><code class="language-bash">cpm create DeathStartLaserBackend
cd DeathStartLaserBackend
cpm build
</code></pre>

After creating the project, the binary will be available in the project root directory. 

<pre><code class="language-bash">./DeathStartLaserBackend
</code></pre>

## Manage dependencies

CPM manages your project dependencies through CPM-Hub. In order to install a package, simply run:

<pre><code class="language-bash">cpm install cest
</code></pre>

### Run your tests

<pre><code class="language-bash">cpm test
</code></pre>

Test sources reside in the `tests` directory. They are found recursively from the root directory
 using the expression `test_*.cpp`.
