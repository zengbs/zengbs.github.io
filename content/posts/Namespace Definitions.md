---
title: "Namespace Definitions"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Namespace Definitions
tags: [CPP]

---

# Namespace Definitions
* The definition of a namespace does not have to be contiguous.

# The Scope Operator(`::`)
* The name of a user-declared namespace member is automatically prefixed by the name of its namespace followed by the scope operator (::). A namespace member name is qualified by its namespace name.
* From the perspective of the code outside the namespace, the declaration of a namespace member is hidden. Unless we specify to the compiler in which namespace to search for a declaration, the compiler simply searches the current scope, and any scopes in which the current scope is nested, to find a declaration for the name.
* Note that the scope operator can also be used to refer to members of the global namespace. Because the global namespace does not have a name, the notation `::member_name;` refers to a member of the global namespace. 

# Nested Namespce
* The declaration of a member of a nested namespace is hidden within the nested namespace. The name of such a member is automatically prefixed with the name of the outermost namespace and also with the name of the nested namespace.
* when a name is used in a namespace definition, the enclosing namespaces are searched for a declaration.
* An entity declared in an enclosing namespace is hidden by an entity of the same name declared in a nested namespace. 


# Namespace Member Definitions
* It is also possible to define any namespace member outside its namespace definition. In such a case, the name of the namespace member must be qualified by the names of its enclosing namespaces.
* The definition of qualified function can use the namespace member names in their short form in any declaration or expression within the parameter list or the function body.
* Only namespaces enclosing the member declaration can contain its definition.
* Note that a namespace member can be defined outside its namespace definition only if the member was previously declared within the namespace definition.



# Unnamed Namespaces
* One can use an unnamed namespace to declare an entity local to a file. An unnamed namespace definition begins with the keyword namespace.
* Unnamed namespaces are not like other namespaces; the definition of an unnamed namespace is local to a particular file and never spans multiple text files.
* It is not necessary to use the scope operator to refer to members of unnamed namespaces.
* The names of the members of an unnamed namespace are visible only within a specific file and are invisible to the other files that make up the program.
* A member of an unnamed namespace has properties that are similar to those of a global entity declared static.
* The use of global static declarations will be replaced with the use of unnamed namespace members.