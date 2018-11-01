select * from T1 where T1.K > 0 order by T1.K union (select T1.K, T2.K from T1, T2 where T1.K > 0 order by T1.K);
