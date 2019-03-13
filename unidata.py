class AnimeItem():
    # 动画信息
    dbindex = []
    origin_url = []

    # 基本信息
    name = []
    cover = []
    time = []
    eps =  []

    # 类型 故事简介
    genre = []
    story = []

    # 需演员员工索引信息扩展
    cast = []
    staff = []

    # 评测数据
    label = []
    ranking = []

    # 需要更多数据
    # streaming
    # recommend
    # relate

class CastItem():
    # 角色演员对应
    dbindex = []
    origin_url = []
    castdict = []

class StaffItem():
    # 仕事人员与岗位对应
    dbindex = []
    origin_url = []
    staffdict = []
