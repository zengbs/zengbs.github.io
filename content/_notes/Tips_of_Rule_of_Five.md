---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Tips of Rule of Five
### Example
```c++
class Customer {
public:
   Customer() = default;

   // copy constructor
   Customer(const Customer& rhs)
   // note that the construction order is the same as the declaration order
   // but not the order in initializer list
   : values{rhs.values}, name{rhs.name}
   { }

   // move constructor
   Customer(Customer&& rhs) noexcept
   : values{std::move(rhs.values)}, name{std::move(rhs.name)}
   { }

   // copy assignment
   // Using ref-qualifier to ensure that only lvalue can call assignment
   Customer& operator=(const Customer& rhs) &
   {
      // if all members are STL, checking self-copy is redundant
      if (&rhs == this) return *this;
      values = rhs.values;
      name = rhs.name;
      return *this;
   }
   // Or, using copy-and-swap idiom
   Customer& operator=(Customer rhs) &
   {
       std::swap(*this, rhs);
       return *this;
   }

   // move assignment
   // Using ref-qualifier to ensure that only lvalue can call assignment
   Customer& operator=(Customer&& rhs) & noexcept
   {
      if (&rhs == this) return *this;
      values = std::move(rhs.values);
      name = std::move(rhs.name);
      return *this;
   }

private:
   std::string name;
   std::vector<int> values;
};
```

## Tips
* Avoid unnecessary destructors — they undeclare move semantics.
* Never `=delete` special move member functions, as this disables both copy and move semantics — move member functions are deleted, and copy member functinos are undeclared.
* Use (conditional) `noexcept` to avoid falling back to copy.
* Declare assignment with ref-qualifier to make sure only lvalue can use assignment.
* In copy assignment, checking self-copy is:
    * Redundent for the C+ code following RAII.
    * Risky when managing resources or ownership. LHS object may be assigned from a deleted RHS object.
* You may want to use copy-and-swap idiom instead to replace traditional copy assignment:
   ```c++
   Customer& operator(Customer rhs) &
   {
       std::swap(*this,rhs);
       return *this;
   }
   ```
* In move assignment, checking self-movement by comparing address is cheap but is risky when coping with recursive object. If a parent object is move-assigned from its child object, the parent object may end up being assigned from a deleted child object. For example:
   ```c++
   class TreeNode {
   public:
       TreeNode& operator=(TreeNode&& rhs) & noexcept;
   private:
      std::unique_ptr<TreeNode> left;
      std::unique_ptr<TreeNode> right;
      int value;
   };
   ```
   Traditionally, we used to release the LHS's resource and move RHS to LHS:
   ```c++
   TreeNode& TreeNode::operator=(TreeNode&& rhs) & noexcept
   {
       if (&rhs == this) return *this;
       
       // clean up RHS data
       left.reset();
       right.reset();
       
       // move-assign to RHS
       left = std::move(rhs.left);
       right = std::move(rhs.right);
       value = rhs.value;
       
       return *this;
   }
   ```
   The better way is to adopt two-phase move:
   ```c++
   TreeNode& TreeNode::operator=(TreeNode&& rhs) & noexcept
   {
       if (&rhs == this) return *this;
       
       // back up the child objects
       TreeNode new_left = std::move(rhs.left);
       TreeNode new_right = std::move(rhs.right);
       int new_value = rhs.value;
       
       // clean up RHS
       left.reset();
       right.reset();
       
       // move-assign to RHS
       left = std::move(new_left);
       right = std::move(new_right);
       value = new_value;
   }
   ```
* In class inheritance, please see [noexcept Declarations in Class Hierarchies](https://hackmd.io/1Fjt2rPQSPqGjqcwUD29yg?view#noexcept-Declarations-in-Class-Hierarchies) for more details about `noexcept`.
{% endraw %}