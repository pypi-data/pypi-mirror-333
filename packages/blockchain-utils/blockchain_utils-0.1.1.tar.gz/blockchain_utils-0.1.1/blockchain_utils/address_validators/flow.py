parity_check_matrix_columns = [
    0x00001,
    0x00002,
    0x00004,
    0x00008,
    0x00010,
    0x00020,
    0x00040,
    0x00080,
    0x00100,
    0x00200,
    0x00400,
    0x00800,
    0x01000,
    0x02000,
    0x04000,
    0x08000,
    0x10000,
    0x20000,
    0x40000,
    0x7328D,
    0x6689A,
    0x6112F,
    0x6084B,
    0x433FD,
    0x42AAB,
    0x41951,
    0x233CE,
    0x22A81,
    0x21948,
    0x1EF60,
    0x1DECA,
    0x1C639,
    0x1BDD8,
    0x1A535,
    0x194AC,
    0x18C46,
    0x1632B,
    0x1529B,
    0x14A43,
    0x13184,
    0x12942,
    0x118C1,
    0x0F812,
    0x0E027,
    0x0D00E,
    0x0C83C,
    0x0B01D,
    0x0A831,
    0x0982B,
    0x07034,
    0x0682A,
    0x05819,
    0x03807,
    0x007D2,
    0x00727,
    0x0068E,
    0x0067C,
    0x0059D,
    0x004EB,
    0x003B4,
    0x0036A,
    0x002D9,
    0x001C7,
    0x0003F,
]

linear_code_n = 64


def is_valid_checksum(address: str) -> bool:
    """
    Function checks checksum for Flow blockchain address
    :param address: Address as string
    :return: True id ok, otherwise False
    """
    code_word = int(address, 0) ^ 0

    parity = 0
    for i in range(0, linear_code_n):
        if code_word & 1 == 1:
            parity = parity ^ parity_check_matrix_columns[i]
        code_word >>= 1

    return parity == 0 and code_word == 0
