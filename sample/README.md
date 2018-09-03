### Relations

The extracted relations are represented by a dictionary in [relations.pkl](https://github.com/hy3440/diffSimilarTech/blob/master/example/relations.pkl). As [relations.txt](https://github.com/hy3440/diffSimilarTech/blob/master/example/relations.txt) shows, there are 250 `TECH` pairs and the format is:

```
{(TECHA, TECHB): (TECH1, RELATION, TECH2, TOPIC, POST ID, SENTENCE)}
```

Note: the `TOPIC` is `''` means it is not specified topic yet.

### Appendix

| Topic       | Relation keywords (nouns)                                    | Relation keywords (adjectives)                               |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Memory      | memory, space, size, disk                                    | lighter, lightweight, light-weight, heavy, heavyweight, heavy-weight, smaller, larger, bigger, huge, |
| Usability   | experience, option, options, function, functionality, support, access, development, framework, approach, range, control, feature, features, application, applications, structure, constraints, usage, flexibility, capabilities, usability, implementation, control, mode, complexity | easier, useful, functional, compact, complicated, complex, simplicity, simpler, powerful, flexible, concise, elegant, comfortable, readable, compatible, incompatible, user-friendly, extensible, capable, available, popular, convenient, portable |
| Performance | overhead, quality, runtime, speed, time, performance         | efficient,  quicker, slower, faster, effective, inefficient, accurate, consistent |
| Security    | security                                                     | safe, secure, private                                        |
| Reliability | error, lifetime, downtime                                    | robust, stable                                               |




