import struct
import time

def calculate_checksum(footer):
    checksum = 0
    for byte in footer:
        checksum = (checksum + byte) & 0xFFFFFFFF
    return 0xFFFFFFFF - checksum

def calculate_geometry(size_bytes):
    sectors = size_bytes // 512
    if sectors > 65535 * 255:
        raise ValueError("Disk size too large for standard geometry")
    if sectors >= 65535 * 63:
        sectors_per_track = 255
        heads = 16
    else:
        sectors_per_track = 17
        heads = 4
    cylinders = sectors // (sectors_per_track * heads)
    return cylinders, heads, sectors_per_track

def create_fixed_vhd(filename, size_mb):
    sector_size = 512
    size_bytes = size_mb * 1024 * 1024
    footer_size = 512

    # 计算磁盘几何信息
    cylinders, heads, sectors_per_track = calculate_geometry(size_bytes)

    # 创建文件并填充数据
    with open(filename, "wb") as f:
        # 填充磁盘数据（全零）
        f.write(b"\0" * size_bytes)

        # 创建VHD尾部
        footer = bytearray(footer_size)
        footer[0:8] = b"conectix"  # Cookie
        footer[8:12] = struct.pack(">I", 0x00000002)  # Features
        footer[12:16] = struct.pack(">I", 0x00010000)  # File Format Version
        footer[16:24] = struct.pack(">Q", 0xFFFFFFFFFFFFFFFF)  # Data Offset
        footer[24:28] = struct.pack(">I", int(time.time() - 946684800))  # Timestamp
        footer[28:32] = b"vpct"  # Creator Application
        footer[32:36] = struct.pack(">I", 0x00050000)  # Creator Version
        footer[36:40] = b"Wi2k"  # Creator Host OS
        footer[40:48] = struct.pack(">Q", size_bytes)  # Original Size
        footer[48:56] = struct.pack(">Q", size_bytes)  # Current Size
        footer[56:58] = struct.pack(">H", cylinders)  # Disk Geometry (Cylinders)
        footer[58:59] = struct.pack(">B", heads)  # Disk Geometry (Heads)
        footer[59:60] = struct.pack(">B", sectors_per_track)  # Disk Geometry (Sectors per Track)
        footer[60:64] = struct.pack(">I", 2)  # Disk Type (Fixed)
        footer[64:68] = struct.pack(">I", 0)  # Checksum (初始为0)

        # 计算校验和
        checksum = calculate_checksum(footer)
        footer[64:68] = struct.pack(">I", checksum)  # 更新校验和

        # 写入尾部
        f.write(footer)

    return True

# 示例用法
if __name__ == "__main__":
    create_fixed_vhd("example.vhd", 512)