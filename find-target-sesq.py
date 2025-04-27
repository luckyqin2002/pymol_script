from pymol import cmd

# 目标序列
target_sequence = "VYCGPEFDESVGCM"

# 获取所有对象
all_objects = cmd.get_object_list()

# 存储匹配的选择
mm_selections = []

# 遍历所有对象
for obj in all_objects:
    if obj.startswith("ozr"):  # 只处理以 "ozr" 开头的对象
        print(f"Processing {obj}...")

        # 获取该对象的所有残基信息
        residues = []
        sequence = ""
        cmd.iterate(f"{obj} and name CA", "residues.append((resi, oneletter))", space=locals())

        # 提取序列
        resi_list, seq_list = zip(*residues)  # 拆分残基编号和单字母氨基酸序列
        sequence = "".join(seq_list)  # 生成完整序列

        # 查找目标序列的位置
        pos = sequence.find(target_sequence)
        if pos != -1:
            start_resi = int(resi_list[pos])
            end_resi = int(resi_list[pos + len(target_sequence) - 1])
            selection_str = f"{obj} and resi {start_resi}-{end_resi}"
            mm_selections.append(selection_str)
            print(f"Found target sequence in {obj}: resi {start_resi}-{end_resi}")

# 合并所有匹配的区域到 `mm` 选择
if mm_selections:
    cmd.select("mm", " or ".join(mm_selections))
    print(f"Final mm selection: {' or '.join(mm_selections)}")
else:
    print("No matching sequences found.")