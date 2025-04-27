from pymol import cmd

# 获取所有对象
all_objects = cmd.get_object_list()

# 设定不同类型的 VL 残基起始编号
vl_start_dict = {
    "1G": 146,
    "2G": 148,
    "GS": 148,
    "3G": 150,
    "GGGS": 152
}

# 存储所有匹配到的 VL 选择字符串
vl_selections = []

# 遍历所有对象
for obj in all_objects:
    if obj.startswith("ozr"):  # 只处理以 "ozr" 开头的对象
        for key, start in vl_start_dict.items():
            if key in obj:
                vl_start = start
                vl_end = vl_start + 108  # 计算终止残基编号
                
                # 添加到选择列表
                vl_selections.append(f"{obj} and resi {vl_start}-{vl_end}")
                
                print(f"Adding {obj}: resi {vl_start}-{vl_end} to VL selection")
                break  # 防止匹配多个关键字

# 合并所有 VL 片段到一个 "vl" 选择
if vl_selections:
    cmd.select("vl", " or ".join(vl_selections))
    print(f"Final VL selection: {' or '.join(vl_selections)}")
else:
    print("No matching VL selections found.")