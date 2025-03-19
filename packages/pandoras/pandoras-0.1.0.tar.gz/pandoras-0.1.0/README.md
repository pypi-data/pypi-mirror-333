# Pandoras 🐼🎭  
**Undo/Redo functionality for Pandas DataFrames using Apache Arrow.**  

Pandoras extends `pandas.DataFrame` to add **undo/redo capabilities**, allowing you to **revert accidental modifications** easily.  

## 🚀 Installation  

You can install `pandoras` via pip:  

```sh
pip install pandoras
```

## 📌 Features
✔ **Undo and redo modifications** (`drop`, `rename`, `replace`, etc.)  
✔ **Leverages Apache Arrow for efficient state storage**  
✔ **Supports Pandas' native operations**  

---

## 💡 Example Usage  

```python
import pandoras as pd  # Now PandorasDataFrame replaces pd.DataFrame

# Create a DataFrame
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, None, 6]})

# Drop a column
df.drop(columns=["B"], inplace=True)
print("After drop:\n", df)

# Undo the drop
df.undo()
print("After undo:\n", df)

# Redo the drop
df.redo()
print("After redo:\n", df)
```

---

## 🔮 Future Improvements  
🚀 **Diff-based state tracking** instead of storing full DataFrame copies  
🚀 **Optimize memory usage** using compression

---

## 🌜 License  
Pandoras is open-source and licensed under the **MIT License**. Contributions are welcome!  

## 🤝 Contributing  
1. **Fork** the repo on GitHub  
2. **Clone** it locally  
3. Create a new **feature branch**  
4. Submit a **pull request**  

---

## 🌍 Connect  
📌 **GitHub Repo:** [GitHub Link Here]  
📌 **PyPI Package:** *(Coming Soon)*  
📌 **Author:** [Your Name]  

---

🐼 **Pandoras – Making Pandas Undoable!** 🎭  
