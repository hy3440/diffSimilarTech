### Review Summary

1. provide **open-source code**
2. usefulness evaluation is limited

* The useful evaluation focused on coverage of sentances in the knowledge base and not *actual* usefulness.
* A user study is required to compare the authors'' approach with  StackOverflow (when no tool is used) as well as a **generic google search**. Then authors can obtain both quantitative and qualitative data  regarding the usefulness of their proposed approach in practice. 
* My suggestion would be that the tool (which is available) is given to a set of developers and ask them to use it to determine which technology they would use, only based on the outcome of the tool; then a **SUS-like questionnaire** could be administered to derive more information and compute an overall usability (also usefulness) score

3. One of the limitations this  work wants to address is having diverse opinions about the same  comparison. Another problem is contradicting views. This **diversity or  contradiction** is not really addressed in the paper. I can imagine that  the clustering can help, but actually the clustering groups things even  if they are in the opposite directions. 
4. one contribution: aggregate opinions into aspects, making the  comparisons easier to understand. I don’t think it’s quite clear what  the aspects are: are they the same the representation keywords? These  are not necessarily aspects. In the online demo of the tool, the term  “aspect” is used to describe the quality the poster is using to compare  the two technologies and these are not aggregated. Every sentence has  its own comparison quality. I think it may be helpful to group these  “comparison qualities” into **functional or non-functional aspects** that  are important to developers. Also, an explicit definition of aspect  should appear in the paper and be consistent with the website/demo.
5. For Section VI-B: how was the data of  the five questions excluded? Was the whole pipeline run again for the  whole SO dump minus these five questions? Or are there traceability  links that allow you to filter things out as needed and then re-run  certain steps?
6. what exactly is a **"tag sentence"**? Is  it simply a sentence that contains at least one tag? I was a bit  confused since in Section II-A, it said "As a tag sentence is short (has  at most 5 tags)...". Is the length of a tag sentence only the number of  tags in it? Maybe just put an explicit definition of tag sentence?
7. "NLP tools usually agree on the POS tags of nouns .. " If I remember correctly, the work by Christoph Treude (<https://ctreude.files.wordpress.com/2017/03/msr17.pdf>)  showed the opposite of this statement so I would encourage the authors  to check that work to see the details of the evaluation comparisons  there.
8. "Note that if the noun is a some  specific words such as system, development, we will further check its  neighbourhood words ... ".. Is there a predefined list of such words to  check for? Also, "neighbourhood" should be "neighbouring"
9. Section III-C: seems that some words  should have been highlighted in bold in the sentence examples for word  mover's distance but were not
10. Can the authors add a sentence that  briefly describes what the role/effect of the word embedding dimension  is? I was not sure how to interpret what should change between 200 and  800
11. In the artifact page, I did notice the  problem of sentences that are interrogative but not labeled as a  question (since they appear on the website). Do the NLP tools provide a  way to identify these even if they don't end in a question mark? ...  such that they can be filtered out to improve the results.
12. There are several ways to improve the presentation of the paper. The  comparison aspects needs more detail about the types of comparisions  that can be made and the accuracy of the comparisions. The criteria used by the raters in creating the ground truth needs to be made more clear. The evaluation of the paper would be greatly improved if a study looked at how these comparisions affected someone's ability to form an opinion or write a recommemndation on a library to use.
13. The requirement that the two tags must appear in the same sentance  greatly constrains the types of comparisons that could be made. An  alternative (but more difficult) approach could have focused on building up "facts" about each library/technology, and then  merging/aligning/comparing these facts among different items.
14. What is the relationship between two master students and one Ph.D.  students are the authors? Are they the actual authors of the paper?
15. In several places, the ground truth data is created by three individuals. What is the inter-rater reliability?
16. Creation of all ground truth data requires extensive effort. It will  be valuable if the authors release such data with this paper or through  an artifact paper.
17. Instead of purely relying on questions from StackOverflow, authors  could have recruited a few subjects to form 5 sample questions. 
18. There are numerous threats to the validity of the results and paper certainly needs a section devoted to this matter.

**Minor issues:**

1. our system can covering => our system can cover 
2. Authors mentioned "Our experiments demonstrate the effectiveness of  our method by checking the accuracy and usefulness of each step of our  approach" It's better to briefly mention what experiment was conducted.
3. technology quearies->  technology queries
4. look-up methid->  look-up method
5. on the the performance