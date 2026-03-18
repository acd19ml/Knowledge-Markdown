# Phase 0：Python + ML 生态

**时长：** 约1.5周 ｜ **资源：** CS5489 Lec1 + Tutorial 1

---

## Go → Python 思维对照

| Go | Python/ML | 注意点 |
|----|-----------|-------|
| `[]float64` | `np.array` | numpy 有广播机制，Go 没有 |
| `struct` | `class` / `dict` | Python 更灵活 |
| `fmt.Println` 调试 | `matplotlib` 可视化 | ML 里可视化比打印更直观 |
| 强类型 | `dtype=float32` 手动指定 | ML 用 float32 省显存 |

---

## 任务清单

- [ ] 安装环境：`conda create -n ai-learn python=3.10`，安装 `numpy pandas matplotlib torch jupyter`
- [ ] CS5489 Tutorial 1：关闭所有输出 → 自己逐格写 → 跑完对比原版
- [ ] numpy 练习：矩阵乘法 / `reshape(-1, 1)` / 广播机制 / 切片索引
- [ ] matplotlib 练习：散点图 / 折线图 / 热力图（后面调试梯度必用）

---

## 核心问题（能回答才算过关）

- `array.reshape(-1, 1)` 是什么意思，什么时候用？
- `(3,)` 和 `(1, 3)` 的 array 相加，结果 shape 是什么？为什么？
- 为什么 ML 中常用 `float32` 而不是 `float64`？

---

## 我的笔记
_（学完后填）_

---

## 卡住点记录
_（记录卡了的地方）_

---

**完成日期：** _____　　**自评：** ___/10