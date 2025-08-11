c = get_config()
# 把下面替换成“未转义”的原始哈希（带单个 $）
c.ServerApp.password = "argon2:$argon2id$v=19$m=10240,t=10,p=8$06uRfpQYuaK0bdGpuoZ3zg$zddAS5nJZVWvhpI4C85lgzPeh+yDMPIAW0Q5YTr/eU8"  # 或 argon2 哈希
c.ServerApp.ip = "0.0.0.0"
c.ServerApp.port = 8888
c.ServerApp.allow_root = True