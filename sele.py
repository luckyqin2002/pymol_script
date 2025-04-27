from pymol import cmd

# 获取所有对象名
all_objects = cmd.get_object_list()

# 遍历所有以 "ozr" 开头的对象
for obj in all_objects:
    if obj.startswith("ozr"):
        # 获取当前对象的所有残基编号
        resi_list = []
        cmd.iterate(f"{obj} and name CA", "resi_list.append(resi)", space=locals())
        
        # 确保对象有足够的残基
        if len(resi_list) > 125:
            last_108_residues = resi_list[-125:]  # 获取倒数 108 个残基编号
            resi_str = "+".join(map(str, last_108_residues))  # 组合成 PyMOL 选择字符串
            cmd.remove(f"{obj} and resi {resi_str}")  # 删除这些残基
            print(f"Deleted last 108 residues from {obj}")
        else:
            print(f"WARNING: {obj} has only {len(resi_list)} residues, skipping...")