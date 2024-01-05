import numpy as np
import cv2

# 图像大小
width, height = 800, 600

# 创建空白图像
water_image = np.zeros((height, width, 3), dtype=np.uint8)
# 生成水深数据（示例使用随机噪声）
depth_data = np.random.rand(height, width) * 6
    # 根据深度值映射到颜色
    # 这里只是一个简单的示例，实际应用中可能需要更复杂的映射函数
    return (0, 0, int(depth_value * 255))

# 将水深数据映射到颜色
colored_image = np.zeros((height, width, 3), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        colored_image[y, x] = depth_to_color(depth_data[y, x])
# 保存结果
cv2.imwrite("water_depth_map.png", colored_image)

# 显示结果（可选）
cv2.imshow("Water Depth Map", colored_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
