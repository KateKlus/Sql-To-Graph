select T1.K1, T2.K2 from T1 inner join T2 on T1.K1=T2.K2 left outer join T3 on T2.K1=T3.K3 right join T4 on T3.K4=T4.K5 where T2.K2 in (select T5.K from T5 where T5.K = 0 );
