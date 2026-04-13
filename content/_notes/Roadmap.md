---
title: "Roadmap"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Roadmap
tags: [CPP]

---

![image](https://hackmd.io/_uploads/rkwSpcyn1e.png)

或許有些老人曾經看過這東西，但隨著 C\++11 的問世、侯捷淡出了繁體中文譯者圈、Scott Meyers 淡出 C\++ 出版界，這些書大部分都已經過時且中譯版幾乎全部絕版，上面這張圖在 2022 年的今天也不再適用了。但我就是在這樣的學習環境裡長大的，所以我也無法在 2022 年提供一套新的 C++ 學習方式，畢竟當年的兩本磚頭聖經本 C++ 程式語言 (The C++ Programming Language) 以及 C++ Primer 即便換成了當今最新版本 The C++ Programming Language 4/e (中譯本) 及 C++ Primer 5/e (中譯本)，也已經是接近過時的狀態，硬啃完這兩本對 C++ 的基礎知識也已經不完備了。坦白說，在 2011 年之後我也不知道該如何教一個新手如何學習 C++。所以很不好意思，我也幫不上忙，這只是一篇廢文。不過當年既然發了文，道義上我也得在這裡做一些說明。

如同前面所說的，上面那張圖確實只是我 2005 年，也就是碩士班一年級時讀完的 C++ 書籍，並不代表學習 C++ 基礎一定要讀這麼多書。如果在 2022 年的現在，你很有時間要走這條老路慢慢循著歷史途徑讀上來，那會有很多問題。首先，你得先設法弄到這些絕版中譯本，當然如果你能讀原文書就不是問題。再來，如果你是 C++ 新手，你讀了 C\++20 的語言機制，再回頭去看那些過時老書，可能會對於作者為什麼要用那些方式解決問題感到困惑，因為在 C++11 後有些問題已經可以靠新的語言機制直接解決，或者解決的方式更簡潔了。總而言之，延續我當年所發的那篇文章，在 2022 年的現在要做上一些補充。

首先當年我所指的 C++ Primer 是指第三版，C++ Primer 第四版起的寫作方式已經失去了它原本的意義。原本的 C++ Primer 3/e 是真正意義上的 C++ 大辭典，整本讀完是不會對編譯器上的任何錯誤訊息及編譯結果感到困惑的。即便是一時疏忽忘了書上所寫的東西，腦袋很快就會回想起書中提到的種種規則，意識到自己犯了什麼錯，並且在幾秒內就能把錯誤改正過來，這就是 C++ Primer 3/e 的威力。但作者想必是後悔出了這麼複雜的一本書來殘害世人，後來曾經出了一本 Essential C++ 試圖讓人們可以用更輕鬆的方式學習 C++，這本書說實話在我眼裡完全是一本垃圾。的確我曾經為了教學的目的買過這本書，但最後它也沒有幫上我什麼忙，以當年的時空背景來說，與其讀這本還不如去讀那本很多人推薦的 C++ How to Program。C++ Primer 4/e 開始作者顯然性情大變，很多艱深的章節直接失蹤，而 5/e 看起來更像只是打了 C\++11 的 patch，說實話我不知道這本書還有什麼去讀它的意義在。它的完備性已遠不如當年的 3/e，拼死拼活讀完它能得到的報酬已遠不如當年，某方面來說我認為 Lippman 寫的書都可以不用再看了，不過他看起來也沒有再寫過任何新書。

以現在的最新版本而言，相較於 C++ Primer，C++ 老爸 Bjarne Stroustrup 寫的 The C++ Programming Language 還是比較值得一讀，畢竟 C++ 是他發明出來的語言，他非常清楚 C++ 的每個機制是由於什麼樣的契機而被加入的，因此他在書中的章節安排及範例程式碼，都蘊含著這些歷史意義在裡頭，讀這本書可以用最經典的形式去理解 C++ 的本質。如果對 C\++98 裡各項語言機制的歷史有更濃厚興趣，可以去閱讀那本 The Design and Evolution of C++。這本書的尺寸基本上和當年的英文小說是一樣的，所以也可以把它當成小說來讀，只是在 2022 年的現在，我就不是那麼推薦去讀了。主要是 C\++11 問世之後，讀它的報酬率不高，加上經過標準委員會的諸多干涉，C++ 已經不再是 C++ 爸爸一個人的小孩了，即便是 C\++98，有些東西與 C++ 爸爸的想法也已經是有一點差距在了。當然時間充足的話去讀這本小說不會是壞事，至少可以知道 C++ 爸爸當年的初衷是什麼，畢竟 C++ 的爸爸是個軟工專家，理解他的想法就很難會去誤用 C++98 裡的任何一項語言機制。

深度探索 C++ 物件模型 (Inside the C++ Object Model) 的中譯本是很早就絕版的書籍，實際上它的原文書也有諸多問題需要訂正，這本侯捷翻譯的繁體版本修正了許多原文書中的錯誤。這本書其實也不太需要去讀，在 2022 年的現在，要理解 vtable 以及物件的 memory layout 應該是隨便 Google 搜尋一下都會找到人講，內容也更貼近現代，實在是沒有必要再浪費時間去讀 Lippman 當年所寫的這本書了。

Effective 系列的書籍是由知名的 Scott Meyers 所寫的，而 Exceptional 系列也是迄今仍活躍於 C++ 社群的 Herb Sutter 所寫的，這些書匯集了當年網路上各種討論的精華，裡面有許多在業界實際使用 C++ 時會遇到的疑難雜症和陷阱，讀了這系列的書再正式上路可以避免踩前人們所踩過的地雷。然而上面那張圖裡的 Effective 及 Exceptional 系列也已經全部過時，不瞭解 C\++11 和 C\++98 差異的人去讀它們的話，很可能會使用書上古老的方式去解決書上所描述的問題，而不去使用 C\++11 乃至 C\++20 所提供的語言機制。但是在 C\++11 問世之後，也沒再看到世界上再出版過如此完備的一套實戰級書籍，因此在 2022 年的今天，我還是很難決定是不是該讓讀完 C++ Primer 或 The C++ Programming Language 的初學者去讀這套書。

不過可以肯定的是，Effective C++ 3/e 更新於 2005 年，它的內容勉強對現代 C++ 而言還是有用的，而 Effective STL 雖然是 2001 年問世，但 STL 的本質其實一直沒有變，所以讀它得到的報酬率也不會下降太多。Scott Meyers 在 C++ 社群裡留下的最後一個超級著作是 Effective Modern C++ (中譯本)，在 2014 年出版，可以說是必讀中的必讀，到了 2022 年也沒有變。在那之後 Scott Meyers 在自己網站上留下了這麼一篇文章，就此從 C++ 的舞台上退出。在這最後的最後，他給出的指引就是以後去看 C++ Core Guidelines 吧。不得不說這 C++ Core Guidelines 的內容相當不平易近人，所以我也不清楚後來 C++ 社群還有多少人繼續去閱讀它，但它的內容的確一直都有在更新，只能說不去看好像也不行。

Herb Sutter 出的 Exceptional 系列其實從以前我就只有一個心得，就是不要在 C++ 用什麼 exception，因為要達到他提倡的 exception-safe 在實務上是幾乎不可能的，除非你的專案不要引入任何第三方函式庫。雖然對這位作者不好意思，但我當年的讀後心得真的就只有這樣。不過除了這些講 exception 的章節之外，其實這套書還有不少值得讀的地方，即便在 2022 年的今天也一樣有用，所以去看看也無妨。另外，這兩本書其實都是作者從 Guru of the Week (GotW) 裡整理出來的，但也只有收錄到 issue #62，因此 63 之後的 issues 得自己去網站上看。不過這不代表 issue #63 以前的部分就不用再看了，因為作者在 2013 年起有小量針對 C\++14 做更新，不過只放在他自己的 blog 上。這 blog 上還有持續放上新的 issues，目前為止已經寫到了 issue #102。某方面來說，他那兩本書是可以不用想辦法買來看了，直接從網路上去看他更新後的內容就好。另有一本 C++ Coding Standards 也是他出的，但內容太過精簡也沒詳細解釋原因，閱讀價值遠不如 Effective 和 Exceptional 系列，讀過這兩個系列的多半也看過這本書裡的大部分內容了。

泛型程式設計與 STL (Generic Programming and the STL) 這本書說真的我覺得它是一本學習 STL 的好書，我到現在都還沒有看過一本比它更適合學習 STL 的書籍，即使讀這本書需要一點點離散數學的知識背景也一樣。它是從定義層面帶讀者去瞭解 STL 本身的各項組件，讀完後不會卡在 STL 文件裡突然冒出的專有名詞上，對於有自行擴充 STL 需求的人也能幫上不少忙。不過這項報酬在網路跟搜尋引擎還不是非常發達的 1999 年或許可觀，現代要查那些專有名詞的定義只要貼上 Google 就能找到了，只是要系統化從定義開始學習的話，這本書還是能給予初學者不錯的引導。至於侯捷自己寫的那本 STL 源碼剖析在現代來說，介紹 STL 六大組件的部分還是有它的價值在，至於後面提到 STL 實作細節的部分，我覺得對還沒修過資料結構的大學生來說比較有價值吧。弄不到這本書其實也不用太傷心，其實侯捷本人的著作價值大部分都沒有他的譯作那麼高，無緣看到就算了吧。

C++ 標準程式庫 (The C++ Standard Library: A Tutorial and Reference) 也有適合於現代的新版本，不管在哪個時代，這本都是教你如何使用 C++ 標準函式庫的必備書籍。它不只是工具書，也是教材。實際上這本在現代也不具備什麼工具書的角色了，cppreference 和 The C++ Resources Network 這兩間網站都已經取代了它身為工具書的用途，何況這書從一開始就不是很好查閱，所以我一直都只說它是一本學習標準函式庫的教科書。然而在 STL 的學習上，它始終還不是 Generic Programming and the STL 這本書的對手，即便這書已經過時了 10 幾年。

Modern C++ Design 的作者 Andrei Alexandrescu 是一位 C++ 社群的奇才，不過遺憾的是他提出的 Loki Library 並不為後人所用。這本書坦白說除非你想從事如 Boost C++ Libraries 的函式庫設計工作，否則花時間讀它得到的報酬很少。如果還是時間充裕的學生，把讀懂這本書當成一個挑戰是可以的，但讀完之後如果不從事相關工作，最後獲得的也只剩下一個成就感而已。在 2005 年左右或許你讀完它還有幾個人會拍手說你好厲害，但在 2022 年這種已經沒什麼人對 C++ 有興趣的年代，讀完大概除了自 high 也沒其它作用。與其花大把時間去讀它，不如多學一些其它有用的程式語言，譬如 Python 或者 Go，這是我個人在 2022 年給的良心建議。如果你非要挑戰這本書不可，還有一本 C++ Template Metaprogramming 也推薦你去看看。Loki 的精神已經被現代 C++ 標準函式庫及 Boost C++ Libraries 吸收，裡面的實作方式也已經過時，不用再浪費時間去使用了，請把它供奉在博物館供人瞻仰即可。

至於最後的 C++ Templates 全覽 (C++ Templates: The Complete Guide) 也是同上，如果你想去當函式庫設計者，你可以花時間去看，否則可以不用看。它的第二版出版於 2017 年，中譯本出版於 2019 年，內容算是夠新了，只是你有沒有必要把 template 瞭解到那麼細微的程度，就要看你工作上是不是需要拿靜態多型來替代動態多型，或者是你本身就是個函式庫設計者，但我不認為台灣有任何一間公司會讓員工花時間讓員工去開發這種函式庫，如果有的話，那恭喜你，你的上司應該是個有腦袋的人，不過他會不會受老闆重用又是另一回事了。

C\++11 問世之後，台灣的 C++ 學習資源就相當匱乏了，我幾乎找不到適當的書去帶人學習 C++，加上後來我也就業了，就沒有什麼時間再帶人學 C++。我在讀博士班期間利用了學校的資源修了不少面向碩博士生的英語課程 (感謝清華大學的周曉峯教授，閱讀課的難句解析真的很有用，科技英文寫作課對於瞭解論文結構快速抓論文重點也非常有幫助)，也在外面的成人美語補習班上課 (感謝新竹戴爾美語 Otto 老師上的進階文法課程和 Jeffrey 老師 的 TOEFL iBT 作文課程)，把技職體系背景英文能力不強的這點補了起來，雖然聽力和口說沒能補好，但讀寫能力確實有了相當高度的進步，因此在那之後我就開始買英文電子書看了，主要的購買來源是 InformIT、SpringerLink、Manning、Packt 和 Leanpub，比較需要注意的是 Leanpub 有些書的排版說實話和大學生做的報告差不多，偶爾會踩到地雷，但內容還不會算是沒什麼料，起碼還沒到我會想把作者列黑名單的程度。網路免費資源方面，CppCon 和 BoostCon 應該算是眾所皆知的獲取新知的來源，Awesome C++ Weekly 也是可以訂來被動瞭解一些新東西的，上面連結所參考到的文章作者也有不少值得去關注。除此之外，The Legacy Code Programmer's Toolbox 這本書的作者 Jonathan Boccara 也有一個網站叫 Fluent{C++} 也是值得去看看的。當然這些東西全部都是英文，所以在台灣出生的人要想把 C++ 學好並跟上最新標準，英文能力就會變成第一個門檻，一旦英文能力不好，你就會與 C++ 完全無緣，這是 2011 年之後的一個殘酷現實。

在 2005 年的那個時間點，我沒有講到的東西就是除了把 C++ 這個語言學好之外，培養分析和設計程式的能力也一樣重要。即便物件導向已經在現代被許多人所鄙視，世界上也有更多新的 XX 導向被提出，我個人的本質還是深受 UML 三巨頭之一的 Grady Booch 所影響，是以 OOAD 及 Unified Process (UP) 為基底。即便當年他所提出的那些方法論有許多需要修正的空間，但這套方法論對於團隊合作開發而言仍是不可或缺的。1994 年著名的四人幫所寫的 Design Patterns (中譯本) 一書荼毒了不少業內人士跟學生，不得不說它實在寫得有點爛，書中想傳承的知識明明是好東西，卻敗在了他們不會寫書。

美商歐萊禮公司在 2004 年開始陸續出版的深入淺出 (Head First) 系列叢書，其中的深入淺出設計模式 (Head First Design Patterns) 大大地降低了學習門檻，design patterns 不再為人們所畏懼，但也造就了許多不明就裡盲目去使用它們的人。要知道按照傳統物件導向開發流程，也就是 Grady Booch 當年在 The Unified Software Development Process 一書中提到的方法論，是需要先進行分析才會有設計。換句話說，沒有正確的分析，就不會有正確的設計。而所謂的 design patterns，其實就是 design phase 的 library。一個從來沒有學過物件導向分析和設計概念的人拿設計用的函式庫亂套，後果可想而知。即便在現代講求敏捷的開發方式大都在形式上跳過了分析階段，但那不代表分析這個過程沒有在人腦中發生過。正因為這些古典開發方法已經深植於專家的腦內，所以專家才能在腦內快速地簡化了這個階段，跳過了繁複的 paper works，給出了最終的設計結果，甚至是直接化成了程式碼。這不代表分析這件事不存在，那只是外行人看起來是這樣而已。

後來大概是有誰發現這不對勁了，趕緊又補出了一本深入淺出物件導向分析與設計 (Head First Object-Oriented Analysis and Design)，某方面來說算是成功扭轉了侯捷過去常講的在浮砂築高台的局勢。不過由於業界前輩和學界學長們總是在捧 design patterns，這一本書在國內引起的重視度遠遠不及 design patterns，因此沒能打好基礎就開始拿 design patterns 亂套的人從沒少過，且本書中譯本已絕版。不過坦白說，歐萊禮這本書介紹的方式也算是敏捷開發方法的一種，不如 The Unified Software Development Process 所教導的背景知識那麼完整，因此學好 OOAD 的人大都還是無法正確將它結合到軟體開發流程上，這種人成了中高階主管後，也只會使用日本知名的隕石開發法 (中譯版本)來進行開發。人才運用上也是一個工程師負責一大個子系統甚至是整個軟體系統，無法讓多名工程師在一個軟體元件層級內合作來增加專案效率的目的。

也就是說，除了把 C++ 這個語言學好之外，還要學會如何開發軟體、如何規劃軟體的架構、如何做需求分析、如何進行物件導向分析與設計、如何運用設計模式輔助設計工作，最後還要將它們化為乾淨易維護又不容易出錯的程式碼，甚至是使用測試框架去撰寫測試程式。而關於這些知識的獲取來源，也能從我前面提到的幾家電子書商裡找到不少好書。它們的範例程式碼不見得是以 C++ 寫成，也可能是 Java 甚至是 Javascript。這點必須去習慣，畢竟書上要傳授的並不是程式語言本身，而是方法論。如果執著於特定語言而錯失了學習這些知識的機會，那我會覺得你這個人從頭到尾都不適合寫程式這份工作。

實際上侯捷在淡出台灣出版界前還翻譯了幾本不錯的書，如 Martin Fowler 的重構─改善既有程式的設計 (Refactoring: Improving the Design of Existing Code) 和 Joshua Kerievsky 的重構—向範式前進 (Refactoring to Patterns)，非常值得去讀，當然光是讀這些還是有很多不足之處。在 2000 年前後學 C++ 的人是很幸運的，只要跟著侯捷這個知名譯者出的書走，大致上還不太會走歪。現在初學 C++ 的人會遠比我那個年代學習起來還要辛苦得多，英語能力也會成為 C++ 學習的一大門檻。不過值得慶幸的是 C++ 並不是現代的主流程式語言，現代有更多方便又適合快速開發的程式語言可以選用，所以我也不會建議年輕人非要踏上這條荊棘之路不可。

近年不單是一些大陸人，還有一些台灣人也開始提倡學 C++ 不用看這麼多書，我個人是只能部分同意，因為有一些人的論點太過激進，甚至認為 Effective 系列的書都不需要去讀。但由於過去的那些超級著作並沒有更新，現代也沒有媲美那些超級著作的書籍存在，所以我也懶得跟他們爭辯。在 2022 年的今天，C++ 社群少了那些超級著作，其實是對整個 C++ 社群相當不幸的一件事。當年 C++ 語言機制提供給人的積木就已經那麼容易組出極易分崩離析的成品來，因此有了那些超級著作來避免世人去犯前人已反覆犯過的錯誤。C++ 在 C\++11 和 C\++20 之後又有了很多新積木，社群的新人們卻少了那些超級著作耳提面命他們不要這樣不要那樣，即便是 C\++98 的老手也可能在世界上的某個角落用 C++17 寫程式並且反覆犯著彼此一犯再犯的錯誤而陷於萬劫不復的深淵之中。面對這樣的現況我也只能兩手一攤，只能期待出版業是不是還能有像 Scott Meyers 一樣的救世主出現。

如果有人想知道我究竟在 2005 年發了那篇之後還看過了什麼跟 C++ 相關的書，這邊可以簡單表列一下書名，單純講軟體開發內容不是 C++ 的就先不列在這裡。不過有些書真的是介於 C\++11、C\++17、C\++20 之間的空檔想找書看，所以亂買亂看，純看爽的。下面的書單並不代表我本人所推薦的書籍，只是單純列出來僅供參考。

C++ 程式語言
Overview of the New C++ (C\++11/14): Effective Modern C++ 問世前 Scott Meyers 的演講素材，不是書
Effective Modern C++: 42 Specific Ways to Improve Your Use of C\++11 and C\++14 (中譯本)
C++ Move Semantics - The Complete Guide
C++ Lambda Story
C\++17 in Detail
Programming with C++20
C\++20
C\++20 - The Complete Guide
Clean C\++20: Sustainable Software Development Patterns and Best Practices

函式庫
The C++ Standard Library: A Tutorial and Reference 2nd Edition (中譯本)
The C++ Standard Library
Mastering the C\++17 STL
C\++17 STL Cookbook
Boost C++ Application Development Cookbook - Second Edition
Boost.Asio C++ Network Programming - Second Edition

Template
C++ Template Metaprogramming: Concepts, Tools, and Techniques from Boost and Beyond
C++ Templates: The Complete Guide 2nd Edition (中譯本)
Notebook C++

效能
C++ High Performance - Second Edition
Optimized C++: Proven Techniques for Heightened Performance (中譯本)

多執行緒程式設計
Intel Threading Building Blocks: Outfitting C++ for Multi-core Processor Parallelism
C++ Concurrency in Action, Second Edition (中譯本)
Mastering C++ Multithreading
Concurrency with Modern C++

程式設計概念
Hands-On Design Patterns with C++
Software Architecture with C++
Design Patterns in Modern C\++20: Reusable Approaches for Object-Oriented Software Design
Modern C++ Programming with Test-Driven Development: Code Better, Sleep Better (簡體中譯本)

CMake
Modern CMake for C++

其它雜項閒書
Modern C++ Programming Cookbook - Second Edition
Expert C++
The Modern C++ Challenge
Hands-On System Programming with C++
C++ Reactive Programming
Advanced C++

硬要說的話，現在想入門 C++ 的，我大概都只能建議自己去書店挑本適合自己的書來看，然後就直接上路了吧。反正現在的人拿 C++ 當唯一謀生工具的很少，通常是工作上遇到一些特殊狀況才會需要在職涯中的一小段時間暫時去接觸 C++，要不就是把別人寫好的現成品拿來修改或移植，實際上並不需要那麼懂 C++，所以挑一本適合自己學習的書我覺得差不多就夠了。萬一真的是好死不死從事了以 C++ 為主要開發語言的工作，那大概只能先去書局挑一本書先學個大概，然後再請職場的老前輩帶你學了。其實我也不樂見 C++ 變成像中國武術那樣要靠老師傅跟徒弟間口耳相傳才能存續的語言，但目前台灣的學習環境看起來已經落入這個死樣子了。

2022-08-13 更新

C++ Primer 作者 Stanley B. Lippman 已於上月底辭世，享壽 72 歲，C++ Primer 不會有 6/e 了。

2023-09-03 更新

C++ Core Guidelines 其實對於從未閱讀過 Effective 系列書籍的現代新入門者而言還是很重要的，如果可能的話，我會推薦先讀過 Effective 系列的書再去看它。但 Effective 系列的書有不少內容已經過時，一個折衷的方法就是從摘要 C++ Core Guidelines 的書來當作切入點。這邊可以推薦兩本：
Beautiful C++: 30 Core Guidelines for Writing Clean, Safe, and Fast Code (電子版)
C++ Core Guidelines Explained: Best Practices for Modern C++ (電子版)
{% endraw %}