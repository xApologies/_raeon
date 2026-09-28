# Build channels

Channels contain intended build records, not compiled binaries. No builds exist at bootstrap. Channel names do not assert lifecycle acceptance. Each actual build records source commit, toolchain/dependencies, commands, content revision, artifact hash/location, checks, known issues.

Compiled binaries require later explicit policy before they may be committed.
