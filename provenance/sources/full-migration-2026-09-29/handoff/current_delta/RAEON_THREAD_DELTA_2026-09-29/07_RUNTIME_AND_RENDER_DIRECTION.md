# Genesis Horizon Runtime / Render Direction

raeon semantics are intended to live in the Genesis Horizon and be
authored in the Genesis programming language.

Conceptual runtime: Genesis game semantics \<-\> Genesis VM \<-\> Python
hypervisor/translation boundary \<-\> platform shell. Platform supplies
graphics/input/audio/storage/network and returns input events. Game
truth remains Genesis/QMO state.

Blender is offline asset generation: QMO -\> RenderSpec/geometry -\>
Blender -\> runtime assets. Initial target direction: Windows first;
later Apple/Metal and Android shells without rewriting authoritative
semantics. This is architecture direction, not implementation-complete
status.
