import subprocess

urls = [
    "https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2", # 盔甲
    "https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9", # 弹射物
    "https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6", # 矿车
    "https://zh.minecraft.wiki/w/%E8%88%B9", # 船
    "https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F", # 创造模式物品栏
    "https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF", # 统计信息
    "https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF" # 记分板
]

for u in urls:
    result = subprocess.run(['curl', '-s', '-I', '-A', 'Mozilla/5.0', u], stdout=subprocess.PIPE, text=True)
    if "200 OK" in result.stdout or "301 Moved" in result.stdout or "302 Moved" in result.stdout:
        print(f"OK: {u}")
    else:
        print(f"FAIL: {u} ->\n{result.stdout[:200]}")
