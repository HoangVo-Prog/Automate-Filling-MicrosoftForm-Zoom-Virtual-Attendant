import random
import time


def k(n):
    return random.randint(1, n)


# Hướng 1:
# 1 → 2.1 (No) → 2.2 → 4.1 (No) → 5 → 6 → End
#
# Hướng 2:
# 1 → 2.1 (No) → 2.2 → 4.1 (Yes) → 4.2 → 4.3 (No) → 5 → 6 → End
#
# Hướng 3:
# 1 → 2.1 (No) → 2.2 → 4.1 (Yes) → 4.2 → 4.3 (No) → 4.4 → 5 → 6 → End
#
# Hướng 4:
# 1 → 2.1 (Yes) → 2.2 → 3 → 4.1 (No) → 5 → 6 → End
#
# Hướng 5:
# 1 → 2.1 (Yes) → 2.2 → 3 → 4.1 (Yes) → 4.2 → 4.3 (No) → 5 → 6 → End
#
# Hướng 6:
# 1 → 2.1 (Yes) → 2.2 → 3 → 4.1 (Yes) → 4.2 → 4.3 (No) → 4.4 → 5 → 6 → End

universities = [
    "Đại học Ngoại thương TPHCM (FTU2)",
    "Đại học RMIT TPHCM",
    "Đại học Kinh tế - Luật TPHCM (UEL)",
    "Đại học Kinh tế TPHCM (UEH)",
    "Đại học Fullbright",
    "Đại học Quốc tế HCM (IU)",
    "Đại học Ngân Hàng (HUB)",
    "Đại học Giao thông vận tải (UTH)",
    "Đại học Ngoại thương Hà Nội (FTU)",
    "Đại học RMIT Hà Nội (RMIT HN)",
    "Học viện Ngoại Giao",
    "Học viện Ngân Hàng",
    "Đại học Thương Mại (TMU)",
    "Đại học Kinh tế Quốc dân Hà Nội (NEU)",
    "Đại học Đà Nẵng",
    "Đại học Bách Khoa TPHCM",
    "Đại học Bách Khoa Hà Nội",
    "Đại học Khoa Học Tự Nhiên",
    "Đại học Sư Phạm Kỹ Thuật"
]

# Trọng số cho các trường tương ứng
weights_universities = [
    0,   # FTU2
    0,   # Đại học RMIT TPHCM
    1,  # Đại học Kinh tế - Luật TPHCM (UEL)
    10,   # Đại học Kinh tế TPHCM (UEH)
    1,   # Đại học Fulbright
    1,  # Đại học Quốc tế HCM (IU)
    1,  # Đại học Ngân Hàng (HUB)
    1,   # Đại học Giao thông vận tải (UTH)
    10,   # Đại học Ngoại thương Hà Nội (FTU)
    2,   # Đại học RMIT Hà Nội (RMIT HN)
    2,   # Học viện Ngoại Giao
    1,   # Học viện Ngân Hàng
    1,   # Đại học Thương Mại (TMU)
    15,   # Đại học Kinh tế Quốc dân Hà Nội (NEU)
    1,   # Đại học Đà Nẵng
    0,   # Đại học Bách Khoa TPHCM
    0,   # Đại học Bách Khoa Hà Nội
    0,  # Đại học Khoa học Tự Nhiên
    0    # Đại học Sư Phạm Kỹ Thuật
]

# Danh sách các ngành học
majors = [
    "Ngành luật/ kinh tế luật/kinh tế/ ngôn ngữ học",
    "Ngành quản trị kinh doanh/ Kinh doanh quốc tế/ nhân sự",
    "Ngành tài chính/ ngân hàng/ bảo hiểm",
    "Ngành Logistic",
    "Nhóm ngành máy tính và công nghệ thông tin",
    "Ngành Trí tuệ nhân tạo",
    "Nhóm ngành toán học, toán tin, toán ứng dụng, khoa học dữ liệu"
]

# Trọng số cho các ngành học
weights_majors = [
    3,  # Ngành luật/ kinh tế luật/ kinh tế/ ngôn ngữ học
    3,  # Ngành quản trị kinh doanh/ Kinh doanh quốc tế/ nhân sự
    2,  # Ngành tài chính/ ngân hàng/ bảo hiểm
    0,  # Ngành Logistic
    0,  # Nhóm ngành máy tính và công nghệ thông tin
    0,  # Ngành Trí tuệ nhân tạo
    0   # Nhóm ngành toán học, toán tin, toán ứng dụng, khoa học dữ liệu
]

question_15_options = [
    "Chia sẻ câu chuyện thành công của nhân viên",
    "Hoạt động cộng đồng và trách nhiệm xã hội",
    "Văn hóa làm việc đa dạng và hòa nhập",
    "Hình ảnh đời thường tại nơi làm việc"
]

# Câu trả lời cho câu 16 - Theo bạn, kênh truyền thông nào của BAT hiệu quả nhất để thu hút ứng viên?
question_16_options = [
    "LinkedIn",
    "Facebook",
    "Website công ty",
    "Hội chợ việc làm",
    "Người quen giới thiệu",
    "Truyền miệng"
]

# Câu trả lời cho câu 17 - BAT có thể làm gì để thu hút nhân tài từ các ngành như Công nghệ, FMCG, hoặc Sản xuất?
question_17_options = [
    "Chương trình thu hút và phát triển nhân tài",
    "Cải thiện chính sách hỗ trợ và phúc lợi cho nhân viên",
    "Nêu bật thành tựu về đổi mới và phát triển bền vững",
    "Thúc đẩy sự linh hoạt trong công việc",
    "Tạo cơ hội luân chuyển quốc tế"
]

# Câu trả lời cho câu 18 - Bạn có bất kỳ đề xuất nào khác để nâng cao thương hiệu nhà tuyển dụng của BAT không?
question_18_options = ["Không"]

options_10 = [
    "Dưới 1 năm",
    "1 - 3 năm",
    "Trên 3 năm",
    "Không có ý định làm việc"
]

def get_answers(n):
    # Khởi tạo bộ sinh số ngẫu nhiên độc lập mỗi lần gọi hàm get_answers
    rnd = random.Random()

    # Sử dụng một chuỗi ngẫu nhiên làm seed độc lập cho mỗi lần gọi
    rnd.seed(str(n) + str(random.random()))  # seed mới cho mỗi lần gọi

    answers = []
    DICT_OF_ANSWERS = {
        "1": [
            random.choices(["Nam", "Nữ"], weights=[0.7, 0.3], k=1),
            random.choices(["Năm 1", "Năm 2", "Năm 3", "Năm 4", "Đã tốt nghiệp, dưới 02 năm kinh nghiệm"],
                           weights=[0, 0.15, 0.4, 0.3, 0.1], k=1),
            random.choices(universities, weights=weights_universities, k=1),
            random.choices(majors, weights=weights_majors, k=1)
        ],
        "2.1": [
            random.choices(["Có", "Không"], weights=[0.7, 0.3], k=1),
        ],
        "2.2": [
            # Câu hỏi 6 - Bạn biết đến BAT qua kênh nào? (Chọn nhiều nhất 3)
            random.sample(["LinkedIn", "Facebook", "Hội chợ việc làm", "Website tuyển dụng", "Người quen giới thiệu"],
                          k=k(3)),

            # Câu hỏi 7 - Đánh giá mức độ nhận diện thương hiệu của BAT so với các công ty cùng ngành
            random.choices([2, 3, 4], weights=[1, 1, 3], k=1),

            # Câu 8
            random.sample(
                ["Lương thưởng và phúc lợi", "Cơ hội phát triển nghề nghiệp", "Văn hóa doanh nghiệp tích cực",
                 "Định hướng phát triển bền vững"], k=k(3)
            ),
            # Câu hỏi 9 - Khi so sánh BAT với các công ty FMCG khác, yếu tố nào giúp BAT nổi bật? (Chọn nhiều nhất 3)
            random.sample(
                ["Lương thưởng và phúc lợi cạnh tranh", "Cơ hội luân chuyển quốc tế", "Văn hóa doanh nghiệp tích cực",
                 "Định hướng đổi mới sản phẩm giảm tác hại", "Trách nhiệm xã hội và phát triển bền vững"],
                k=k(3)),

            # Câu hỏi 10 - Đánh giá mức độ khác biệt của BAT so với các đối thủ trong ngành FMCG
            random.choices([2, 3, 4], weights=[1, 1, 1], k=1)
        ],
        "3": [
            random.choices([2, 3, 4], weights=[1, 1, 2], k=1),
            random.choices([2, 3, 4], weights=[1, 1, 2], k=1),
            random.choices([2, 3, 4], weights=[1, 1, 2], k=1),
            random.choices([2, 3, 4], weights=[1, 1, 2], k=1),
            random.sample(
                ["Cơ hội nghề nghiệp trong đơn vị kinh doanh", "Thử thách/Cơ hội phát triển",
                 "Cơ hội nghề nghiệp quốc tế",
                 "Đa dạng, công bằng và hòa nhập", "Văn hóa tổ chức", "Lương thưởng đãi ngộ", "Danh tiếng của tổ chức",
                 "Chất lượng lãnh đạo", "Cân bằng giữa công việc và cuộc sống", "Sự linh hoạt trong công việc"],
                k=k(3)),
            random.choices([2, 3, 4], weights=[1, 1, 3], k=1)
        ],
        "4.1": [
            random.choices(["Có", "Không"], weights=[0.95, 0.05], k=1)
        ],
        "4.2": [
            random.choices([2, 3, 4], weights=[1, 1, 1], k=1),
            random.choices([2, 3, 4], weights=[1, 1, 1], k=1)
        ],
        "4.3": [
            random.choices(["Có", "Không"], weights=[0.7, 0.3], k=1)
        ],
        "4.4": [
            random.choices(options_10, k=1)
        ],
        "5": [
            random.sample(
                ["Tăng cường minh bạch về lương thưởng và phúc lợi",
                 "Cung cấp các chương trình đào tạo lãnh đạo và phát triển chuyên môn",
                 "Tăng cường sự linh hoạt trong công việc (hybrid working)",
                 "Tập trung vào đổi mới sản phẩm và phát triển bền vững",
                 "Xây dựng các chương trình gắn kết nhân viên"], k=k(2)),
            random.choices(["Cung cấp thông tin rõ ràng về quy trình tuyển dụng"], weights=[1], k=1),
            random.sample(
                ["Lương thưởng", "Văn hóa doanh nghiệp", "Cơ hội phát triển nghề nghiệp",
                 "Chính sách làm việc linh hoạt",
                 "Cam kết môi trường Đa dạng & Hòa nhập"], k=k(2)),
            random.choices([2, 3, 4], weights=[1, 1, 1], k=1),
            random.sample(question_15_options, k=3),

            # Câu trả lời cho câu 16 - Chọn tối đa 2 tùy chọn
            random.sample(question_16_options, k=k(2)),

            # Câu trả lời cho câu 17 - Chọn tối đa 2 tùy chọn
            random.sample(question_17_options, k=k(2)),

            # Câu trả lời cho câu 18 - Luôn trả lời "Không"
            random.choice(question_18_options)

        ],
        "6": [
            random.choices([2, 3, 4], weights=[1, 1, 1], k=1),
            random.choices([2, 3, 4], weights=[1, 1, 1], k=1),
            random.choices([2, 3, 4], weights=[1, 1, 1], k=1),
            random.choices([2, 3, 4], weights=[1, 1, 1], k=1)
        ]
    }

    if n == 1:
        answers.extend(DICT_OF_ANSWERS["1"])
        answers.extend([["Không"]])
        answers.extend([["Không"]])
        answers.extend(DICT_OF_ANSWERS["5"])
        answers.extend(DICT_OF_ANSWERS["6"])

    elif n == 2:
        answers.extend(DICT_OF_ANSWERS["1"])
        answers.extend([["Không"]])
        answers.extend([["Có"]])
        answers.extend(DICT_OF_ANSWERS["4.2"])
        answers.extend([["Không"]])
        answers.extend(DICT_OF_ANSWERS["5"])
        answers.extend(DICT_OF_ANSWERS["6"])

    elif n == 3:
        answers.extend(DICT_OF_ANSWERS["1"])
        answers.extend(["Không"])
        answers.extend(["Có"])
        answers.extend(DICT_OF_ANSWERS["4.2"])
        answers.extend(["Có"])
        answers.extend(DICT_OF_ANSWERS["4.4"])
        answers.extend(DICT_OF_ANSWERS["5"])
        answers.extend(DICT_OF_ANSWERS["6"])

    elif n == 4:
        answers.extend(DICT_OF_ANSWERS["1"])
        answers.extend(["Không"])
        answers.extend(["Có"])
        answers.extend(DICT_OF_ANSWERS["4.2"])
        answers.extend(["Có"])
        answers.extend(DICT_OF_ANSWERS["4.4"])
        answers.extend(DICT_OF_ANSWERS["5"])
        answers.extend(DICT_OF_ANSWERS["6"])

    elif n == 5:
        answers.extend(DICT_OF_ANSWERS["1"])
        answers.extend(["Có"])
        answers.extend(DICT_OF_ANSWERS["2.2"])
        answers.extend(DICT_OF_ANSWERS["3"])
        answers.extend("Có")
        answers.extend(DICT_OF_ANSWERS["4.2"])
        answers.extend("Không")
        answers.extend(DICT_OF_ANSWERS["5"])
        answers.extend(DICT_OF_ANSWERS["6"])

    elif n == 6:
        answers.extend(DICT_OF_ANSWERS["1"])
        answers.extend(["Có"])
        answers.extend(DICT_OF_ANSWERS["2.2"])
        answers.extend(DICT_OF_ANSWERS["3"])
        answers.extend(["Có"])
        answers.extend(DICT_OF_ANSWERS["4.2"])
        answers.extend(["Có"])
        answers.extend(DICT_OF_ANSWERS["4.4"])
        answers.extend(DICT_OF_ANSWERS["5"])
        answers.extend(DICT_OF_ANSWERS["6"])

    return [
        i[0] if len(i) == 1 else i for i in answers
    ]


