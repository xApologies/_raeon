import {inflateRawSync} from 'node:zlib';

// Read the supplied small, non-ZIP64 archives in memory; never extract paths or
// execute members. Pinned SHA-256 identities are verified by the caller first.
export function readSourceZip(bytes) {
  let end=bytes.length-22;
  while(end>=Math.max(0,bytes.length-65557)&&bytes.readUInt32LE(end)!==0x06054b50)end--;
  if(end<0||bytes.readUInt32LE(end)!==0x06054b50)throw Error('Missing ZIP directory');
  if(bytes.readUInt16LE(end+4)!==0||bytes.readUInt16LE(end+6)!==0)throw Error('Split ZIP unsupported');
  const count=bytes.readUInt16LE(end+10),entries=new Map();
  let offset=bytes.readUInt32LE(end+16);
  for(let i=0;i<count;i++) {
    if(bytes.readUInt32LE(offset)!==0x02014b50)throw Error('Invalid ZIP directory entry');
    const flags=bytes.readUInt16LE(offset+8),method=bytes.readUInt16LE(offset+10);
    const compressed=bytes.readUInt32LE(offset+20),size=bytes.readUInt32LE(offset+24);
    const nameSize=bytes.readUInt16LE(offset+28),extra=bytes.readUInt16LE(offset+30),comment=bytes.readUInt16LE(offset+32);
    const local=bytes.readUInt32LE(offset+42),name=bytes.subarray(offset+46,offset+46+nameSize).toString('utf8');
    offset+=46+nameSize+extra+comment;
    if(flags&1||![0,8].includes(method)||size>32*1024*1024)throw Error('Unsupported source ZIP entry');
    if(name.startsWith('/')||name.includes('\\')||name.split('/').includes('..')||entries.has(name))throw Error('Unsafe/duplicate source ZIP path');
    if(bytes.readUInt32LE(local)!==0x04034b50)throw Error('Invalid ZIP local header');
    const start=local+30+bytes.readUInt16LE(local+26)+bytes.readUInt16LE(local+28);
    const payload=bytes.subarray(start,start+compressed);
    const value=method===0?payload:inflateRawSync(payload,{maxOutputLength:32*1024*1024});
    if(value.length!==size)throw Error('Source ZIP size mismatch');
    if(!name.endsWith('/'))entries.set(name,value);
  }
  return entries;
}
