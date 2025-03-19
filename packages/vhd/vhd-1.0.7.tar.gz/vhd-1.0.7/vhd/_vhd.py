import struct
import time

def _calculate_checksum(footer):
    checksum = 0
    for byte in footer:
        checksum = (checksum + byte) & 0xFFFFFFFF
    return 0xFFFFFFFF - checksum

def _calculate_geometry(size_bytes):
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

def _create_fixed_vhd(filename, size_mb):
    sector_size = 512
    size_bytes = size_mb * 1024 * 1024
    footer_size = 512

    # 计算磁盘几何信息
    cylinders, heads, sectors_per_track = _calculate_geometry(size_bytes)

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
        footer[28:32] = b"pvhd"  # Creator Application
        footer[32:36] = struct.pack(">I", 0x00050000)  # Creator Version
        footer[36:40] = b"pvhd"  # Creator Host OS
        footer[40:48] = struct.pack(">Q", size_bytes)  # Original Size
        footer[48:56] = struct.pack(">Q", size_bytes)  # Current Size
        footer[56:58] = struct.pack(">H", cylinders)  # Disk Geometry (Cylinders)
        footer[58:59] = struct.pack(">B", heads)  # Disk Geometry (Heads)
        footer[59:60] = struct.pack(">B", sectors_per_track)  # Disk Geometry (Sectors per Track)
        footer[60:64] = struct.pack(">I", 2)  # Disk Type (Fixed)
        footer[64:68] = struct.pack(">I", 0)  # Checksum (初始为0)

        # 计算校验和
        checksum = _calculate_checksum(footer)
        footer[64:68] = struct.pack(">I", checksum)  # 更新校验和

        # 写入尾部
        f.write(footer)

    return True


import struct

def _read_vhd_footer(filename):
    footer_size = 512
    with open(filename, "rb") as f:
        # 移动到文件末尾
        f.seek(-footer_size, 2)
        footer = f.read(footer_size)

    if len(footer) != footer_size:
        raise ValueError("Invalid VHD file: Footer size is incorrect")

    # 解析VHD尾部
    cookie = footer[0:8].decode('ascii')
    features = struct.unpack(">I", footer[8:12])[0]
    file_format_version = struct.unpack(">I", footer[12:16])[0]
    data_offset = struct.unpack(">Q", footer[16:24])[0]
    timestamp = struct.unpack(">I", footer[24:28])[0]
    creator_application = footer[28:32].decode('ascii')
    creator_version = struct.unpack(">I", footer[32:36])[0]
    creator_host_os = footer[36:40].decode('ascii')
    original_size = struct.unpack(">Q", footer[40:48])[0]
    current_size = struct.unpack(">Q", footer[48:56])[0]
    cylinders = struct.unpack(">H", footer[56:58])[0]
    heads = struct.unpack(">B", footer[58:59])[0]
    sectors_per_track = struct.unpack(">B", footer[59:60])[0]
    disk_type = struct.unpack(">I", footer[60:64])[0]
    checksum = struct.unpack(">I", footer[64:68])[0]

    # 计算校验和以验证
    calculated_checksum = 0
    for byte in footer[:64] + footer[68:]:
        calculated_checksum = (calculated_checksum + byte) & 0xFFFFFFFF
    calculated_checksum = 0xFFFFFFFF - calculated_checksum

    if calculated_checksum != checksum:
        raise ValueError("Checksum validation failed")

    return {
        "cookie": cookie,
        "features": features,
        "file_format_version": file_format_version,
        "data_offset": data_offset,
        "timestamp": timestamp,
        "creator_application": creator_application,
        "creator_version": creator_version,
        "creator_host_os": creator_host_os,
        "original_size": original_size,
        "current_size": current_size,
        "cylinders": cylinders,
        "heads": heads,
        "sectors_per_track": sectors_per_track,
        "disk_type": disk_type,
        "checksum": checksum
    }

# 格式化时间戳
def format_timestamp(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp + 946684800))


if __name__ == "__main__":
    _create_fixed_vhd("example.vhd", 512)


# 示例用法
if __name__ == "__main__":
    filename = "example.vhd"
    vhd_info = _read_vhd_footer(filename)
    # 示例用法
if __name__ == "__main__":
    filename = "example.vhd"
    vhd_info = _read_vhd_footer(filename)
    
    print("VHD 文件信息:")
    print(f"Cookie: {vhd_info['cookie']}")
    print(f"特性: {vhd_info['features']}")
    print(f"文件格式版本: {vhd_info['file_format_version']}")
    print(f"数据偏移量: {vhd_info['data_offset']}")
    print(f"时间戳: {format_timestamp(vhd_info['timestamp'])}")
    print(f"创建者应用程序: {vhd_info['creator_application']}")
    print(f"创建者版本: {vhd_info['creator_version']}")
    print(f"创建者主机操作系统: {vhd_info['creator_host_os']}")
    print(f"原始大小: {vhd_info['original_size']} 字节 ({vhd_info['original_size'] / (1024 * 1024):.2f} MB)")
    print(f"当前大小: {vhd_info['current_size']} 字节 ({vhd_info['current_size'] / (1024 * 1024):.2f} MB)")
    print(f"柱面数: {vhd_info['cylinders']}")
    print(f"磁头数: {vhd_info['heads']}")
    print(f"每磁道扇区数: {vhd_info['sectors_per_track']}")
    print(f"磁盘类型: {vhd_info['disk_type']}")
    print(f"校验和: {vhd_info['checksum']}")








# # 示例用法
