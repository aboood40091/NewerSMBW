import elftools.elf.elffile
import struct

class DyLinkCreator:
    R_PPC_ADDR32 = 1
    R_PPC_ADDR16_LO = 4
    R_PPC_ADDR16_HI = 5
    R_PPC_ADDR16_HA = 6
    R_PPC_REL24 = 10

    VALID_RELOCS = set([1, 4, 5, 6, 10])

    def __init__(self, other=None):
        if other:
            self._relocs = other._relocs[:]

            self._targets = other._targets[:]
            self._target_lookups = other._target_lookups.copy()
        else:
            self._relocs = []

            self._targets = []
            self._target_lookups = {}

        self.elf = None

    def set_elf(self, stream):
        if self.elf != None:
            raise ValueError('ELF already set')

        self.elf = elftools.elf.elffile.ELFFile(stream)
        self.code = self.elf.get_section_by_name('.text').data()

        self._add_relocs(self.elf.get_section_by_name('.rela.text'))

    def _add_relocs(self, section):
        sym_values = {}
        sym_section = self.elf.get_section_by_name('.symtab')

        for reloc in section.iter_relocations():
            entry = reloc.entry
            #print(entry)

            sym_id = entry['r_info_sym']
            try:
                sym_value, sym_name = sym_values[sym_id]
            except KeyError:
                sym = sym_section.get_symbol(sym_id)
                sym_value = sym.entry['st_value']
                sym_name = sym.name
                sym_values[sym_id] = (sym_value, sym_name)
            #print(hex(sym_value))

            self.add_reloc(entry['r_info_type'], entry['r_offset'], sym_value+entry['r_addend'], sym_name)

    def add_reloc(self, reltype, addr, target, name="UNKNOWN NAME"):
        if reltype not in self.VALID_RELOCS:
            raise ValueError('Unknown/unsupported rel type: %d (%x => %x)' % (reltype, addr, target))

        try:
            target_id = self._target_lookups[target]
        except KeyError:
            target_id = len(self._targets)
            self._target_lookups[target] = target_id
            self._targets.append(target)
        if target <= 0:
            print("Warning: The following reloc (%x) points to %d: Is this right? %s" % (addr, target, name))

        self._relocs.append((reltype, addr, target_id))

    def build_reloc_data(self):
        header_struct = struct.Struct('>8sI')

        rel_struct_pack = struct.Struct('>II').pack
        target_struct_pack = struct.Struct('>I').pack

        rel_data = map(lambda x: rel_struct_pack((x[0] << 24) | x[2], x[1]), self._relocs)
        target_data = map(target_struct_pack, self._targets)

        header = header_struct.pack(b'NewerREL', 12 + (len(self._relocs) * 8))

        return header + b''.join(rel_data) + b''.join(target_data)



if __name__ == '__main__':
    dlc = DyLinkCreator()
    dlc.set_elf(open('NewerASM/n_jpn_object.plf', 'rb'))
