"""Motor determinista de la Run IRL (Fase 4 / Post-Cima) para Sherpas.

Implementa la ejecucion paso a paso en la vida real sobre datos verificados de
``cases/<case_id>/`` (``financial-health.json``, ``investment-analysis.json`` y
``persona.md``), sin inventar cifras:

- Secuencia ``Dia 0 -> Dia 3 -> Dia 14 -> Dia 30 -> Fechas hito`` reales
  desde ``savingsWaterfall``, ``score.top_moves``, ``score.combined_moves``,
  ``goals.chartGoals`` y *Transition alerts* de ``persona.md``.
- Modo Enfoque (``get_focus_mode_view`` / ``focus_step``): muestra unicamente
  el proximo objetivo inmediato de 3 minutos (``Step 1``) o la tarea activa/
  vencida prioritaria, separado de ``get_mountain_overview`` vs
  ``repeat_expedition`` / ``reset_expedition``.
- Modo Parejas (``timothy-melanie-weah`` y ``daniel-emily-johnson``): reparto
  por responsable (``Owner A`` / ``Owner B``) y check conjunto ``2/2``
  mediante ``check_step(step_id, member="A"|"B")``.
- Avance implacable del tiempo (``advance_day(current_day)``): arrastra pasos
  no completados (o ``1/2`` en pareja) como ``overdue`` calculando el coste
  real de inercia (APR de tarjetas, ahorro fiscal 401(k)/HSA perdido,
  *tax drag* y dias sin cobertura).
- Navegacion bidireccional (``get_timeline_view(current_day)``) y exportacion
  de calendario RFC 5545 (``export_ics``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
import base64
from datetime import date, datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import tempfile
import threading
from typing import Any
import zlib

SUPPORTED_CASES: tuple[str, ...] = (
    "michael-carter",
    "samantha-lewis",
    "timothy-melanie-weah",
    "daniel-emily-johnson",
)

DEFAULT_FALLBACK_CASES_DIR = Path(__file__).resolve().parent.parent / "cases"
DEFAULT_PLAN_START_DATE = date(2026, 11, 1)

_BASE_CHECKIN_DAYS: tuple[int, ...] = (0, 3, 14, 30)


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


_EMBEDDED_CASES_B85 = (
    "c-ri}+j88<l_>fv2#vH&jf*ARfueWph!ROj<>qZjs@pwo1qZAGNmx}t89<4mJG5gS&L7PFg7X3ABhIJzOU}AvCK9*0sMT%nID5vn"
    "SU@6k<;s=olDRHFKU*ZzhbW%!Pouny^JfP?Kf6oPD4izJeE%Vi=H<iiFGZF<J9zf<PtS_!L%fJ?KE-*FWa&@O4(!2C&zA5d{P|Ps"
    "!=IkP+i6t9@D@LwukNW`eMoBckgbaNA)C*j!JmJ|uJWS1NuxzfU!3w6)HKiL{BSx?;<Th^(LFwL0(>2pNgglY%?&^GLU<Z4mh<ds"
    "LG9tw<I{_i^B<3oxWlCQc(cs2yF_&SHqRar`Y#_4{-k`Or{h&oCMkVUlu^k|um403{+29nrrC_21z})X^tg;Z-$1WPdVhnTtO|O6"
    "H932Ga?Bk)rR4(vJcSo!zKXx#vuTzKj4fBU^Q3r)XE*Yp?Nf_LKx!IgW>}_4o!v(1j1iM3&}GEvnr8ECmDBS)p3$R4TojBOm}~MW"
    "PK_sMV$c{yc4xpKhFVKwnx)e?PYWZ0w?%TFCU?+zTF#%0WU-8<fRuagAOpIH=5ymQp3nDhV|)%E8OuC|F=R92F3%Q5G<`_oPt?M="
    "Tg?GUh$Um5+{HuVN9?QufQiXS3IpKAj^No{mbb@D;r)PyOv>LC#x!5i_kf}zjz1dl=VhFi#{DXpLC>*~W{>!85v70(qbPIuoW9QE"
    "`zT3q;w2Cp4Z(v|FwNp=f?J>%5=NH*f0P%3c=;Evb%c}TZeb@p7<cpRk(XYqsEMCvNm>>+#Y6U(-X!Twv|RG?zOp?a!$G~zqxiP0"
    "brFPX`UqcHX1k9``YA3-+z&;qE7xArm1T9pbCUcOPzu|GW(iv_zmL=D6Rc}Gt95R#>)d^1cfwh$a#}5>q^yjA;Ig#VuN7|Ym$q`W"
    "Ebuw-4dOHStjv}-3s_;fc4bnEy)~ZAjMd^c2f~Vg7Cs416^Zdhi|5uUZW+}O2r7?~A~s-O135>xu>Aou1(5rku@T<^@iH5dv`|KX"
    "GT>K>Y()$Tb~OH<oZ`)Gd{^84_$<03-g)3y@Cfz|%ssk+8N#ExXkNsG$!azy*&|Rf0`-`b53@Xa1S-ynjnyZ0xGHI@R?P~W)N{)m"
    "IHvjPDUNbu&mWpEUcx?sZ5$WWYXRI5HcfOpj}2x-^{GB2_YXaDb+(+TZ*MizOG5uW@o)oJLpF_YaxjU<D4!Yk^JLbV^eHSaO(UUw"
    "5zmZ8@|ihR;J(25hv5s^=N@%oj6y&G@*(^#jX#&hLzX9h%hLV3q$C^|fB(<_Wkk2xss!|n1|!o%QmGAdn`IxjN7ZQbONoNELAJO}"
    "QV=SN?mwX1xzC^l%N_djYPDEI`IFce3JAv|7_iCp(~?pC{rGTvJvl!ks6R#Xm5?nN5)z<3GM+mF_|EtgiNyekkUtqnOhd8h)c~F+"
    "XumeZ#rw;{cjGG|HdnXm#pUt%<mUM5dVGC+Q)^VgaWRi@`Hkf&2Q>nSBZ8$`#I$(NVYmT|2TNkurX36=uXq6E<gGvnB48#(KDOF7"
    "E%?v1X&%sjhS0&k)1dumQM$}^^bsMDsNj{3^Tkm$fC~e-9Rm=ez5<XMUKAh~b#!cx*#@+IP&A?Kn^hCq%j4_G<?-q9*>xRWp#*|t"
    "zf?M2dz8T24kxe2XWw1Ezqmg9@#f!;FV7FhSMPA?aVJ!|AatFiuwRsTP{16L@(Hl;d!vZvv{?{6a)_(($@uceoAKGv%@5<Z$5-?g"
    "X@34hQcKV|2rSyPf7bNe53FV8D4q`h#kj@ebjH8jfF`YAxync<xr(Q&9EA<iwXQK&0G%IBU`?-%58q!-u77O6V_McI9NODK<kcVw"
    "P1-c5VWmYIS(j2zFRL{ctE+~09G|eU0IlnRp4fn(`b4oGkYb5c3fg@hU*1g4uHIjc&kliTfr=*YPwV6Ofn6KL^Xp?AOC7VQ_kJ?@"
    "9`yE`<3C*-pItTA()Y~<@W{moC((3@jIB*T5ApOPDZt!7h$Q;^MvdCp3e5`8R-;ncGuPukjb96!;ua{8aC2bU3>AZUL;7rTyF#vW"
    "Q)VR^2nT)drE#S<U?VEdZx&HGeGu<DX{AA*QVCu+)2>EaPt@ByQK!F&nrpqy*G|_pt-X&gjs4mlY|R&1eS|jGc?7C6Kq1Vv&MDs<"
    "9ltrgycG6oHE+p5*3H{?x0tvUte<(XhEvri|L$tsJzx2vdxCE+kDH6S#hPw2HTRpW>2>s(RNL2i_7M!u`?!0O>h)KVvA@M~uG`bq"
    "a@t=zY2;WLXsG#31bnc~wJxvTH~8ZD^}FNCn!@FHTT{#H(;o~61XrHKjcyOe^-kS&!jiz2##YjnKjTIG*#IpN44c)WKF-DQ<<<Ea"
    "2*pF#UX$w^7`M60gvOho>;bL)hOMRpbEpZDn`I<Vm+WmPe^st#@QE?cKt0{>k=WPok3g*5oScu(Zr&Up9bW>d??J-7zM33O{=LN!"
    "EP<vruqK^@b%5)A#aa=}bx6nWug?k09^TvqQ71s&hIQ7Ye|?qd*l3m%(&p|_6Hd-SjDw<ZdUG_PH+|X;+5GaH49tV&JetM>gAElU"
    "%}OwU!RngfVL}~M1PPvH^}+DNyYrLdo0G|#<82{eZIKXguURGQt%^=Vq-n|B<?&xvcwocJcy{)Fe4=SLz+#GWtKlkDPIjCvZt!8H"
    "!j@U}0JPW!g>@Mu<wk3yZ8(yes*N19W_f;gd~-cH<qlw7Q#6OAdB}P{F`k>K)E|4k?<vMA`u?Kzz`No=w`N_>vHR#h=%jzgw7j9^"
    "iBSrA@@2zvG%#n(fTC27H6`D2oUX+Q8jE8GYnP@$*Q$FvbnKzGx%<#u-#u7hcvkylfanyGL5+cn@XJS-&a(pbYJpCDfRXFFTVdz}"
    "n~NXgr<+9#Vt6W!Pwt{=DgMMWU;c|0x;VrgO{b6WXq6_c4)8m{IE#d@3DQ>)J()+h$Peh03Y*~>Qgsk6O)gY8;Aw(N3LP{P?<g84"
    "A<ocdk_RrH@nu1o&7!A)!KX<^3e($1``!>-hHg}d^A*gXa@_F6P#yEWS*5f3F9GJ>G+Hj>nGu!7Pe1+i?Dv+9|Gea523GdR>Fij*"
    "Kb*@`<U{y8{#@4koTR4}j;dqebzmF{=6Q_MCoVN?tN}7pVB^=>>lg;TTNUx_hXgNvaGrQfhx~m3n+RCE0h+@t*q(rVxmvXNh_GwG"
    "mwr?PeF~XKSTw{=9FWY2XmiSE#wwlTwF8buZ4+2Ybx_5Z3yMtMUmZ1QBq|ItiN(cEMJf&ce84nOW(MA|(E&kH7JO={^9fyrtCNY|"
    ")c9kRuA=;j4$KA!yMCb8K{N1e9vuP%=c^JgK#D(q7-}ra*h8rBlH{p|u$M{)`Nt!)!9R9IsN%cZp!6GKP@F;t?r^9$(i$`nQ}|s0"
    "n5BCy+{1`alyk;RUK&)$88>*(-ffhAlqOICpREey<YYm??unm_MU;Px%a?Vc6XIJ#kx(NIf`?B7`}QjhNux(|7{b_#KTqeNU>6-D"
    "QZo=?c#L1&7b}1V#^VF1VMsbeU}|<^&yy{Ncsz^anPldR=rbA8w(p>(v%st31Iu?{-3J;4pW#LUIOlV~Xu@<_U73M`5a*vZlj)A@"
    "b4avGw+RRB(Rh8jIKM6?=xd|BAX`X>X!e&C-gaD8?DRBAU!6vu#|vd7ZzB=_sjmRf$9nJA1Q>jF^^oNyvSM77Laj6X8scBvas%5}"
    "kY6%##FDokS8MKhp|<3%@6}iQSkhqw!$ad534p2fx1t1X2|5U2&-?p-{+BNVT(_R_@>>#ySWgY8+R}alx|pQQ@78GzdC%}CuvKB1"
    "pz~z0THpZqFO#eWa)Z+1`V7|V7)?e(v{utn#(1N5)=)COweC3Ou?)ICG>VvSfFt6MU3{TZD9uiFa#zN1+M2Q2%o01KZy|Q_)m-*@"
    "{Qz`pkhV?EDM<KPI)5_mlKWL2)4laySFq~xnig7<H_Nhw-S=<whOX%mOR$F)ag@rdZ@$$fo$n8T17zBHObyXv1%?FlfViczG8j~B"
    ")Z+-m2E9eYgZDJUmz2f==1KzPmcSrdps|LACKZqy+&=MKuycS5`{Mq;i{mA|!sR~zNPr={ddkIwN!OV_Mo)!NM9IupqTdQE-vAoU"
    "SBs@ltQKM}iEvyw%2>qBW&?P83rYsS4#)!PUJ^<lGcf_7SBc3NILHG!&^*LXgqc!+$WvjoN5q1l4R9rZP1qPU{=^^skSA61s9+96"
    "E+6b~Fkamw@@&%?y&Q-s5dMwH)j5B)hcEZdaNo3E);lHA!%5|$_XsgFg-w75wR@iTqShz*_AFp~?3qK)lbwxe-mn<|A?f-*jClgK"
    "qXFjMKAV5A3^8h9G+)vS$uk004@Zy0qLUUR77R84j%qBDVjf2`BtBYf<A(?K%0ka2A_;OF$dKH5j6^tXF##s&a)o-!UlmQ$DiI;0"
    "Udn_E8czwM42?I~hal02tUjDPHA1@hP;;Xb&U?Tr5WctMOrY!J;^Jl?lrQq10{)ErWO6yK`H>_ki9(<?&`(+aK^GEUWb_kYi*0C3"
    "h+ZBabZHh9ABlenfzXzWun~TlaQu-@0CbH|&RUQ#U-izim=!}}n>ZKPYvd~;K&$acZ{%C{Fc{U@q?jrDmLW`zLs+00>bPGgK13%M"
    "z$)*ud6FFgnuQFJfFtW{tk)zJ`Ust^41nBkl^Md0YQ*S;FsNYp158{p3qgzIRkIwzM_|0nuTh#!2uCc>uqAEMxF}&qp}z|#JNGP2"
    "rbu{r`f?!qW#UcB-*#nF096_b_`46*x~&q9d^a3=!Pl>9Lp-XNpy-_Ao+ep8OcXj%1Nx!bOT#{#?-A11%!28IDfM!df<f6J5a!^I"
    "f_tX%J@C&@vC{B}l_Aj#jVsv2kI1P+cSgQS4Rm)xDnjY7Si$ZVr=u0hAG6gQsSMa3?j00=z^j0YAB>_z!LrPXgvKOkej86CAbb>|"
    "iK1OVF52PWT0hqPHIvFmvYHtD2NpQ=>XxhRI-{W()~TU2?|FPziaARW4{xMT7&h;q47!Iqf=4l_uB`ix>2hvd9s{x5UC0lo(K14J"
    "<^D$O=(URS2o&dd#)Q*84fw_T?X4O@GEI<I+V0zHxU39_h0xs{@KaDq(Y3a9I^cN2ApEKw_XqJ%Xdn^%k;dqz#~v*P+5IT}{}$&N"
    "-sVWZpQ{JhH0O5}8&zl$D#R}&H|$;#z|#gMrOO~b-8J^AwIq_2+5onB**yDoUo@5VUyEOTUsNm!IMrNms6u}Z#@6SPa(bxF--U(H"
    "q|Qrxyj36KJhnuW;mtgIMDzMbKCai<+cj#|e2NAlkj||5n2HT>zA86_69?UxBR0?j0trL~DoCF9hx&I*<X=e%+H}SWj?na!(x9|#"
    "5OfAl#o)_5&;rv{Az>>FYvehOkBZQ~g?}9gJ#C5RdRj6)$nMaoGAi^Te+4m$d|G+2^H}P{R}$KO=+J41ZWGEbRpT918u+48BY_~|"
    "YH2H3b||=?AcXFoYLsxu>rO%jVHD>cEYalF1I+-bSR8OCDNcQ8T=uEB`Yz;U#5ZY8KV+Rd!_6#7MZQ73c)>;z`mDk<hXz8<-;nW|"
    "mN^M_`1me<6eb=IjBVz4?t!BV9gW^fjT#3fn?%m;K3X=(Dj`NFBQl7{pcThea7!VKF|Hzdst5)wm=sKnq%7y88vc5U`dIKS!7&lT"
    "bp+R>&9_s>2h1ucl7-%qft6+qff65Eb4!hIhQ(?LG9KGR^D*gmnzpy$9I0lU5%t%%%UHP))Gt%eMFI50xH7!Nd4M$kld?JtabMJ&"
    "{Bvcze_N5*wYFrI7gAQLT_k83MR<q6swAH`^nU}<r!Qs={YkcA`TBU<hcA5MMS@YNA0o~~+%C_fWWk&{Gb(2h5%t9pH0(wNYE}*q"
    "A65<}CQVG8Vrp+h^vRd%v!jb69uU?3lc*>!qAHfoHXU={47y#eS>e+CwJFX`IyX$x+AEXz_WjZIq~itH6Q^KKG~WF5?1ZoTfSNo*"
    "cuaJ5L&v%F#ecWV7p&xciXW2cJifS`2&WJJU0mb|yJ$F$Q#on8&9kCVI<s_anq{C-JiP;g8mCX+a|hKlWsj%ag+N@P{G7VJK4CYK"
    "Mh^hf8;pv)egH--LM6?iRc`?bb(YQ=O+1_`F5PveYy3HrCOWct6gr7b&OsO+m16cj&HlbVZRvEH6RWByp>p8P%X^@tLYu4R8;#Lx"
    "+M5x(pW!xo2dWip?BmLboPD+Flw9EN{C1w))0H+k#)PIX;1*pTOFRBlLP3|WE|c>Ek0ADB9S7FPba$WZLknidwS|W{15kalexhu1"
    ";8fxn1~OI~t|A37nh53;+zFe!R_=Co=$YNvR>)qDPwjL-?wC5QIN_)tPyFRrc|SRVku+{an#`*NLpWQBu&0W5afCvepWhuvc}ngq"
    "2UbUKj`Dg$c#e_+gqIB4<%n0Ft%mWDWBU44t^(N(WM8d2bKw<%8evhK1HXJ774a$E0rDg$ws0EJP4S@P(!Lo>MGPP=rg^edp=e#6"
    "bv1V`0;3T!CH>NxoppKC)jMOy1o9Cm@XqB9EG>{yI5Ba9&DWV79zJYUa`<*~{}2}?u98kTKRtUVW7!IMp+mw_U7T+pS=Dq~+y-xA"
    "nr}Ki9Crw&sv_{D8^<<??i{`HJQNW#l9tBuF07xP8ds%n)G~<M=kAwYeQDJ=yu6NZP>@U^emW&b3AG<YOvEgnm(g{0+PG!y1-0r4"
    "n~m#1Fv8K|Y%A~j>-Em{XpdIx&yh~DwD)SDDw?w_KV%-c?&`U^*5`ZQ+Utw?s<<le8x9|9I+I=jU9J$78${Jxx64G;PWqMfEK3F7"
    "dd4)q1+{P6HEn#Aq+5N3>m!^dir%Z;gZ)sf$$HQ>%xky%<O7mSXah|&mvYK-5vL$Pgo^Mnp~e(HivZRnQL)7HAoZ*I&^D!LUgfhm"
    "l`+@^X1ACkeVZaUSlIFCI0picNf$MXq(H8!8VTKit`e)3`xfB?SPyWx`BU|R*Z~OrhZ3ZJy>nB0^}gPnSwVN$bV?_Yeb{_wwm$eS"
    "=BZwZA;j%xA_u9@f7Vtm>fIeS)PyDsa=6;dM%PuZmu%x9!~R|vj_n~CUlJ^>+rF<GAl1Ha8er5C2)>2i?uJRKH5_%d%euPkYgFsb"
    "Z0-yB?rpSWPn@aJP{oqTCl%7Jq|CwiF`Fz(A|hDpq&$rB8RxOUK3cIhAWDyFn(uT9T5NWAr-vPfy;kR<W^AdLoXT=P+A1o!%S7!H"
    "%!h|!w6iQ<aHN(aUHk#Jt+yk47&vl_>+G;TKdVw7isQf1J>Nvc4^T#%AsJ?s7sL78;UN-N-9m-&t&vOW_iV*#(UrWRMzoX6e>=Vq"
    "%O<pb_&kp}-oX?xy;I<+7jb@v!1FpOl|deaRvnwwxq)Yoq~xzewEFZ|0!1p}SXYW`T_2-JsQ1s8pW+#%8Mw~0!K7-fY-=?X3K2Xg"
    "6OL4pskh;ggELrTFrCS-i5Vd?@C!!2iWF~U1p+F*BKe?=wA4Q`hkd3Lo%_T96LktCz;Z&j#A+?ZGFs2<{;>X7H;%hLQ0E7higW92"
    "Vp9|EOKpGE$PA=6=IEKEcXOed)5%Ij{Iv~co7&-ho#tRW1wM__Nf^Kq9BW7-lCEC)Ky+MI-H(a8xqxEJ4u+&?>Bp{gnO-|}1<T6x"
    "ZH$Vy*7iC{i9U*>Oy&WytRV10Z#eR*XgHmfNK$QsXSud-1?DjHHh|YL=*SOj+a6lMPJ^~P3c?ZSp+nnlpCxODC-oP+LLp^oX`E=v"
    "y)z75TArwRzAal=uIrDSp*`wqbe>k{*p@#E!(bS;2NPShP;z)^dfrIxajm<fRgPytI_=d~o3H<o$IFX!I)0P*{83;$umaC!K-yo}"
    "re{LKCQO#;`=K2UeShsdo1bZS7n>&28c|Wkmo}i<IZt(Lp9qFD&<}q`9_4+g+g$R*q~}P8=cgULSYUt!UHBpb5T~k3d2e?m?;I$o"
    "^K>;Ylci*yp67QtG-xC$F5#+NHnp(e`CQ)8ajc<C72uhc>4eN6y1gY-A1zOZ{+{sQVRHTB&E)Lx91j5Mu#o@5Q&%TSAht+bMXd>f"
    "xo#zO&|kDZN8Ghif*f>Y7Ab_AM*rM8;Tw%Cpn@Us>`pjgADEyBk(RU>Ug-hy<(rI$X*?$9XOx}g==ja#?D**B_3;_}b=^S11^c5I"
    "uZ&rIhl!J<_sDOzO1mM44w;!+ud-FnH&^<M&NVj?qmWG+lexM+Km6_nNcEyg6lFI3NLPe_7%kfPw?G7C8-N}3=H&c`HIw@70Fs$G"
    "x)5~~-^DpP3H)Plbv(XAqV8ljYzP15*uoS&z->A~x+Ep%w+HF`$MMNEXK9)=SMV}>isrzT|C@oYelwo@{^H{N^7`iba(s662D59_"
    "_aEqlARPfHP=C|nP9!G$O+b5l{{8Xg8Rq8dVU}<4q#z~lwcnge?%wh1_gBF9udZ$`##dL9?~l7F^EKYO;VttrDhhN<{jF*A;`03B"
    "_!5ZpWb$wCCr6aa;pX^z%Ar*kRWfd#JwR2iz4V_-R+(S^0UCpJtLs(;s~b8EO_mu3Bi9ky{aiU3*1kNsJ~S#PM)heB*yac<D7SB_"
    "P7ns5J^5kZR6WNZjfQmDx_PEnID+OwhfjOtCHP4<$m){Z=mvgdnSlf5pBMB2Z;!mtHSOWZ>4V-5yiqV3ZU?>erthT-$8iG7wT8ac"
    "H=bjIg)?IR;4RQ)T9)ncsfAqEaULH_ulefWvCr|84@O2oUEON8>98PrJKDy{6&gE^w{FyW>y6{LJOA>f7A?ud(|Li9$GjJMvP6C~"
    "uCj6SgR`zY-W*(aes}ng%x5`Wk!Z*9N%8SQOUb?GzBFW7Zq<mVF{Z|~lQXnW#aYKmLPw^XQ}3-$xhFI9)Tf}L`)#wCs<1Pi-MU<N"
    "8%FSI7n}e4I2BaqhDR~j@th;$&#3KT0IE1Lg?4;bY>4^d193)asLKIVX~lUa{Q2(q<oxibXCFSu^{xVh@g)3H5<gZcSmXty<|{H!"
    "KGl72Jg>*2#}4VxV+S7+IR@>~buKu4x9z)JnktJ=p6(rLIpHL_#~P)*%jPqoGam9ey`iU(LubW5_iTfTG)-#MMaWefoD4PVzTdAJ"
    "(*F5S4?D#5R0s0WQpm7ad!!Dp<tO~CI(hw4zw7D<?p9&^J(1l_Cjh=!t~U{v|9w5kn}5-ys|Rn5zryRM&ZXCV7^;z_Z%04L=<W(T"
    "eMb%lEl;j?j-BpgM^5uYbzj)+X`naN?-8wr8^yL4{n{tTZ7}*jT<c|U+zI6x96Az*W%PMG`xMdD-RzrfTjHXhyY_NtM$+nUP7!M3"
    "(JM8VsXD6`)WCIdllJ&b%;WoL`h+)UjRa_&C<O6wqJJRrxa<3yUmy~`OE^}Uz9e;y;zsG`grfP;$`LNpACz`*6fd&-JX$`eyj=ez"
    "+DYfl`s=7ra3XeUZDd|gp_A4+;2o@*Y#8PjUf}n2tN596B~=}t)|{+5og1do1);kkJ2#M4D&5~3#78lbAegg4MLWmk4;WC2;@c7~"
    "u_Sa)w9rWAhvJq(>q5(Xk9!c`aB2gh3HtMUrKd=hgm#W{{~lNa&RA-DQV8<-WF&gC2An3<QSXH%Gq48%y`gNdyx-)sHKeTd{s#hj"
    "FFv`*VBbAy7tqbV#{C=h%Rm2KB6KQhxROP7{w#^&tT)pvy{=OAtA#`Vs><(4d416;S5Cr89iMjZ0N7*WG@3v0ZQ9Rmv<qED75Zqt"
    "UoRkK>)t&hV>rG@*Z)(ha#Q7VsPyvY?;f9lul5XRII3KB48(k;D9`UuS(d`@O!0hLB|NUvOabW+Qx!20F6}CpLA@D9U5j1Xoyk^^"
    "fPBE=9h9XO*@tfrJyv=9v-aw*um@B25F#5GxahV+eYEotACgxThUlXs9C<+@cF}K%ynRTnQG7<twyB2)bVma8hu~n0Oqq0q+UV<b"
    "BnEA|7FnPfR}7-#6rjxt`rN;EbMD&Ji)%VP?RE#NKzZHtKikRkYr59+Yr4DV*HnJfaQzZq7DNzw^pcuae+1Jn2vYjeX%zp=5h&jm"
    "=Z|T<#zP~>Mn%>%Lul-9lfAt|01bVikK7R|WrvM6UBOb0{iT+43>A2;*+q&5`7+1=b1mAr=8&emVMMG<?PWVQMvu%Ii{Of8WDf3i"
    "5ta2-!CLTf2Sx~Vcy;}d<PAJ{{H6;<?#7U~b)jAxqq(+bKJugwmj@-kCf$@*2mOFIt&GX-3((GHS5(%8VxJ$`VGdgU1xt<T*C=f#"
    "<u2!Fl5`*b!QX2)A?vWCc2*x^PU!f|s5R_@OIAivV5tY&%xb%@o0S^Y!Tlzlp);b)yl{=tHa&yeemHXV!PSG_!QV^{$Cy{CpG=$}"
    "sIQWIunjs~)Awr-sRz9fU1=$)IuX*YLsCm))j5fvNov8SRcXcUY#zjJ4q|T_<lWVHW4CUjS9epVlsk1(uTG;^X9pU0nl$cgq;Vnt"
    "jLq9rN#)LwMG$K>vV71xa%Tmm&Yephe$~F^pIhNW1khGc$p^hqp_ni(bhW<|8KCO1+Fr8|I-zf}olPrJvkEqLzYV$6iLf#cHusLl"
    "c{R4>?jT02#>eWxc0x#~Lz)nhPZ~n#E|257Zq?P{ezU**uI@zMA3E@9C<3aAP0iO*Jk+n`PREn8b(Djt4LffO$JfVi&o6&mr$Vf`"
    "37niAO}?KT$&wqLNcEbG&})-RQ_E};S?e*kKE?D#98q3#x<!lotakzp+FW~^y3GW);q)C7?3&$<Q)|QCqHQejk_*F3?Xac*w1ZBF"
    "sl7bXXl&`K0`J!nmbg`0i|=(GHm>8Ul1S&5*Kf{GCg*F}V~am-v10X=Za?2)<vN0a`?bhzz-?)f`^chpN3N=KwmmwV8+^O{?RMkR"
    "-5HexaWC?=0IrR?necqw9etfwRXgCaWd?=Yk*3{)PN~|q@EJ7X6ly5#D(=^d;jKXK<x95CN!^yLaJ`*5Q=fl#Cuiyc$!WM6)@n&M"
    "0J*_v<{3vwi_@reu!%5<9RYHGJ%FkL<$I(gkORxh9pUqSJ@};W>W&ckzaB(Q&!6pq3U&Z$9R&Ji&kpjozgXcGN{(xG7@k{i@^IIl"
    "niydJu|YdtB2u@TJ7A(+1#$}vI8EN<cspQVv};do8u-v_FSXP;H`p4bwY%mXGe%uOS0kt=4ZEmb#j<|lroGw0bgA7e?X=8m%4Tl4"
    "-pxhYcD1b?`{}jCcQ)3xsL8pFNz*!v{c4fERZpEPe-i?}wdigX+>7&qP7}Xo88*}!{Z>|U?+Um(_ta<GeZ?Ah-)s#uQETv3@vox<"
    "bP1NP7%%uG6Yu5jE!Nw`dB1d48WQ;ns;WCOS4=%(pDOFt6P$JWYJR(X6us^`O|#}_m5XCsyM!#s=u<XiUy~}X-?r`EhV9H7GDAa!"
    "DazF_ZW>)x#)geOOHg{-ic<{@5_zm}A1${`y`U#;kaO5LjOWVSJ6c+b+E;I~TrFmAo~+JEwV~E*)ork>R?xC27HKQoRm<-C!Pcly"
    "UpZSN<5GHX`~rkjGjyEw9x1=bTaCCVx-Vf>EOr+8>DhJsIVv<iwGGZ}(pj4l_Eg<>dzJ_X?Tu}f|9_op)%-Ns+l-w!yWA*i-e|0b"
    ")=R933^$DudlhSI6l;|UGsSp4rCe3|$n~|`^a6Y9nki5Fp5B`264y8Km~mi^jd~KkX4X5EA(K4zn(epEm$+?J!<q;Gwx7ssft%;k"
    "`MJyyxz!B2dgzf=$_2hAuO5nsQkK=d;a$Flf|nwtT9m3LnkQ5BzWKeb#NqK=vjZ#=q;F+v)96GV1}1r=<yNb=30S+xVM|W(^}yEK"
    "H2P_E(uEY^*jybmuI;X8Vzh!>zJks-Ir6o?=O{fwH~rQSQhDhaMg%Q1hY~358VLa7kthdmb3#=ju9lmYsNGU?<30rTeV^q|4fpK}"
    "<!vOKLu-yfU;;`daUlF@teUg7diY_WdxzcCy~BjZ&DQ}W9a`Ae!yMYSH=-BKTW`LqWlu1U<7m4H@Lf9l<mnMy*uTT>s_3-Fn5aHu"
    "w;OaA^Mm^QsYc1b8k(VJcOXHZ&A~pv=K7BC!lNoGlXfOGb2!pm4ksyP0INcadb|#QW$!}ir$>H+Xd=7=(@GxsG(7YA93XpP`R2}f"
    "8-47)ji=;}p2Ghp1#~+Fw2EOsnyQWsie`c}>2kZ6U17Nk)?@=RQ^X@t>Bu(8AxtFDYi9^s%$N*<z#WFJbVG(+z&Z0{Y;gS$rPAKS"
    "9)Nw-Z`il^MsR!WyUNL5Mc=6K8l#jh{v2b2ML43$OM}}~vB58>WEMq&X{|V(pxI2-mXmR<byp61z<2jRrsl}0epo*9$IfedXCUs?"
    "U@L|}^~1M0MxcJhVaosS2@!(Pd~3v!LIg(;t_c`|2CfxUKRk1!1-*T>)w4q|PW$+StgeQ9hVdtt<F24aESXemZS3jZhrc&2ferH&"
    "niRf-4-9T>e%tqHAY&Qn15`EkS4(3L{RKSp_uP3?C#?h<79iwu_RaD1u5m1C5Cey$*32Y~Jz0Gb$Dydo4?;C<<A`8;zXYRLoksNr"
    "8g#3~v=1%>z=t(hsR;+|veJcB0K1mtSd}lssyvOwK}~L8xTbSEFyeCBvod0cxQVVRtn`p-scp9mSF0rzMApCX&3)h5e(BZ&^r0)-"
    "lw&W)>2c$^3QraMOUq{82+~#BVl7%wk6YsNjGidnmeW8zOn$)HCY}FqBvWTfeEkb{b>RSe$^KsH?yOoEu;6|wY`+}`Yz>I*xH4Ry"
    "%Hv@=)GF2u#rcB>RX(VWT?g%~|DCQL&7}X(=sS8rfeq}AuRFIB1Xo~CP0Lj-ov{COd~`EDJ%5k+ktnZ9oR^q2E63XBdRQNQ%^{MU"
    "DUV^!QZAu4Yac{4%$B>=oFCP6Bbo;mFm3KNVfbmo9%^G%soba05~nk(k0}l}<X-Oth`K(-bEf2Pobg%4MB+u^pC+f1e?R6Lsj~Rj"
    "do>z$C3E1Yuz5+0`dp~u01gqWYZPUQ;i+Jyu9wkgJfM?%1zuJGdqPKG;VsfkV^uG`{1y?SblT7IS(0KrMp<=ZVvZ${gSLpyqk`kw"
    "Yaw>eCX?%~=f`(<@sw-LuI>B-hwUS~(er>3^Sy37w_JN<R!Oejc8BEf&ggq7E+-ngbUn-R+j%kr14f!59WUx)WfZ<JIFOYBTI?6b"
    "UGlje1k>n)RVuv~u+D-}*lzg-dtyNA%}r3NtGrH9)zvdvYj5<scfJFW?QF+xrNyRTDK_I|+6n$uPd5JRg|=2A;j*2HyDQ60W#*Id"
    "E{zKL`-QH@YA?l;7b3qwE$=(<^R{uwK*?j{S}GNB)AZ*ml$FJj@B&p0sS3D(4B{@Afw(_XfxHq6Hz!@K_nxzO=A%eOYx8*~S|zFB"
    "*`u1U5^Z%#Y&BzP-BWl^)XAvQVM#SpPj9N_j;QPdQ59U40u(PaT_UTe6h)r#VbEcgwaWcfS*JJT7q4aP-cSNk<$wMLmmIOI3C+z%"
    "*0(SL>ZPjdi5O~Ss1H0pa9xqDt$mBdeRitBy_KyG_O&A1s@%~eJrlP%KXPTjo{TPFDL=$1-p+DGbgcNSoO-tXq>)-8^m>YI|6<~7"
    "XJxMPCd!nD9B1B4DlMhnx|GJU4Fh!Fk>9#wv`Pc0)qWO182>-ap(lIi+7_5^3e(+m<jRq%X!VdU<GRUTH5#wYuM<rllK4}sCE4kv"
    "eGN*?T-22(ptngC%j`NHa51hIP;L2IXFqqp5jXFi<GG&C8S(3zyw%hUEOX=yU6*RArYCD#yT0rA*3h=9>jI)oSdt%_Y@8FsR4b{c"
    "=;UK<?WM}NDOHsQLDo`MZpbl7eP4HUBJ)&sjZq`IT0+jA{%Rknl$$c!<6k)2qd*0x&=ls}lRR3qedc^Ol`~!-pJdg;6pSLKgPTX0"
    "gva(>N++rw-cViO;%26bPS~~=j+F1)%}n@N+Wv?l+pB5;H&K<oCk(85x2eP(4@pP7)dYgp1i~#R;D;eyU96jc4+HqE3AjFpJHKZJ"
    "p=D8UW7h;|$i@W1)&xe|O~A42Fxa#LBWL8g?Fo36C2C@}Cou9xX3qq8$i@Ul%?Y^XmJ{$tfn~3s0PHz4>{tP3G@`k8(h!iH*Ea(i"
    "vpxgIY|X&hZU)GS=*)iI3_@?@dL1)>ZD94yzz=QD>7D_P*_eUVnt{FD3_J^IeEkeu*R(>XJp<eK=^CtS2DWX6j@LZ{9<wn6yEOx6"
    "%NdM()8DWLE-2+)YXBA~X{?<y2u3Dd=5@`0#%#>MY0bdhZU%lBnC^x(@I24=+pN^J95d|O$d2ncVb4C`F&i^*TQl&sn?VqIA(6tG"
    "8TghTRF!V38Gu>U%S&C$<=d~08St2m8F;N3_}k3@<P<wZuA4zH@|`v_bw&aE3w6$5WRBb(dB$TlX3!GI?v?@>7`pF|HcSDGG;7q}"
    "2u>I>&+nRo7XY{I*~((j#vEEQ+1*kmgKjhm!VPl>Ez@(_BEf;x@%om*_uY}xLr7xK#vEE=+1*ks19P)2bAwzCLCtZk_8dSu^^#KH"
    "JC@TU6vUv7IkY6Rx20r;Z3nz#!#a#yAey#Va6o++_0dx31Ly3cB_6as2e&1gy)9+41$<?raJEbvmfvho!VP>X*Vd^Zp}%?9GYKBG"
    "F^QIV_O=wyph{Yfy>SvF&viRi0xhsU0d1iM==R7rF>GTNEfMW)DWbu$3f<7(Fbf#evpd+UZ97ibtLniFgTA%kVH>k(iD_?3F%23`"
    "=r_h{&%*Ysk=3!Y&Cm||2+DFswq^HhZ82<P7A;ZjdE44;qs?XmI*0}xJQmCeYt&0oo(HPB)n~hn+NOis64&0A;u^3F6uN0&xK?Pn"
    "9rkAsn0D_h0yHywM1>f(F^iVS_O`X512^!(4SJL1nI5OhY0LtY(6DzFBQtbIeRebt+n7a5XnWfl(jh2mp|xoi7HG&pdls(MFD-!9"
    "MuFeAFL>C-ELvjQ8*Muaut|J-6GdS(Nn44vL5g_2yL$war;j>kLBlp?(GuLgx$P_huc;(-%mP%_4(-E2o4QXGw?eES)3>{M*!nEI"
    "mgx4aZD$d>fwO5}fK@s&!}csta`zrDg|_1dUf(Qe*v2ecvfH<}o&_Lm(^`PKG#Yix!n5t5cV7gcM44{yEO6MyELyVLceb5{XPefh"
    "wQxWsAGOsekcK0xmq+=&GjjTP6c5{&MN4-3+sf_`5Vq-*0F(*e?9ga|2YJ0GH6CceZtu3BQ5%zJiEe*e(H%JUh!o=WYE)=B?al22"
    "W%qI@G{P;vPg>BZjY+g5x4*6AhDG-_ox6f=iXImoYI*4PpZYn0YxbVJ(x{C|v;?=mt>E@e-?TP~Jktx!po7i!YUFmmE-OZCOrRyR"
    "{cUBoH?qx*s{qE4)1g208K_tU*$?^z9go<UKucWv+lp(zZS#1pZJ~y~-?5+j;RmJ3>stUGumOKdPzT!zY7cam(FV3U@*F;&+zx&;"
    "$b0FB$E$<yw<L71t%L?$-!?bU&&Ud0-`g7e5CF7#sfWgEfZr0$!M36q3{A5!R{M-5v~6>H>IYtL1-*6yjn@FbC6j|~WwHyJiobz)"
    "LKjqPYisbS>Ukgc<nbEdw}f%9tuS`oa3l8wbcX)+wD02~L7xQU@fzT_#Bi{!7)JHk-(W!p!N_&}t-<%aQE2yVT^_FieoFuc{?_1w"
    "l-WQ$0jV`xgAZm}*mue;#%qAz61_pNHTX7X`(FpXV};K4jNf&9&#`*J$MG8Aw*+qx?g0L1!y!@tlDEUk?7im+e9Kw~{-|+!<hR6b"
    "Fxnb?&j~kx?~hE&-vNBf4_&7hd>pR<eoN|x=GL6Y3OAk2`+?>8+w*-`DbwtweHyP0e$bM-;kHuO^{kP-LF)Q=7Q8+7@dDrK6I(o9"
    "1N@fM4Y!rLuJ3O=wDV!PcaXZ4yoBfkpT=u|-;%oF_EOgkgAGc94}*F;sBB=B^|E~$t^s{Z=!V-0T|At%H|<;tjP4!yChFIH8V?QE"
    "fW9Sj!);}*=LF$s6X}5d9t7L-9Xsq*mT9yG@GXfOZhcq{CbYXj-|<G4y#v?TcS80|>I9$0Yk=R9xZ&2uuI1UmCh$WLx!Y@-`=DU-"
    "-6@Ol8sN7iZn(9dmk+w@220TkeBavv`xXEc_K`jh*nqz!a>H#!Zh*cto6sMC#C3Ln-vOPtkNSDQ2K+6VJK9#}24U!U8-x~Er+m%1"
    "E&M<}y|y9`Scg9}zZ(7!W9>G=AGn^m1N=VllRj&U2mJEk%a>;Z@j1G`?nfdfZ}^uYOP?J)!~8wdhj<a)e2Vje9rP)LKg!vUxZ_)P"
    "`Hu<_VNlFh_tbR3p#=L=_*TR?s+11GY4i@$3f!b!!3TLJVhi-(z$$E^iu1UMs{Cpk&Z%l~9iLvDoc}07+47|Lc(c@k7G%Hzm+0e|"
    "pP!zMS4Ej{S^!!3?x$zhf1(F}OO~*-Gkz9?foXB_y6E!_^qQpiH$@dlcQrYCdveSjJ*DLX06bL*_%J7Qk*Mg}pH)m_Jw13b{U|~t"
    "IqOud)WF{RtD{yD;j4FIIb`0D1FCr!KN(y^dS6cnuNMx-kd-*Oe<*K~^rixa6LrO$j^ZX4kt;~kTnJo)x+i0NHHSZ*eOI5x)y2`J"
    "@p_(R7=CeYyo2G5ACq`KGhS!u%s9S&Q=guEP@7%jt9C{7-kI56$J8*LgWH;0cgFE*YFCHvE*f*2K0HRZ#{1#b(72vlT;Xi~{(t@7"
    "TTEz@-pwfzYX2h7N)C8z&n#R!v)-wR1Fv1?_N$Vfy>1$2=QO^K_+W*Ox>xARI7&WYzBZsZ4o2IK@J=u&&8VXF^eL^`PF!oRb8Y<H"
    "r}h00=k-~AAEg+FGBe&>UmY8ibqmw`@DdbTP7M%(?EfwS(rb26pX=K7b2u~Lx0>s(N{G%{Lfo1TJ6QLdtLvjb)nR`F<Tgi26WMFM"
    "-&1L7qi^fOi&^~H;N)=nWZ%3$JNilv;;du(oy)c}=lK45(nFl5S)O8cff6RoF=Sj&fEQ?|4fuK<H)iIq-GIRw)`*(G$N1@H5tq5D"
    "Vtf}(OO=SDc<3%(kJWqAgwe7P=>f5>YQzZ-00*xkj?Rj15m5)C6m5a&XE5VHT4K1KfQ#zr#3Dxp4$7sQ>wE8~XU@>(3_?If8K(^-"
    "HF98ZJy#<IqS^=LYhj4|w4^yL=h2jd?co>Ysv6dkFV=qvF!!d>a>=3hKmGL6v)@}b{=<8(ofLQ2%ndp0N$<#UMJ2}-tph{VJjUr0"
    "aSt17@PR_T%IoYkrc}5CO_QRxc%Gnt8F`hE&`4DZA-P%~I4mv7RrV>Fa5@uO;FtrLMZTtikz$~nG0PrRH7{e8&M~Prjz(=0SV?0k"
    "l0FT&EVCpNU|kIwi3)>Cr-_^r6{$3mRvj=+l$n9Lv;j+PB*5EKz_Wy;YpZKyqBk}E7^N%BX+WV*2zzS8fYT>~O`R6a#F(xX+3&e1"
    "68Yy3L&SpYZx5k@iKkCBguNsj|8pR;k%wzngsS{r+o1FtWAFnfKoQ*GP;sO+XdtHWyTTC0CGKHFDCO~)$+QC%a>fnbvv(V%A7!9@"
    "0iUf3L!`OD-2-xUL2UbFOQ1GTbjv9h41$LxL*IU-A!+nz4nr7w@#pD$H3QDr9+8?QDdybO(t;>}2gc(A$R{KnA}}>OvFFLYmbthk"
    "GhbkR&RQN-Jx8jd;4|DP0Ox!T7)_W?725(}ia7tYnM`+FAJTkEN{MjL9*x(hi}UMZf)gsV7i0_R5Y7GqHZsQI>ltESokpL>RW^!k"
    "L;@i7)z&#}#X8fkA^ycJH?VyL`6VMqEP4BJwdPtPVJ%;<TJd8^hYbvam4^ht)cRXdg0=)5gs|uR{XhT97Xq$Z&v^MQ2}7)>22>-h"
    "@h_$enZ|jY){yrMe*#+-mPw?{ekIdv6Uk~IHz+Nx&tScd(PSh<Yc(x}V&l&mO2)U=9j82&5#eA)5tk)ZFC_lh#TP1t((F_xcV!Hx"
    "tr@G$td%_YKtbjCYA*Y{egL{PNZU3dP+pPnvvmGsaPBM0Df8DAtUAf(l3GtQpweXtyYJuV4Sqvdf<3f|BeXFLOuRxbSm*l#-~gF+"
    "9#ccm0B}e^4~SdN<pMjHH|lW&VuRkI1;cxq;Y&(m0dpmRa!X(kEznp)Lz4=~4Q`)!F4#H1g?(}V-^KBgUg7c|03^T=UOnYv!ldiW"
    "AET$jD57L$V6r>Z$Oh1GzFI7eVzm%+Neb@pC}R;fn+@RYEhrfPJ0J_|v=K@lGcf_7SBc3NILJfxh`>A%W=a7fPleGQ5etGgz?A?t"
    "VPn+z6MytWo>a}Ff;kYSlS257z47WEk%!@AF9%`@gnwglb<SVy;mdt9+&8V4^-hWOa8kMGJu<3XN5J#E7qvc(Sv*Y^n0Lq=dY<fT"
    "O!J1t_zy|f|6yQ0q{0C6Z=cOSScVw2Fq$vvg*ep$Ru4yy#G;cHBo+)d0gh@cl42f5ShIr{+rTU^##6R}%@`9&U~1Bb49T6xNa%I0"
    "k_jzWsJHx8(KM|R5i;tfOt_%&lrYNBcteMuOrjB4eK>h)gmm$tc3dtF>48;HO%X~XqU+=$8S6kOU$AB}_YS48)Y2MZt``)AKx?3%"
    "vi=j}j-f@)Qkj-!XiSJ+9v^gR78M_fe+hxmmW;3wewlC-$#FD|P|jMAFsIj<Wicy;#5Qp*u-ESLY*8!dEqSC&uT*D~G64_vKrlHD"
    "VS#3-<9?m^5S?7eVv$FHW+6i);K(`~>orM*K2l-|@Bx+7QRSa${fN;EVNk*H2bj2I7J?RG$;xawG<s5lU`yJhGIQz70A=T%rO6Zt"
    "Z<-ar#zenNyh-`nt}I@8Nn-(j_rY4XRb--*uV2-Mc<jzXHtfwUGwj3p9wB|rEIw#ei8#qrgFu*rKML-d#+c_DltZcE5i3KY85&ox"
    "iyx6wiSCSil^WTqBq~Dbuvo$F#znzoPzvRb*=mkd2J8>_&ald+Y!oF57QX8GB&7LmJdJ?xQG_Onb^*C)hktARSXHG?F*B7)oLx-}"
    "{sRjfdUeaSN)o0~Lu=mi_^uRlmLeYS5Qw!iNF9_>Pk%P-O;tup=rY1<$^J(A+8>J6P4-Y4v*hkB23!$OOXHF`J03e2dsKYjrM@Oo"
    "ZIBj>$oVUddMR@#P7(7jqI@l+xWEkH_Yd`tmbm)B0gOXbg|Kt69&&0@P#2_~04dhM8ye$^UTJao_=ocj87hI>0qQT<J;0-Mw{OaD"
    "t{QM3FgxAHETBS+5H&E9m5O*5GZuMbJ7vqh<#8zpT>+O+^_<03_Eas6?65%<!xohc`oEoux(sL)rPE}d@Np|Xeglt>;&~ZuFoj?p"
    "4@Gk{i#hN7hn`$_KY!!ZdfQA#hw7CkEcQfhyep9#Z$J`{ie`fN=d5={>oALQ*nO3N_=9*T6y`|g(L?r_muRnHLU177zr}gRWp6}r"
    "k_Xrpm}anb#UM1^Ur5ytwCk8(J#CPwy2`|t5yqaD_YY}X&xHB1c~#-QXxf&)mUyit7aVSr>u;b8+9q{Us?M$Y5Z4DCWMAXQ*Judx"
    "p|3$6Jcc+`-HO{P{~5_Y{?N&A!T8Hq9~Xv+(s7khh+J9Zm*jlHV6>#GLc&%UT(kulF0-Wr!KyJoHc|)CgX|8|L`H=^<gdVl&uXHJ"
    "#!^gCvCwb}4!WZTK4|1_jjN^Y62DxoqqC<PB^>g)lTL&%ieoxfz~t7$YFaTWfOH>|q%0OM`z$hj7xFUVo3v)mu!)%AW|pKP-=G<{"
    "V4EKBg%}<h2swX4XDuKnNDqaN@8U;sBEbV=n>ilS;poDoptsTh#6ih~mb1H$mQAu^DSnsC=gLllRs$M<TM9j;%t-31)dhn)1<N=o"
    "%Q;yxzn)z=7JN%^OvG><!8K{~?X1TEvkJruzoqklG-C*q_}H3TYJ@Y~kX3lCtgoFV5cSu$i@;Zd{KtmOEnl4zh~q1HT9uU5*`50W"
    "m<`CwBqgSqtFxwWD-yfbmQIlhDJ#`3610pWyhC7BlFu9Zzk%q}7qgXVdhPP{@wN|~^>bRYE2?4`bZ}(WbG&nbNWDJl7O9xO=;!T~"
    "n}xjI*>D;6rCB+0!&MGhOk85EmTOtBHDGXgH$C&X_5>K>z4}c_kWb_V1|>!w`S2f68*NHwtlEX6R^vy!1%j@>w;UJ!jrbp~@dK0-"
    "iRv}CD>UY69T`UB!nW~tl16LZ%OY*&z;?*diU0Y~dCe^Ebo*<3PKBGs_i;W;ro1!nkuK2t7s&oP!%wubXQ9K<_wBLRX`%jHkeDns"
    "DXb}cQ>F87m0Qtk=!qAGUTuZ$Q)>?d9gtTkJyA<+NV=?OqiXe9E)I@ER;%_zthc(r62I%6$Qmzgx2j2<PDGIxs_!(Qf_|8d((<v6"
    "i_g_p#KT&ZmPRk+9!uW8dMEe{|J&%J+dprt_s5=Bjs}%uQ(YPHKVjA5hi_5r?Vi(PcUN`$M^=JUfOQpo`?@l5ntw>m17(})aqDV&"
    "i6SEErF3aWKBtxJ`C0SczXV~rT8gc9N|z;#$`xlBm2=T@#Pb0s)lI=;Vq@=`h{;An(X)L{N<E&>rDw^$aNjU;P-6$;s1S7@^8eUp"
    "{|`fX(GO*nDgEsXS#=I34cf06Z9Ozu_RFaFNGz|>UiC%?m&T`rc_s+i7#MHKT5yzqg6{D2P*~1Mx?fDQWo%&G8j=ol5iB8^$k(l@"
    "gLc1vdRjxkRSAkN`w-N7ljrv^ZVL%BZbkDOu0=X1FL<WR<5QU|C!``K7qAJVl)PrDPq=j=uc~n6N%eU|d`Jf%Qn1#KI*Wk^=GDM1"
    "4Qz!&ig7&>Z`u7To+lu!(Zu+Jaks*XLp1{j6paXt3o$t8`SEAEVyNo()GEILRs^!edP^n-mim5mB1|f0meMKRVl^+5<s4m~#i_15"
    "v!m{X<|*Z)tV1=SD?70z{-q{rQdt>AK2UWGaf!=3j!LbJ5r>o<KE%_HbZf5*vaW~9mzln1e^7Pot+nfVR{xgEY<CKuo~mOAzg%1?"
    "yXb`!H}YR>c$dd=Bu^i`Ay2xil~s@;-eXyh2_BzD=$$Uh<;rEGk1nNt&t<!eS1^I({$5IGEO9_y1w93%sFf|wt=_ydgj2Bb_y7D~"
    "k|bdK*LgJkC=`NoSsjWGq6Ws*H69s*1)HQr?Uyl2it5C5P}P-6$X&4@XUKH_udt8U3x6g;6p9A0C)bB>X>7}5KrepSM`9+Pcc(SN"
    "8+F?UdKP7X@aRZzT5+nk%(Kr=d~Ww|?QsXti$0l?zRAe?BUEH-@A^;NquGf@im<xo>R(k`lmgn`6yWVqV}l$<UTPbDP4{V%l!^$j"
    "SG-<m^<3j!lCx;#uAXDU$B}7vjZmxhHS8+%#bujT_k5{Ot}C=0c%VTHWu9dpS4)Yu)A8F0uS9!nsg}Z^$ohfo;p6*cN|59+9*k^)"
    "2aVar5KZU^DE+E}z*Tf3;H|APea!pxPXx?${5dKFIT~QgM+<GehZsT!n~{Gg?%0Hbmz(Dq&G*UMqc*mx2B)1_*Y>VucTz<xzN<Fx"
    "B)zQL+;7^Fhfa79^GcdUs={MmkvLVvPI3|W*Z93*^8bj6K72kQzu|e-2(#*#Rzh_ucRc*t(<!!Zbohbl5vH?uLYVi<EoR`{j4M29"
    "F&k6erqWF(x>FFPcGabIQ9Z127Gv-ED|#mjb~ZR(<NZYNM#T|oZ(%w2QO0z?)!9}3%~kK4^V*v53DBNo%LL!=6~Bf*wT@l_d9&K4"
    "vqmKfNh=beC-`WUr)W0whB<tDTvG+43~j_a^#nALF(=|V_o?BZ7fC@C-X8#z40ZuPHP52ihyQ)wiUY?DzchuYTh);9sO<<+jvKXn"
    "Yd9JyL_TLO{M;WpURZn5^$%FkFLs7@jS8kBOxFZ=aZqSrIzzVwwFTO?_v=9I_CviL(c0=P<NpxtCjD5&vDU*+Iq1~$L#hMST6*_a"
    "B3OS7q%t&hLog|akUFEFMzllA4<+=DJ=zF;7!HGAcld)f@NY-Ejym!BKeUS&4QoQHihW(fw&;A$4Msz^O}iK{ZT~v7JL+d!GH|sX"
    "VJgaG``(aprzlblc^5plhv6vL2x|}wEo(Pu>8upvW4F}W&ZJI#En;zzZve`(Tr9<G1zHI!Z*&dap~(FbMNP%iKao(qzCIO`0R8z5"
    "sAvM#qqvNc`F6@@?RdUs<*Q#cT}zdj9ji))>@dEE=UKdaU+T5i>t|$}H87!L{X@2-rr9(%nmFq|>pVOlut!5HR3-@?|JAO6G&^{o"
    "PizFGdlidQeeBB~w8Gc_z_smK&e}q*Qv+qHkbcaWcrj)v)Y)zzaA$88*D@zWZ|~m7WB+6B9L)aV$Yq@{+9+dX7KVT8>e=^)l+caM"
    "MGNm_xZm5Y`|XF?4u_O8NkDD;AceX2>DIkpt!_&}eTW6hi$rARKyM>W!`wnl3qkyk+m#*rNTr(CS2BeEwgCe}U+you0-&9Qbo&}T"
    "7+%jaI`9>@DXp7L`QBi!iZ!=%lZABepbeDW8Lf6;yrv?Y2@G1;c6j;mWE6a_Bx0NJ+5=g`92(A|G8$Hl9eX>JkneD;Aa=j8CvG#y"
    "bK<4g{so32${bVgQ>?X~{0(41BU|sukj@p2yQl5<y;|6*8nm(Ey)R@qIysblken&cKI8ERqWc!t37|&row;hxp@+sR_27sCn(~<3"
    "pW@kY3lp}%UjBI};cU$g{(0xH8y6C{;6RVB#+m^ks2mR>&&J;yXq=gN*l)y(+juq;w2fC!v$#m^)8UScWq0)LSG|gh&pMjqcXHoz"
    "bXo&Hf(gjWynhl6k8dZt^}NQ#m9_EcMW)>9m4<-_mVqY2Lu=?-+7{k?LSp};#g|Yv))+;S&N_7sR9mQm0xKIf*zTdOY;4hQFLvFK"
    "bI}RpTHesEsTy1Kt!Wy*4c3~kX&S!Ys|Qz<BHD+V5VxEl90u~}f^W5j6c<zr4C7i}@}5ROzn?pAE9H$I(XhHAt`7ez-*0ZABC{n!"
    "s_rB7)9}{Qj{A#-(Cl1VJVI|=H8yut1=6_N?_ept3^wgZ@`L~$RIv93T967BgWYG?D+4cz-e2MM{Q`Y{DTfr^UD2)j)Bco=TWl5s"
    "FXb3nbSy|`80jmbua}fEfUivTOOA>R3*a!7mq8ze{`Bnp@@R54zWlLv>GMy5rpse-uZK4njGsDQC{GH|(do%W{YICg@$n0!n!>m|"
    "KinFJ^;_&39vjy={~!d`9Doo#w^=&dFUltj>t3Z*2vMP<pzFGBSZUz;MU>ij@#lE4Eaj!Ver^4$PEg(&FWI52C{`3Fju(c?kAhi>"
    "i~^*a*ZpD{Phr)j#$uHwcxjpyA}Iky4Sxc`E^f++0MHsRmQkrZkop`1{sFuM{et%u42>w-WrBR3yc#IB04GBit#yVgr**Y%TE9K{"
    "wx&itmFwoFZl~MxBVR!n9oWJGb+Nkp-(!-_G7-fB4CY94g!K0<bcB>ybMsPv>1Z!+SD<~wMR6289SSGNAauSoQUha}!PSCYzFE@#"
    "4R$H}5@*87OVZa7d3$3*UGgQ3@@4Fx|D!dueX2C_DZ?XYOteVP(eo4!D;DJ3_=pab^nBkOVqL0%%zksBB?&&waJP!HrPUI1s2oO1"
    "^bQbR1~%pM6wVTyK=fkDsRq4}a-8Ep?GHy54VlOAEVZ6^mC?9mNV$Rnzjc~#EiRiV-yW_Ot2u?q(p#)iP=WL&`7EQ^BwV&dmDw~r"
    "V5ldC7{R&}vL0cDJ#<67SYE`r2xvn`S1N8&Z*s&j7F9bB^eTJwMfk(M1tGOm>5h4QU2og<U7&rGw=zO29fni&Nhj7$W$;$Hh=<CL"
    "T_+lkiwRUteX^@A-?tWRSr(PZ=v%Qslr&c$%9Gm)Dz60;Ql@QoK_$O#lekO8Cwjmz9n-3V(QVFFK>1y$ay-8asBYiAHi#ir?C8Uk"
    "3z+&KXhwB?qByp0_|}1P9StbSUYt${xJYDsyUU#5>ScXHhn%&&bF*W8>ov3Tt!l)MEolXzvwqJ~y~x`*oj#zlGA>1?v^m)7BBzUv"
    "4A(R}IiO`yC6rz&#k#SzVTAhdD~v;nj9J<7N{HR`h(f7MQ59^+KJh<eDA$rNu_Q`dQ`D0Z&y@@Nbv%7Yvw3#UVm2wj?27XwnjbcL"
    "mC4xeqva9lufhRb4hYioZM3{t@>Yb+qv|=p<0F--f8Vo4V2=8nmTb0~mKO;f%<3OoT%Za=p$M5WjH+tjbatQ(V~1Wysd?MI=&c-J"
    "yPj7Qsv@<T2(KdkIj)lFcZUZUhgIT!Zh>sQxXyHExdYo2O2hFdcp&A8WXJ`EY|7O7i|8-n1~R6$H66hW_HDmaBme_0M3=nkh$z=$"
    "Mq3kER>e||Rym+f?W~c{F^Q<X9H%omq`Pm9_N}0T=Q=3`7kGodv*>kbJR~2{)HYysF`1q>^n}XJ-CdQkE`pi^A9T*p=K*8VVp?8G"
    "D(_OX@FKnhl7B5XSnnKtr(=#z&m3*X`$BAedwg5=zU6F(Z_BmXumnAzn1S1iZ)e}J`tZF>K4p9?3OkWxJtj|ej2S##&a<)~>o^m$"
    "59@SKxi!{FEovg&?VD*B2D@S1rG#eQc35}ZQRlz}XW;hX7zP-1;rQ)51EFpdF>sB$J3{pLlRtq)4ipaN;4Mtq@XbCfyGYw&@w%{V"
    "?Sf^;@1I!c?~GE|#o=}+wf)|;q@rG(7)A05`?*BUuACSp!sP3jx63tX1ZcfpG&;MW(GGg|pzT<@q7iMhEh*FT`*^KsdZRuxTKiTf"
    "VP5B$%P^jEGEd`CT<mpXuL81xy?sL8PFvmcduhSj5qloS0g6P=8?k3vL7T~#y$E%?>5_(Y%r1l;#W5&E@ke7k!P9{0$3A@OV0TcX"
    "IobuEm^*xjY5DHXD2B~rZ-?U0wR$;>(<7dEfKCcMNp3{|wsC|hC!##LyThCpDcBfOaS+puUj=g~z3znI(6)OgWxLMTpmVh4ey8H1"
    "-6NZx(~nNu?n39t+@C2l8cRBI%%l1IX+0iCJ#@Mo({${hU-<ap&RFz7K5V(~O>dVCGU_E$uZNMozuG^10Ik({8>jK7NFo?)9C54K"
    "jaul=>LpP!c(&&OrnAEoEqh0z^<gu~gT&3~4!Vp4yBFVKw?;){+MV+MYPCcw$T-YaIp*@pNt2@L1>GE@ZxQr)b?{+-H@W8a?^WCS"
    "3WVERDp%&HpXr)>tk8vBu$tU1?5d;}#_=+l8gEwl6RB4~<&z>u^HgFSnoRO2U5i~Yi7pbicN24dKNrSw>~yHn(_8(tiuILS^eq+{"
    "FTjptZblFJbV)x)?l?#r^_^#1WNuPN+F_D@`rCK#%!R!B4sJX<>_2$+9NYWyr9ZPEqXEzLWHpzs%PP}Ka6=`U=-g=Agfo1qbtSVf"
    "5?py!6bet4JR`0*Rp(T;6EcHYW_cOU7*ADyF1r8prsr%wRJk8js@F4&OO(JkBYvAKC^8*%=2+&>$JeNR*_)tg19KVA6Fy6or|k6("
    "j^f+$D$YM8Q!aYqaz>V!JP5B1!|6M&v%`5-#Jp%|o?Ao9*6{EHp2T6&&YDlq>y?V37Uzw8owh6~b$40iT)7ej7Aatq@=)R>*gU##"
    "crjSiYcii1BH_PQAEAn6-E&0RHR-iw4(wn=X9jP`wTXOks2DZ%PhI1$@obi3_LeI9ev%feoE#bNBfRAp2m-Q3rXZvXU`h$<Il^rU"
    "+U)ZMms#td@<8BaG$rikjCYh8wVAn}AXAxlI=i>rfM!$mj+^@wYahU#t`Y}wra|Pd%RIs4NLBt?>AqHV;ce)mz`UWe4W0OUC-1Jt"
    "{JqH1&~6^+&5y4xE{wfn9yu1J!&J@`-0v@YMhyv3PsT%X|FExOHz`f)-v0<*yp$gF2n6&`DV>B%ebvcG(N>u~Vl^{SOQM^^e2v7+"
    "flNsyJKvWNs_re5eBK1#q~piStbD*^f7FG`@TeZ#CVX@nqvIC6r;y5Ax0h1fW*>G72+tnrK11E>MDk0GO?PLnwEUE?G_*GY+G+yw"
    "E_j00q+E(z`NR$*%E9keySB2VyLuZcPptbqdu%Q{=otkvvw;z<%Iu|b3GRVR`U`8FGbw+By?|w%FoR-wkC$LF@oy(B3Wv$_B{E!0"
    "V)sPpJw&FRBGP|F#k(S^m^8e7-Mlo^vz{>X<rM|e)I~5pcXhGWl+Ui{PCxHIjb{mF8>d3TC;&KDdGuLuesxK7DuVT~6f&7FpddrD"
    "?+c_~Z9*N{Gf<+E-hnN%R8$}Sfz&wyLmu(BolIZ1u64CG;^np6k1Q=kyG@w@P~pLSK&knFd|<MtSsq_5X2tbGl*%-mTpO{Cm)B2H"
    "uB{bywTv}|o>{E@;;l%fHm+sqkqHSgy}&}Pfn+6Z=7Iks`9zaF;D0H99qnY?z>WP%I}?Q)yNh%ui`FjCuCXowQI=1~uYGD(J-f7~"
    "5NXL?D(%ZAZSPlAmg?`jdXR~}PrweDKfTB5ALKiQ6ahL;v8_f`n>*MO=Xb|l6C=Iev`E7)tJ_~f_#}Ok<x`<g=UK+)Pn29Y+Hrbm"
    "{#uzQhqar}nj^)VR||BoL<iOaO)$rx>ORJ6;D=O?)Y!*royOrj0(D5s{-Bisy?#A8Ve5<va*7*ZC#*XnsM?@c|Lwv68mo$cY6V5l"
    "&zl{&fo=74#2&m<KULHft;(np(B0s^79~}6Xgw>a55kF0uF5=)%m4TPF|d*~{G;;y8b?@dD#L=AKV&(m0rBVk_g7t0f-iq)4d+_^"
    "Zo~E0`PD}{K5dR<`ewlO&-I&eu-jD7_O!X5RWdjZMMYlEnXiA4)$Og2g?CIA?6L41<c%{5eK4KS9)OSMF{y4MhMnv_?ePx^%=+^S"
    "t#Z0KkR|C+8&LR=J+glh-SEfReI6|zo?e61b1w+}&sah2UOMmbc*fof43C;3J+srQoT*GY^d5vYJf<ZfMQ9j;YDBNbMH1nL5UW8i"
    "O+V1zDZ=2Fp2dFWCxGVE7{iBvaeifS?7(R<n}MQp9APlyfR3s}hj&$5)8%K!s~l6!H9;_KyZ#z>0sbxCTGd;2#2WBno<800ptD)F"
    "kni}5!zhhrQT6P@pdyUdPb$)*6}YCyeP}Vt*V5~~ma<cDUM*pYtTWi3EpyjG!!qDo{;mgpi=$0)h3X%3UB!2my+aPLCLCUjMv}3A"
    "v_^IUekMy_ugSAfO9%Q(>rhwW{i+c4x`~k~RRiE_W?{)rdZNj;D}XMuQ^?;NvQ%)*at=~kGx+A3@+yBvoz!F=4>^vxVH^+uK%QBK"
    "juQ7qBZG|^OlG)|zuTE^h<C72vu3!jStit?ICB9xXEj}~kR@n232Mxj1&2uMRB7&XE+S8^DHC%-S(6xW-RH~1oFQl}*yg??Jj{>h"
    "@h8^Jc)x>X9u9ph76+tY?Ag}P#UHpn#vX=AzmN?74d~OUs2D=38xw?O`zZPTyDh!=r&x+m`6kj3o--V&Asl;XX+yZ$5bxq>UOupq"
    "g<YGjzp-n77*@SG9`+^%3Wv7p8SsuC|G9DaG{rEvIWKzXhMNZPO$~P2;r<2eKF&nNaZoymgb$_2z0=;<x6Qy)-&Uy41b(?1^a~6>"
    "U?rrEelwt0yY<72hF&#HP@95-ubN0gvoS5`Je!7~3$4B(xFgR)Y{M8hpd)|afFmR?nZzxHeflI60?Xgrt1Z@(dUds40q{_Di^0}Y"
    "L%KH##Mu5?{9`BHNCVn6wH_~l5{+XrV}u$KIGfNMxEk@<zDC#Y>AoV7OJ@0-sm|wpD0hsfEtw!XN&za4l)BhTJ+7`wN=&>ZmBq>A"
    "!pO5J4juy~Y$>%!j+j)3S5z}&hR3~kbZY)#^LwE{p?-=Ldc}>7%DpbE_#&Ef%0gib!*bXnZjx0NHAJj*>5jHF-guSVr=-1;p7cT2"
    "fV)ukR=)f?X1qo(hIaoW6f9T+it<_;w@Fm!(O_w$JnYd5qFb-(pbdx6^l}CdD~o9wI`L(%an7b051nGDluk0^TCgPH{*xk~%G#0!"
    "6rI9qQQJaYO-ch*a}^b&;faghMzy#aQI0^wz0^H>Yv*OhZ^U(3>t^t-amD9a9Co2TJgf>U=ogKfd&0}Y>cpS}0zaUe#^!g9?bW_("
    "0$>GR1Av~6KsE8W5(QlltN0Pb6CFCl#h6ZrICVU_LCDjJMA-K5gvP0UAIX|e@qU5)o?_rwPZ8BlFoVE}Dhtx^P;O<Ce~1nA2F#<R"
    "h&i09Fl_I3*>oKqPz07`iE6l-kFkiNn}U#zIkPO5L<BO!gX%fjjM&7sWknr1<OAw*D#p`tWf>t+YizpW;?D^R&t<9nYF#d#GFz#Q"
    "fP`CC6|frtUb?e%vRFpb@+isUsrnWV=8F9pDr8La)dA9GUuwm0C)Bg>LH{fusW~g40^1j5R(W5SGHL_{e{~v7xvJVGs%g+jlZuK3"
    "vYIJh?tL{8Rc_Z!B2uf#<U_T6pD67-g;xqUXajRXM002xAbsIU1tw!a+JIFWP<jbU5l(fFQIlcM>Y+MTgDKr}KKwL(BoZtBU|g;W"
    "^b9u8?l6Auz8D%5aHDc~6~-ODCJ%=B6Bcv?-uQ%>SR%ZFiMX;ewI^3D1CfsRqXMTYvbNZr@RZkhC*dW<$9+r#FJ)_k^tN&<?;^kp"
    "QM7b78mxTLzX1*YF<M3`RynUd6^D5D?9bg~Y_I-!@naA1>E7o};`=d9v9dw_WPoU#VI^zyq@h&<r~u(u<0HeGUs$B5<TUEE`T`CN"
    "Kpz?e@$U-b`ut+@Cng!o9y%{*0YK}*7}o^v$gNQrfc+ZbNetc<14$`w^qKTV_b|IIfP-%(^-`bz6M7W&m$D^5j+;bydcoHV43eE^"
    "h+j;j@+MEH2jrOXGAS_mG+-Z96)dyx7{?zwXmYYx#IuCbiNM#Q8f2R`mA8FAZQk8=66X&7_+8|AChDT@LY}%4zamez+rI&SlnhbO"
    "=T3Z4_u_ByMRKu!BjhT%*<<lJtd>r)kZZ$5RM5Ae<WT5=4^;3e9vBqKjQmLQ#ahiSs+|~dQXCY#KxUG=mMmX?S5TRERO_d)tbr*G"
    "xQs`v$SCT(SH;Pmq*s9bg6r`Cg^CVm8OUfXT(`RAv|1%`@10p<6_W5ZEOA}T!nfjtdZ5EM;Dim?dnXTM>XbLlpO$6TOJZ8^KvRFC"
    "5Cn{?r~D4zMKD}syaRri6iSZHpIR~$t<!;Vlsy{1cfi&kG{mR}W;OGjpMH{q5PQX+SpE(NyN%M1K*QAxnVxwrT;K#RsUyzB0Yp0k"
    "CU?IQBuKeVFfjm<5wPkb^ooqrd!V*dBwj~(-6pUrOcT&UT`E#zSL*5s<@k0)RV|?+stf2Cs~&AnQN~^wPaj?t@gfm?{p?c$yq+z<"
    "$^JY^Q3z2^lpbQLMNTw`34O5RLU5VY(oo?TIUpt~V&+xA6!r@)OER7Svzmc|5887?WiQ`eT<^P7oE!{EQC?NBE6e~fFo1Uy_*8N<"
    "m>u*2)DwTk-vt)#<Vm3*ERE-0IC_n2Q_r!d%nT~p$)Xv|WOB|&@ktg%ls;7_Bb+n}_Q6?H%%Z=tFm{F(P<~B5Td*&_Ql{#0EnVct"
    "N5(2SNuB<>BVWFi_|z9&kslsAzZy?==4gq2+|jAvNv_tAw0-ngMVfRnHx;a66rk}ek#GR5$uiHT>|jYDEqj*v0#n1qK!zYa9rp!t"
    "Ac`s&08^u1$L|M*>(ig#CvgeLf7vov0cH_>z^1EI`pi+qLy0hPJT!eDGXqINb;P<NJg%s*qCaErxj*!;jX1~c^s;TM2sIKD{^4!N"
    "r{q4FV^wD^VVkGLE(}qRKG|8z+bVSE8xp9Zf?vQNH_>O0>bHh4N1cQ@rix~`+I8m9Ac-Z=$$lM=1EWdQks+drIGiX;yQrI$YV4ml"
    "8_HYC4~8-U3oS28CUs*^9OQriwruak%a-6D4LzHUngopR4*p5$ftcz+7YG%{{0o2$--A(P`7f}L^E3lZ(J^0(8Y!$F%yy<v5oxun"
    "z+NAU^{wQ#P6WRqT{ie83VBgL7n4x-6Q~N|>LE}`h$w-h`A6bJ9AY()!WY#rCY|U$kC}3EjB1Fx=#WYYAz=}L3342nG)jxq959~;"
    "l6-#e4)JUTGhW6t=y(zREyLp1Gm+&f;!5%}yv1Q{gGxI;?N1+~MB48-9*_zqikiikXP&A`0luhD#+S6%b|gjbYjwws(QDt38db>K"
    "ugWElBpv|pVrx^l77W&L&RmZ=i|)XhTabAv4nzcJoMG5QA?`VT$JxK|GDmr+FSExOk8(1i1d$tTyv!4{UTm+6ZqeRdrSs_VZZ+3T"
    "Yd$NIs;F2uuu+ml3<J+Wkj**W?9kXd{tQb;>3MNvT(7$)<ko5Y8BEeuI()gCEvyH3?MiW97r*zd$WUMBUCHn;U(H}SlX>U$#u}oW"
    "(e-xB8hx>~dRYshYtW?Nej+As9)Uc50D7EeoM(>mCE|fYEmki96KH`q!x$t&IVo4uIXWHz9w`weRkr6E>?7ob;&X9J!Y3G(jVbK#"
    "GDLO>U7!o@L$V}V1<Rc>-~kLn<2Acl6XpbKwamZ&=YLras2kESnLqu(&<|E+x@J%*F_r_hJYiCkWnRGUsO<2VuK4$v-!i8i?o7=p"
    "9CBw>^Xmd8zm@K(lZYbcw{f=2@cy6NPQHBj^5xm!nTWR-E@saTp8bpQPGupy;1>tV%`N>Y{g;0+j?4q&2Xc=wfR1x~dVG3(`F3*l"
    "7FJ&Qej2o0I9KU&%k>6$JI)s>KsAveoapwRhbF#yIWVGj5Q&U$K?{SM$-_mAP}+M=y}s-k7Dx{(|E)?6*kU<~WW;3*sTZs$h#Kw+"
    "9mR=|pM#+P&Ol=e2sBDR^2bSGJhuZJ%GjIAny=3-o2MlG{hwQ&m`ITsNeiImd{xll68A|tOo8P-w*u-1bkD2zq|-cis2>K=czybV"
    ";YfEt@{=&0yMzkdn|#I!JLnc;3ht8o73i!(;aI6Jfb9mVQw+1g8HHFwgrHSE7(7*r-VAYN-{Au*6a$i91hxUqUEG6>O#Dg|ERA!#"
    "%TG87Db<`DvMZcu5Rpz)((wwX*CfmV1b4t|5~(WPC3KLo<UDXgNq5!($bmaL$hnX4;pyba7#|+KKYf2PzMh<)4JD;wS57bx27qK="
    "nK6Ax<}=_sBJD0L!afJq0GO0XRXBFc1ihqulQ&)!Ws-uC^CuuV8?#Lt5#Q^+#Q7B>9#XG+iL?tZypWRkP6@HL$p_>{^oS-C9Tj4x"
    "UND7G)ROGS??x6)`C7hvz+>%XVcf2s_$KkW=kbD&&jtYa$0%Ll%3uj}W3Px=c>rZ2WzTG|t>V0VsW53D7?lqlrdgX~)#fL{>G{#|"
    "<@oxT&Ph4FEZ)lS(o<f1nKD!&QQuZiF{6?S+Tw<;k~GQ<Piqkw<W^ujXR3T+$x;tp9EfecmNAIKSyhM`eiZe>$^`=iID7=CVm#&r"
    "il`FK&XOX!r66v#=m3F=9#vms1Yyj3=KvuaFXGP_+6a`f!ql$$3;~rDev5KNO8h*FQn8bv3IEJkXu{6s!{~mlC($Ta3r9(E4JSHC"
    "p?t`De?0r{C3b>jOEE``ly=2lJga0<;{E&F19FK7`yzx-QHXP3yp5KI5;pMoYV!7M@@8^4KD##FjxVkl_~q($o)oBIR20R|lSVPk"
    "n1F0wmS?w+;YintoCOgwMbHPxDF=Q%#?eRQS%C6rHZxYs0a;VGPa^Vmo;@0SCUyo&@iGJDs!#%eqWi?Smc?!0a|%Jn1$OBXfgpo}"
    "#UsTSjga9Sh?}V#2nBj3GQf1ezz$u9St%n9Juye*`6P=>!@u*D(!T|X*J+!D1fC3YT?-6RrUNyY9DYRQ<PmkM+6z}>j|{q^MZ@6^"
    "^!<|7Yv1_Sf32eA4*vCDnGw-`D1ikT7~WlQB4WU^+#WR&DUbuvDn-n^LJ!&JXTh<A_ljaySb!Q^jx46N=Z-yaoe=_t@9C;T)Jp@w"
    "vI2U&&p^yBqeK>QPnmpR;@FSIIZ5CQtRNV8p-;3Tis#NaqoUaH^Ng+ulT!3wV!WpyYgl31u`uqFWD?B*CY}kG;pqxVT8f)21<r#G"
    ">Uba-tMuYD2wq?peCo=l{m;YEz;{QIVW~N$F|H6SsboHj70Nf(JmqGCPc27~4e|<a=)W)`&bwe>`h=k|ruBNjoZd<#^Zag6iyC;K"
    "8@L`wHh_oa3OqCe`0vQW2{EaQorw!I%VN$C&O{m4GHvIAB@CH{4(0wr62kGT4F_HCKMx0v<14b?cZa@1h@k*Nfj8KS6kiB}60{WG"
    "cY)GL(eL7|(8zHIc3{86O^S#!WCR~7e7;bpXj{tIU3g(x7!>(Z5FWKcFc52KE6OE63wyy-8_`j9rO3$q@HFic$sTapz<JTL0@<-r"
    "{T%*iuTtJfmwWEWkr#R)nS@eH6ScG$I$&q4R3K0vQ0B=AqvkgnIHr#@EhvvE#~Iqfi;NeRGW##cXu--*asG*Q4b&fGa697P2XZk<"
    "$Mn2G==jWZ9%9~N{Fa!4q;8R!0f3ybYEsiHD9eGdN87-%9E>Mm<6JC_5OaVQJT3bavBTs`rRNalgr>w0Kpz4?RDylSM=4M$EfJ4U"
    "22xule3%jsymBI-1xCT8L&2`mmcHJy$Eb$8=OdF}69lN%u|f}X2yCJ8B6^U0YU&WEJgdcR4u%78<3#EXOFAj&8A+zRz%{mL5R>$4"
    "oCHRoBKV>_HPU*bY3Jxf=ncd6P8%9WwS9rR*&jMiO%%yp#}wPzfAqAzy%xwvS4$9_Lno;9bsNuxbaH@ivB|H}DllcTWf2KUK^hV&"
    "M!3(3C{R5i$8?shnu-LwS}YZCK=giBWP=8fY~raVFDhl$JuuJ?2TUcho|=@3M{dN$6K06v@!PkT$5&UA?~hq)pFU&-*aDdGSlSwh"
    "dQLfQ?71)H3c0s{x=%6sq15{sNNsisY&<Ga4dDx1#bl)tD)$ZB!Hm|1h4@lz_W+|(5RgO^P+?gO3u4hl40-JhG)fZyi>(D+hZroQ"
    "e`^JRQsM4rP$F)rov?9SkR3cwpX5@MVtV6B_z6>$Np)zPe-c(RtH!J;z+O6o%_<%HeAXG1r#2@lVwW=L-*QL>3Xv#~$#;#o>sS>V"
    "+AsJxwQ?x~H2AhSpC5ysf))(yvd`QFQCGAO$7-Tbyc!v{lOxAeD?CLvB1%xuq?9pqm!yIXt%?UAuR)Cm5KPE5hye*cK<5g)V^}v}"
    "<|r&^{6Xe^neg2NnpjFh#EFw)ORh<<_wX(3K~(r6mP~n0rXZ58vK3(`uI9u%#wVbvA0G|b^?x={)GL%eQE!L{9|yyO1U%d$#0hEw"
    "#-(<ccYw~C2|66^1Aid*Dy+wX?+?#UPR6g#!DKwY92ke^XKyA)$7hGfV5^`1Ah{;uKgC0l5(9?fN2-sAMOzH2%YvD(`4UFh??OAq"
    "Jy2BeQVUw!hiDl~kzX_OmI>0Y)C7*N-@ry$73A(pCq}#qWxYU?&?vbW1S^GitNFa4vg2GL<W|{7)U#0AL_HW2i_8o@LqiJ_FoTi!"
    "V1wgEnqhd9!lQp+oMvV6Ngf3Q4+i;yZ{J)VA0M5cwh%~=U0j}jKe?KmpN&rth%T%YcrAnAlR69bDVd5&6++*#0m&q#W>?$-6i!Bq"
    "P-+_jTq*Qie9kuAU<g|rH^sg10U%_<uAK?zynF%hm2%qGjbn&Ha_4t+W+bx&wT>}xE5k!eDnBoWuruWW4<)X_{c*c`YMqGeJ@-I)"
    "6aq&MpiUmvDKCz>PueZp=^(9L&%xMF>?jbvV^VXIUnZ;y0$Tz3q}Z}JC(7<v{*n>H-xG+e)Pq8mk(Il|Fz~#5A~T+KK@YTNPq9XE"
    "(jx^oHh=*z97`FZqz;b;uJ3ZZe5Q&E;@-$s)lXKc2I92smPD{T@=^rCw8OXZpg^M%3*<s4A~*{{ECBdlgm)R}0gpw;!6zv_K{yDk"
    "K)A*G3~PvHo-LjQ#EP-!CjAkT*o1A;2!p%?(OVdJeDK7W&?r^V;MMB(FQT%NbUDE{XUJJ+F-Jw$RlJH<^>QiM`FUsGNa5#}p`Dt5"
    "o}!^wX_i3M(k9nz@X*sFJehJp>}YNi6|b|mg_$k1@ye8LncBRNx&caN#1I`J4m0Q!u>!2$85l>Fkd)_keMW~e8(JwTTWx5;YjF<?"
    "D+Q-YAJ8c`Z`dA7XV7h-=r)e(wXV^$ZI*$&2VG-%)Q@A)%ecerFe2$8v#4VTmgUHi7;@?uI;oo_YTXG5!p=a%h+{@&vyg=^4=fpy"
    "in(-JF1pFV8g6x9uTDCo@lab}3A$^@<KF{d@eLIRfoz(e(y-w}8)?{p&NQ7z$pYPZ=5+5u2Ngnlgo*Jng}R_%N)^`*)yYSj3f-xM"
    ")YBmq*JIUr1%i6^l?NCD<Rq!sX7!`K`;3T8o$~Zx(Kk*fXXlp(boEhXH$zKE;;?>rEQ<RGNm3a~a<iiVqCHKBBw7ShgJ_xElri1{"
    "<uFBB@QDKA19^K7jDdvleYzs26v=_IY$2$T%9`Q229nf}h{P#=#haenE`dBx7D-8p+w*`PEX3*WG7|?XdwiZHj>Cv-#j&$Ew|+@F"
    "923p7N_DrQu)XIz4BnBb^n1phOgP2%B5t51$0Iy9c?+P{NBhc^#24Y;ZUr&k6w-yBi=^9$tx#g?yr!qq5uprU)e_SX0y{3wVl2E^"
    "7@<An6UEv&U&Vps1t7E_BLNhIg3*sAW|da~k&9g@cQ^85sZYV3;<mX}x)@SMRtczU%h-E2dHe1qT0Owq<+7ezEF8LZCA=|;QGqA&"
    "Z0ihC9*_-IJGL$LJ1yczQVvKHi(H|EXwsAmP94U4tWp^Z-WEvqc*BpfSv%5}S8o)MN9S=-A!0`8LMIauR+>Z<Sh0=0)8nJb`%}h?"
    "RpG@0^a{<YBwncIj^cIwQM591sjBDy$KIPLw~b_pqQ8RhxTfW43dRmlb>l|R5^bwX+emWN)a`PpArg|%ra(49T2^=X#{9#5-|;@;"
    "ead{vJ4<FF6AKqxcGr9NMlTkDL@p;!o-NN}(57@Ur|3eHM%mUYM0BR5b%4sb`sQ4Hf-_L^YRde?GiPq5M`avC_nUlqU$)J#kVKYs"
    "B{q#BbC>f7%z0F}ghm+r2+<HYgU~Of!KGZH$7TxTjwNpmqQEKhzoWK|<c)2t1?9AD$bosOmszBy=*xMHIYCM4#ra-8DwzUs40nWa"
    "5_k{^52>=->d4-!VLR62X3d9_2*~A!)(+@vy!NO9zQ@1^m5I|8lFLd;uG?f8yTQOWy82G_O9(br@XA3sCl!|Mrxfv2Aq<IEOo&#V"
    "NxE7fMj~#mv0FSpe8f<N#gl}y133L@IU&d<L^uBOm%qp;e-Q*<pbv<2`hZ_9D7Lk`czEjVDJBiS{5`9Fg9uN9bWgLk;DhV>gHip#"
    "o-}a4j}Syq%>n^WK*<)`^lt_0n|ruLrn0GH&u@hk+o_=`v(po=@x*UD3ADBDTAF-9KZQs@f5+P2iTryZ2s2Fqs4@~|`qQ)cRM8J#"
    "{}JdvLbMjpR{d5y``p8f=YUFg>Fy+Z$jfJY|EOZLcJJtV*8XcbEuQT?!-NMTkZ98@k>e9H#-SsUOxa%lkVCrwiXvOWWO+;N%pn^&"
    ">M=<G8I7+hhd=QJdj(HLqItcVBqbydVk7_f6+fk#H_VGga!~X*K07-7btnSC^YX*htfiJ9IrG(~GQ>-w+C0!%M4N`2w0$`En6CLO"
    ";(UJ6W$QRk?{n$1CH%Esb2`Sq=d-KPbj;6u-xXmuARt}ABH$EXl_J|V0uPSf(U3cO1SkT0Mp^|ux&-GPQdjg>@*ySAMrS!5%3;4}"
    "M^u^=<pB8Zn|B-JjU^{7M0aWi)O}W#yhMP4xO7M3vxgjh1eEA;x)d({LdO*HESfaM&APbg2O9Q>@uLdWSm{CPhxgs=^)i}bAk|0u"
    "6w}c?a?}98J0q!sdLV_*whpGn9~MN}C!C1kuXrD8Oy)-ra4GYjreD+LM_!;OEmjg2HqTOojV?Hca&4v{+f&$>@GYF>vhE)uJpU5N"
    "UfsJZ&dS>-b|ntU{|`MHuF#lLT;;`8I-9XepZ5~cflyHE74LwIPF%|L*x8Ho(rf8O^PVs|qY8;#eYws{3@EMlrLI%i2UGbs-^d(w"
    "o6Xb>TYEoLVhi>@Qx||HAl+3R2Mhu_lpy-x3(QK3JNBNdS6*SPvfRRjs(?X>^ev$cqsin}B>zn-k5IfhMKcHtiprB_u`8@Ik;$FR"
    "B;~Z~2UWyd@<|}4+mgAw?43P5xHL#M&aqCf%HwjCip-09#d0!{Ah=?8jq0G|GqPRaqkyV1+yHFSs}W_Urqs9u>1wg(94#S2Xpr1l"
    "wGyD_!e5cU31*BUG2HJ{Fa^d`n0H-LHy{Udqet=sA`e;VFp-ezL8c$Hyyrz$2gsfDf31TfOnfe|upS=%Ht@J*=`~defn;#`?Ia&("
    "b)Xz0y<urvq@2P#Dgsc#(IyE9f}+nI>H?p<Frg&m;N2S#+3GL?<=mAp(uTR7PCsl6D>rt(7FL|G_Wl~SXk4A1_p;KoR%oQWP}!9z"
    "ZIGNq#5tag8pA&i_F0yss>LFOEbwtM!=Po@dd}V-%2r$%fo<uuuQ0-C83AR-;hSM?0QO`9O<$Hlq5beG_tBl_q0(CU-X0r}b%xr!"
    "Xdk^X{Mozn{kMY)!Nr%?>c#nRaC9}ixCHs}%4k$g@=Wlo%HGO^1!wX+bkzJj$9HT=@9sdTdm}ak!9UhK#$ybpb=*tG*`xnr;>-WR"
    "sZBaJMXOqkI<MLY5%4v?*Id#AN_Wv5fB>aWB%w4OYbT=botno!D90I)R4JC#=HPqni>%MVcQyltu{UZGXXch{zPt6=I-AY53$pdu"
    "o)0e%&p~YimBkFa5pwt+N=whSUmqs)IYegNFs}wDKb^ljyWIcv>VFK+PdP7Xy|bu~Su?iji~<(8AhQtZ|ADbJXtZsVo8KoL;t$fO"
    "TV?dqf*~#jM}zZUuLdUvSHBG23@_*{Uu&TXB<Tflat`yU^p*EA<f7!NIuXZ?@UI}K<qEGk9^wf#RG(@}r~8M18W+R;cjt$fznU|O"
    "!+sLlRHJZ{IR(a?VuuJoRwd0h;5C$Gb4qhUM~6RynsGJ!kF(*)MIA)0lQ4+HjVNXwr|jN(&xX+R_Oz0S%z@sX9uKb$PcGh_4^H;s"
    "Q~;WyYHN%qs*_Zs`Ej^nF!N5e7T0xtdNw@2{PpT`@E`SM_3Mj@Lk3<|Yo&&4()(P`s4W^_sUcOXRBMH*-2zmgg;HT*LW5UAue(--"
    "G<<=KJjpA)4#gEQAdz~#?Y-2e^#;<0eI<(g>~&*$4VO*l`u3%^HQIEg;RY*pSF};9tu^}M74L)QI342w9>`cEU@k8@Hd!@(_vU!8"
    ")xu>Rn^g-BH&}Q0&6Z6zlBZv|=lre~-kxx~vEWyA-`?%d^SVU`o1l5{<!FvHZ3=3`{E9DP>vT=0rgidpc#OOgskR}Os@iIsK>BPt"
    "N6VwNpFU<qQ5#}^aBlRRtnT<dDJJZUn>YCz-M7Axd2*|D49_pnt?Fw3e0Xqpc?E+W)ON~|0lc7CUCl+gn~FVLiEDx_5NzeLPcPpN"
    "&%ebK-cu)v_nP354co(_I#~A6DM$vF!}H^-1FqH3DV2<>;*xHSzKbg-MC7C{I;dIEgiQDDTGAh!#nIvG;l}gu9H(m{UQnONyQaH$"
    "$3)&8zd9ct9Stf`<|$?br;7IPR@2;8YhJC&T3y$^nR9Rv+ocC5C+`MFnkaNdzG9mUr$i^!@$~)*A6CNgVp=@_`MAz(gw|GB;nfO;"
    "2k+XJ;Cd_!lE7OV3xwY4iSMjgP;=}`z!ih6S&#2@tw(90U$~m2u^Ml~)yR>nwfJ%3+LVdAww$EC9Iw8dHhp%nR+(+uK5EPJn@D(i"
    "GQ7Gx6ih{Uwp~dJ2Wx!95U$dN{y2=hI1Fs6GOuro)(Luaij3ZJUZ77vD?9Ys=&S9-tt8g#_e0xLMd*l^e_pdGHTco}vg*;;BtV4F"
    "v6G~+O9ZPL(yiK~8iA_R+QjwkI9}g>yr%ya?Me-T+hK>n*AHSivDUP-zzKMd)&uH28xB5Xk5~5@$WS9;kGx4oi_*x0{tvO`<vs@*"
    "@FT1S$@X`8C)hLRi-+02<fArG89I*HTM(l(RXJJ}=T(m|V;{qsaWA$xX%B!npYnAac@XzxBxbYtELFCni#KL8WK=J0bpeAlg3MoH"
    "nmeO(Hsjb~%!Bzy*Ta8U&adi5%W`|Ril)U%mD#6-+2>(#T*0Wio>?^wS$cYi%O|E{*Y*H;Uol-=PG4m(=nXoo{gP8@Gg#-M=8{+}"
    "DfWcJ@@OWs`3SH}fR}Fl#3%%DeTh)4Ts}C|*6?{+788tl$I+-Qd2C1$#8-a`O=PN}3P;k?qSz~uW~4%u8av$+ULI5OB@@n2C0_&R"
    "6hmT)V7MBZ=uHhb2l9f|E#xgYL-kV8L-%yK!0XBK&+l!GSXnzFAia1r0QN%3xc_{B8ti;qa7sSh1<%3q7VnY22RMbnNsx+tMV?l`"
    "q!uVGGjekrFqe<fAvLHGB93oW0c#W+C?jR`2-g>_dYJ|?>CQ^?VM}w@;jKby(+T?G?_{4SOu1|sk)6&sx>nD$AttOP+8}IGs}lr("
    "v}%MS*F_h^KK+CSzCP?ba(m2=yBGDjV2MKJ6WnB&<z&J!NtC5p-D^uP^mQ1!<?ifP(XxBZ(Rg>-n1IeP*yFvq9UCx;bc`Mo+4#Jo"
    "tjBrr@;Ln@YyEA=9RQ{;0m?(YcToei7*papq{_G_rP^isW#eC$qR{+G4xna!&cG2Hj^7W^<3l}u+Vev@#4aTiUof4i6z28qTFJH*"
    "@ex>9=lQEokXj|>{E@g#0BFLcLixyvHIxsX$VB;}JchLii}*7>tl#S>XgJt%5_Yh5i3)pfmAPI#<;f5Ttxd|n?I$=GhXs@SRT9*^"
    "WB4QVX)0|Imw^M|zkFu3Dc6o#X0Bkhyj7>8=3z6?a8H*BWaMI%3qbg?QgoFHtx+2*{lyz7c#%E|?^Qm1nEUESXr`!i&iKTNo_0iK"
    "&r@?C#)fY~z^k#Fh)d~{R?vgEn;L8)>3>50hauVnLCTNu;P*P43sHqO@wkSUXTWVP7Pp(L1T;9}jLtu5own2eFV-0($1=tk(nKh4"
    "tQt$=Zk^wl(iVTY<}5T>3>^kTeWAfmYTCzBE0r=Xo==hK(Y^}DetQ<#ZmXubt)Ot+SaTb|x!l@(Igx!{QVJwe#8uu1iVG3B>`-?9"
    "+Y(Shx<r-24{e4~t^ZDMIAuP-2@dCdmQwCGl?Q;;K}jCw88yU2U6}V2b4(R<1%eUyOaX@I#Y1nY-~fk%)BJ#}P+A`pFRy7Dgbp;8"
    "ZD~>>GDpsGWKriZFYJr^|0&C6^a>FGBek(e(BoVzn0@;nFuie!4*4>D5#<-aM6%`bUaTb-9;XLW7I?>)foOTXzybwG;xHnBK>9Eh"
    "3lJ)oSbT|th=fy*1et}HA}@u(o{HqKf>zfPL5<Z%zs&Qhd0L7n10-@BZl`o7zyG2qmO${g4lhpms~vpF&Oa~AP6_pJQFGCIDw7T3"
    "4ctyhMJcO3$#wT04#<vUhoS6jK<kFh_>08rzgUwTQ=)yy9(UO?1lvFv>p4mYl|~hJgU-fc)7g`eH;j`<rq+F4PDJe)+HC6=)DO`I"
    "8uRfXN|1DjE~H`%>GjMAm>07pYB7IPI8D1mh|EdNuc_u7)giO3*OUd0QIygv(Bi2P;srT-NcS~i?OIZN@Eda5(;4&0)Zmv3nZ1(b"
    "B9Z2Ap)_?FdPresbIz{B0`P*e36^*|MwGgIB$RPZJcrZdVm+MnVsWREh9CywYYakJ%ZRh$Hpe(T5&E}Rb!v`BM2_rQ@;MoxF&zdc"
    "g=xty)?rN$uoKB0L=@6>_J~RNL`_F4^!iewG>L3KN&Fb_(4?}65$Z%&`R{o=VOw4=hrvPzlgS%J*rgLDS2D%dhWZP?&$2l-7bdW;"
    "kav_)Q@Kg1QcSCjG7?j&&FYC*XW;&~^Yq>TU)Z!T1Ojg`&jI(c8dj--hFU!vtiJE^2Orbl%i_tr)O^vv3E)g$DF&NcFVaTn%U@@K"
    "Bez=OA=Qd|ltuy+KlrC_?F1@+)r%j^!(M7OI}GwCuW6Zwl^n4P5rtvOI>;AJZ}x@5FABSIm+7qGAj|uL4CcSeyhi{xDkQZtpDsyR"
    "MOz>1o?CRM-mpz@=lKinG_7D)3X7N~E933BijA-{y?4FyOGTsGJAJ<q#Zl<eGr3ChOg$O;(9wBH<Vgs5e0NjiNhI=k{|9-#5%REu"
    "D#)+DQn&0y*tFU;ajGT|)KF-MU8;<o9HA~a_zj84yyH8Z(GJ_07Vcd)?t5`)hp~xTQZ!eXAo9*sVE__~6yD8qy3SNc`6XPdmGgHR"
    "S~3$M9#AGl$%DBN#dT+@zRmaHhL<f2kh2Uig4ft#%}DAr8RC|Lla6$&B&N0(t#We>#!_BZIH#gut?L{!NuJFyvj!?KyNo8<F)Du~"
    "q^!0G#puR{H@EAn3GD@^r>u|{K3zv|y|A$tIB_}@csh7>DV1YiOm8#PbAH5G<a2YwV3Gtfv>r^vzL+GHJroCc!K^|RO-dy!nfjyE"
    "R~2kcB-k1R^&E>ipb?|`T3SA2GvVOe@^LA@5|$1voPvU-MUtkb5+=Ir>E#M|9+c<=)j-V9lu{NfGR}j#KT99^N=jpMg$!_&dfLOC"
    "zV&JOfka1{!sh8QiK(}df<UIG67^a~>;xk+6N~(blz)Je+40oObMJ<}AKF2U2Fv7CQ<;j=iz?|@2mVSr%blFbB$WpMXF&tx%n`Y2"
    "8+KTTD-v>msb?w14djHmY?7<y@}ordl#=XDxjNcnI<qY%_(UHM2}o>5=j0riZBQ_{aa$JWJ=rfC5c0+M-CE=$^7@u|T*q8Z-U_=K"
    "#jYKBU%st18>M;)NBtBD4in5=!4qk~FV$(XyMVq!P+zeOMi9o;^JQ_mZ14v%$vg-XmP()^Z=J}V#3`EaMuS*$Sx*FqNsU0VxL=O$"
    ")@D|>Dd!a@S;90WlzNFvT#-ptT4i#T4ZKuo+n)ONW5X=-v2UV75F}CT*`Z$(wdyOMWH$>lpFAckmG`gMyo-k%z@tn^y?AReV8*f-"
    "0=nFs$qz^AEX9ls-HkZ5Rb^~p)Y(K>-4c**8ky-SpPo8^JGJPt9#Ii;f(M!^vWl38&QE+l!eo_Sa^`+CD*~kON0DJ<vXXV_&aJfm"
    "o^f4i8KZZBS$I!xDoU!rBrLgKiExzUS0KRS8ak!(A(7*6N6WrL=^lhpmU6<??o7P!hx(n#x1v}-mlaV0S~U?gs??unAk!QzM*GT1"
    "Qiv;c>^#TE8}%VP<`#H!^LjFUK#k&8cBrheK!o6ZUMx#I)#T%(V%KS>L@4%CGa@s&ABjLppHg~T6u7b7@7FH3^qGB$TmWBG!We)w"
    "tAJDSgMC3i1Ss2kGGMvSUROk@7c$FiDY$|}Uc6V$#xmC_Dp=D8Omx*DDC&63dxLKZL&_4lnJH(U$loX5pmbRkP(UEt7S5c%F*4s#"
    "CCdk)5SOaDmbfCIf-flO&|4{&$~y(My4!TNC+;z3cu8JR?kgZAH=s5t@ex|}#N9cz6by}$GCo!~Gs!SN@Fb@MFw^22in{}G@&(PI"
    "G^z%G4SM~ALT!&}Ev3Gpx3bC=O+iuMjR}s1IW|=;p*EmJk$|L$OlvGXhK@t%Z=RQd3VAU-M$rld!d6!4FXCoXUS#Hr>RLDW!77))"
    "a`J-i;^yia@@ctB+vd^*V=38<Iz|GSkqfra{EB(Fp6z`H_Mz{l0snluX8*dV8)&qj6>||RTm(i5A9~DFD6-&Ss!J^2$Z-hL;b=OU"
    "avGmE{F`si_S=G>GzX{V`_I+K2WJO7ItwIv{sPK{B?C1M3*(hTRQdMc^04IvNZiLDaM#}a_UwoqmH|~l&Ct~BhMchIi~r_2Kd=z="
    "F}ur0lkDvLP=vAY@A7P(o8f$KFd3~9Cp`y*HQPsdcs#wl%O2kXstk(9pZW7@k+Q#I?&VA<qN4A%Z;v=4h7!2+j0wF)OX#I6?LpBn"
    "uGs>l&1o^NH3>gcInryuD_tC(GtOa14aJ0Di&J282Mf9KTXV^wLIET{XGU}*@S_E$+%Ibj6u`rDShY9A07d%qVU_;C_4%%VOgI8)"
    "r`MDGmP|RN2*wf96<rRcc6%&mfn$6YiSFRJI9_e5-eQe+os*TTH`}jTA<N&mhHPArLlaJJOj*O!){6nzfcH>{va;8US4IeG6U5@h"
    "Y7lB#vOE_Cc)S(R;qL}|+@fQ6wz9vXNqo@fZC5zi)#(nW)F|esH^X#ZP~6R)+tQ)*YG)z*ATNOd$pn6!{EnBagWF+zQT~x?+Er%_"
    "hkl2yJfx@ItF+9>OHcU%HzEk?X_K6`s?;qZnnuVO0n*G*)YeZkGScjYuG{F=MkO@|j)H5*3uPdu>}sQw{P635mZ3t>lnd2jimI$!"
    ";NIx?qSv{VPG!X9l%MJ5xs2*Tu$ur+Ectb7ylf+VQQVons1fhE9^$Kqes7?U;pi#cM{AzSuNBB6cK&XE8Jc^lI_}<ANdvOSV+z?A"
    "n20r5q?gmW1866XAkrHx)jqq4AcU(Nuq)?w_I_@6W!0lTR`exZ<J$rvs$dA!S$o_>MZx-#skB0*np`(vI-PXe$Obpei+V$^?^Cu("
    ")S-p%YPXl{UgR>=H*^vfsJESG=w9@hbIVmX(c;Pkq<A2{f~|hYsj(1xGJ}YhGrVY1zpC#jT$dQyaz4(Aii)?BcaknCzXmf29vSC<"
    "D1})#!T5QJbV)T5lOl(}s^zXru#f_A^@0u=aLc;|uuZdbM|<_o?9QoX*D5!Uru+4mPUDN8vd5KjdbRj*lPQ~B?bl`c+W2xP<7KVu"
    "s@HSYZII;sEHtL(kPIyGZK8GC^>uAZ#`kqygIWS=>%a}$loD>37g|GC6YDhXrLE7dMn->5{Y1!jpjz`)=17TjV$bB03ThXUjuY|_"
    "_P{>pi~V#y=IpVgJsG0jU0NQPBI3QFR;UF?jptyaWOQwcSSz6e!o9yQ#yXkK?^S*)pw;a!<i*?YZ*-Y+D8l*WTjeW!db7We`)_Jl"
    "EL7HRcNs9m*xn4zOh3++OqRL`5Os<G4;h|n5`051M%yG(w1G%4EqXp#kr!jL41qmk;z1Hbi7n?ns7oQVEtk`a1!w%;bvR9g2&^=f"
    "0P(N_5#s?HAgialnBXty+fJmtCP$o(Hn)w7_W`Jp6o;TqALAV`S^a)G%VBl--)X<pf`TBnJ%5XQlG<(rvFDn*5q0gxmboR(y$BsY"
    "f;Dft8Ll0F?Ou3s6#I72@7@Wm#j1VKroLt){C?l=`>Y!9C~(v;)3->i;cH!-Wpm88E!Sl`aU4mIoi`Cncg7MXpwR1!9A%{mpcU>J"
    "%6G*Wr;efeV0=$3UQ!C$%c(YU!_cC}eJ%Wrgr}B}64v>hRA856r@BfzV{)dFU^WuT1O2`rVMwFkGyNmS?ssV2?6m?@qfUXGvRtI8"
    "?5@#bAXA6+D<;|ay5*f=LTUL**_K?k60B<CF+DXMZVW08LMj%QKdfBRBpQnIX7D68*6wUf^z1%Fj!ZVgrtiU`>T;mCxo%e{mjlDB"
    "4uZ3X8DKccXLo0Z1>r_{AY&G&Z^6QK{wk4k`^hwi@cR8E_B@*;-_6HrnQQY(K(m{fFW9h{&`#Ct(&BU=!SJf{sVzaa@Etey?5MTP"
    "X;IxqcnKVKLEmaO7JL><B~$_sJYODSt-FIIW<fV_$=K2=54!XyAXBRZ<FBmBL{1R84pW`x7oHP3(6BzIe&B&}X*=%9W!AsaZ=lvK"
    "rv7b(5TBb9)l7ZW<x4I|O-~~xHq{tFJ+z|T(qPtM73AgVrZ=x22@9JEE!=%yIw{J_*9&=XM48-<my<<4Bch0NY4hsPuv6TlR+68Q"
    "WDrA-3t^^{0L6(%UJ}QF?IfKpBdU*vyGM6VXazdF{PpVaWS`P7nsXs1kjJ)86xVB@waTv~u;sFmSyq41_#9!^$Y8wJk_ovKzAD{o"
    "Yn@-e4`K=k7Gc*sUB`8u$c{IfuJnTW{1n4sdgQ~?6G|q1FnoP@GCa6?H9Ud8E^8n-W0xH3CDzwN_hRWl^ZoW{JJ`_e0^{lh7dok}"
    "=v4ERu}aybwwQ~{)BT^W08!8CC_yE<sd`mWY8ec_2OucfCY+zwSUahEQQvPufI7qTbHJSzKpkYF;PXERR>Q$LB6TaVVRO!Rht~P<"
    "<PvC2>y*w(s`>s?I{kHUbjeBO59>R4K7C9lK$HK~!dKsoBELI3J3YU=x;!78T)f8QvgY{%ArK4f{;RdXI^8$f{QFJq&FRm>^AoH`"
    "&_OKUpuMXg2fpu4CAaVR)w>HI{1+EjX9KEL*N&O5@U9gd31(PQ?_>7eaa85LKRW#PcZUa*j`V8yGgXB!S(Qxj$WE}T!b<VG;#JP)"
    "?=LS%U&nSiu)3?&pyaw<;(MTo_$cpAl&huj<<aH7Rk?9ipZdNR__ovUS}DFpJB8b|(!dXs$o4i{sT+B265BB?ReAIuwNF|3L|7e@"
    "ckuGa>+|64v+wuAAo4hyXY2I+zT+pM9S57uUj`L)Vn*P*eKM*f-2n6Zuvw0~A;cm#h;6>Y5^x&Kv!M(gsLVcH-nVSz@CgK(#MNxn"
    "qC#}{w27}TxnR&4=^WQ=zIFyJy?_2}M4U1XwR&;jmBpD};YHl|k=H|ICa)K6WN(JbaBJ3Q<l;xv_n;~%$q!Cit5I^=m@4X46vY&`"
    "RC)Q~Oe-w86TGlwaY@yPAu^!GhINgS2C=c^D5oom_0>dHR}qov#cOL&{{D{BOs(Ehp<`9~jx|H@;@<y%$77|kB_3ppH0PACe@3|x"
    "(<%vrDzsy721~3H9|*gprEbhnI2MLZ`19@X=yV@FEdSgnpdhTEPS5Q*@83&Is3H>aUg~3>JyaQq<<-1q6Pe^6O*b!5uBOFlj9m@B"
    "#8ZhVLARq<tCPnTt^`W0ls3bCt+a*Q2_604PA6j_nC^>gD|$5y0q)k5qoJ$Atya`?(HbL0ceU3Fp|pL`c7C*W6v9jm+e?jTO{uuY"
    "`}e(?n{Rb(kj?}@&a_A7Rb}-hzY-SyRp|p&qR5WifprHP_VB1R;oI7-9;921Xwue0xWX0a)nhAmY3@PQz|woE8!0tUplv=QXP$;T"
    "Vly>edtULR{-L_NS6)2&Tm2fp_0D`-cN^`KZBpjdoO_0?bL{@QIrYz6HfJ#Yn9>dX_{oR@k?&8flwxxl(E9=^faJZyn+e!cI(ihz"
    "c64^ux~F$(d8B_J3X|%`U8L=SDgKmmJ}~-H%hiED4=H0F>TklAAJ-(gq`Z1Y#|80<ueh}r3B0I;sDtbtb2H5DR4V=d-$`k$emAeu"
    "Qmq*G#%LoeG6_lF=zvLzYNCZPJh6XISC5LcD&K6?=ds~S+3NQ+lFmu(4Tawm3HdT4q=xqtdkZqiv{Zrg+2R)rRVGjMzJ42jq{ZAK"
    "7RbtIdLNqa4WcW);nanM5%lNJN@kPd8KJf*;ki;O<A11yimiaRED<FY%Vzzs=k@yhivQvBF4wMsW|OcOz$95==xhqd|55WLto2yA"
    "FKB@<|GOMX+JA*t7qEj%wLpAz(pk8SURPyM5d(&mjGvd4d!_W2$OvT=xciRMp=v|56!S7itFURKkrJgzjoOdy05j*NlSjT({YMi="
    "Sj=nXC-tU^oUCl!dF~|=ewKkh$7um?s&prnmR0|~$~EMR9YAWHe&@~6+|MeX7OFQ=tT<6@lXeYlxtew-oe8bE(h6CpQt3X-W|);g"
    "@=>Gi+&(#8V*UvH?eKqCQ*1#azJgLE$Fwir%P1;CVXOu9Gy`~ABIMd7$&a@Oi@YT+P6zIR7{A4lvc-tgNin+oQMYw19gU9LJXEW$"
    "O;Bv*i8|`?L~VUBl22={sM4K94+d0oZ4C(g;());t@eO_aJ1Ra<>>=kOHM_oS1ou=MyzcZnkKCb+eD`EH~P3OA%|3$OmEW`bm)7Z"
    "jqFaSYoOUlNFAKIOJp%Ha{?Ite9G5|qS1_3&FC{d#Bm^^nCg*lcpf>vaoeaz_^bsObZY>wF7NVr4Fn;-X@gGSZxC179Xh!-HgXe!"
    "AWfdQE6B4o_Mn_)=m)%M)}?OTEVnkhpz_|772tt=3Zdm+r@3jlY6dYFPo_#dXa4)o{9e0bS_K_-q`CleMAkyfXxKI{Rmxi{pPaPK"
    "OYdBXVkRGK>pyYL-sSI2VCK3}?d$4E=iDw;Rk~KVyw1kx4{C`FCYPc#Lfi16>pMP^jH=YI_N;RXuMhVJm>jGd=wavv#=7K#O~4XG"
    "i6mvJ1N~X&ye_o#YOTO&lr}apvbD`6sAF~DtV13ukFl;_*J)to+J22f)K4@*=N{C*j@Hgka6@bT*;Uu?6)v~Up<kOqfBg&q;}4DU"
    "kga<f*0wa<;>h~7kJW?Ch-Ag3H9Dz1tdUAAAY(HAwr+P@dfn~lROCM*14WH#san~FyQO%jU!xrl4o|vwm&?PnUhxeshi^{Le_h4y"
    "R@~klo*W$he0U&h`L>d@I@-4Jpt>B?I4sTQ-2NCVk8?T!!|xV#tCP+p)K2lrOVACL=+~F%Z??p?<!!mN<`r!N)2DN?TvI58Vv+S3"
    "C+#z)_ELFmaAcWj?@LijTuH5j_o@$TcUe`X_0#jq*QZB^r>l3Yxn&#dS<r!&!S-m`V0{h5TzL<$#d5udAh_9L!}hg?TQAjQlpCy5"
    "-H>dtN;j;t*YKab$}Xm(;sh%6^FwF7l(~z{XKV6g477fXvGDzU;&HmjlD9ov))1yHFYi{u)HWr5(?!A0D~!t@bD+N-ZPzh35h}6e"
    "go1B3p-QjXAt`~JPhM;}zwq15PkOL!Iiu*?&8Y6RvjxLz+!btdy!s8E)ps`0A0$ZP?fY5-3H`QV8z{8cpSJ<TM#4)c7?LLzgV=JO"
    "s!PGmakRe$j@D+-tqb)VOt5;idQrwL=|8@*f4=(Q+l0Ik#dD;;*+Pvmt~9p7IrDDh+jBMd%lPlbVmU^EdNNJ7Wm?{sji@37zF^3&"
    ";gjYp&a!zqEr70m!7PF=Tezmae8HgMlPz6iCl=qTeH%vCMzz+A_f4qxmz}5hYvBF<i>C6qwUUPj@vkc3$Xr5Z$a@qv^2fFL4nA21"
    "2Wi~@+@jz7LnW^m7<WyJw-*Ds@UHjruBx+5Gb@EmSx|w5k{1lxj34W|Tsyq51ZY!`=B3+owt02}Ip>XgH}WzVU%j5rhgvPnwj3h0"
    "QJRz70+QQ8sJeXIc-gI=tX{bIWY@7{H+HvJxqflodA0v_-a$la(P0A%7V|CrZ_i#&rt^H9YMw!B+=rysFJ*bE1|YX5>DpU=7b#zK"
    "lbRS#bi#4E&AUzWsjgSS7P(n!C9V~nF}!<a$#*5~*4{QUWv;FqUpZ*kQvcPODKG4f-s;&RS2qgzh}X-0H?t3RBsbikX1L}Z-9G1*"
    "qT;%H_l94{G>z+5)Ase3FRyj>A#)JrA8l}vyE3K3a;B?v5O7RLnTpJJX`z~EE+p0a+V>R~4jlJG{p;VJy(>NxGEs0oPqhShW<N2b"
    "`Wz0};k;um(qGAJ)G{HXLCatyM$A(<fjP>pEBn$Gr@y8Bm`$dS*_^D4jm5V1pB4w`kKGtZ$_Xvsz(D*B<pOSjT9xdn;nX6^sTdBh"
    "`#?W$r}M{}<LjC7&yX(Px<7@rYf0IvC)^NR)5%pn)T+f+Q_=3ugs;Mv%}HKws>^HOYEkUdyO!HhzDgvw8a>(uJK*pt+v6AdH|#Lr"
    "*g+HowI#|`xVGbkam!Nm2_yT&X2LUxs`?!^b8<O$U-Q8_EGUCi6$;YshV^azt)$};c~YVD{1%iPX;&~^l{);vI_L7_9!qQej-JMI"
    "Y;%vs|C4pv$U3c@v1<hx>lwVH*Wvw`(iyUhNcjxqBT-byV+<21*P1z~?pbnj0$2hk=pqMBKz>ffpJ9tjn7!1%unQncrfRdnHzJTo"
    "`>t{rRsjhr;=o!+cVP}Yz+xR~<q5!Ts?gCNs5}(~=4h?hH@V(SRdSONOQySkCjt}jY{tIvgPONq1p7U4b%P|*am`<=Vj~<o3PR8P"
    ")e$MtH6ha^>lm)gU#nDX5nIr-32>!XlL5m74$lW|@n=|J$!KluTvqJe`lEFYB$%&iBx|MRV;oxj+pbTM{qrW`2PlT@E@##bUP_0~"
    "AG!0ofLZZ0tocV31{&k(UE^5PAOq@3t(i(#JF?(m$2jkW*w};^&Gg+2R8D2E>GY^>7gy<MoQdi08#AXS9BRqp85ZGd+aM{vaYdin"
    "R-wGtvjWGz?pfJl)Ui)uh^!7gFObmN$E8}EZOX-xD&ZPmM9yyHZ@!VMC-lB89+2bH2F0-UoNb+oqE)tydT^x@42_T~Jt~6j25r%m"
    "Elw1*2<V=0?Fdv{71Fnty0f0vToSt~aJqi0UvJNZ%~jFUN|Hu1N+pLa(obmIkn4w+Rfvb+1Wckus#+}aq!(kNxky*i>3p0Qc$2uO"
    "x*;h;38dsmX1o^BA18;0m*!`VpYZ>)Bztp%c{8w%XZs)_w)WzL7Q0|mk)B?VPS$1Zx##-{=IM=8nv^%~9_dUvyIu<W?5c#?sywq{"
    "`3$|j8I;jlySYl#OWHboR6q6|DS;bmpP3%^%_JX#^eiRdmKP=^OPn7p4%H$za}R#r<eyC6^jas(+4XK5JMQ=U&6cmRCkCF`+;bea"
    "%3>o$E<G!+_NEz0S;al^b2GUw#V)WKAw$&pm$@x1L0j(ACG2HNbl%J-+?I`_(jrk<x6-OYH~s!W7pSzC;>izd(sIZkP@(V|N#lV$"
    "HFX%CyEG>ni5bLI!Jq%EE)bb$3ct9aSu!5W-rdY)5ZbR)_-%n@ee<@~JI|SSu>DG5<zzAyt@6Tx17J{J(N;&<Ml&-gJP{G$)~<zl"
    "=80Uf20{7Z0hL2NR6G)K;@sRLDqnB@{&TOhV4WzkQKcY~5|^G=QVVUb<YiHmT9(igFEmCvHFG&iv9qD4G|J>viGJ7QZ8mZvuc@6_"
    "<=lM=gL)<_5_9{$`xNr9St!{I*EWhE@9p}2<c6G?ta&ve=Hw{jcuO5+Am4h?XH|9Rus9KS1;28oJt8`&9o}UH-q3N$Z7e9PJS1qO"
    "mL|1;^4RaF-Tc+~*355P<)D-K<M`0j)AOo8&=u)nWgDK*ZA+%$meDHl$0#K%eA)ju%|<4>=aK-J_6Cz|v}EXz#_8(eis<U9(O_j("
    "k92gGXP}=~sXaPx4YXNeN|m<imYq$ivKWyQg|6)fx<iqE(^o&?^%Ly5aX=(1X`JN7VGn~iO6)$R8kiPGD;v9>+Yh72)=C=?a>9=M"
    "QYX%w8KT-rJ>?<WYqggugP|0JYA9*s|67x=kNUoB=|m>|Ya7ErIwQYfM}Ni#RRTkqH}9{UH&4KV6A}so<fAm9c@a~;t14tCmQSYD"
    "!(us^Fdkez$ow0i7zdP}Q9Zq)Lb>JDSf%X;5i;)k%BAUQEZx+Myz5sgJSISg_Q>e7P@oGO4~8ToW;Oq~G5=)K`GZ(Z?j5V<ANXF>"
    "k2jxx;`sfzYyL?b_PyHtlg9k}8_qureXqX`{z2IH9e3mTgOCx0UGop4xF6Nw->=U<bT*uS<Og9At($+}@q;bq533~rw#`2ZBd_n9"
    "^Y@*`{M}9G-w*okTKM<-vF|tL9|U3KcOp?g>XT`^Z4t5OM_6&dScKbHgty@$;@FAf{+dOEo)bB7%OaeZ=tt{LfEZ6D^x77Y0B?!n"
    "+9JHhBK!>(kwi%xd+Qbv#(vVW2p`C7(zS@#i|K^6Eu!zb5h~ioBK*c8f(;h|c+w|HeB~m5V!1(c5gu@+E_8~#(2c|PMZf{}lgOzp"
    "B4{ik+-wn^16xr8SaT7PA2WW}7vaZ=-?fOui@OfC2UI%t>*y3V77=Z@2oH{gyN)qL3H&!{F2ap{r)wu-BzRpr;l&^ugtbL9xO2E6"
    "clLZgc7t^X8_+v$;m&~zIM8(_5~OKeiwK+qSbl904Hg}4$fCU<4x@10PQ<YY?5`~XcxylCT14N8ybcoU0b`AlI*D!Y>2O0n?L~0J"
    "oOOI6@c_e{XTk>_L+rb45kN7##O+u_>?BE?)E3cT*3pK{+KUs<^VXqL0uoiwvWO(|JE@cFM1JUZFbXdL9U`car=Y>IqYYWM*ALxj"
    "Ez9ovVd(Xns{o?l_q$dB%7f!}?1k@yP8`)vMbO~c(S|(RcYQA;MzeAiu#C1<M8MFxPK67yt{-*mg%4;Pdo=<TG?;d@A=CDKFAn`+"
    "^(s6k3|+Tn6(BvhU6O~3_~v%-3Lk}*y66!!xOTK5*9O!Dv0@F^_FxHK5H?p4gnklsts-<m6z@=l@QvftMDd`(wxbQ%wvSbm`oY>&"
    "IEmL}7C!8x--%HnP>n7^3#z#9#`RS+_;wU+x)&ZWjCC}spCm!Q$+vxwgq+U3Kt(G|y7mI($FP378;m>JkZ}Wof(E%xElLv5#hPk`"
    "4_vK#FM#%WZU^Uv6P3XKYO82)?kL&xbb}5PtfNt&1~~mDMtSH+>v!@C5HdZdYZV^sRZYbU8mv3&Z@LQDT-RGGM7d!QHCGXbZoiA`"
    "0fh>pu0_C`xNav18mv3skahbWh)15kRwf4&ZypOTM3ui&CXb_9$JHW$vIS0UC&C8jj@?apUL@=oE43rE5H%%152dJ}Q`vT-IPPM3"
    "zz&m|_z^Z3cf2X%c0hd#)>@nb-|<=&;r64XOZ@OawGF#=!c71yH7Xl6_;&1XDnt38sypk<esFC3rr8FlZ$Lx0Ey4%#?R82}LDa9&"
    "*s#I1<6vWH79^Q<8-Zeb3v~irI*PkCVi(l7!0l2j&|=`%B&e{#wc|~dZJ<qIxK5e{X(;xaW)BcAyr_#h?ZR;ZlGCMGL}9<KZHEo6"
    "9dD{_2Yt|D*5MO~XimR*DDbX0j=NS7qtT$_XaiA<qq^ZEY;f&(V|6<~-FNjWK>Ki7#K3;+bXp8{;fsC}C0*)v6vatR$qO4yJKj{?"
    "2C<^QPRUC^Z*DP&M?jqX&P9MY;B`slKqo*ute@=$&yF`$w}Cn(>-35^j{P8R5y&Ig?Oa5Jrtz+wa6=FS>O{7|vy)A2<DmDt-WtIp"
    ">W87T`PIs<3y0e6yqxIw6X?xcK-A#Z$)?8f7^TfM=OJ>Vpha+Ux@jw_&3>0n*$-h2wFNYIb+V~pJPiEATO)>tAmwhe14yj`ziS8J"
    "2*HeN3uy4^WK*NK9|JvGvjagC^qpXf1tg9ib_p78fMQmC2O3N|+0-EJ_VKcG^#Xvdc*zzh<h#H|I`39|tfF1B=tm9yoNUOSUB`*~"
    "?iv*GJvU0iEfxTL#tS->IAHd!*RKf}QG+!n8?xpEj<CN*N&-cV&5E1OKL#A}J6J(K0O`6u{RU4?Hsr|>-q5TQ@_?PSSn<0BBPR*^"
    "U5XppDjU#maN}e{ZVbX*6s(i(K;4bEIKQA<xNet_4ce3A)#SRU!H1KL`EVGnQ=P-a3!E)x53-K$cbX^rNnL4<8VtC<Ap_n8%vpDI"
    "ftW;_dj{+RW=BcVMf_bLV>R(1cD{V}9&j&b-Sp85Z;Sc+!0Wn<!_MdTpFcnAi7(MvXEzn~ChWhK)8g6QGYo4V-DUUb)yHgJvWp-^"
    ")1`BEdTRNWoetAdI60P+<t;TWg*W5wBzq98RAi;_aJj(<zpJ9v|8YJQ?v0}=U?HtsCo5;utF%f2!T}X3?f>xj?CA8@;Q@D;mmjWX"
    "n%|`KnWP=9O{I#MtLA~;z}ht2r0qj?nqBo-#5F+J-}<*_$9a0s&cL#q#&6GFb4HiH=QF^fF+cM`1a~-8IsJ46i^z-Ht5TLq0pJ~;"
    "yg3?jM~?tSfX_&a3z<#JT!qu1gP`;cUY8OwAAJz@A%DI+<WvtTC0Saahu+vap3V!5?^vXBi+vb5Eug5eIJ|sqX0DMBMk<gP^HiZD"
    "v-N6{6=S0UrOZM5kma{`i>ti2s^;$4QAFoE<Ji@!c@^5~2+P)*mFh`8|M_e6R<3pPg?1!u{pT+*Sh<_QR=c@=k-waFEb{f`#n7S*"
    "4H$&ZODi{A+d)pm@g~p4jV_wySv%M2b}cm81Z~?6=*9lq19QC>qq~Rn+In|k!K5(*3(S~<3bxtCDmX*03fs9b-=~Yu4cE4I6aRGb"
    "Q*BXa2j_rV(<yq9-&${B4%V-EHW^#5rntb3R#y9}S@X7g-@0)$_;P~t{q`<dc>teq<G$~by4U2bAS%p^KV*+r_t|2uDy-e4qeWR&"
    ">us;|i50qvoPlvKQsrPVrj!eK!Mb0vEHFv0Gp_E*8FerWJOi1nSRi7Ec~QpnOazAFpca)0Gbze%&tkjJf&AG#pK{6_k{Wv!7lE=0"
    "5KVU%+5FxTdDBQ(noZIXheN_IN)%xmiHOW!VwyXnbT;GQ$lreZ?b#n)5C37*Z6<58>uHkgj#NiR!SGenXck<xYkTmXoY5DT(^nW)"
    "d;`)Y`IqxLK?bt4a=2EZLiy!xy=TAqbgnW$$OL>-A&Ct*FiWIO=vf7N@>^JYT0XOu#ROA2;%L-1hn=)$%lYUIWMZ4^tw}U_cX3d|"
    "k+ifjsv|Y7p-L@r#2(|sVrrrMY{6DrIdH53;B2Wf*czsYbQBtz=uNFZrNt5><;Xc3=U!MD!1U2#&8C4fjpE;bes60PxUC(W6)e1X"
    "GywL3VEp?4sF4g~TX4z@8(r`mEN_9*e;0649vej}_7!<r0TZGSe<&@XSmJ?3=u#y8ScYI$kQ&qo(av>Re2~$EC49ClEfI^1M=5)>"
    "?n(N2(MpsxkcrCb7R`rQL)YP@A!+n<0z+6k*{9KDIR-M>9Fdyk1*VwOqPW$Bd)C8UKDt9ZB5YHu69hn2OIHCPTqD~|Fs3CBQ^<UR"
    "n+&s@OaPuaqpYG}Fcqqqz7}J*+#O07!ZFi(&Cz&w+L(aOF*s(lxg8rY3Rxf8Or7@fIQ=xJ;&M0P4gk}a8>e~`yG*}q{EJ(z;Q(sp"
    "qI|vBaQuF74Ln3We%kZHDP3>?YPOipC_hXaa;#+AiuedDtn>WUCrGW5lsJjo?~StN1^^i4wFHA&9zlijLwO8q6Sl2OJOO-Izt>UF"
    "aIobh?1caIpZ_Zo%)VXbdhwJeLm;#^sal4^uRa(uz2hngYThyY5zs2wCXp`lrA(<wXI7hX?Wkqu3RcTobvkMuHUka!beVuKN8k*z"
    "<vZATcz_i+tQ3PEEf(f@V=+ww{%)Y)MfwPAoCF3seb>{)-H*^rQR$rVNu<Q7j;QQ;Y7WHM@J$GKHFgtmaeb@kLEKFZHj(rxUnS;4"
    "8wgT<EK1pRG#8=@ZDKvI<r#3Bi^c8cD!~^f%lsOhL2@i(3@(sNfwgKZEoroI2ux{9mR5eh5%D!SkD<QM;3qZh<EfR(5sxKKQJF0k"
    "RKSX4rByig+q1}aTQ$vX1%>0rn%e;Wo&sX$%Zcps@(v(pks@xTb3Q85V)AI+<hM&WDJZ-DZ3!qr!ux_+kETGhXA7VN|4wi48-f!Y"
    "&igDyv!;c)AeefPIw;A*Jfnu7Y2c6mAUK7bUIG{zQ-EO#LL|LKg9ei;o*$5vdldgsyu7Aq5IWFUwxvml$Q-X9c`evE%nSSC{(s7{"
    "8NEUT*n^n>rFr={7Yin;HhD-NORG%tv4zQ}P`l_s!^!e~W|hl(v6j5#4iBa*@Q%klczX@!80HSZ!fHJP(ub*7fKa)_;!7OlZu)?e"
    "c_hdz#1wfc4EB_0o1)c1jxh)yfAq^dubQVNGh`xiIDczL=}vzCMNce&;BOsXobp#Y_>%J=zA!r_)Wb#1MenIqrFQ`lApF7T(;8=^"
    "{2o)SICdDy&IYt@*o?nOy#9-YDPT(LL-x4KmLb@N40SSEFDZ?<)Dm_NM^DA3lTIWy3=RQ~YTf7MBug>RJa4vzSuCu_=@O1(Mkqnj"
    ";S|xG$H?jRT;(^JEm4d4o5E?@B|>CWS{ZRc|5?B&w)L8fnv9|;NtU>HYJ_<4UeCuQtX(1tJ|#fV88hZB(D)^sIKKa5xrq6cXo3{P"
    "whjpuCdfANOu`nj0KA}lVkMrAQM#m)%E~xC<Y{8bU<}a5QShTj&Xt20h_A8q`dUVu6}LHnQ)ar`t2#BuBO*t3E%_X8I~G0Uzzb>*"
    "J5b~59o7T^JLn*X^UZgyu*yfYM2nPFl#545lqQkwCzPuoG^s3NggVhk+>mm}i9Tj>E^Fj4Sm<Cfd7}tB9QtcaJHm-;@U@}-!tXQA"
    "HX%%4Um@=(rAFbI*a(>bwbLjgF{RopRNkj>rhxn3&eQu=JG}<GK;R9WDACJmSfvUYYV~Ze`o7B_d`y2Yi`UX5ufz%9OkXJmn_JJR"
    "FO21{v%qD@kco#>EAF8UE&|05(;iqmfvRBr;z#qamzvEk>Y+ToTv(2P;LUsr%oLMhH)NePsljlN<$Xa0b0ggs{I+)H(<LdZXzOF$"
    "bBpd;l7&&HX$8AdSj040*{FA58=3g@&My^>ZtwK{MifV(OV8vg%`^36=tD>6DUl~3<ni52ktdPJ<NY7x`9{b?G7IXVoS}=8I5(|!"
    "O`NI;1T_?*vMO?_ti4JOenVn1@AwY6_)t63!foWI)KE)`<_Z&F4?#Sz2<6BhNMez~yLnF8@D);i3D;`n{GEoD%tVL>lu1$YU@nBV"
    "a)QKH8$Y(-hL<f2kYpc$;5BwwHr<43XM9V+Nk_U>5>wlYR=K$bV<|5yoKyaA)-_0vwskhga<Hht>@u2Y$Ef^~kh0n$6r&p(-rTOQ"
    "CbSnIg`#aiAuoKoj^4`Dt~IHa4h3aRrqzLBO7i|~hI-DAIE#F4ZWv6GK!(<XiP#sDq_(B2x0?xS?baN$?N%$cCa$jnrkTuSGm&4u"
    "<>OL*B`h7a9Bn0x-L8a*E_>oO3~)&1W28LaTCz(_7l_7rQ1^jx@s*Uu<_ekFQ0i$9cly?+<p&ZS1wg(5CW-ut+7+E#wXh;^hQ{$U"
    "<C{9NUG+%yV^XT8kyhtkCf%$ZeUZcwyP!#VQ6(Mgz+Xvcxsx+lfcgO7ENFn7IU-kW!ww5^MY6#9Cp{|srz8p5KteEKlB?$OqeON%"
    "7s4JeMKyG0TOGOOuq7EvB!e4UlWB3wHoXz5&3H2RWWQ`c$QR#tYmtx0>s#V+9dk8#tICx3<=a}bQMPBNwL7yD+Fd~3A*iod#(S-r"
    "A!jPB^9M4?JO~q3kzpAWysi+pPGnC)tl=9CV$GsEYrX_F4Z<d(5t``kmvFvuS1_Zfg89RAIYBf7!GjDZRn-ZUJRVDn-GM&}ld81J"
    "<O@kcSVq7+%1?d!A;=jmpz<cy76$)?4UYYq->8;KRu{GEE1zUH3$bcxX+<|PasN7-NU!cD4^e4x?aq|8bSp4R(RaJMk-q!;qIGTm"
    "_r+b5+*H}Av{aU4o&_{0vIUcUbP}<xL4_*>7<P@30<281yN3o`>^?0k<Mq>u1hskZF)iE0-1UNp(>^eTlXnqqlu(+;+9<nLhDyJK"
    "kn`$rt*Q9Aktg1+?TFpjp<eg5BT+C4@2rYZKFRrF2_L_P#|PPDk*?8lU?=xQbCkllJkI-$bj44tE5E5{6h`}|Myq#3dgBX`-nd5$"
    "he}2R`{l&NrAeP<8saY^&p(QXLNiEZD&$HnqU+hx`g=B?Vt|IKjdlkI12aQ69598^|10tOj?UeUGC;3lX}ZY5uA0`4mbw|SThCAa"
    "qISLJg+J7<*S-~VGx9^*n<Q(lB-=W6QUdjj`Vh{QEofhtmJovXd9f@lQEsl3cY4)H{{~d-L?^B+Ei0O`Ee+aIgzVLF(q|QL+L#B|"
    "<!bH8<SXo;M?4+pC|qAyfRM<GSMV7MFyx?!x;V0y^Ddo2$79|bd{Y<#Io~r)@i+kA=~?Aey+K9fo-YRJHYhJ`3un&X(1k5fT6yPk"
    "lRXIA2@i~I#BCDZ$dF7-Z>0(&ub<TFZqwPG;G#41r+{P2obU!TY^7;HtDbPPz?MSxSxkv@s@<JrX;E5}e6g62DE{p<qk%a2g61HE"
    "O#mD8`U&-)9@AO`48NsY#bU}+P!xD$f}>%My{25kN_J_e!-W3kc@Y4s;s3xwgC*A7s8n5X2`=xv^F`$W5d2`3OJF&9LD#l(bz}Xs"
    "T%~Pu=`OmI>_#0Ufy~GSTWEg8JY3KAz61Nvce7DLW99yJQMdP;_<Ur@#g%D>j33&qs8&r!RchX-;KXO$fu{=OkY1xJJ$ygct2D21"
    "k0g1Y3#1waC-iDl7T0IhE4FA)fFRzg-&6_WNIFi*ntGz}>4@AkG!N$HTfpY__osj>sVGW!y}Y@h(qGkU%c}W(*WMl$>5BKV>}pl~"
    "ui>LE9l|>cXOD#M*3a2|oR9bfX2RPFqlZ&;BE*km6&KfboIWQ6Y>cKAX~!p3<)cPHG`*UwjMCEUp^?9y@j&b;g^$q_wOy9Puxg*H"
    "R<9(`aU9a(v?pTsl!K@EZFbTESm}-?yaK<vpy@4N_qJCq{byD?RTFDgHT^b)P*+x_6vffhTN#;+M|q$k<EdPqH1eOrB$hLQfyd-j"
    "RI7b;GNqbzS}hp1K~YgS@}JqcBv$32Hi0?bs2bN`GLi8ZyCUepnuDa)6V@E$?i4k#%TW`S3I?}jbwvH`7^%@5L~(Y;A@nbo*Pz{("
    "ALxYF+N<8kwq$+GnM42=$$-u*SkO!7AE7%m@CfxPFLuk(be36IoR0_~+05mP4(02{(m{aTJw7%7aIpYcj$O~q-lUBc#%%y$%&lmB"
    "_DY}wdq%S#k5A<t9WHkb2tk1+ReNrlOMfohcH-<02n-oBL-NDwA;)+TG_OVt<fsSY1xHS0lN=ZkO3y!9H_HWjo$0bWu+9|aW-%^^"
    "u-PXv|5n8bjk=`(4FP0?uJ72Cu2u$mf-bjPS?oxnnigcqxnE8e`D}s#(Zc2??K(7u5UeEeLj1gZoMngP*Cx)xzZm4VkQLM9167X~"
    "_jfVR(uG#2k^NNn@3PSc++~Bf%ZFykv`<=1PES;s6e5^W*s}S|{MHxzpgTOfrJ$wRMbOoS7AL&6lTd$Fi^y#++F5;1m+P_)B|JV("
    "F``|TdY79_ADv6#_JWFNSud^2d478<c^XzYBFEg00-Dsy7lP~Sx0VRGwf^fr|1XI!F#fA~I{F}3=&7uV$%c%cb#aMCN6_E$qBMS4"
    "<GidacD<^eW=_F?C50LmyMKdI#*zDD5rJIRCVO<b|AxkPg@NYmmt914B8N9xBXmjy340-n2bMo7A}p*zv-$MXBk$n9H^=QkFZyDR"
    "x)vi#kWrD*o!3X)qtgmTa$mgU>Zes(WDwfP71P_H#uoWpztCs`Z<C$y0Ah!;@t*wdx##;>P|^DD@TcSaWL>~15oN6g<OI2Bj%H9h"
    "NszP(o3hikMHzKZ?Y5GqTqkmQ%f7N?J)$i_6`x4ZWIFw@oJmj~58fQ|?li}i!W|5XoC1yle0-aaXeRTFZr#_+2erG}5cS#7q;vx~"
    "O;_QPn6I((^f80yh$i!TGM(q+R3NDZ>TP<jVS$aQW8jGL4@FVyGhrm)m8O$ja-%jzS2c1qOQ><8y`U8pGx1$@qz{X8Qwx3FWLaeO"
    "K-en|n5tUFT_tl>X<t8-SPN9f`lIFG|5cbQ)OPtDuhl@$s&m>8)v=q%PJk+Oc8uTDI(;vEncfOPpquB>-=Z1)t><AG={kz8ijc)x"
    "l$%!<l4bSKpgY#i^Oy8aR;aGg!`k~pK{*w@Fy6wp?oxbK>sy_enQtyS-<%rz!p4yuNwjHxe^k^Q{?s~p0cg(ho=!NGyg(9_Nc(_~"
    "mh%ENO+GmLZ-%BAv4WY)q&a4G8%|K<#Wv+p++~vD*hwUai=Fgi@v!@!IJRAv(do~^_Vs@CFHLw^Ej@J1no<q<zD+6AzVEF472-<A"
    "Y&ma`pF}q0=KH?$4OY!p<QQ6$6^L^Ig@J2R{U|kmH%j<V*Y>^s+65$u9mm@*AY6;uDp`w}V};AD2cGTfxGiVw1j*VN!|B+5zR?PR"
    "%X~o13_k1<A7Y)<xG~!Zi>ZH`*~S|j!VdUSG9C|TNANwto2&ruiiy%p1DmqxewVqvr>uC>(T5G$=ZO?@E=3k1Tn{kx>0B_hG3=4x"
    "qI6f*!co75W2&r1kA#+&m&aleAke%9UMc2!kS)@DvY8ZM*c}aJO#L#Lo~j`}Q1xaxG;Rlt61?N0L7SDsV1*}W4*0bDnxe2}_77m&"
    "S{g@z2~PcA!zQeW{UkE1_)Gu`XZcSARvUaIWYP_#1evz5srkW6&$lV}zLYBi%zW490j{?k;G|Wpr6X%owHzrGdx;%IJjQ6tF)o(Z"
    "3$dB519GoqVJJTMEQq8VOCmDKVLN0JuKX(@6WV^{h#{`G9-<RA{m7;gwh}geVEYVzZ?yF&I&{2%!vP37eLLo=;C{MR;!&9qTfyS{"
    "o=sV<C0ruU4g>D{dh@<J;o-tsY%263Ard&Q?YTU{X!8+tSOlSOQ*LSmMiBWD8bP{Np7K`#qwm_T4huJySQuPy+;b-=Vh>Zs>E|Yl"
    "?L^Fcv~m9$AQIPA{2du+zrUSO7Ova8007a~W{hy(P>u@Mfx{2rkW)T<*}Lm`eOc~)3(+T8Gmz&eHdQK;<0PT&^*5DQ5@&t)p1H3{"
    "=*fL;;Z&+pJJUI_2lyk2`eCJo@FfH>E@Tt0&`aReWJ*?Nai7z;a+L2a_FSMTtiprCd+A6)Tx)t`b+iVJxDZJQKuZRWhgUI=R>_xK"
    "A|nA_!XPW2K*MpmNbT+!XuG)49Ju{g&7ysmo1-_{eetN8%&{+ba0@$)5IU?Kaj!&P8p3W*A@8Y7lKrljXMmZ1hq<8DLhs3vejK%1"
    "KzB<<{pb6<q)4)n8d`|eYhTC=d*s6MUW!HY=_j-*A<(Z8Yhmsj%qE+2Sc~;iJvg954D*aUt|)+POG|}htH0m1_?z>?-|r%Vjak|6"
    "cMaRJ(BJP$Hs{p8-!*J64E%oAvW3X;`(4DwV$JqT*sZ!1ejnyk<#&?VauS=`90li<J`KMU^9cKAv>Qp}tyG(x<e+|I^|iK=YOs~|"
    "66J^ilem<w5yvU4`BUpHzP#zCbt}h;>gubCO6C?S>6bhW)s38f57c<ta)VcsZd$cFygZUu@ao#Fz7N%;2JOx|GwGePZXd~g2r#!~"
    "mnSsZsoBWHN94+cm!<D6(Cy_OeZi?F0%amZkU#E@*q(^Zvi!E-1WZ3tejrREB~p9MC_N)P6X+LwmC8~AUREwTUE0iV&rZ(|4o?Q>"
    "zt%23e<y%CABy{JyuV`znUJBRynsu`M`xzD11EdKFA#G|>-=<oV<?&)9tI?9mzn=G5E`Cy2%zg}G2Sf~j}y)%r2@1{9SCh#)|$ek"
    "U&N~8mwn3aXA9}FqWg?|(*;WZi5c;=v@DmDhzzgHm6s6{78!L)9tgYTEE~bTjja1+k)!j#v=mwIC?xtLums^VLMVXBn>9-p%5|^H"
    "edeD+QP69ASIwdpBRtEIz?0VxCvmtF?gl2|l?%IAwXlB%3O5!<KF6z8r#v;9D<n@_7#)biJ#uo>clIGK##0gH1Z3twa}<ttUG!j<"
    "m6PTR{iUzHyk3GJl9lB_`nWILgyVz)1oU!LSlnWH&n4YhCi**^RO;_`Dirg)c$HE#02WmuU+Z)}%lt?3ME3)#&irwTsZD_JJkoQ="
    "b`mlb-IHtZ1Lp3b7rTz_y5zggNoLQq!c@moJhI{%VmZTHo%`twU1da{QAjm!h3^oT&^Q~3B0*Gq631zNm-NZDKF{D;;Xd*%qdkHP"
    "oA^}GmEZb}w;@&Dm2dZ#_sa=|BGcP2Ak&(d(d+z^j2D#Ca=EIh1_lhK#Sk>umr@qMt)PcKyl1nsY%W3u(Gi?V5}Hj8I0UC^=SDs{"
    "Vtf`3<8Odh%~Z`R+F&L0uHWGM3{!+Qs*ovhhHFJg7w}bT=(P$zkmzL~PatY=R?e}t9+lr`1HW9Kii39Sn&<YpZqlk*YU)`vPtR$a"
    "Clv_(qG@_m9Jq6uabQlfUGu7@=R2+Q<4TM53AVeyHs|Q9!vDVOQX(ouE7kLnqU*YDRhyHi%}J7=R$Ae@j@wERWT`s!(meB^iTYji"
    "APFLO)vEl82DKgAIPq7X>xjt0byke-P^uX$L=OK6sDmQ4jfv@mt}U=9w}P%|#*z2g97f0)-(VctWvmv67vJpijO53sQqfh!s!E@_"
    "n9kVAK*A)zq;T4E6(n+*jqZx+WO~cII4?m<%jP+za58(9Rr_w!*#U{VBE&)t2rTwZIy;*&BXPL2yL^05m5=ni*s*<=le&$Uqs3WH"
    "7Z3W!Za@W?F`kZqDI@Wy0d`KMXdB;aql5`a9#jdt*-O>T52L{Dy9VPGX~9K+9+B8VRpYTE0LMB~1tqx!rOLaU>dvKmZY%_g;YWBN"
    "d5)ynC5HXV3XJ#ZUxkB6Mr{o_!ijgis8PHUgO)^>yy*zYfcc}r)yQp%k?mkP2gper0m2+{SSw06!(uFl40fIVt{YeLxy%=W3cN-S"
    "boA1-?(z?)m|FmLEOHRqp%Cr4yNiXa*QwUPChIXesbO4WCU@7Rc=P-09Ps^>JY8KY4BJ*1cdamt+|NYRH;1<C?YjPE&~|;dIhmki"
    "E>046LfhZ<-7aX)@{gc=pf@udLlOos<D+kl;puELU39}7SK@TQoCTSUp)Me7LcMFHK;OdcpdL`fUAQ5RcOW#r^W2~d#xOv?4aRRK"
    "Q();<nE}bTxgkLReE1)rxdVR7A`X$$1?2!STWnqnl<6{gV<-oH)V(q<-WsNGh?C7=>N{OT!f~Ux1Eh#wNjH(0v&S<AVln=P&h=~s"
    "9AUO$8ytzdkQdR$fb{xF*K&N<-4>3h$8Ct4ZWMOH(FwcY=<d3$sChZZ6x`W_Goe}!;=Z;OeAOgd(9nsuJM3QPB9iTZ7h;UB7jFhU"
    "IK53O<8)00PDCp_X-H9~xCYOIECX>U`(O<Y(O@w8&;?F?+HK(6igt>lwc)Bj3E39HaCW@SAly&lP6FfilP-7$9i;OpzZT*A)&V9h"
    "N$2^^4Q5R#K*JabQ%yT~)tuW7JCVVS;j0@I8dUSkz}epnoL=a4j_j-gr{}eSv+wMV6&S4<87AlHWb(Kgj{PpN%G-)&`f<{^7`MMY"
    "7(?I>-{jnP12*iSqwg+u_wPVxwccb!_A!+Z1`S7C+qJ_Mx^p{m)Z18U?OchwB~T+cGt#2C9;p4On-jGQqSU|F%F!>DGgND={poU!"
    "DbnU798t;4b|TOPR(%aEl$AKo=8P)pMp-9_zW}=4hVl|Cq#Yx3>X$a~f*usKfmfwPv4*pJWW8R_A4y^Y#62wMX*N+HhbD*fv{(sV"
    "v4}RTb+;l3PP~G?2_r>EXNDn!#j$IQqmr3XY`0IgYI?}lBF%K%VlweN4A?#ykEk2XG^E>mJ50?^qP=ZeVIt#g&D0#h@%sF^J6j{e"
    "0IhVg7TA|$8ET|EA{!>D6q_d?ViVPc%xy{YnorA8!O4?OJ!Vs7bn;lun@#5nnQpx54Rf$KoykU<54Bu&DtYY*M&*jhxQXv39-9R6"
    "drId3LU1P2VpDpRe&jgorqrC#c{a(}I4UjcW(Nn^_2MF%f6U3Wiyfrnan7lVj3GFm&E<4|GA%Q)SsDa>L30|WKs9_vUM*EV0bw-c"
    "tFzgHDnTu(j6E1=y(~qTH0AWf>#j+9Tk~9SsaH&4F3KrtMf|E5?j2tw;CrE*g+SGd5#wHy3k-V2_qo0%4M2TULYMJ)j>&(jdTzNa"
    "!hoskN^;L<1GukHNc9=ZCsn6D1wt)E-8W8pNa<zk1>kr-G9i=d5)`-EG!Ze6v4$j^T3G#TGJVYE7U0zAj;QBso?}9+D&y|S%Ypb>"
    "b`h@WqQq>g<29W`dM9r$2K;?T<5+Jzyf{0vc7{A|W|41$btWCM@I=4p=mrVu8L->C{Pu2FMI=*l+nxU&|L{Vj!P4Mo?nYms&tm$J"
    "&H;<K7-u^cMH&`Gcze{7Imq-KHwJJWa)1&<kt~Jh)5RU;b`+CoF3NRlkffGDK!^ZPqEuwN;<xsh*BA=RU1=^qPLJzkMD4@+`mllH"
    "ez0Cv$bcKqeRx4=&O|=Yx(X=9?<0G8C~vN7?FLCjJ2dAJicOtNAL@Gw0z!$TsAr|i#q>ot2pJha05(%)k$WI<w|MI$Qy#bClW>AN"
    "ogqcU%!7}Vv_>S4DpUPeTD~oTD(wM{E0K)C>ngDsr%<anA=5{(V}N2hm#kjM9BDNc>eQ|4$Jsc?{N}_cRE?<1^phaX>PF^Rq>>;j"
    "r9=7x$gj}w=Ms@nTTV;P7vOn5$vxO|T2M&!wD^UDtzWr<$6nIvHE6;?doNyG$`hq(g*a4IW_6MZ$%846BA^GX^msbY&hN+N<y~6H"
    "tf`U@)q(QrQ8J&E{K&|{RO-p&nlEH^l7W$QN~Vv*ychRs1LUzbPBZ-<?u<Nrc<8h<#{VBDf%9G!@NFi))^4IMvCIK7|0t32MVFLg"
    "Cd@V@5-kH!CH_Ptr+#Z`#eCn^gG^z51bV>a@f{X+<U)bkSzIU57>fs4{`6+pwk|RUge2fDs+&}T`C;*TIv)vfc0Qf5=8@)?wRW5_"
    "o4;17!M<^eXgDssetD0cjp#dCqW0rkRI}B3g(VHq+sE3qhL^9c{YeT!iI#F?A;PTDT>9$ph!vv@xS}{YAm*F5`ah=yCX^mq7yo)@"
    "0ajqQ^`3q{J*{^XgkDEK>@17%|036dbqJgDiD!*-ZlCR|lY{yg7_Ddy!fAId7V|7y{6GJ<b#ZoZ4*#h9%hmx_)Sk|=vGvPz4xBps"
    "v<pydSrL5sOJg`cjJ6xDo>ZcJq~URWBqvPRalyE{2CYeDtQgf#w8~t_QTKx87TMw#EFnSHntkEMl9Bp26z+O>*b_hS`?il%v!ujO"
    "Bw2|(0(26z$G@m~n$OQ<PC@aC^GP8;R{)VcvOf>qmS<QOYIgVd3N(&ef#`q6GV!<4UyjGKc7C9$Z-~$AD=L>N^I*LLJ`9g(Pe=f<"
    "`(BvPt3jEkcp$`f&`Zbnef_0E4Swr|9Cv*LfG(^7d<ih;S56pnN~(N324Q8GQY9s_p@<%Dw8kDk8!qRV8gUm;&ceUNTetSsoTB5p"
    "`qF-a7vt%@c;|Q=0+<%*I5nSPckC)9pT6%^xbf;yx#l;*9Cb&1EhEFFbU8ONuL`oO<>^rclh%btDr%tn0yAY`sa}u<d0=FU8Ts2x"
    "HA9Q^Iihau&=;e-hx8h$r^@}n1{F1!%BNwDCi800Xb}mf8w6o~o0WQ-4gOSXP2_MLv1i|8je)az)TdnB%5i|K!{nw@bSAj9YDsL="
    "U^2;#{M}4;LnML~noWTD`toAf%|c`nBl&wxG9$58^1<UIE#&7^_hLeNprv0iXfN{(kxHx*&B;z7ZN`)tJEu%tyhPo73KRu)n)IAq"
    "U!-arPO^_Il`&peJ24P$tN@OiXYGKnncy#2F8pw9?*~cm-)8A#amV^ik1TyCSN=Codd!couDtT^<KBY4=nV%7BCTuR4ph&tK@=}U"
    "brli^8GtS+oLvJ@mtk!C)!e<%4y(Dx+S~!`=wv^)P~#~|vXkN#^+_RKy#{m-Q)}=d+tt<(sS!ltoSbb$Xuc&SZRPAE2Z11G?>pM;"
    "`#4N}^81e?49J>@0Z7MOH$b9+C&u|!TU$+jSOESq#yD{tt_4Yyh^Y#Yc&ghFVWsAMkAVuJyrZ$TP8_YDe8STellN^$jgn}{gR$r%"
    "OL_^4?%g=q0Cg&C3_J~4&H>S_At^7Sw_q(ICIKHJhHa?r-aEP|$mPOa$`i4&uQ*|};J*3>hKp%ZLRw(~Y9lFTG+UKDo9Id*3!TZ`"
    "m!>2R*aGouCIv_ia8$M?s$Vijd+QAutKYAGFXSl{O@UBm;wDAq#1|@hnNB!WrqF}Y&9v`n=}^@WnG&O0+8T7RqI3i<CHc0&>y3Q*"
    "WmI^DJPhsrdm?D>MSfe5E`ecS7{PR%r==czRfyUH;*11d%?74P|E-K<A$>*$MxY@<@S{S4N?(#H5E%`xGpaSJ(k=`?<qHcXYZXbO"
    "Eto5GrbZ-+DDWU6MNBtW!<sdGEv}pD_i8t_8#13=RMltuRhbI?l5TB3c+*zt`)$Jql#!@0ei-=rclGf-mprJ~cjN|v$7Ma}W>rO7"
    "Adtvpkd*_n?r<dnbP15QhFqxT@Px*xejmspRM~EcOpU_ESj-T$V=!d;NEKPBIqNnG6WnDMddAJuyv#WIsI<KBdRF(M?NPvz>n^y|"
    "s^)Gh0?$Ukr!r1Uj1>|A$IwtbL4^;Sc%Cd!B!|31p-lxwx`C|9B#NJnmJ7;FpCcEUEtHdKz@=!$OLYpUV0BiEg?v+shtmCq^ZQvk"
    "S{&r_Y^1(LqguH;MtO=6zB2!;cPmyj^N@PxC?!M#4tLOR`B75s3d*V+kry(60tSD1oQ}B6+d8bN;Yb~e%6lsK%ok)|j6{_Wavh1("
    "ZZi4+(ND*ZRN{al5`|B&RRSeUC(t%V{6ag!l4HSfmwITP<&5;!I2+|CuCbf3t&C!@q+71NP-G8;V&#w4`LaYeSqqgl>yN<?wnecg"
    "D%)Ub-Qa7w`=3187AV(1zcANKidP^h7n7#;<kw^&(D9B@z*GgJmfItqa-nWTyuAFdi=_u7d#s_}Mn2YU2zVxHm~MxIm1Fi3;NYLq"
    "Sz2UeW<C`*xLbB^t`oMGe>(fM1Nn4U>^k!OniW_@WBzCXUmR!FvOpIU+BKLJ032(=OtFL-R(x8>tnIM-VjdW^ZCf<sKa|$x>Dl3b"
    "Fv_?dNMW=AAUI)2XpZ;HZa;}ZQB6_d#%owWDdn0ymaf?$CS-=`;9H5k)aU<%9z`{)=?rF$heSA;!PoZ~Q#zR<e6e7}YfNMQ$P_c1"
    "<t64V2k4`~fh9d2vg|_(P9EOhXXBi5H^A4TJY^F%mFsyoZr<FqBIg#)>22tFB1*MxgPyuayFyRayPtqQN`ffxb1S;2d$c#`BDtHt"
    "7JQXl&asx?bSX;tajCtO>id?I{tCU(0Si86J&OW=kse99XjDL>`n@S<AVJ0pXeO!ag8Azouv}<ygOd3ulSMgiCajk|q$N=7lrn5p"
    "rQROpy}S1Vmp23q6&;SJSa@=Z^=>$E*n+6{)+DiV&;JsVxXOS3sVJfD^#25uu*Q3Dq}9X3ywUt|wwQLJnC3@cm*2=6AH&coCBjcB"
    "43}DOfga|i;-izt1`qW>m+x5z(+BI1Xwc}@*eC|fGu`>^H#rEASNw^^1aYwIwD<rxT&<Atnb*Qab?_27<@6PRv|}K0w@ZP7lp+M<"
    "=n;*8R3D%_VOHD%wiO~*Kl1A)f?Z%#eFt`_poML*t0Su6>5!`0LWNXk&@mR++8m>-okcdfds$}pxuEMOA9JAfto|MDPVxeo5G4}n"
    "Kqe!Kpk58^E+?i<(_hXk6`C*yz@%lyv<isAZpn3S28Teb#vtH>^qf)^(Klz8y8+cI2Q4xk$)tp&AWX5?4A71epGt}btAkzud$LdX"
    "yTm%EyeMRZ3+s89^j{&_)UyaGHG^uPGHV7MnLO2zeUe6z7LS#2<1U9k=Wq^A(sG>sjhV4;yMXxye|F(qd?8QOV?5f>k1f6`pNENm"
    "?NK04#Xj{-SLlaU<ClZOttncr8!cJ|JW17RoVE)etFVh!;-(@utP&)i86pmVHJ{C=Blc3H_>LXd`2q8AWq^jjJ^kPZq(J0h-vgpX"
    "zlQI6RuIvjKj+y3fd8VQu)>^$CqApLQs{H~6%8fC#PLw|eVAH^5~?GX72$D(jTQb`JI^CKy0o%69;X*gT}6nInBfesJwE2Q`2@>M"
    "b4B2JQEo#J^-zqhrM!*eXr2&36&8F2eO!m19ira~#O${s=76f_;clD6qlOYQz>{4Qjy<c6)Tt#xY&f=NTC`y|3)R>^Q8whalvWFQ"
    "0#*W@Eg03U9bw1;2JCv_4=);wzi)>gD>XSN-!1f$^64<vgDj9JiuqTVHhd3CksJMhb+JcNkQ9CAl_;yj^1*m({1jnF+cNCcaY;|b"
    "w{;}=hIm<{o5<uvHDb*8*NvbmoT&prB_bjRPA4CT5^=auPcmN=!x(ka+j+*AGslpCtPKyT3Kb$2A(%kNzC)ulP|XMRxhK)*kAaQ0"
    "8B8yj(V&C-^zT!wB|a8Okw7IOO#?4tSlXaM*^j%UyEK>jJB|maf_at38CJxgl4Jlc>XYFmHMT8LG5k{5acv~m6JnzZ|N5p>@<74?"
    "CSGo=3L9ZmEp}!zUMsx;ZSJ1bOJNWZlyQu)1Esj+_yZ@)!Ydi&13sHRWN6Bn5+;aLT7%g<NA1N6+wd0k-DNRJA8wWtO|@oQkrYM6"
    "zJZRC-)AuJ1Q^+bb9>s>&hQg#9pxj%k#WCn9+6rX*(Xp*mxcXeJ6%|hirN<AzAW<XsnAg0=WWq&f4&^UcIK1T>x~siIi@@Oj3xSV"
    "WAW06J*(lQpnf8lZIS{%z5{$5O*t(ar5HqmgAwGGg9>zym%A8$L5UofBT$a!z%mz<y)j?hQTzy?7uJH5pNm@(wqUp(W_-iT5ZNVk"
    "fxfeM`HXNCG<QlE2XnBkSL_N+kQ1cUb^hx=|Cj57xFHpj$>WcfZdiR33KNKw7%hQPo=~YtGcVzERC;(ut^m7CZ<*5CTVu0|Bivfl"
    "{IW>Hr;<H&6jA8>CY#Qtc!f`%7oXpM{`{=>OvF3b_v2@K&;G@FtCIGe@ryl6)xs|DKmYPC)`7EU{X#x87NGK+pAV0R=Wh;A-q@=B"
    "A4;q8<h1DcaKg{$7)pp2-WDMB^nq~bIr^canFduI;)wW^=n#&9b{n9mH~B5*i3G&@h=5yC5>o4V!k^;p3r0KP?$h(W=o7D~0WDRT"
    "QjlUN%aR*Y0!|=)&jVLX3RHQJMVILJt)>M}r%X>_GL)|q4VSRj*27)4z`>^MG(dgkC5y6%=x@=RK>8`*o9AxN@6%8;(GsoZ4;f{?"
    "1crMH;>0yBEDGt;K3~YuC{&g*se)jDUx^Y3Xfego2Pio3aL>Jv*Uiod*g;BtVmEyUrU9FdckY;z6~?F%HF8!_I@qG%s9o*4y9b2$"
    "hAb(!89zQ6Tn??l{{Fk;ckt)o=}EQwIBF30gcQzJG=KrfYrw96iRHK@7k8Ol-n77Ls_}BdnNrmwIJX7vKQ^TZAr|H^Y6DF&Q7AzI"
    "{kSpPpsn-)uNV*(qq}@E23kXiNB)hVRVOc4S_8Re$BjUrpciCZ=F;(Wp0KueVGWkIOQ3F4{+AF7lawM_K6gFz$dmCtIR1E<nV-Zq"
    "4MN?O=BtF~hf4z82e6CFw^RDm=Min+$5eP6;hBG=rLl3nIxXaUp%RPJwWIGyh`__*mTI#zS{5J*mvlRWc!Q58YCpAo_V%pGj}7yY"
    "O|X#oBR4ocJs6(DuJeZ6VY*s4uflYO5)E$GSe0-trovo>{Q$44$TPf=$vPPlDv>tq)E*AC3kwhhy`TF|bznpQ%yUNaAF*ND3;>h;"
    ";iTa6sx2xIBjx+5My0!6Np~dH^swkLjf`&?eQ*xXnO4wK*kA(QCDpmFNDLwzyWh}_Y>$G?D8cIR@^xwLaGGNl6zP(0f*0~E3cQd!"
    "7tw<9E|YH&y<^B@ezPW#Ly|bBF~uc}B#mbv;Q}<R{q!*_(3T{-pG@&cA&%up#;R>Crg{xv2_|ul1<k|%DSswlgebwL7}vM+;e|}*"
    "`=NlTisOrF+w%myt)UsAGXoqG8Y5>Kfy}dKQH&~LW>3qcJI>4WngZ2n2Fv^Fc{Z7(7RDOWW810<uuu~t-9Etk0U=$|H1e@rM)897"
    "NhYwDh6ssG((#?I4NBC079vq`iE&60kR=s@Ca<IFz=-n3h)xZ3>){aM9$tm}YG=^jv)-gLOL2R8adG(O<nZ<3{@~=&dNVk?;B!-*"
    "RrYJO%F&dkn0Uk@;Q+YE!GyF1s{p9tMaQ@&P9iZLy6pgdV_O)`L~l6w9hbs=Qa3694X;HgxEOhO9QL%h<=7P~tByky2_VYZp>a~B"
    "g$C7T!ID*v<1kh4xIG~4<zxOF@DUVeoG!*j(_0Nq@l27s1yM;{7NHri5j9hrNz1?e+nE}2@8AB-x|B#qEZQTU?=aLTjCw(1V?KBi"
    "7p*ywR-`R%PqJH-B8VsG5`#=@&54sSUfs6dN$eeoqy_asnSS4AC^6MX7E$QJ%vwJje8vQ8O4<F$%5QXm0lBbkolJ>hz~RJGi+I0;"
    "`O_&RiD6E*uuR|x3n2HI*q1ric9^8Mx16(lS<vRAsf>VIg;gSO&zppVj+XV@;a!F8|EsvA0x&%=Ws`^odMIr;;xb;s0Jvgb96W%2"
    "5G1`Q_Hi$enbJL*C@TunqQidu$al+l{mb_@%yzl6zRL$mV2b(}*(Dwt4Zlcy3;iCZeXuU3!qa=S#53BXNt4WiUifI>))-;R8x7z4"
    "NzeBqNdO6+hz01OCL}%~><THDMYreZLk@DY{0{btBv+y_0#dkDav%%yS<ul(Ph0#$3mi3W-K*t^z1x>Z1-DKZ-H=%I5U={Zh$U?S"
    "Eg3AyY%x-TxEyWA3uttN4Z{L>TghS{h&h3q$Q9A~=!xZecErHo?Dv4JMJBtEUEfYKO&Bz=YfnlCvUAy1684I`D5-<kx;n`1WLrRJ"
    "D6@+og!YBZh^$>ddNl4#il99;qbwcW39LsX6vIDv5Y;f6Udf<hnJo0Os(?r1c|YkTej+jXx$DSDFGyZP%QtB-1?A5WQ$A9p9D70%"
    "OLG_6iVzc&;K&FW+kNT3h?1SkPa*eQQe=%PW@R@2NShlX6lFRCUVY@zL&TCegp<#>_1sMeV&u<lq^PiVaDhq+#)(ToT?pMTP(Kp0"
    "jciwqMzn#B;&T{D+%#MRpEKkegaVT{)PQ8+8)hn@9q0&1%8r)Sf1YV=Sx*u1y`?1lkMs@+u2$P2wa6)RuCe-H&q6~2kl<XFyyKU+"
    "Z3jWhB@@PU7~i}(A6{G>{yb!gg?WpSc4F#iggIx9wswLSw*34W_T*!RJ~V9|OzIh}YxJ29V*-SUWlx}&Xx2vdY$eVQBArUbBBb05"
    "JEV*AAXAYS7~&5wzDFg=Qi5!jJ<2;a-{0q-a4AuOernvVheQl-LeXK7#&Y|1`~!VtW9UW?nLVNZy9=Rjh?{j32zpY*lovxXG+GiH"
    "zps&~HXFgtb2suNWs`;iP#dclB^<(c1kt)v5eQO#q)GRQs3ACnB=+t?ZPN(-m?(n*Zd0XX?WdRxU|Eu%DUvnQ)X~$?7<B@QZoL=k"
    "Hp|dmk~19}n{W?p8e#yHek)pSu{nU43{qez>@%;ci&iA)2xAo!`E`m!L##j&SC=P#D+Uvo90?QF;0T1^;Q^yBpA44vKrpA&Ik<m_"
    "QFz*sg%;BP>y{3OcJRVIbVAM1k#hGwB|Vc$vv7-_VWfk><>`6P+CM#ceRwcD*&ps%N2kA_B}o)JQWAcp8i@TT+Kz;QDbDpWN5h8D"
    "8bGcm*2}KCs1Ekv=%CdfwuKC@;v~!Sg?NO-gD{u@E=etsFMwDjK`T{?0$?U7C>GLsMwU|$`q0txZp!+#kmS*=Zhl{C@QL=U<0<T="
    "G+l#a4=kGBAH2K#wE-CF=<NLT=fjJ`)04rGaPs^p-1Sgt5@1Rv3>MabTeNXh#ApXAO<cl2@<(J5)D9VHPht?=9&dp7NTe%$UKnW}"
    "B@|I`(`6Ps&NB@*mmuCT4S@rb%@-xVAt_~?aSxSMNwWt@#?`|ijaP|~$XIpxQ(7$1bVuJP4)}m<eMZ@$;Fq-P^vI+mj6JB*<6Qx<"
    "K-hoRLze5wKm^{Bn$@V3hNEhM7t8Cvit;_uNuza%N{r#%A$!FF<Kwais&`A81szkSsdQkZiI6xY3C#}$Y9+LHl4(l)qnguc$CQwQ"
    "p1OOwmO)bjy`hu}uqOPn{$TCwpC4X=E`9XEUag_@>Vm!$IEd{Fp`9f$)(j+FMER>H<jR#=3JIqxRTU6`r3qP?JEgf$($F5cQJ115"
    "A9FTRZye;aFe2_4kUY0%9r%LroO*lKuPdmywWHY_2v8TDqPvxnIA<sX0_^4l)ZqS}5}u{v4obbXBiSDfD8*f(9+g<D*awQtqEZM="
    "Y}IN()Dmj1Qg|zyg+#d8_zJ^O+hu5*CO0{e4pW=K&4hFGnAWPP-%OJ5Afm!Qo$bPuK9KJ`?g5)j5<1BV$acj0u9suX88n^}ohMuX"
    "(L~ohkT%i`)f&|;1{KtzPw}V$H(E@pn+(O2b1^YI=*9*DOoNdGDzMQ@q%^Ef5e_uu_~XNq({lpnsS?UdTq{fFY~o;khDTf13AhKc"
    "0?C|q9q1GxI%%<lLb4apiTWhg$!)-n@fKGrOGdIA?;b|Bb_kS0Dp9vCnD598RMjZvB*)V#Bf_v(B917GBE=5bT^%rh43qdOVHXt?"
    "yoE4h03x`SkcjuFMrAtw2y`|@6U`*Q&xtlH%LayDkRR)Ef+o|2wVd&77$zN*n3N+dDdFCZv_`;dRzW!>6&^^wQoy8C*PLDJg=C_4"
    "Y?!2F%aVOU0u;l=wB0xkFc+*nl2dKYc`7qQVmiA@c~hCPGNjPh18dd42o#pGr*4d17G#R%VP%FqGv}6KK3E|wUtsTah)_<}A?@iz"
    "B_Uw5;yo=Ireg!|pq*gcx}qU8NrtT7b9_$#zDL0`6Jbe~^%qMr#}L5%%BP)NE2*g9pH6;K#)zJW`S}EeQUx5T8O31>O{95i@;nKB"
    "+d6I(gyqVw2w6b$Z1?(c7ym^i6Igx?N)kf-J?pI@aYzn`z(u*Ei{w@X1=WR@>O*2;2%1?O27+-GFZQsti&mJ>W$zIsay{<@)&`sm"
    "XsYY`e5V$KPS10KDw7`o7_>|x%`it1-SXV)_4}bTt+q28DJ7zh(Nq^xE=@5-nS^^vs?{yniVIh~dFSono3{j{w}vHbwQY;5Z_d|Q"
    "VI`|o5_URcom_}a;|z3{D$W7FU@<^iPUUj=wr^40<I_#~n5zR>JEs7rQ#eDX{)<WtBs?$$Q{a=hInxD8y3p@bu$i6HKCr=e!gs2E"
    "nIPvcGcnS!=KFlS7ZzIqqL0wBl+%SWZ}57|^|tNC@$lgA-7!<qhAv9h8627vne_G+1$R=7AG1Yeg;ruJqMKj4RxxBTh8rw=Ak7=&"
    "`E&-11!?zPj{0SFl}{$HRG5EBwLr8YtFU%E0;<;?GA;oVl*kO_Qoy6Z&_UbVjGd=-8y|JhTZ=)wsBDhmfv~cj(~#HBXX!70`HRfw"
    "C8F{RbV`vvDDVrN73$6j@EA5-k{b90%dOw3!P6k!(+p+!;JW@`WONfKvjqGAaY&gC;3o(rs4M?gu%5VwfG#k>Rw0!bdUWbqQXiq8"
    "o<1>p;%g(q&%pc{TEu1O?@0SQHk&2dtG@PXAt)8i<<hl~%Fv&l#VAfcd{puY_`em;KKGt2@_WGS$KCr3@Ho$QAF}lB+1@{@c(7e&"
    "{PthV|ChZtOO7K+5(Tf~l9Tx!C<R3NzA&GRNDvDXRm9Q&$gJ!t3fdXr0K6E8hzbvoM3r!)Ki&=AoZuZ`4lzgRlZ-BA=4R&Rv2e>A"
    "k!oqFB*NXzRMpf})zoyEO}~5k9adHV%lN*$7NtJ1f*b}t$-3(Hhnz+RqCk{om^|Fld#;H)<>av}0Y#==w+T`F9fu*$L`itP*(0|j"
    "^Nlj$*ZgZ5s!AoIS}2A%pT9W!^-yG<!*;)(JNo!h^q>XF2}5o{GTZ9_6Xi}|{B410+l;!vc~O`57A)v@(cnm3pZ#&x+^zmB;$nm{"
    "VC@p*-4Px|YB<x#$TbnQw$GJv|54AcM*u7b#K(cm-!4B~12Q1Pt{YLf8?hQ*TpS-BT>tUx`1I-pH^yxqK`#TrMp|n<IzcfL%^%)?"
    "<$YI;ujP+KOpG1mIeiWT_eBp%(N>^oOWS~YnLTg`#z#ySeow!GozgJQfBo)P%!cJt8%VqqgU4_2pdi9MSRFsk9zcvwQMbZ`c$Rzf"
    "xJ$p5=s`yfv8dVjm)l|jFU&xoa%d%m_|7Q9uxV5Q3l0Ss*UfBk3oQ1Jk`E?_(>r_wpFARP?VG|j=Oo9fTynJn3RSLd>yf&o0%`m("
    "Mca=DxX0Gkco8#Oid!L$x|_@i1xmOe+j=&k+d}+iTs2rfm)vt4iaD=k!$91v{Fh)9N00$8uUIv1R5+_azh9%*czRt=ugm$IBOucs"
    "F=>r>RvQ%q8;n7ys!iV@LHJ|n7(@#rG{;&6Q2rxk-`Yc&mvU_|I2wV**a4N_>;*J&j()6M8x#(s{KLk`RK%%o;EV}CTezGz_&b)~"
    "70ZQT$|4e$D%QanU^XF!mHrsALC7>4o?o=nUc+E>*ns7db|1m54R!)HKsiy4Hrya|pjXkNvRXO~uQDc@z6nA?U^$y#qdP@1+fwxe"
    "!9w74P-qbtl?x%o+Gt;V?R%>EN5?!Y9FzY*Z}Rbs*p#lL$!l|Gl0-QZh@;8Jk3-zb&d=4&%}i)P41RvN*ZRL+m!df4(*VmiDlECE"
    "Oe?|gH?p^+y26}hST!Vv5{3rq!!hqhrnHSQKK(xASY6!2?VE%rCS~!Jomwznr}Zex&1~Zr=dxk)dIbGV5i}kDP9%d9#816wV5cI?"
    "z&gcz#!Yc)>yCdCGE`|=l=8iQQ^RrDU|;p`)%@#NU>8YVcOas&bLhdhas!Fq;b1i;SBl0F_jr%7KsOAWq>F&|3DEIvRn6T@vQ*qb"
    "G2a6rz&;T%2L{paAA|MlK>Ju>aW%VDKH5i(N0m_{td4v9AG+P*uugU)my?+j%1>qzV%skb+-up+U2E>sT&jv}fBC1?mHXoG>i7aq"
    "esE5rM&F`R^k2VwhR1GU@{>#wMz{AK%ht6~<aGHJ=i+Xt@zRjqPJKx#wWU+u&&KqxhWmWDG$(&PqmZ@f%4qJ+1aab+VgKyKi^J!K"
    ")&v~(S$V3{5qs0xfcKs6W0u_L<D=jRd0EQuJaMAeo&Nmg#s1I3OP;@Zc%u=1_~QET@(NCn*TzdNkl0uSDc!ns*u{g8e4h%Jp1OS8"
    "gc!ZhygK~(c>l#Vki4tzYAo+Yz_hfY*nDaA+`-ZGx!^_Qys?&JlVJe@Ke+P!r}Y0=C->jE7*sEVwDpFln26*Fks-Ud*K&B`obq%#"
    ";}el|IC88bv>pzFFba<I4m~!btOaaVP_EQkU?YDsqOAq?jtUZP%8?edeNc3u&8ei+T4?nhs(_VOo9b+BuWz^+5OMGYfKVrO8;E2>"
    "AaeKm?yeTbw!Z@ojC#Wr*DUd8%p!!nJ<DruOCy~j|HPb33T(1_W9&-@45hA(_;z=ya{E*w-SG7E<?+?8*T<*(XD3W?c3|RxN(xcB"
    "+GPc+ygjdFt{zSu`boq|hx}J&_0MoXqpHhlz+4Vr3@?7Y9-bat|1x}jcxi$|_1-rGCrov4;@kq~^I=K4uqc<@R<K+?EZ)`cKyE*)"
    "rqxYNAs)I*tp(_8{}^P#<>CIz3tX|wmlv;&U!7fCKRY}<JUYIz04#za<~D&FkSohpt)3k;f?8%15KV~kB+udjIRQ7}r(|1*bdTtU"
    "5EW7352zFH2Fqx1ct%>aYMbsD+wV|D7&j(7FOFXwpFY1n{PX$Y>7~t7S;#y^*KzbqN*zM<fzL&MI<h@}K5GLa%z1u>%?x`Qcw~6G"
    "4;lnS47$Ee7UA}5?QB7u4Dx8jd~<Bju~<HG5WSUPesOkwcmaHQHT<)USd>_Jg+(w(nSyP{HA{eL*M8!lOaH!BGw#cjI{htlu2PV)"
    "awY>j!)GrJg%4CV+fo~tfxOl)&#%eG#05!uUy<Hz>m3<YdM(=dJ?)iOCYh;$+@7(kI{1oruG&a~evGdV4v!8mE`$rcMLS8>V;yAv"
    "dbESUUx|0RLR6cmKeI3F-PpTd+jP0(4OTlyHo-gbzr=cDyv81fZfvsV_~MGiKDs!x5e_#%crCJDhOsedWzP`LUxl@^4KNPFO_n%b"
    "y~Ozn&ELDqo1p&*tDJn>Rn`zi*-haL*IW+4mfwG@-d7Xbs5-m)`S8Lx&W8TR)YMgxt$U77&{+Ffny_;8DA|1YqnYq#wF+iv!7AFz"
    "ZZOzY)lACOqeUx0dre+ccGuPp^PbL*`}-Ch4lgb-TK#$-w#V_+HB4#ml0a~;Y!!OFkWCAzbBR#V*CO78!Q2ex_FU8~AE@pVCS+UY"
    "*wxDeIO<%#I2)c`A06VI{fq0DV5U5~JU%%7_s*V{(zXjN8;D(S!}JrlNySOI+3Mu%;_CVExxM)$Z#jTV-LUyvv5$j(!<ScQL_C{L"
    "{h-8dI>l>vPqQmc&TE%hOG@amLSLMLt$THNadLgYy{`HU|54lV9H-_~k6n-bXGRRYIB7e;;f!ZDAiw;4_TupR#qrVMreKhLW7*zx"
    "7yfxz8;6Te$C@DdG=%#g;7(&J_Q;Bp#@R2YAbHyJ##h36zg&Qp4ErFF&b@B~M(`Ve@mjl1FgB&`Bhq29yi3XqXqGF6kZ}|oQEIs("
    "+S8*S<i#MxRx5aCe2ou;gM+T9+aK)1`-+)#D@mIvjKV>%!9>|dOOCo+(@tl$eJ^sepepL4N980NzF12_$7~7-HLi{Ud4_Zh;@rld"
    ">w1;&A0E7PA%Gq4ed)PqM<%~ZH63eng=^61Os$Xs$o+_2IVM7py(DqihfwRr{WOH)po37dAwp{E7NIE0vq9lt=D<cMu@Q24@|SDf"
    "_}!Z-d%?PFcy@YteRV8MToHJFEpLI?8%)OKb-C1kPO~KPlR;PrjK%ODwL#d@c&cAnC9xmI@gR)cW<};U7Lx)#NoC`4G9N##Srv<Z"
    "bjhqnG~@tS^J&1wmBn_xwMvn{a*Zs}-TJAbEFF-aZ_W6&NVCUxILcZ{0Lua9>*r5mME+Z(3V>4wdA<>)`uSPEMq94DL+jjhTHGAw"
    "Uy7UKEQ|d?qVsZ?ui@n=4~lRQZ^Ox1lA4U1Y{AF!Iu=Wn%1Wu;O=WXJn8L0MyILXNoDt+qx24Sie(Dd3FEX~7TxbhUkehz=Mdn$-"
    "&siD`@?`xiVZL^jUhz^Saqh4(K4lK9>$I$<U2*~Q4&q=VYQ5&WzPHum^?kKm)FTl?a#N0$jnVS%pMrmzea>*?pB|>Qh{2<0;=ss#"
    "0Rj3S**h^&#aK^PR7XLVD<*tkN{*;BiDB<nTtdJt>_G6<GmbP~&c;|$U384IGA~30Z8CU8^bYNmW}u=+j~=FD^DhDA4o5{|oC|h5"
    "`9l!mf4IW0$Rrw0$A_}Giz@!L51&^bmgbnp)037&ZEWc(F!qJjeu&s}ShBSQuQ{CPYWA#xNpCP$@t2x<&;y=!9jxgCwGRW@%f+I#"
    "M}lE7FFk6bjRNDU0V*R5j|!!cC5A!H7*0)*UHC3mlT%S69JQ>tL>859S)^>R$O&U(aEfW>K2_186v#>iz?Y(~q`uE2p9n)(;}ZQ<"
    "qgnuEZ0SKp4wiv$7bV^mojoiuu)6un>w&h#y&X|&Vftv$>xuMpw4A-KcGC)?5J#i$LnMHeTK3aeMu)bf8e02i2Yd3gDQi@gMdrFu"
    "7`n)YdSZ|)Nc`L;nv6>(fH-uZkK1TY&Z5J>G;gQ+AoA_IQ*zB$t`p}hb)pKC62B?*1jmxk83}nxne9S2l^;;N`Uwa>az<hEo~L;b"
    "<VMWhDXuf;#x3teR&pChE|Rd;a_yE2M7N9_?)tPl8!wPcZs|gfzV^BcvVm+X$A5dkesLGAFgU5FKc18yhWF}@YZHM6H2o3ie5j9p"
    "MS#I)R8=1Z39d?`)|vhq;J^6IH9|{4e!;{MOOD?UF;`Cg{AITg-vg^;yya}J`m5Q?wNle4`IClWNPK83s@1zl;Ypo)C4UnMx|C_z"
    "K95bd&k~F659MaGfW|yl6xg(7ztwio_|UN%cJlxF&;PZ$j@pwixjO_?Yd{(N{RKA1@sy?hD#gF(nf?X#A8H1oh9ypb|K)wFfoyHJ"
    "%EVx`nP5v(bHf>o_*AzIh;szbuy&^Qf>^Vrl6kB~W~<0x?Xciw`6$YEw{_=!g4dL!u9=^NyV6kt!<>k@;j0MocJ40Ya?bM#nc%OK"
    "37Z(HA5asX0bPbdq@UpS-|c-}SS_@WCl+s>gVwoR-fnKq(&WfDx*o9xb?bpoHg~1wGUhlWKqx;!%_aHQ);p%*#b2)34_#G58^W->"
    "Y4TIcaQ@QAA=wX>cM{f|p)e$}npW`{=C=)E=P7Ahi{Ye$w2R{05q|M7kz-!nVFN)rLsCA!s!h-B2&k~=-yddey@N)SsG4IJ$bX|J"
    "TrLI(1v~V<Dyg6?<*$(lp`(nH5sQi|c$G9IRgDxi5I92udn;iSKRu<kh}?yP-~-u0c`RsYz9BG(A80PDBK58<rBKOYQ#3fhg=6vf"
    "f08*b$N^YU16vtCE@b}&QnBx`(r|+{tLCB>AeLdAV7r^<;a=cUi=G<?Gq!!l<6UgGy2Lh$DCe+H1d;UpOduf6Ujq3CC%NMu5syTf"
    "r2vspVX~K^g^du{!k{svAAj`AqHbR=8&Mt^B^}kd*-_=#qT<P}K!ND*9bcaDS3CHSBeI{EgK}07Ahi&qm$J_S24L+Z$q&Yu)XDT7"
    "cF2xDND?{Nkno1Z_z%g~{~;;`y{$0e9i1Am4AfVT@TCK!s<DA(t;C|!`A94n7r!X6&biDSrp3mBIa5m5ZK}!>HFlR&iBQZ@PdRs&"
    "8L*ztAMil)cg54RO2o+AdJP#DOGdyf1MdjO5G+cibqINS3HgFzL1p@iaMW=5ljoEIr)%fanV~evxrTYTY#hlt=IYo!@Q#TUs6x|%"
    "vyIpiRz-5{Y9VbsS8gfHZNu;*?kS;4x?-KSwc5Cv-eMyYSrztaJE%DyNjdV#7`-QUQ4MoN5lY`NRJ*Oot<o_@nY1_6BNhf4JuIl<"
    "j#e$rl(GR{6y$@{l(NVXYDc$S`glI!<Xvx!0iwgn<hhdUGNExeoj&km<0K4!pH~ZfUAS*P!{||`n>I~KHH_{dBi`ISRgBWE6&~Yf"
    "6S}6jU5Lv)Nj>Sn*GLx&w!vycJj!ZPm5LY&dA?)#w%Fq}-|q!`ay4}yba(<Z(`VYk#?s5Owi@=<R^hu<4PDBrBNfsjj2&7dJpAE>"
    "sJ9cVazsylGWWVx1vJWKP2wOF6r|kpsmL)lZ5`ALXE*yI;Sa4{xy-cJaF&PrDLH$8Wf3+*g--3RcNVh;I<cbPj}M?*45yy3e{kpf"
    "Cp>7`60Z@?G0j-U*c(-pU{L9!>w{k@8SNhQ^+pm$vCFQhRl1w%i?I*yoiE5falq^oZ^%Azpx7t*7yEoA_TdZ`uwc1xDpxA$I`Fz&"
    "WtjvP6CL7^sty(nDs}h`8OprmJKSs!-!uK)aq1U*F{&|^w9FM7i0ZIy7O><Y#dV9C?h_SDeu~y|D*j$)OJ#BccI6>cl$8)wK&w;}"
    "-fyD~uN?Z1OdnN^+R%okDOLC#b-1P3q%+(qd&%{{X*F9Ume#W3x3+BDn;IL`oG+@Iin>?qF_&mtsQHN)vRxrGqC4x|U9Ha+vzK6l"
    "Qin0gyYT5cVH<{ty%q?#*_%UjZd!`^1wSDa^}<{*0Fp?CzJrNa7gL;aME?-4Mpc0zQ%VVErvB6F8w++Q5^W7(dVvim(S^}|E&U$y"
    "HBmsx@o^)+5`GRX3X+PfiK^7yBiN<vGNYO-E(9D@Nfi%)SY8liy(mZwhy6MBYsJm3={VJ-MxN5%-|0(VHg6lPX7^X%BvJBOyQ@>R"
    "xY>um8Lp~8GP$mHxpA1@aL3f^VV;D8+>*eu9S>K{0hpqoHH{Z$1ZuyO<w4G6oyr3svk(CiaO5p(y^d9daPHnieYM(}n6Q4LwlX>7"
    "T3CLPybjw!I0LZY(QH2OSlp9zJSG~QielVcsZ;5;vDR5cHA{Ia$7Sz9z5KQ-OYNM*H7;qm9$2kw<UEf2i1S@Paak<~rFsZE{S4&|"
    "%gb8P6Ggx;?PePE5q*cKz5)%dq@sFJ@yDB3Dq9l$x!vx{>YBCF>6FD;^;86UE=o^YWX}RW!Nl56BKuF`N1^Xa_y?znD`ST)UK;No"
    ")nbN`>arrh<sDG&?55pJicZ3l_n8{(u3S{|CiZa+tLl<SbR5{x8jIonl}<Tot7SROi|7a2Xa2RA_EppJC9vy6uxX?JUV&D7u^jEI"
    "Fg2mDZ1%jspEnvqMEfk!bAL3My+@PsSB?cUElui*N!4_@6S0UR;ae}!yi#ObQU)J&O^c~{Sfg1+LgxQuen|cH>ZPcxkGF;Faczt1"
    "OK&&!bz@w-kkT%(lix!lfor@l&in{$_ykpA7#68N$daeRX^LGxkVl9s<d{^NxY6hR3L+IdPqYPzX)bjxP-%H7Lu=j9$Wb>qM>sVc"
    "e9>AJz!_D$#;w7$U(QP|FiITZ9?4*deP#f<!r{VRbZtck548vJeh}N`av&8R6lU)S-bJ6qqi;uEPJA*o%mr0m9>k+y8P((s%%rw1"
    "77}^jA>{ncNVPR!fACH9UL5R1@$y9_J>68$9aT0xl?Ik{jkhgF%DK&1HA%!9u>X}EL<PY49vI(5L%$~9ds9BPJcCV^Fq4d$NMHxY"
    "uV%Lmg#Z(xlZsgz1UB@Jl`@;=*&xk6Nh0pD%%JM2^i+1w<#O6mk8CV9HO3iGe|mZcP6MRrHQm3)TVdGhYz{IZUQ{>B;Sy_J9Zttz"
    "I=D!$&8oLCn82j+TdRMKxfD?rz!`av7nT={zftcyj#me=BD=WHAM%-N30R)poXZbKLL&6PM6@zR%TT41nE|8db;4%l?U_Z~Wy-6|"
    "df8s&#y@~;1|y@MlBQXxi^nf(N4WL@T`4xwz*yhx)4pRL_}{=@&>7z#e?42n>V0|u4zVAVH6b`%)GZY8-jlMv7tRo`O&k<;oViji"
    "=a`E-vi&x>kPCsU=n(CRDDL^O{p{fUfG5Ob){C-Po|kQHZoV@v+@-D9O4YLwsgkKoqd1-#k9^W`w+C0pjt6(M_a_gdJL}0`zk9(U"
    "&A?5G=6~uAL*ZHU#s3J99}qtgpMQRFEb>eE@8*0_b1q1bX-V+U7qg~OCk^R-8PC8Bd;A#~YB+s-B@<*MnsUSw9zqbVQ3=<suU~M&"
    "iZuejbcFuVD_J9$ll09u;21KSj;&WHQw5jqYNnr)7R;LTMj+n6o(Bg@Mm~rFyfVEtv6fXe79`bMM&NoroHgHQXoj&-!wAb%>rV?#"
    "&&O@_GdC(dY%3@we49Xi9znpfH<S97{5_OR78M*zIc|qNl&9bm2@PFLBq4FM=!Pn`r9}px&SYC4eAfXvEW$)5Mf<)a#0p&bu!gu)"
    "<0*wd$xYX?gP4-teeYQ*;2Y0W?tc;WQM@JiI+7atmiLW8sxYLD(L*Z!a;P#Iv1)@67t67ZrU-k5wkS%WJrSihc1p78;_T+ITudq5"
    "<Z0*_RYk}13GSe7K$poX{V!xmd&XT`fI{+;in3G)1Z`!9PI^GZ`?!twdsa3T#rkQH#hs)Canq|3(nu6k&1g~2RrO{^_OOww#Kpj<"
    "D4A?60{R7KucyjGPG!wUs=mJ?cZOcYgc)iwQQzKy(Srom*Pg4O^T|X;m66s{(WaXh5VbR_H$YpUeB{i*7ME7ea7!(a(~28DQpgt^"
    "itT=wo77c<_fuHztm^TE(kK)Y<pSHuvb>tv!I*uc-M0f#%%)izO=Mx5Zd5tzYIWf(JO;NiBo~}TjB7xuR$MIK%6M!&+MUCp-EpmE"
    "GRTVYWVF01Pom9{(1vp-RJ4mCl1_S-r3KKvn^s2cx+MU=T2H%}rJ*m@L4>pR2hKhX;y4#_XQRMjZ6j<KF#43O2jhNPT&94n4{}v#"
    "(YH0dEtFJc2<T>xjwbb2`&}V**TZ65O%3_nE4#@orAk$-1$cVI;+XqT(sc!n(4fpxFA2yfTCjbSc?rY{h_1<F`#Tb<0kwFy1pR1^"
    "?Q4%-nxn-naQk*46;fsUp8z-&%l|fz3;6c!sy7|1{#5ab&?sIlhcTC?b;>LKX^ygQA5yIOSInYQQky5VDBU{~J-y&_9jcaB;;`5S"
    "l4&R=@CQW{McM>?Ls;|Mg9PNP(T`vBI&5E^_KB}dPy5Ass=b&cj`wEHAwz$~tHz+J427}v<qOZtIp5}vl$k14UjAY*yzwLbbSaf8"
    "*@xD$=?`NHIiQ2^2$sKI?w5-(H@m@EyM@f|%I3hZm`5Wpe`hy0dXen@6YITkP*e5J+Ef3*MwO#o$6L3ChXvXfvz^Ws_Y?(~CjKCc"
    "SsQkrf=(Uyxt!!`wr?UBgssWc9R8i|*N#P*1Gdt4m9GYQ^Jae^`O`ezV$HHN`>01TU&@PNq&t~8&xhw`c&($K!Dc1L-&ZJ>Xx=1E"
    "QHG&H88Rn|floiT`uMH^c9H}E*a&j;p<P}^5chJ)9o&L|?*N3&)S60u`(sNXW*PRUx4(vI?hm3&dq$B_t`}}Qp%6njzEfU^4moC^"
    "V1v&6a$aKt4{nLo;*zI>G})r+y0#8+6q)M~^{vCU1=y{1$fF_{`0=Le5P$wU1Vxw+^0<E;+80)?Lks!3b%?`3p72?XCxMNIZK1?g"
    "i?kumtHllObb-~t&!_+mQS73FN*fv{e051!$Wwwzn-$SA%9mwKV$r0Xi7)NN6KV!>HPfb*$64jsQj;Eu*e?+@C*<?G7@(HmQqr`S"
    "+UG3BRPp;x%RSHrmt=mn^Ud{dxF(9rkHG;%02z%5a+J+b!wr%rSzx?2l%-FjRws9ci2Tko-B;E3rSj?p?1EYKO30$r41zKQIGhnc"
    "lTVJ@C_%}HV#67#D-5*j$1a1W{aeYGm3a6rXSi&~9V$n(eo;ihAjUn>Q}jd@X*%$Wm4h8miBXyZnMy)q3kyNl#gbFIz=UZM6fp?b"
    "VhvQ?xzZTG%m&n&Y4bU|<AAJ4k|gBCGp`0Tuci4wIIDx8d#fzA4$9s<Q=3=AM7|Nh=3=}%ubfTW8>Bdl^Kd}kKkJf-w`rs7U;xMu"
    "<^I-2J9t>22Uce<V}beJ4GkoDyG4F)Nz7llj94DUNbb=6Md&9!ylBG|`avFL$)E^VqS^gSU9hf0#{N`s#m6q3nrF4WE~|wU+HK`b"
    "Fo?vd!|>6lQ&o=_mhsa(oS;#&EOyX~Hn@!JmB9s<^0JR=o1Q#Omi3%OCWGUOztZ?qL<+RFpk5(qh>7A;;RuyPrO2o>$Ne{;-j(j?"
    "uC}<M9hqehmBL8kCf06hVnV}hP@JO#NtzTvI7oB(tG&QcoEF$sDQSxh3NE@5gG5>67tx?doiEtq!6q*JSX|n4x>Y=NG`(m<=$QdI"
    "DC-o#3d26YVJAeH9}fJm5AXoCWSnwAwDo`koss|u^|5clB=SQb1uw31!Xz!QmK$jy?1yoDc1rzL4i1lwPY(~;#wG?C&N<4?`_UU$"
    "HyAQ5L*fjA_<dmcebD$Dp{<oOT)C_==<lPv0%E4VoINb~YFS6=ObdSV8u^NbO&Enq#9VoKb+-SfYvAj1n?07;(U#iPPaCb?>9-&V"
    ")pdvMc7$EE`*Hhr0LdN!E<zn(LcoI3SAPpy9S$#$xt+3!9b7JIX&m6*-eCw^DJ}W{%o2YPgd0H_fke*9=)O2Sy#jgU1oeXKq;I~k"
    "7iYf?UtDotrek|$FJ_PB1VsCP^YGEP0_pPQ`T5z!)%DfI@bvNs`x}`163j|avH%nq%G2gXw59wepgli(b$D@#^`Co$>2q}OO(|se"
    "n@iEp<Kt&9FF{FMUS6LMFE5W@9lE*n8Qz{_#K^pCn)+S!&G}WeMS5}kZ!eDzsJ`*_;VY`hZK^d{GL|E~RDaFs?@F(=vY|)k2XT=F"
    "ZROOi&d>a~zz~#8)o7d`JCGU`m+5XJv%PB9rDh1{hP+7F#+aypYvaooSNmQY%q>5S!vao7A)is4$fEI*WLyH>ZBRv+aWNpD!FpW7"
    "I7)(e5C<Rmf}5jSUbtaaQ7@hw`XEnWxH#mR*6y{+f++TLcCWeDs>p*ZALN@YmCP>bWsVe1RWY3UqW;YtrRa4^Hq%pKkYr&z$ik1>"
    "+71`hp-dxbeL#Id_;hZ~3aTWpS!s@!d_Qm<Qk=ulA$60uf4X2I*6f|!dfoTQHM1HFdx|g*K7KS3keQpD@i}-QbFMd-6j!|zfS?@o"
    "?dBn;Ja@ZQZsWEI5V?xE|16EnZkM>d7&^5YUK;m(!V#ToKb=~QKR8H;iVn3I+v4h3T>I6{+ZLg}ezy}p@t!Yc??taAeu>F9q?e5w"
    "OnLEV4-!4`PG;k3AtPGli}paFimk*;dv*%FsOe^Ab-TOOZSG_{36l<5!BAh1==ge}NUcZmpjwtSm#O^=T8CIKOSos@J&tMd1c3O1"
    "@PK;iMh{KnzpDnNKOeq0+s8oKzjPWu312J!uW-uxuU|_Vw@IgX&GoLX-nZ3~Wu%23Ha4l>nW1?i(!~+%7e^v!Wy@%?yp04j!}HAO"
    "yq*}MZ9+uUaZ~yq_qCQ^a&d+lBmF#^jD<zIFAD4EUBbi)xMPS~)+2_aH#>aXzJ&MIuV3$4A=T|oKsgs$uF`%oFC5!1`H}G2uPV@}"
    "igET-XY9r-aiom-l874X8$-q^iC0`B<SW9fo;^C3v<<mx=anI8{fuD5R&Dbk1xIz_HoLX|+$F~;c)03T12n^;^ym7uzw@qq>(C|b"
    "n{Db6I-;cxoq+a_(1rga_wgH!-<5RlKK^1mlEmo;*EV%FTWtT$-48>oaU@^2n~rK*Ix}DH=~&tRyXR#$DDvgkJ<(>9>b4v`iXut6"
    "x^gngUD>?QKcE;YBbY&!TLRerRC66ShN!Kuf`1-Ur9(V<iIfaPM#LS+3u+8(5KqKSc>5#{;7M!k98~vMRAYXps`vlPnEE2dlru=_"
    "S=lH$BS#qT$Yz%^tloY;v)?eLU=g}+bO`l(UTQ~@J>-5bK~;T#C`F~R0u(4GM!2stT5Tkw$=oky_UiW!siM_JZHSutRgPApLyb(4"
    "vIGd_*nxpIYg93bYWWM0gqjl<i539yLQAcq1YmigrVXJ5Iia}5CtSLdHVggpm9lN68A~$4w1fj`y>d_hy`hqbcEjC-T8zfI6r}7u"
    "FU5SpE=N3u>RWMg-i>!-?oJw|xst1rG#cSnW|6_Bcqu+PpMiXR)WcD&v4;Hu`QyLj-`AFZ#1M+(FM+up6j|}nX>ZS5daQB-h&d12"
    "V_My`F~Tyoo0wTGcjT)!k>*UQeXcpfE3Jjp`q7Dp9fP;+bU$l!bt)dYCEpOsWS5gizMTJOm+QrW#Fv7~ey)VH(@c?X_lh-{iuqAy"
    "@ST)Xc+yrhYLDCY->agHJ~^Jq3LL%Y&c?^@kE&)K9&e>ld#a2qS}ye2YiE5KqUtHG7x`(bu8;W|RxEP(1I*UFC+#27J>aLiZ1yJN"
    "fU0*+-lq^_EHZ<<%OS<o2^ph+!;HUJ(b)LX{DIpQb8}*BM4X~`mF2YA&{y!S`cA?cC%c$mhHeHjBPmDI@M4(Rf$mJe{w!QflU>%1"
    "Y+HSq55%N)gm4tcTE>InBiumzc4ci}jQ4f{+}lQKk47i%kna|hXPqGPt-`xUE5o}-pAz0Zl3!Wz-69waI8{$?R*3bdIDbYK^GBy|"
    "?4O)5`>Hv6&pyO6k*sQE;HtFS4fAVTms=;nc4dC8{7#?VkxxyX*YtN>8P!qv(I{$%2Y>XX3QLnK7K+k6W(64|bXG;~iELWqVK;kL"
    "&)^=4>`gm+7X^Y$-~NQ8Zur(glPKj!S9kToqC~<^Ttteab(!-kQ^Ge$`rcSZNq0N05!yzY0##vX^aniYv~lc)U^rj91R1g5V(sra"
    "kQd(k+pJc+tgaw4<DBHO2V2wb_3vg7?Y?ydv945mQ|IHO3XR%{tQB=7TB1ncqBKmiL6K`PYCkC`EdZ_7u1ClFLo5qujLhCxg*Zr@"
    "#K1d<X?tp;7UcUh<EgOsK@aFblBVGx%=9bQ_NRW(^|eXDAOK;IXk%nyhCM;I2ey@beQWW8t~os8MHiQ3p~WQXhu$Sn2NBbBbB!MB"
    "BZuawVK3(*2(b-Q=WBEIw6c~?dI;y|)uIHg526MmE46Q&8z`~&Pu$%;fjk~fd(*VnP88S^*^?xlN$B2X-MCq@a#(!ay9TlSu><)i"
    "N^H1<X7<)I=!tH~JINngR0-pCoT-9pT0!L+IkHfbfA^02Gs=Wxqb06$9kawFnfSX;A{f|;$|5bc@`qliP$_!n`WAE&8cbX|cx<p+"
    "bCWLe?_LPB^VIs$(a~m5JzX=pe%jh#_#iZg7k_U;e5xN~3gIN&R+xuT#6=K|fucN&GjpUkOmi|Zu|1n<T*~419OG+trUoackLkNQ"
    "i-P>4s4z($P|GGNrRUR#k{3Vfkq9Tl<I`1a)f>SuygGb-cJb?{e0zL)aQy1{fJ%R?l9p@5rEgo@wmj_o%x|Ay9ZjylW8_PqQ=?6d"
    "?8InvSZlVRTfL{jCqYhMNaspN{mR01pGy8KZb7?}^3D(4aRF)w42wNFdvSc$FJaaYAnsW?Q$u!t-(u|?IP@#QO~5r*2WY#8`+9rg"
    "_FSTFLEVnQqJGfCn1i}5%5F(jVO}Bh!lUoPOZU5PgV&m62z$8Zi{sVHCmRqxbo0tsWG8ITFV5TlEvVW#9%lYV+!BU8dok|Wi@BA0"
    "<|43Wm)rc~2wT_!%Vdphog_UHC+op7=)p4G8p~d5q_dA5D?@PiYMoHuJ%PQ@MdCQeB<nR#U&@hF^SHo@tjPA>gERbjjfHZ?TsTNi"
    "CGUYvr1@<LQ2g}(YEQ{KWbRNb<dZGoOTHd_GF4(rh|;eIksU<3g+<f3_uR&yj5=mn<ZzVrZ?<gvv202tUFD$Pb#7zZsjJhiNYH`W"
    "Uw7747r@)h!$AwWqRf-c39Wk$6MLk@F_KN@pi5>m;$kaO|FL>sO%{*a6Tv2SxDB@z+m6)Tb-jMKyhGHm>l+DEm#Rpm8(E9H`KNmt"
    "6^_$78X~`E8op}gEcLpRNc%#6vc=KWxCY+t<f>mMZ*^+TZD(S>#i9pWkJRf)*%sp!*Wp{A+B=sKo8ljCJ(5$`ts}sfwplFiWVL9>"
    "@%$;vU_}&cMf%P?&^GcW-g=}yZ^b7NKlx(B*Nh8~gDO7V!Z3qSwpogfb+DD8k#0SbL)EQ8ew~4{^(yo!8yUUQo=PGI0w102<wT96"
    "wmYM&_-K~<NkgNSqxI15lsk4LV|=kPSMp-~qvNdkPgUM)Xv7FCf4&?_D)&8?Q3k#5bW3;1Qcf*JsHoG><vm$9<l5<luTcX*itF2Q"
    "zFE~K9p;TkH|kXxUxDFzsI_kIlvuN-=t4+&(dI0xNVzSE+KNw!QF-grzFLjHR$YqHmNzAV`Yu=(B=${%c1gTr;9^sQ1RBZ9hDm)h"
    "TTJUxFAlpVuy@nYU74&!g*IDYQY{_JdeoMPF{POisxLF)?7&m|g|?Rmml3F!kC<;%eUL3NrF^r*nvs}wJQc<6RqCSk*ilLT-YP|X"
    "g*}{>Y9uYm&Z>oNy{Izjdd9QsxUYUGXR(3>yv&N=8&zZHD)aWotIB@6p&p79GM(;5mfnWn$m-?mF>-zV=_tBJ6Df0~y;O>up~3E&"
    "lByA#*={*sfx|;lGP#_pSF{Mk_PO<aD>u-EYJZJgGaGGJ(>vA((k+cs%+>-iTLFf6wgwRWEgKZ!JFXX{R=(MMM_fiOKtdcZRuj#9"
    "#{n_UGuw2g*+z4%ppOBLV?JzwLJe)Ku~xmhY#rt+F}2>CZNyCaQ`!UE7?FJXq8aw81$BIaaY}tqm(v4GPwW6CGj4hS6FH&wOybDj"
    "gZJ9G`f%!*E%kfx0xIxa)HG$|rCI%1TLHEcek;128u?lKpp9>5!V}l#Wu2=4Qjtht#Cm#ro;+vl1~Pjf0prR2>TIulI}~q&?Gqbm"
    "St8^zpkV$sQ23@3C@f+vKMf5T+@zuh{Xv)(oOocz1aTk>rW%A9z2FGY;z%Qo)TVdZU^<FU-sKQxrc3)7N9p0*X=YMEb_3nTTKI{B"
    "7&=N6wM+$|RKwEaZt-6jNee_jo>Gb0Hap!Ni~cQQ&SmH}MU&$h_2;UbNbjc^tlbwHzXGH$9<jYa-1V0Uq2Dse<agM2NG0Cks<v*d"
    "#;(vS(;@E1RK$EJ(qMPnpG0rp&`$&XY|;I|e$;*#wFR2H<!SH7jaK*z+p}?hv<jbG-IY`6ioj1n^q6P-4Zaa-K?|8`Q@~Urt;&@3"
    "mNEg1(`B*eV%f%*@jGp4m>;O!CMD);Z*j_*{Tg=keb2WGuJR*6E6Ibx58J;&KPk9Ufh%|_*$rh%76`LQ`zsd`u_vn+RX|jT<X-#>"
    "EcTupUo4~@hn(t5X=-V@BI6fc2$NX*BTKY81K;eJy+so2YTw(Y8L(X^9e1uV?Sp?(P?4*!2F4m0Z+km>#P=U4kcThfl{&{x2THkf"
    "24MNYvq$P1h^**LFN85dqiOG9?(JZZS>peJ=X0FK?4MdK>dj}|hOPrgXG#jJ!nZ1r=JW}RLT{%Mh0$<+VNvsch?VHH)1fN?|8jmb"
    "TPP=NZ{nN#sHcrETRjHt`E!BjzJVhR#<gkK62<1Xt_43--ORD!thMxL-tKy_AHCW2s^w^-br%y>HqohmiB|GtpZcwT@+x0GfOce7"
    "QG=xZUK)KCvupzVYgeHZE}=1;9$LTiJ&F?bT7NpLij789tww^L0L(tco-#IVjGbAOMoK{Ed#z*(b~$9qc+Uv7vWDfTFN*P6^@%<M"
    "oAwm^wpop=U5*|#Yi0eY=WOUN3st3xX5AxeU=xHkK^={uJ5ep@X?t<9+wBzS3=Om!1;R^zq6d^M$O&$G3^GA*2^=t5J}hMN)t?U!"
    "u7@XQFR`8}RXwa0ORRVc#vfPSkVj1Vn#)RX5p0HeHod8D+eTlyyV*M0-aJhBC&RKNJeKvl&Y4m8DYR+#wYl2<aHDdL=#0%dg$q&&"
    "BPT#K^a=WVMgJF7hXLaa{(O9L{O^a{pIkQHeyL`op=6;-)!t3=nvM%~Da0u%b%Cd^`D}mXs@s8*o345I8?Sl#dt3ALH(c}Ay7vRG"
    "dD?UCviyKoFH!=-!?vD+Fw)t27Tt!hi@M(KoaB&9)0{2F^%U>4m+dfM^U|3<N<!9CbYX71;1?19FTHSje0*g*7ee^(=BA=W>zM{y"
    "Uf?+~4@ulD`8G>$1wrP)mGyfVgjrDxicpoEeeTY6X6a}??Bu^%k5wwHp&q3R{GWOgCbRjH@qV}M5_$OHBb$F+-JP7iFs%;aq#jr2"
    "rF1Yj9+;+Ek^kUvSrp1$4u9}&>JMhVvo!`Ey!280L6K34ZqID9FErn5?Tkk_7O$5Hpdb3-+Sg~+2W{nIdCJ$@Kxt3(&^W&5m+xhw"
    "f{oE63X}I`d<d6L<iA>;S<yYp(RJ#x`a`khcF}EN<tp3SIvvT6D19pO?;rG&x%N=}^20{;TZ1^%PRxib2>_#GAs9+sw-#d}Z&Hm?"
    "q9PRIFMm;?ZftUj2p#pJhan>#is_q$tX6|Qmd0DoyoYJ+dVA-4Hp%&(PBHgnG81prQxEp7VFikJb=L2^rq>!wMV&#=-q_!e{I;UZ"
    "AQqS|3UXoifnJ3$5)}yfn*_g!)i<<#n9JGVH)^nw&*6C+J)>2lmgi`_H;Gm`v31A%O7*%u;ggaNy1sMrmx~(zTuoj(xXjFEA@+-}"
    "cO8B<qb-$iq>5HlYx<1oExhzshjynZttZrP5Zh3}0^Q(wmp>?i-;X1P+*Ah@P_8veWW4Wic_;zr)bJugMV&jNWOz{LId`I!=QGC)"
    "qbw+V(ep{QZ9kr#ieM1h$-Tv8Z>wMKswqZuT|7+B9zc|wwvo!4eqz-QbQi;Obhi5JJ=JXnr8Rhxy_x9EPQNRyg_Y_)#d3N@XC-OI"
    "F^IR0W?WjoC)NGvb!)onCF;e_{a00fIS04r#FEum#nw>*SDvWaA35O1y<^l%!<A)o%h6q3y{oj^xxKqZgA!{XyK0N|zS5R9%Az<A"
    "27aoi1?bUawgBn0Ys^C*`v#H-Gvz|(RZsy@91L<?nCWc#V&&U;;HM#|nD(BT*c4Xe7hBzM$<THs^)4WMsi{3wJw2qMXz``d5@SsZ"
    "3mW^%F^KAe;hMzYI-})B&w$1UZBq}~K;m!QKtd3Mn{)_Q)T6wdqV6vsu&&#D4qyH<Ykwro2aA0zE^wY^aNx>Q{m1Jib^N#<t9F?n"
    "S)xGM-PdE0ZIb5^ZNawH;k7Dj09qo+jk&I;l6E{Lc~x5Qvkv%y3;e<YKMx}?C)R*pWGpL8@RK5>F4!*c<GA2@VGi(lN(=nF1AgcL"
    "pO!=izlami46DJ<^E`;V)K8<R@O!{d!Z_}uK2K?ZUv$8aT;K;5_<<k8Ml4ptUnD^hrd{#}DRn7y!Jh^(*9UaKFXl86i2M!$u?vCF"
    "Mj%LGuLY|S0K2yEi>!-5mLz%Hw*+aB(}l4M1)kMHA?ToxxKM~}6e2$hOvD^0pjF=rs}_YM_lf_UtB_*9+8z{mRttr&gF@;;A+}LK"
    "A50prK_SF4E8TsN#D0+%Jt$-#q{F^d;8`scq7Dj~3x&i+Aq_#D`D;*!g1~pJLYOB-9}0N^<Myor&uXC%cTmV(D5N$DSpn#;+Y7Mw"
    "!YFd==AwxD7%2dYF^~K9Gf!*bkaTb;TsUMl4n+nBlza^ii4R;6J8<x0I+r?e0EKTW$`%Kn*21BqkrS6jj%|$`25D9#>((I!jh{GJ"
    "39R#=kCkB4rrf~VfrFUV!l9#<6PH?!ZM6*4fd7lu;E?%Ao^|CasIDySQw^|d)2xq|#IzO;9o?L`baP_s<}k?<+lJ}lkmEU|%S&;V"
    "hP_)Fwr!Z1G}Cb4X)PQ&3OaEq=)_jgVeZ33>v$;#1IdL$8YM;Vp3VvoW<C2sOl#s0cXV{(($R^nqaz>tp|2CI1@Lar-4AgRCe&2i"
    "i34ogtPck<t%XBJNhdBPo!Ck`!p)klS%=Wivch3!fW4E&eTFtLUzB7$yd<WzaOi01#HFPZTT4et6ej)}V=oMH>>t_10azmKGgm`6"
    "umye}4m_=eLq|;~E;XIlYB~bw*6N2a%yU1<yEp`Koc8I5Fv+5#PqvC_EgU*}I&tag#MaX>SVBRxMz)3#@OIlqQ{fO5MV^O!IOJfV"
    "#69McnAXCfqo)&>o=$8%4TLPhaLvIdOv12m=(s44xtyQ#;OQ4}5cTkqnAXCfqo-4so=$8%9p`b77Hh0l+<-~c-O~{$vAmC$;AEHP"
    "L62M#(^@!m^mOXd(}}I8;h^ZRJwL-qIMs^#wm8H^;-|e10N6%h=*B@zYvIt*)2T~Or?#F>;y4V}=?4%$xnCq*93npq`}8z0TG6ZH"
    "#IzO;9X*}8^mJ<L=_E;_AdJ_pgP*02{Q!vd%GM}{O`Z1Pz|)#IBpp4Sy7Y8v>*)l}i%Gnem*DsicX0@F5TAYCm<W#FdEAEsPix`O"
    "(bK6*Pp7t?PO>yf(si;m3yLu4I+VgRO8a@K2-CRe@yUp3EgU*}I(6yk)Yj8Uo&tpH_CuOSvBReqf~t!9*MY7vdT`)rEgU*}I(6yk"
    ")Yj7}97d9Lj-?P-CUw{va3;=!zVibpageP&dRk0t;n303sY_3%ww{J1O=5qY&6kIGN7umt%%~(td%crUR-}D6@U#{V9X*}8^mJ<L"
    ">9i<<JYFZ4iV*C#u1^3XeR}tF4Cl0@&(;vrS~zs{bmr32X~)AICt!Q7;U!Q5@KRSU1wk77y*|Dmg7Zb(<K^aQEgU*}I&<mi)Yj8*"
    "GKVwc8oM<DaEi2RYvg{I^|4ZtpqkElP~cfD6gp};bE)afR?|5g>(girD@9?P`a$6^z1fIzqEL`es>fN+vsx&0v~=du(wVKLDSvz|"
    "Cq*EW9J`@UL8nn(<WZlqo@X?{Pdf@ab1CS|R?tNn23fksQw$OwY=UHS@Ii40X&?AJqXm9PH)k&0oOK-CzMuI;w&u_fC85vm!_DB&"
    "!bsc$Iqw>HN(+IGV$NKOIqSH&K^^94wr&d~8OX+Ta|D3KQP_J~!c$rZbhL8j(#l!K$?fMwoJDI_AW!48*c^d8FM=rSLx88W5a_7n"
    "%%zgEj*B}0O%(@gSD=WKWb+*isyb#rrt_|cr?e30=;O?#kF%_MU*%_6uyzFsAZfli0&xI5SM*+1(UcYf9c7%mlyR1K5CFp^D5A9p"
    "6zm__5CLHE*za8dp3*{~qlt5uCeCb49E4He7m>f7g^Fkk1PV}mNgo1YN(+IG9?o5QIQKgUfPjzlaP1~e@?vuYiU9X~F9JNJg+NCO"
    "=PoUrcP^d70(5$wtQDhSxP=}7BRmeXpbr6_(nKKZ=;7R@hx5**a}=Q`ZJjj-rdi={zKM&}&;7g)0Wqb8Kt~hjE=`<wubfj%0az<W"
    "!<;*zZHNFmUDLP^0iM!ApreU%mnP0Tnm8&zCa?1YgEgIH#TF|7c3kN9-8PFUEd)B6ICp8{yrYTZAcxgni$EGg+2)EY@PjD#qu%>+"
    "p3}mhql$BvD$YBqIF4i3pusu}KyYWl78ryn*b9A3B<8d*=;-3yrHk{d8?})6akfqqL>bU*8w>#7uvZz2IV}u2%D8YT<GiDc!EA}6"
    "b=R~J+V^q31qMLoqIVyNIV}u2+IadfnYeK1=;I{90LNf04xrDr*$H6s1ic|hVonQ(d_x?Hj!I67Buk2Q8V$o5!*FvP!19Fu%lmNP"
    "IV~KDPsRaktR#=~wKx>9?{9%al;ufZB%Yk}<Li$fzuOf9V1VgfDH3)Ee`{vb@1A~#Rrp4C)qQ#Wu39u4Hc!=2$^}R2I=<yl{IU_*"
    "2F>K*mR?<QTEX5urwi=8ugW{sb+r=NG8mhAgLPZ3r>=B_#Z1Kh>-ocNB14-fa$UCh1Dsf{I^iCkoWD5xRb)Oc>gMhBTuUmDDG9W`"
    "79@J2Lkr1luLDe!JAv`H1*XkzaDgN8Z**8Nzes~4b$upMa8`U4ao=&y>B5RiQ||~1H`dK)Mz6`P-dKK@e)vZ{2R0w`Z$%6ufQuxQ"
    "AFctJdU|`^=((pC7srPO*MB@aKD~Oum3y1V>GBQ;Hq!F;=d-3(<r4m>@_~E%s??*mBGZ`5Y#I%_c3xf{bQ)M({w$bP)~+I&Ppe1o"
    "q+GnMmV0`$DUs3eRLHmYRegK6ysoF$EnJwiM1=~e7}E7Z<oKX0;70Kp27MiqS}czCPp|%LqH<J^s|hAZP^M*hLp2?BoQ__e9&~Yf"
    "fhk>jwoQvmmi8k93Nv<~gE<7kqTCLlm**E}CO+qj+2viis2cC(1n_}Bz03c0p7_3r)#24q7b&WDFumQ|dr@)D$=H*Lh&qNLM?JYQ"
    "OneH|abYM7HjC*TO^d!2+r?jm?N)D`7you(B2kOwsh`b0eDJ>aj;HT{kIHcc9JrXzP&j$dW>X-&SfbTyW`1Phm#siBOv&7GEmY8D"
    "#hzAgEuOD_u^91HImL{av3GQJdFW9^Q7kma>(Ok8-9b%S@}@>sw1(IM*C-{^+J&p1ZjbBb{?FE;UXJeGmv6k6mmWZj#fIh1*$___"
    "CvCp%*FdY=W$|0>GnwD)!Xo%G+w9fha25L<fIyqf=D<ag|Bk2Q>Vt>%ZE=Y_-jo}x)X{7KSWG=$v1gOY+H_G7u2?ZVQ1z`?v`YT}"
    "7HT>EMq2r+B9VM48NX6by}CN?VZReBH9oxsV{PGa_9VAWW01EJ4_#(U@_Yq)dAvERt(AFSb&>Kf&1pT`<>>hNWuN_bSuN@c<-)RB"
    "OiNMNjSW2SXhW;e6b=sSuvmpDg=}@!Yx|}8<LRF)?R0){0o*g2VPf>H_cKiH{aRO(@ivBr_0{HRg>j#finrcppn1>Tns;zH@UD)}"
    "FA<yn`k()M1B8yJHxpXtJus4&TpwpU%!2q!%JNsg9KQH-j}-Z(n&6plIh(S|;<}Zyg;Q_2c~hQzy`idA@wu#tna?quY~NOo*Z0+O"
    "QIAAw=uJ6Vsv3gLoveI<h57eqVAGM;<eylLsb>1zi=zE7*qf3IoB<(z<R%T1@=Z07q6A*U+Mif$YP!TMcmY>~`=Ju0?{HFYgfp3T"
    ";$OcDQm*z2+kM8h|H(JB>%FONVEcO0s$A@W47m41Lm6^B%qQiD>ny=vRNHr8bVV@#5>W1p%K4nDF8%ed+$;h9!y>cW#b#jlY#8+P"
    "UEoyQC8y%90)r?Gg5nUdrxhPqOYoY~qnB5+XIM?^=Aq#NuZ-vNuJRUbUjT2a%D2kJdd;ca<wBL}m3@+C!kaPVswtwj?yfh*<Z^F3"
    "d#_r!dk@nI_Ts|X=-nC?(wjdlM%Y_zK<Fwi0gYp^NZEK5ifmC%tmPE5!tYb&h~>;fx0nYj?bTofPJzr45Q9%-`_`6A^jEz<meU8U"
    "X+!D42>R5+BlDxj{>u)_RM>U}mF5{&`fmR6dVoZb<Lw|+fcNy#pw|;5@oO&JCOCUv?WPq(A&&m<jVIil$bd**DvCLlwLMx=4Xu5%"
    "^QN4>mD;6&&mJ02ROG^?2VH(oy8MZ4=I1ui-f)d0j{suX*2ir$Crw{YU=DAm`Y@V2jA2`Mr=-{FDYkXd>X|8scfI#__2>>ciTF*S"
    "CpeZozOuWMltlOC2fHzc)^tNL^eL`0z&V)!No!_XwdnwurdqsP&$U}F5Sd$CH|%M5HeMi?+|q>{*C6UH$Of{l9RKa1Sz^H!z2(S{"
    "C*_A>TlHxZfd(}FapNW_Vx8%)0sf2MTqCp;<QGgFvE=yu@C}GP_4AkALVUQ!3Fx)uY))mYUCgmk(<u3)n#$OUYV|Hsc+y!z@;4WG"
    "?NFv=d!s>*)`v&2{h{297SLdH;V$4U`>nQv#)ppGu#^ASfBvsR=qR_P@Z?MG4#CtKP*#Va&)yueJ<=-0zv!7BUAeGKqWjd3vOyK?"
    "TMcAuyHzFztIY&knwlHVV8o}oZ9tqOc!ss}9V|TjaI>i3aD!!JJhnl2VX=ZB{@r20%kmMlIT;SL1K)s^{S&;VBz4XFBr0LI+f<G`"
    "Gbdth_$orYox97ph~G+?;IEVkn;5Co?+F_(424KP!R^1>`?|1NXd&&sQ0Jg^E|<5PTeF|oZ0d8&U8%W@ISvUBDpRE9(t14_8^JWZ"
    "_{%l>p{r_WLl~AfO@3+_&R_aCG~&6$PHL*<620doSxu|>49-Z&Aa<UTwzU{eI!L=H{+h}QEgmLv%&R*fokwR#56-u=UuM(EqsP^J"
    "sXpW1AAl#wkYCc<qZvr<`4YszztI!?h6n{a^u8+53Fl$4Ko%i%l#w!GQPGQV?7%63La-IN79nUg76XSR*pu`W59chi7(S3K_kb%|"
    "nr{dU;s=^*;A!R}YRET_j0+A9aN$@y{-3I9PLGfSo&qEwZhm}R2!u(rP2QJ}jn|a**u!G+c+%K~7bg$*bFX>07r4|74|p(R+jl(P"
    "g{N;|BLnO}EZBK-BI)~?KtP<o1o90|ayNUAz&sLVmI6dZg~?u$fKvin7&M0T<Bxt>)a~nK!&;dn9m4PJ3?FWhcvx59$*w?w=<gk0"
    "p7B>Z_;An9_x#|AIViCnBDD~smtI>p)Z0mtAB-`*aW$&%v4$shc9Me)32#`8|B!tBA0E~gZM?S?hE||c1D2t}^BLhw2S`M<fz`v="
    "OR?y5J`xKCn*e9^?(1e!(XA>kwudDIy~o)D?8k~&g3QDjvOCXF)8mCIhB<%01I^zRPtz(9BjW*<85fR1OPFQg9g%;IS+pb*6OpHv"
    "kS|{A#fgQZMzpV`dUCpU#xii4(u5tyktu8(v9c1cpa>aw$HWQ~)Sb8|VF}q1UQ(I=26xA(e4w2=nN+tG{m5X}<cfn$1GC^qk6eTm"
    "IS?Puf#=t1<7#?a136`vi>K|N=6odO$R{IzN8kK%7uE2R-iH;iRJ*Oo#fO4+FhC9an}dM>%SUvoiW1IL<W-oJ){SKl!GU>@no<@y"
    "LhWc2ZYVh<ppTV=WsNZghz=){=Ss4}rhkJK9l5kAJ~mFm@b@_v?-TBu&oFw_=|=IHSP1EF?2-|qZk{SeY1aym@iW*`p#5(bA}~kY"
    "O(h)%O)S_3Hk24;HK|HP42Aq_a@&4e>@j%g_kz9Fnr$UdfM)tkTi957t|Mq*Z*7$@vCyqhACn4c5#B{Lf`>n<gS-<<FIw~DCv&ei"
    "UaNNUU9`y`mR=AF3f?ScpiHqvU&q#2Q*#<;dAOgFv)8C24S#z(i`fI6SkdqIMAWw3csNHDY8td`iPs3{m}V>+O@s$VS$ci&D<z}d"
    "gTCHK;wX06HML52Q++Y^;l1+(*(VN|ec}z-Ck_<*B>!Tcuf#rNwct^d3nFvdxvm4R%T<<1U@;N3LYJWO0aohp8#0u6$#*E&lioA^"
    "-EF%Djj^O<uGjz;5Uc}_7>=SsB@ZdCTh!EnQ?cZyXf3DW?{&6RCO5oClN1dPRzm1CCo+7t17r(rc;(Q4Wcmp1wzQ#XN)>)b9d2nh"
    "=?u5ZUUEHfTFn-TrM0a1O+{#XZ@_jOc;}1i2HTcZi#_HNZ3{I&5ks~sghq5{y}PUR*<$t*Y*2J9DBgun*9lwM<;1dSX-`m(Gr|sz"
    "rDW~jR(Q(!38APL=7Ir`L^AXpOvJjF;?&iRbI|S8GH|wIaXYQpp~y`=^si+1OYLjv_mHoNZkUdb8~K&+b65qh8<^XD1QSE<ifb|8"
    "Az3<~I{az95U>tA`sd-W4_b?FrZgQll||&`Dee88zVv1DmJCNhkgvc=qLjUMS0}L+J_Ig?Kb}>5Wk;^7T{`%&B-Q(*wSmZa5)N`p"
    "0?TswI0C^G1+8hU(|)Ct<w4G|slaSf&klghLIg;_k+-b%I-ZJ4k|nle-t{o2L|GBEe#BqGA=kq4ljL>S7Qz`Y!!zi7;PsU0#y81J"
    "B6Zu?o6M%S?9m(HnHe|cQ#mes59;N&U0Kv3@*0;kTo0_)HL@%^{^`qVIVjz|P6oY|-Uod|-yy26K!X{CS#`ghmm}3asO6ERH?D6$"
    ")=NvVTJrYBumEpIHU)p8ye0Kg`S0ZQn&@#Uf~BY_8Bzh`*?shMHBxS1d*9nT^Q$>J_-f!epc1e*UZF{c@nkl8%bqLtgzS3F4Cfbd"
    "0Aa|m;ap<Fk{@b1qcD*Lk_aJ22m}udynS*1B47esnJm&V*N`_7)SE$wuc6E=0G{$T+`~3x0-H&7vlN?C(!{lirEA9}lPuMz0P2Yg"
    "X;qNX=xbo{(4fOpD{X2ZC3@G7fRJeRaogzEJ-tZ2^x5pW-5dn{X_|Q05xq+;MemYbl5zF2Mq<yo2T5az1ldsJlSIN#;zwbNma?r$"
    "YlzdOVB`IxTFkg*3j<EEb=ViC6Rak@%%91Scf|QO%Hz38jOtpF!`i$ZtqlvZrQSX1iFKh<L_gT~IbTbl8l7GSn{-@hjVYTwsio6K"
    "V~9vJ2j5$#AV8Qyusllel(KCz!P;8wVnhDql&vH;$p#a*0m`mXH!+}#J<$P(dlY*2_4J{Uz=5!hGe3g!WrF6Kl)O)c(8OMw$RorR"
    "a!fpIl#M>`SCFEohPtA;lxR~a5JHEo6NOt^U%OVbuc}>Rm)0eYaF1lL#6B|sT`wYxB5s5Z#cB`Y-F1b!pMw1G5DPlWyXdpV_3g;Z"
    "iBG16Da-dWGu+jZW#khy;qUoEjc!ruX5b;@{0&`nVy>dNtGKD&3#S85jPHnB7`(|KbCRA)<6mCeDC};_xy@NMNyM9)!j75G;H_N|"
    "qkwM;+hmDgKejwGsmdu>67_O9AuIOlohgPwfC<rw6gCNL=pFNrD%!byl0@8PnSpfSr_u-_2$UY#SZr#HGg#AyZl%^Y&XKw$`U1?F"
    ";S#&19ZttzI`B=JRmd1^>Utw=Dd7yk?Qo-pF_%K`;--6O`5X1V<LIwC&kcH;#8E7Vu%UWiB3hZEMevp-Du$kH>)W2E#XY;cR<D<B"
    "kU{(d$YwAy>M3cOg}M~~vUY@PAJBDoBMl5Cam2nyyT_sBwfK*L{|)Q~o$)(u99Ob>pB{M4jjBe*(W`a;kb_0Lch&mC(j$MveuE$N"
    "5TQ27LB^-9i6%B;F*&|&O&})i<%fIhqH44d)cZVp+-6hnH>&*t+T&LJEn1C=@GN*<_=8|K%!_;w=et;+dJu8*K#q4Z0;qSBVh{wo"
    "ap;GGG~bPb7|!a(+raMn`@U)(cs8#VGO_B-1D=7Y^>bDvIlQyS|DrcN&k9NJfAM%)c3(C76=HY9#NUNOL@)@_-Ly#XzptHf^(u(H"
    "v7*pqM!-k}nZ2qO<9fu~xDsJuSb3wwh)4WJwj&J&X&Q4a=FV&pr&x*uCH~kp1;zy)Y6)KZDw$_jJ@C})yCS~O_(5<6C2i3!YSBH("
    "t1Y**Z#|Q1gY!_&ZtWMb$SNRJ{A~_GwD05_4|TQ>Nx^~a1MK^O_D2-*BI3U@Kcn#+3BboDt0i<TPSqsjw_(nI%OB|{8qS?YXTTT}"
    "IJtsPf|ko)b?|x;yetr@r#KF*Lm0O|weUGp;jGcPyLn&@M}G&M0ecd0Z2%L|omn3-X@BDJx_d{4Mru*2Y73FLS0TU{OfZ(!PB4LH"
    "&kx}LuYCV0{Xgc<{X2nn%h3mRE)UmLQEer8UyiG0w5aDIu*vy}aN-=H6CGtQYtPfum%|ru?0@}nv%bB~CcVq@1B%$8D%gV(U7Z#$"
    "K#@Pp#hyN)h%&3c_9>Vcjo3GQ6~;bD^dxie)Xo(d5h0%JW02HTW_UQ6$i$pI!NuMJjvKq;J^*c0%AVQd>={oLfEkF%PV}c^)DjCg"
    "f^sAlZD2TE?k&saEs0g@eKi`I6p!A!nx!x(_zDF4l20q;;vEc!SLDJ3tfza;Xg04vW_<8SG0~NYgy>j4?w}5*u)UKLg8-LHusb>V"
    "z#L8b*kRrd5yt!$;Wt=GbTFLI?aT8=ICGk21FGeC4t!lsDeI{Hh~KYeL?5m_8D8&^A~J)D%)8a|j`1>Z(M}!X)J2>QsPOiIc*@yy"
    ")uaYf0S|*ec{dMBbT{ZnQLt}HJO+x%VNX;a=puloKRrIa!ULspJtAEMxy6c$d~Nj4?zIL!8N9P8nfmt+lVv@hV2utD-zq(%G`z5T"
    "rOZGky?UHi#}wHpHpTy8Xtk+q#x8&0)K&(@TP~_{$)+aZ5VYD)m*o3*)#xn+JR6<ZMe;d)8PabKy&`_1dN^#bsM+Pxh#?}@m`+{d"
    "{?!D5!>oIBhX4bASMy_Tg!nd*FLm|A<_M%V0FGf?08mf{SOsJt!0#s|7H1L5xi6W6zPgZSmP_h&?fnRF)wj3O#K2a=6w)mqI;t>H"
    "dE(8$z?zoA;0a?skR1K&i9BQPzy9<8mW&4TKU<Wex5A=16JH8v=&pBpg>HZE7Is2o{N;`7rggjTsyX3H%qeXsV|BXsci5d=gk~(t"
    "yEGQCFRu2V)7(MAfS&)dhg*bX>5cXhhBJpL>=GEAl0JV@5?r`<=Zo2gM|R-;TX)`F7)3|sMISP<Q}~i%sP~6FVljxEgro}}AmfGc"
    "HtH8`&kF!|=w*-M^`B^hgg)_|!%ypasn}ph!LrNl$c9Xm5=(U$|Lb?(hXEO1t{KGZd_Lk!_$&P<J_c299&S0NnnEgQLC|wSf(oy{"
    "9_Es8C&TB*ycXTLrDYA1qEZ3IhmUXT5ka!3C_ZBiJa|O6rm&$Sp!5qT0#|X4fY(@O`j|l+5-|J7Kv;sL6kO@eON^gs7kz+L=3r0q"
    "A4>Gv!0?(gvgKrtBJK?UFouF^C}?*W<`#y7V(8?KN_^UG<KyXt=}|c9YBuuq;R+~iDf53NL{dDp+j=2+FpA_x0LkM0!NYw4{}J4K"
    "B|I?lJ4V-F(spoK6*X`e%Yi`>^bU;QScAS6ac@5hqoH3v(!a%P^l!b!%t${b>Zd`iQiSR+&Mu;+D{H)+?|-CcPlS1D$w2G*v5=NZ"
    "LKshBS@$TV&-qjrVCIv{-X~|qy0D*XM+$0!?+;3X!#}lwo&cw_fv5{hrQFE+67?<cr-#K9&-=W0_MaabCWpgtu<GLU6uxOsq<{Tx"
    "k6!%CecezL;9ZSnJ?aqvIGL5>*Z=>0D!kEa{?hEQ9vh^s*=SYO;Yy2fTnwlzGZXTAf5m@-L6|1`FJf1218cMjR#lF1RV78Pp9m+I"
    "+yVBW$fC7~0OxEEc-(I-ZpgLDt?)0dHOy~Y2*{F;ozje4%@0U8$U7?^4~i)NIxC;9IE~1%jcW=mGUTv(2Gos2f<6e+TyCu>EY^ab"
    "=YuTU9)WBH0;(3HSwfKkj)QDK73=pbIpD`%iPm|~VRW+{X81(^wabv8Mc*!y6(8LN8MzE&lI4Rq>a2e_@crWJtiLGJ+;gDcj18na"
    "_+Jb_6b)8s+|4K|{n!7ZC{Z-*Hw9!NOLI4Ioyi~#xe%NZ|9L7mR9<9jH&m7lg5VRj)G8m_X6r96Z2q<WM9`H^$F@dhPc=&_6qxwg"
    "fLdiJUI?W|1?5_}t?wu_v~D;k@=sugWCc6O(wE(0l>~L*izrf4AEbjQ`AYVHs5a=_YpR&#ib|9Oc9a9DQkNN%C0_~bY!!>Nl`7pu"
    "B?;&-2nVTQEJjjX_=7Zbo^m2lcI11kl+37w=^zNVL*O;_Q<#n3Zs<xml|HX4QH&GU23BFV5UVqOXqLjGLeYW_@5<+RPgKe9M`GBk"
    "s}q65vixwgs44;LLA5OF$z~oQBMiWB#;d;!2MA?^DsTKq#VdI`c$vj=RJ`E2A~W0~YtHeqK|-J78r4mjb3B-IrUg+x2;=p>0&)J9"
    "9STmJu6txqV5(g60!CmFM(*Q%uldFn+HWH7-8V<QW>NARLz<ME=o?Xg_TOCV6~w`S+Mh{=h~h!QW53yA>|TBdlL7T?l>CqnqPPfo"
    "g3%Tetl;T11JFaAr_%`RC!S-x#T=IpZ<ZpeDF?Dd(v=YUDF{tI@RyrN?^Of`g+q;l6|e;;ARhb87Gw7kJb)cXT{R`e<9HxoA8j%I"
    "3VLTD7^SI>LY53tfx~!<IWGI>2ofMus9}+SW@Elgt8J!emlV6q4yeyNt!V*TGczLDwCk}wzKRv^%9<ebT~Z{2LYnFvvmiAJit^u3"
    "qqvlaR3GJ9N0sb{;bdCiq10G$IH2%q1aCGTxtC=lSZwMRD;FCS*&tyd5sWq-Ut8;_fC1zp1)++%4A;B6)<PRcV4v$7EQk{@*fkxu"
    "+DD~)P`|Z;+u+!j|JM3#?SW*SI7~C(Eq%2@;9<Y$+xV(~0x?dZc?&Uobr8yP8HY*H#>Z{;3?s~+ft`+FF(Tru6J{!(dmQz?B2@DD"
    "UZyJ0exKcVo%cX;PDNe3Mb&_mzyPsFui*eZQ6vvT!%&({;KgydEC;Rii-_(^$hWu<6~fBf5fNV$+5SXGE38CT%C34Zr;7>}<R1VF"
    "N_c%FPX@nR@p-|<dtEWkNKI;SRPO^>|C|E;UrRx{n0>&DTO{`zTqjJprSc;3b*?nv{iuF8pvriQic)!~q{p@*=J$)l7II8R7UNR>"
    "IMiH4f<Z6};dJ=Q!!xyyF+W~)|E8iM6{PszJbL4*sc)x)PZ3V}7oB=zar66Kxs7Go_9*PN!-}v}6IA(~lsH^q(SlKk9~o%*J2`-J"
    "<f!`?ZbkKN7N8(P5Pmz&8E$wd9sJgZ?P&E~?^<&#1$#UUbOj#;gCsC7=G`}3vY}Z2SqlB~VWGP-@@(M8`q_JhuV40%av!`S5nZ7U"
    "-qD~iPTm`g+;602{y;x=2MHWuWBu5@!RVSnor1+52dxYlq=j|?zRCx?&OnQUfN#DPsF5PE>txn$M`hmY$Fn>u`1rf0;<|;ECS=1^"
    "`Qb{2IiHjuB|bPKYi0B)NeUGt-G-*M`Re?JD&Z`Hy4#33Jx;6ht0ThBGK!qsg9mgG7Tbo!*^;XTYUqx>pUX)5b&`+r0YKI_oWp>Q"
    "R0WMJV@tUS7|;0f5<}SUF+-X9u~Bh(B>Cgsh<&{H8r^?TIo+SA+A9_X7KNJURB@jJeDwglmVX+M<ZYyVA8Y;fyR(af<I~~AuU25<"
    "?}Shnhaw6U<Lj70CS|DG3h>g&i*qvqnM-%$7sxq{cX77AF%`|IYlD(ju;Fh;LL(Ih3G`+*9q%>E#|c*kR^?9`od~XwQe_sIfs$(b"
    "RUfMR`BH|F>yc|;6+s#0JSR)AY?=ouEA9C|cq;Or1&gdzL_xxP&Ab}Hx{bX1hiQ$$y|YHtFsB+<@4$!>k=?`sc;@rw<x=J1tnli6"
    "dx?Sxx_b%=tLW3bMuAU}_*|6lPJ{!Sf>$DTxeBr0f`vQCQOe#b>{KLm7eh**gV{ki+@tMlCd0k2r{kHZy#Zq8KuZ8j_X11+lzq?_"
    "OZ{P_J$&;3Hd@s*2j%0w$o|Xn=%dx}9vkmH+*2JAaf<i{>{J@>b|%jA_4HXuiPzW}ol+Ic#k`6hDPPymBXlFao8hG__J*Y2G4nA-"
    "XZt<n`n|_Gtn^?Ho)kf{E4#>?YwhOuK@3)lcO`BWPW_)_`-S~-j^XTLzJPjyiy(gv6Fnb^zIzF|;c>3+cYZ>(?-mvOHVqzmrO}lk"
    "pjFQz`&kg^5BDGLA0`4s>?&MDK?~1O{Xtgakw5{wkx2(^=z*0{U}12%qs$;5X62pF&#Q$f$U}Vt^Uf;=T<)NK4^AgwWYPL!Cg^ie"
    "R&&+4o>n*v*01ml90YNR@9|j8ofiK#tAzp8+B4j?PUdzxtnoK0GdmHcoWV431c=N8H+>*G5v#*nK@f*4)+<d5s-mm_bRYj)7-Qc7"
    "V?+_hHi+(_y4;_yVyGlF;p@5hXaNkn0Agu{EbJ$uN<-^XFU<2*zy*m3o%1Nr!j`#+7p6|?ZM?u?nydh^NTXf?x`7N`To}egh^+}2"
    "`6PpSpo7y76=B9*sK$Ju^q}s&G5O7pHE5*BPI^`_bV^VeVItD3@v$i)LCA-F;xo%g6k)}dpW##wQsP&x1^hHzvD-pFYGHB6zbK=)"
    "mK6drqg8lQO-FZV9}btI$sGpCh@!6sonpU7;pD4$2A9R0Mp$gU^Q5tp_<m8W+CEtre5CbX)XiHANa0LA{4k>XtF|JQYAdpw%{hcd"
    "5iN+~UG4Wa$G#ffO=pwYEi-uCz<IY?)L7iu92HeH>4I{8K!*mAeJ&>iW94}{Kc5Sg%xoclK9G$(p6;au2Y<{Lv+=`dd0x|fhyH0m"
    "pHhvXHm*s&fX`iDYcoVC-t7m@G1}LFcJUxJ%@@%tOVpI1dIQ5-mgl|I3A|sb^3Etxz@JcLKws4Y?IU_l`{HV*XWcy|hm{<_{em$0"
    "4&T8K(io7+w87LDuEK-H!rw$VRYmU_7M`E&h3uoT?6|QQl9>pXMrcXH+z8rDa`3Q#)lmB|<yt*#dvftBnlj$=i#-wJM(|wKOCfKL"
    "Fkcr_9KE~xExJs+WDq9*^`HMM86@J+#lu~qrE229Ucxb^QebhPs^!Hrq;g#M)dg&!XL7^#AsHq4HdyBIN75ae6Fdm_L{#lsf=g4;"
    "fF<n##ZP<b9qmOyAHC=GyBS}Ez{Vys4IAr5-WYzJPiD)0sv{zPFV#t>ZA|rmOl_O$aUZH#5N${Hn0i<xn~^<=a_7VZXcqKQ873%P"
    "RDM30f#u*e6^Npn8zS|q<3D@N9C%!IO-%hhI>*S}V)<NjCMB>jox`l?M=cJwCMxXYd^4hkQQsb-Ui40qB8TPuf?~n>qFC~RIXLm("
    "%vaD6fK7VoNXE+M{95FF*Z`v2k`YhY8}eol_wIi`>=OVme&A%ys|B{ZswUiX#CtC;;hp4bfpn5D+HSk|ZtWo4QlchU!YIr(BcC6n"
    "T{+|TQZ$L26s0L6-$l`bssbacdg~33(V;VX+ec6xY>S}Vi%&n?3ahON44Wt1jKEnC^a_};pPX@z?0iwb5q0al1FUpfF6x^bEO<GE"
    "1I<Wy(%jTlFuT~bNVXww+N1wjA;h0T&SJyuo}|4q`(e;e&M<V5v+(!Eij3Zz{KkuNGI?B0$D)r*^R0wt7)SkN45O{dnCt}`awRPI"
    "78@k+dkLHL2-26Ad;51_xq8p5Y4xs@6ozAyh(mDG7KZEB?Ec1@-QQ;S7wL9{PGKKOC-8bg=l$v_%bZlD@k6JYzkHbEdB@wIJuI+f"
    "{DLedoY8X&hCWj3I5^li-0Fl7`29ANALO4v-Ec!2$}d*ToW_0Rg#%LTBCo0m>K)GOk$3d4cqB6lnEAL_l+{F$99}tIl+%^u6-YR3"
    ")UD|2$Jq+{M(hsh8O?OLL==$l1`{bo(NBL6$8`BmKgzNYt+T)Do=Nk#=iY(+OgN6_hSHt%y_W+)y29fVW<me`Kpc^I)Z4s*seryh"
    "*^v8F>hN|70zXxbnT<>IvN!Bfw&@_S7PF>NWD2FH*L+p^x56-E8=E_&Fqzu%QVc8XZTZsu5oc1}V@|Qkk$@v8vM`FdWPW{5rS!lo"
    "u4G#(>U9){fp}vjI9+His!7fMS#=j;j&M-DSzcC)clC(7B_<(`QjVoV+n9&TcwWu+C$pv!%cYUv7j)jiG!r9A?%9K?%_dxweC0V`"
    "Qa|QpTZ|UVSUohN0@Y;6(Mv~@^45wt320PoC3as=>-&d$PnA^GDrD_MqMW}71*N>iJfJZCBZ~H;(3~*!ahYif8XdW8I36#svTfT~"
    "y_T&Iu@rtIYo)@7kqnkU2Z2<hEhAzH;hjCcqw<aMsdObq4Nxz3?x#R4aO|e+0ya_Ov;{dxZIDqyoRlBxd)UQoLkezTfdX~DsIh)@"
    "TTopFqqajNYldh*y-&w$21)fne!d*?_dPFX`pbux=jYzeA<tWR6rtjs%Rp4z;ZJ&o$%*uj-d%lrx2NhpQRAMS|1<l67C)Eqzc2xp"
    ";mPe)DHKmFXYb1euoi;W$6Be*T5(KC(P=~ud$mq^9+TPL&Jp+&0xHBM`4{Pq=lEhs^)>^a_ppR=PyV0{5m+Rq5A!TBz7v0IpM{;7"
    "u{X6A(dF-AOG|wa@wYZeq|Z&)N<V7tPhgGIzSxb66`LZqiBG3-Zsg}_^-AB!%Sjo_?PLHVGIGFV_TFXyFfbaFV!K}Xu$<9qsaS9a"
    "XhCPQ2F%iLVNX!U(0dS_w|HGDn?iAlr4uv}NPIR&d5dNLAE_*<s1Mwf`d?-9b5m+U8XmXRz`68zt7Td8ibV!K)irSYKo%Ca)U$89"
    "{ZFcKjV;XRTCwZ&*B@u9Mf6qqLFfc^@pK}}1B$D8x*b?xS;<!oa=C`Bqi`qcTXM<Zo3km^BbrTrAyZFY+Y$eDBePpNsW?mRCGqr1"
    "?p+Qo5G%H>_8>wPk?}~)4uHu3<CEE<y0{-VS9j%9Hi5x=<BtyFJbRSdZ>2&ss_-^?VfO9=*`{=8R34Ts9<ZR{y;=w<a~x8J{#ObV"
    "Lypk@;0j8);g%HmKT;^5EU>mdZ}KEdeU1%6J%`<JFj{0f0t>gauJ5j}Z6eY!%u>8{+3mO2M4KmJBRrK2lB}Y%ts$3^x8)lcU*>at"
    "5FdCm795Aay?|rQ<nd+OZm$hT+QdFHNC2mkvztQ~b{JZcvc0}+FQJL@$J3+PVkE5d#calBsj|MZ-s7HV{Ixpk>>C%bM)1thkM|f}"
    "ivi3Hp64R(1U04i3}mc_A!pv6cX)N=?N3Uuue7?9OHqFTy~59qU+__{0;Mj3p~Bn>l6X~4v1QoUyZmqG9?&0$wMTk&c4iNRCScD%"
    "9KwyoH$)W~?-&;71A~n~yTN^SdSFk&myh}+T%z@Ixu~k;|NH-Vm*)o;@E_Hi$~%Cw@nkly#@;Wp#RU5@?g1GcD8ZM%*wguWoNhOr"
    "UFOX_)8R>HrYH?RzP7LZ;S{K9$c^lctqS6EJr3mJl>4;-rqt90_9yS3iq6A_B50J}4C5>sP$UVaXiO@y3}0yt7qy>%QE-~SpUYD9"
    ";t|&#MiWC3M2^S?J4G5)*lc=!_xKDBQMZEAL59me;1!<F+xdYS$s<E^#Ii(H)<=E`x*vX~H6aN)$o)*TO?g<%IDU=VOB9@>J8bF_"
    "_KD&N@igQN_CLbeZYqBA6a53Zs{Ak%%_(q>c?FMwmGR&5X{-bHC-`hUyXR*?mWVDM({fyj-y+VZ7-BsXP^wKW9{4Fwb5f7TV6+{U"
    ")D)WTWcZ60z!6h#2(STj$VZII@J9PBh)r-!YybeVs3dWpJ*xDpP9CeCjHT6exspi|MmrTDrnSnis%3L;D-I<x^ssdnAAEEX@<Z+_"
    "Sy@Z|ZC2PKXKTbsE&X#|j_%%<Z@ia-%Yk=wd``mQzy9a{HmeEA3071U60;R6C$maxiK^0<Kd-A1+SjZ_5$x#d@=z0YQvCD_T3PB("
    "V&*RSCy=6isXiEL9@VR#%|3kazK1#AdCwQ+82!6?u}-yWvX-a(yHnGXxt24)`eywkN(N%Qo<w7Vn7yK0miLr@uPO6MBuq7AdNPCs"
    "8(w;<bP>BT)x4@Ir^)TII_IYIfXag9oy{;L<kqu_da21|(J%RTxA+%%bX#`csFd7Bt0YJ4E8PObK}W6!<{S1npwyMA?19A<)jVzi"
    "W>#K%DeQ@!5^R2pOJ9W%$sfN|)WUH&oATD;Blc`z>@QW%OHJ%9>_rz9@!H8hg_3c1NL?6#2oqcP<pgvO{E0SSBI@z0y33LUR@Gmo"
    "E25l>M6H@qEgl`8%Nw;!svxzZmc2Z9(-d>1t5q|63Z3xCMwbs1MQO)Kq88Ljml@UxTUMeZdwUipSERfsqE>M=RXpd6Bt1A24CjJw"
    "e?osR5^XLHC)GPXyReG$cH(4E{P1Mg1EKBh1enKyfBbUh?G%Ij2Wbx-!Rd4=`asjkhQ&`1Q>5Jg2xWfLXjILYD!Q1)#FSJT6K4za"
    "L82xIf<dZg5M|qHcBE1OcD8nC2`&wt3<CUvwk7--3_>;d&s8~D-my;vm%E^Ft=_S5xF|>9BwdIWyB^9(_$xz_$+l@=q&|RX_Vyn~"
    "m<c}N8S-$031T%t=xcN-jN$JwEsM9bNqj#G*G>|rf+)BN0P=L;w@B&aS7@LYX4-K63(S!u$%;9c9#J4zh?XHkx=XY|#8I|jn1WUi"
    "J36L%ajS<73w_vBA2!w?$6_NRPevg((kzeHF%OooQo{pbG`>uct>j67?)GX)^MK-n*D-vk297epMl^7UvxtE&fG52}awSL;K3Kb)"
    "iN=&ssKe|FrlCeZ!o%wlH)ck1+tQ3=4z_uD&qq97GU+Pjq+2)>%;oWm^YE1~nK~nn@#f`*Zm(Xie=g24sNX=|S4!TCUXa3D*1*Aq"
    "%zoia!n%}ss5PEZQ&j2@>Uh_XnU|oW>D)_4hS&Ph(M7W7^5Lfm=@kb`tg`Fx<w7{0;9bTY=Agc*%SKP1l{N@V#)9^J>+#0XwX-Zk"
    "R!%1Rsdks{r31^?t(~}?s%a^s(S}BfInn){Vx87UA>9siDWO$G5vR6#>EY>7<xpxgdi{}|v3d@o=%Ffd1kKQV!!3PyB(AJGm-9E)"
    "HG2~0nReHFc(mX4gVpc)*N=o3_N|}I1p&v1bRa0QT>q{EK;$R8n+z1BS;75tDMmwO+993DRaZ4b@~v_gM+`WUKE7HQlJE=7)Ber&"
    "(Sp)~Q4LVeFxxJopEXvPd7+vaTloNXSI4Wn%EQ3hMOil$r=B)mn7o<Wf%?0Ytr`Siabaq<7SS)Vjz^$fEAAWxf8os`UKvgBREn>J"
    "q3oG1r@X`SgvyE!V%aGEO@-O;82?M125VHR^QDSnkGbXZ_(5$1WZWg3nS{|~CBy2e3HANF94!y(MKx02qD#Bk8>5lNJm0!q*Jmy$"
    "VS7v?b3zER0q1V%@j`fr>dVM&a~+m48w@7@@uVD~XNkO!E4jwv5u1yedz3XJzGMGnCTepWY$j5x$?OB#q8vX`!%9j=7fA;m)?6wl"
    "@NS0uh3-8p6okBiXCNxyMC}E=aW$&Zz~MZGfpSIzO1Ioeb6UM87HfX;E*=_;!uK%$(fdRE!@#3NI#vF+@ow-j1rbdi2i|@Ovhfk?"
    "la+WGT8@b?>3xct^pNNnrXXmlDiJi>GoH%Pa57%qyxqh0ky5W(thZ4Thl>H(H7oL?H|D`M^WzKfAh}bkrZRsOuJ2pUov;PlkAFP>"
    "wTJoiOb?s+eyyh16Ls<EEy?fnFvVatS~Y+Q2#!5<fy_75T7Ail5^41X99Xhr;1R_Cz45Nj&X51hECa@1^aCvbSX@{SpvF*@pvW`t"
    "*`!2=Bt~xlOR3C{vCRBPuv->@gHI**(wP4jj3~Os&*lI*ZW0mY318o1L4nB(>5FB`juthIfD*Hs*A4cS1L~uhf(=^VSJhhwPafaj"
    "SL2#WUBTDQlOEnwnJxXid2{1r&Mk6ZT<m#T-Im+3r=BpQ*prX)UqC)efhhQME4irW%XH)-WwRU!y-FD^Ank5u4-3|XyTqmC6r1@r"
    "R5B5hU4RSTRl6QleL#66<s$M75k~g?1steg8!BF4Gbvq{tY3kbN3-b-n)D+qHBsW^!h!9*FB_29<kA7D3ZsIW!$OiGPAB|<AVUrn"
    "1CD2)qe1XC4{x~G<dUTK)*`XZ{`nM<xGFv9OG!dKr|1hvLQD7FNH>kid85VSocpypSxigQvF$fX_Q4t?R1fD*B}`X(KZ8818>L4l"
    "j~yL~C(~W;VD{eoLj)(*T}zE7gZu}UJAeJFoP@+H{^?EX8=UM-IeiN}++xW5%(!r4WDEr<xpomS?HGjI?So)Jst<)lRFI88R3Bhq"
    "ay7jLZkvimim0!<40eenReHEf<wR}ET|G%tUyiBTB~(mx4g+J;^vyZS+gVnlyC0kCz7}%*^j$p`tw@K*dy{&KN{FgR^)Qo>qGT}>"
    "W;;}kkTMT*Pvt!=fG{PV4^UQtP}pm@@$m2%gw+@fe6XHN^oo1W&#(4k)NmynB+HR3WJ?Ex8Fv2#+0o#yQlbHNFbZ%_^#T8eqvgP3"
    "q)-tqz3-E}c!pwAuRN=c852CCv1*26GUdUb`lJ&@Iel!sB3y<L_Q7e{jLW~XGL8lTaK53R1K1azs8jU>G8g-?8(9@|GWpM)V)muf"
    "r@rWl{m>Qt<M4QEiB=nTE-nL4N;ON<_VHtz)a4XzDlg1yz~Y%B;{aLf`C>NWP-n^>+X?(1uxx1sYzW#jihn=}MEN_rAk^ru!<V~W"
    "oYFsE)zuP+|D<zZ1(-#i4<B8n(dQSf3?;_I`S9rbe&!)dsDap4gr8e(Z28aI`92+_S6;Qi?ewI3RuN_-7KFtcxp(z#Jt?QC@6h|R"
    "m^Rx8L_N`KYb$S~EWIztpo$AVLq4wK&mPln1!ERY#vFqFThMBo!oy;TIq=DzNylB!X6n)t34ENn2d_D}n~iE5pClXVTdJvuI-&Z2"
    "ZfIt8Z$~(CKmi9~^23vk;xDjgG%;%phi`}cq+)8!^<WF+N@D&Ez=rSPP!yzK8(_>KSc;MVO!Pcv`(V5^e~P5WZ58(Ftj8~<w{<4?"
    "ihOCwO;qxH5}^Xg{S2y-C3_fDG9qf=a`KiW5hpY5O67}Y7_&}!yQr9R7MNL7x%iM;gd<}Sg9&yle43@hYIygzE7|7{@c?}@SdF=&"
    "Nr(64KVWSq!U5f2Ek`<O;H?W=8_ff}{kS)}Lzd+8JI)8Jf<^Vl6}G6NuJJ%G8k6ZIPi$MVV)CiB<JvsYFUXB5x%8__$pc9T0KD1w"
    "C~PETI{eIL=4W{Wr@4DNUJ8eZkc?wYKx)K2$A9NaiFlEtaz^H}_Z7NwX2c1ij^c2>sPXg?CN93k^X|iRQog@=m}p09_7zD}RID4E"
    "QR@2&CZ2#In{X-gfwyz`0hW%+x8uyXUN?^@t*6xoIFde02T!&;3+wrn+j88e<<Nd9Hq_U7TQ=NZJd9yE>&gGe-kT=JjbsVJSAk_K"
    "yQwZR5<3veu{H~ll*B4-O;XCvsgkk42#`c77!e(aki;sJS^t<D^qgQ0@EzhiN}Xih;w#{YMN+DA%xacOF#xzffByV!{ubx;#tNbw"
    "(XDsM8hyR7dTC{`HfU0CKamzYE<hgN13eC>T$7XP%c8@<N|&v`1bV;=XH46oD!$7h7)NsunF}i2TP^M>?+nPRkGxQPE^bNKgAs&S"
    "?h`LV<d84~hOOUMGon?n+^Je9z|ixab2<ZIPO#R%|J#54cMyTPAq|u9<By){Se5M%K&8a&D%A3XNllh{4W~of;U!)C?=in+PTSj>"
    "npH;f)~e>`<t%?K-P0ryMb0nF>1>K&1r#sx>FuXa-|c=UGM{=6qwk)5_fOs{Rk8J)A3T%6NQ6`wz%}{P<e&b@JMf=jiLfzH2hj8!"
    "e?2@oym)zZ`jQ<jy8bJmAH^Y=B%*RLm4pT%_hGsmqg=crt?dEB{eh2;(I2;~E?jVYEDj835WUDcGTWnbDcm%Rdt{xUJdT$#WfFg;"
    "+il*Yo``KTKBWrOPr|_8#oK$}pCh3MKfz#gbRD7jMN%4nCEj=g!|nnV(l2t&aNOXOdUxpfMxzGMLBU%9_LCstp<uHY)0uQ1$XW4k"
    "UJ~VsNzB~AuEV!cs$Sx(W&t>;u`+Uk=D_q7R8<HQbX#sN5X%k1(;h~k0gCn3=nB+N!i;Cyk$W!T-jzEKzl8M5(_K{H#qRX|h1^wa"
    "h=W)971wUw$Lib|`&{%mG*i4)kbblvR|_TcH8-V_n$vAXew7)Qd+bTl3!Z^kxFx^N9ns^-(SbME-+z7b`gm}4bavWPgbPE(zDd6L"
    "OO#8JDZ!#eMF1~lfor|M?A@v!PJu~bEFR$Z9Z@r9w6ZRVsbA<3N<)RKr!-s&$P=>whQffI;;ds%rXToN4DYM)2pAx3%yCsbcsnV7"
    "{`)Bg`$b^l>`%uatA*c+bwqj-BjlHNOTby^M>*eH!!!EOd=>|aKAArc#egCq5plp97>HYJulOJ@W@w?s7``8a)`I8uNt_U6yf1+="
    "VV6|z7ryFbK;X4h92q)t_Dd1a-szM#3{X%^?r0;%l;K1&249m`=4zwEXP%A&#EOpN@*^@p-14)7!;8VyApt$-9x`YjAhRhYVJrDH"
    "l|lpu0l7=u895Bsi}t2-X)>~h&B|Qqd4~m@$a;py#)Cz{Vi&rct0#iv84DD{sp}QU0AdLyVjgi@v=dlWPb?mYOj*IlT4UgK8KIe$"
    "r&CUM2?t`M1Y@N88BBGpy&e7D5R9S<`)|#WnJt!Nc#Nk7U`6gT{`FK4g$lSqwo!{B{RPKZ!#sd)V7q+VJ=PJmS1-IB4847dR3Od@"
    "D58WTy{O{j9+2OhNN-q50-a9A=tGz<#>n!$@;%@DJmX76@+L79ps0w1;C34d79uQq_PBel`qJC^{plZ`;^#`6>D&`Vk<l~nWij)V"
    "C^jh3dpS726zE#sz~MpVOOr20gnGbScng7B;0XlA9w28vqD6z2giZ<MF1{+7kFiy}0=_BIJLidNzvALeB;ZpGd1g=rHVeYbS25HW"
    "*(Tl2((#*qVE>CD5s083Va<1nRrS1|WEVDMV8x8tGp~dt_)RGoN}3a@_Pl@nSDhsL>|g(tdpRI$K|!u==t{<yabE5Kc6fz(wh$Nu"
    "aP9S@@1^j3WQElDt`_~BK}KUlnh3g4`J7f&{y97EYxE|GwAgWZyO0;z=)M&5Ff$|_VK>TxU9KI%K+B9;?$c0v*iV!Iq?A+%`_7Xz"
    "V988CKUI>aSwNw}Q-wy{kZZUzZ@<B#!kh<=?~|MuEItsYX&2b8`b`R-9&Z52NL7;pH^CZ>w;TRfkOk_8Lm(C{JdxEs31a5zQfe1;"
    "zYl6Us?Mso1}ytYCiR7a+XP^h4|<TYrqfe0m<JB*fu;Ote;@b7_gD9o(hj7nZ^pSxsBHu7h^4=NxS5yZaUm#AHka_0;&%@#o=^!L"
    "UiKqS`Xr#~5hgtn=GM|Eq*PJG0MwTH5krKJRh~cak9VaPM7^*@2fXb8MvQwXTj<2e_GGN3F%Lxp38`zJgeM(xj0V9&{3PJ*2Qm$S"
    "(&(f<iHNjFZUP(?FmsrhRY*ROsMsOMs_H?B!i+xXd4mPJE5P6=#p#9#;cdX`FPsquI?qi>LzB_f2w#iDVVEM8g_NQ5bzc^s4L<Yu"
    "dP1nw1iqF*NiWe)16DF@Q50Km_?8-iZ-`Agl$C>UrzTU>ChmyQP{#`Z*-TGofKdYATY}#_!Q!q|Zpb%ID3x;%yoQfEv6qri^d#O*"
    "{eCYDZCe;$-}UAd?JnUOe^Eygb$B2<1QY<mSRNEOL(^8s=?t)bCX0xW$4C{Lks0EWd+PHDJ6z7+6S?QOb$$8$4jfM`X@WmK$>ZH5"
    "%X$fF@~kKd)dcPF*?3uFSXq59-1G~YgU6Mq5nM;$=6xa31;`ZfcSGQXi7(bnBVk%UUc1U;M;nE;3)I7ktess>(-+*5#kXX%Ls72?"
    "#wkWpL@;oi4X^M5v@w0h)?6)|4*NQGL<V@Osc);hB_;ilNF)Jv><}07LnRcXbg3m4AL(a|JU1Hp6dna*&e8moS`xhbu-g!CyyID4"
    "2{}W$kx)Y}2`k6PAPSXA5<m0M8v#0OC3~$(5quCA+;V4x_%>`Jky*AAKW*AZDzA$y5!;ZTiwGNhO(;FPQUj$9Ou#7?AIg%^B;<_b"
    "qwx)V|GvbK9wL5TZT9^ddze|5aFa>nm<eF;^5w<h<>k?vLsD!hC}`qk{`UfKwG@tgW~J-<o}q|JmOwh>a7?~e)XfEY9;%P3cNJsE"
    "{ARwS$?%Ij_+A641lpnv1JWV3nG_yc?Hafxa^zbKg>aaS3Z!AUCz&O5Go`J!II&hkYBlTU9a=d13&4!u&0-R#g)&e)F6PD|e>gTQ"
    "i4P&cK!uG;VJy;?N3e8ViEfwlf_ga?0_CB2q;mjA6Apr+fg#3hk&2Eqplvvrg(tOAxooW~NoP4X&Z^O2{m421Gl{XK?68thO?KVV"
    "U&(yZnhn+3(5YD+N69-9G+^0e@+~$WMy$zJf?S0aLY6;*ugwv}3H@B4jfv-;O-wwo%*zRfc*2e@2ggS*PY(~6nk$*NqHQstKvd%v"
    "e0f_;WJukD>I=wIt4L6|QM7z>EQcRq+KpDLX4nnKqn1>+urlsUDx9HsO9pgt6)JX=Jj3|j3S(6F9tw)|qn2mn5<5FS9y~vTJwLk;"
    "oC9}T$Mt;~61^+w0GQW;AuW`mzRSXxCWT)spz9A4V^E0{jb1qZ82w$2Z})17q$;J!NrP~(bwx?(Xax&ljI3B-x)vC7u|*OY1<Ml9"
    "c7+iI0&EP-1Mdo_e2_?G9~Ky9IYwNuU?^&eI8sPYpTRaSs`v7$0rnC!XnYFi{_1caonlUe)3O2F_q1WfSZn|)isYTH@zxK`5w8FX"
    "3aoE^?wD|dVo<Z^!8RP_0h8`0ELzv|&Mk!<=X${VPzoO&mG!JzaCoO=_QE^NT0bvLwu*a1k8nZFdv7q%T^%LB$rUgHF6jZFm-9u9"
    "zn`MxWK@b`2g2_Zgvi6S_lfoquRJJ{;J&&QI<1ubxIJCIuwCmdrzdPz;Y0ZM_;+@rvGY#c{YvStT!|RjEtYq=y!l0R*ps0&YJqc#"
    "We}Ex;(q2)p)-Wd+B|9}h%H6*K~t<lsx{)Qfb<|c1aYyPyqmypJ<eEvUzH!oiS}V$0XLd>tdPRm*gb&7(~zww&)%66c$5)m(z&a7"
    "xi$uOE`cE)y*Sz*oL)Wc*(wdarEE=0t&s-guE>2rF$tD|r*7P9&36!gLL)(fCU1wxYU8a{t{wJ&j0g*$T~3ImfcZtcppy-S$U6(4"
    "k?*_hy4jJ^j~3Ff?UYR{>;dut+2(?64YU1)jvrwy5p=5ni=LrJR*A%+D8<@<YtXccy@B!rsN799@{Jpaf^G%&tm^<_1sj(45Ln#<"
    "2L7;WiOd<Jj&90Fa$>2nXQVq@3z2I8)mNE*%A#9N@Ly#M!@e*CYr~acn0=;2*fAZ5wxf}>)^<*gPR}lQXl3%SI-t!at+$v4RHKZi"
    "mOV7ExGp0t%%_OX`E+@AKjs@5rIbyS_NW<_v{+!2g{%!nx+*zS4ZBSmY%EJnmPHPI$=#SEMGcpJy^5?r66x$r;dB@HV2Eg~s%n7k"
    "X*ZENPzHiftA+KY9eGL<*ZT?jeN*M$HD^P8m&Qfy6{wcgYMHev<&{%+E*4sGHkTjY$fak`yw{UuO;_%^A|DX^0}_R?w9~Sp<7(U}"
    "s4v*#QmCSz-VU9Nsy2L?U`F2&A3&$yl2RL=Bv@Im7x+&-PHZSJAA%gtvhbhK^LJid4sfB~lYBQzd_z$rKzF@mO+IiUnd(;Xe=!)T"
    "E3)k_`cKW9kzzcjL^<-p*W|kwtP}>A73jt%z{GvY&XXW^xHE&G<<BHJL>8X-RQO^Lar5bvy^p~66MHb)%_nrgt??`a?MWEZb6UJ{"
    "12$U<jYAhtWC_V`JJQW)ZbeeC1z9T3XPbktQi7pJQ!VYT0@#nEm#?0pIdm2%$j%bQ6NEl*XicmG^+e5=N^zv&wERd{cI+7puvDqC"
    "E~gJSq*so+WGi=YRssPdA~`A^BQh&$EGtZ8V`Gt7>Wg~m#R4X{U`~vup?M{uZa^r-lCC<Wm94xh6op@VStQ*HBr<`9C?*I&C34W$"
    "8GLlJ94QvQZ&-R{GE;8&VmcMa^(urTd3bR2`h<{w0P0^=17Y7y9w_?YELFR45EsJb&$|1+$W2jt{*Le%kk%pi&r_lOn~PIM+zmRY"
    "lp(LV9HO0_By33_nlO^vFz^(AYdL1*$|7rJXQ4q>AipQ1VXQHA8?MRQVoq_n<)}8@f#OP=oYd^c=93U%X-_GsfNv|`^G?85BtqT6"
    "+YkYoOU8-2+^P20$rZ-l&hgn#yu4VAAyo#+@@DgDI;W5;22^`&h2K(DoM#6cT@GW$FA*K{nq6^Q2^)*Ws;ye9DlP;I{cC@sG+a<S"
    "TcG)<9h4Nd2l_5ve-Tgk^Pm4L3n_>)0~3s_kzpn97wE&y@CNu5)Jmz{z+aL6i*6y|r?{}*h;N=5{xbYwXg_~uI2_<_P<2dW9ezQ<"
    "u58IaP1vS-hWjzW+JqCS$kR{2$_!PVehH1~;LphZGq(RsJd&35@6`BrCjY$<jFe^rE{aT){t43%>C+#P`A6&l$q>f>H2Ln+?sp@U"
    "1>?Q)p&CE#{W86ufKC0~v%l(;wmlYly<h0TcUT`{cn`+vwWvIdr64hGOE#Hke#n_{pfHKz6656^z2};^)msBAE6|0)wa%%b?>LZp"
    "D%xXkm1b^L%zYqZt6#!3|4K!Z_`*?CEyf`2^W(Fh4@K@gFq`X{(N<N~s-pPE1|WwBc>|8=UK^Cq35vfhD7wR|3z)Mpm!q<vK?j5Z"
    "3HCv4e|b5b-HTka&M*61$W%t%9h4I}nW&?KX=Yqn>@U^qdI+G>Z@C}J^pE1>H7o@f(seC*7vP!(7Z*o|2iLzpJ375O=AQ2L;{=$="
    "0#m6}FH;hhOg~D3Udtc3Wy!D*u=^au?u$OaqP@!d<#+<<lU03&pa?IycB^di{s63=SNo^$eiGh%lF`7ZVG4BW%soZiQWdN)ssNoy"
    "1uM(D7`cZU3SN?dQSl4LA~ilGd5ziv{VtunX!Y&glqkTw<8tvYHN{=QVnBN*$v5STRTUeG6&WxHfs=cu^E)^gf1%(Lv>V45B8)}2"
    "o3n#jvJ{R&n8pK^4I0P{-{SF!w@>NH+4xdaOsF2vOU6>16kxDx<cqj0jxU{6vUw|>U;c|}O={s3o*@JU@4DQ~m|{RdRMyv^m3^38"
    "SCi{vHlxpj^asquBPupV#oK3VkStv_Nb*DI801J_w%7m#E5^!yz?9<VQ0jV<qi`*!y)`y<LFj}tat?l^lvd%hT$H-7j~v)vF|N<c"
    "rvqKg>T3>;A!hrQI}cxDs=D00h3Y|cfjLNYZ_WEYRBdahd9}_`8I4HoPE#GTsp4%Yb`Y&46-cTE+*8gM;kW&c%al)rV3DN42JLkr"
    "O3ywE(m*u+pygk4(2Hga_*;RQGx$?Rjd5-PF~#+engdWD0m8CgDlWnH3Aq<}f~!+6;@SvDWS}btPkoOOR~xTJmE7N8HR(pH;f*U~"
    "T`y6J-CoZ{$(I=%fe?j1uzTf}J)_3`G#al`vs4S#;%$$IK?6s<MEuDL9Bv{5Iok5UiH|q{Xt<a31_((y5W;o1+4!@_Tm5?teY+^)"
    "ZEJp#>gZGE>=?zm@lITmM$-t?x3<C~f<W<2Lr*Y(O~G_;^=}Z+juZA<g8vIaq;9`o8$@alA-W#P_F?s<s@L{M@za$|c(^#cI=TQe"
    "3ak%=UDS@lO8jWfu`100tf<U-ABxGs2=AsVnV1v*??3~<P)dsMme|s#l&jKPbH5qvvz=zo{Bnv)2|94l5={&@tXI;t8V3qBCP)QS"
    "v}Qot?C|AbV*(B~Ee*344b)J_obNml=>+IYrGPekfus_>^Ry@B<2@KPF9o&{w<9CLB*W}`Ke+P!XY~KDR`dVlN=Thp(1j^b(<;=;"
    "MSke~!N_2Vsbooe0>X;{NEA`kpS6IP$Wm~~7<<EfXn+xQtg{71@)f`^Y>_4y{msBYtR)+O(Kr~kQHN0^MsFL}9Q`ktgO6QvlDFIj"
    "NE&>9#k@I+-f#8|;hsbPqGD@RrA{N!>2h#9xcK>caC&h4)8OUdB|T+#4{1!|G=XYJyy}nItbQw#sc>G*qvEVE{wt2{-WmJS-u)tI"
    "!ZtL*w%!Vu%c&@oJX~T>Ivr}mS)idg+dmo{Utb>XzrHxS`q>6150WV9#r=(tL$4`#vPRdH%jNui^&WtDUQWu}ik!vTXV3-C_2uh}"
    "H%D*IF0P*+o*uq9y0YO5!!(I|r24EyR~A{|CF{|(9y}YGEcN50=l3^(h72hanzu%ipC*kT${^3$hUWO_&C%)0>%;#zKRmr`5>hU@"
    "rBMI_!$%!T%z@8Ee?Pj)dv&Jo0PJ~Qot+$BADzNp3{LkCug~EaqXW&FE)reE)NB#f8D25n47+vA7nr{Lv1}~t{Nn8V@B+5~YVaS;"
    "b!ACoS!u}F)2*f&90D7Nkte{Y+b{lot)_Iog?<`}+EiXC0BG?1_)xf0WCJnLK8#_!HvPfZBvOSD>Uu6cWabMp3*cI`L44N14;mzF"
    "U+TG+>3V6?Rrc4fGVOjvE!2MJ^VX_*j~FbiwN}wo<4UJxbuah&;PA!a#f5M;>NN+lN#D2HTg6;E7Oa`lud`m?|1Hom#^x(E$g<HJ"
    "YsMG%ny-52vel@2?Jq74o3tHmu<U#T;?BPUaf`kU-gBdkrDN&th9ujttaS?}U1Z&g8!v6VWMtVCp>)j|zD>4m3X7(6I66TM3dNFT"
    "?PN)}Cb!#(?dc;dmjbc?HzTR{E4eVZu;z%8jiz`@t`~NCRSvC{g8wdy8EE+P=JF0NF3(Ou%h-qGd31FR5VTIIATxP~dOcS?3rPzT"
    "!tq)pA+bri5udp<Qf+MZszu1v>jTi@uaD0Lr`InI@rLgB`ZZ_=&o7S-j{awxrG#C;a)0$Uu;GTlTKa@cA#&5o$=Su#%fZXmDUiCq"
    "1GqGCV>0-15+n55fDT??oe@eK5Qd#w?Pu<-PQwl9)6n*8>in6qgR5HlY&+D#<1<h`uMRIxt`E3NS%;0FU0u&`QcmgJ_1K#sG6Fa_"
    "RalocAa-<$4Z=^a&W;bSkB?p)ZU_K(-?nFwR_>Rr*wFJof58%z&s(z_1TrXn+VMNXd!yzw?QV0PhQY3cK)qNoguDsl&=0Wj4C2$K"
    "Ns^?!9Q#gS^wc%}E^Ju3a?w9DjmQ=AXuZg=fP$n)X5YGLl20uW?C?lAomfq$-|d`A2M_sfcyN09dT_iJf3E4&GStB48p!xJ*8uka"
    "+on6B?ah))I6QdmT7ztsO@^u-I})a|@k_R5MUKg})gA<X+9M0tUKGt^E-K2p7G?UzK66n?Yf=3T7iCPY7ZrtRzt<1ji%Ob{>cgVQ"
    "zxA$synZM_ry2?e_H8j-)K)8wzX}dt?{oQd{t26c^HmW&6C#6KmH@mzFl=L0B<f^EzGy41i&GC9ZsefHb&tSgucjPCu$Ydp)}zR("
    "Z^SQ)(tgDG#0>(4^VU6e1B{*J?7sw<JG$ZlmSX;05aNHh^q9C}7)(a8OLA{4FPO3ATKREdk9jmX(Kyl<#H+yA7rgTjm(RfgjXikF"
    "ml;>n=OyNlVnibbN$@%sjr7~elJcSf`Es{t^ATZJfG^Xdt}aLhghiP|&Jo!K7eABrT9%VBRw<!?OMI77b!9j<M;<6Lk=5=rjTE(4"
    "l14FVkV=CUJrj}RT;zjG69U7fyGx~V7?dKIl|d%vtKRR6$r3d-yfL7(81tILK{J$Xjmg4i%LU%J)_;84LoCSgc0_99<k3RdQ>o%;"
    "+TK^^X$4k@q)`)?QpkoZ{y^cU?DDp7HE5ii9jq3vL(nm4T9prZpw4_;uk5LXvOxG%44larOoE5q<z3W9Q*uQZycY9zM768hF(b#~"
    "PU>n@I?B=1MvNlSn_8WqSTYL{kEfLHF1S<ik(-@oLDnOU8Ow@43xXiBuO&}$qXANp_2W*3SWCBC?$EwYdwAwZyr3O&aW0e1af(8F"
    "OE%zc#Rwyw%F%^p2Pf6!hm+!?Y!$pAO9Q0-0GK{BM;9H}CnGBOiL3<orB*vlfA#QR{N@_Ar69jx<cLjg|7`BMAKJU_r@6iBhmsl_"
    "SQeQ|OtasL8jNjl5W`OXxBvR@{>s`4ProK{h&?rcvbOgt(8ke(x!x+tH}9Apv#(*BL@gJb0RPKmYk=IKw$fg~YB||tCq!?Sq@@zS"
    "rwu{*we=s_n1(_Xu%IA?D;C5hUA)0miUOxnv@Lr$X{}iuX^9`w8W2D8<yek+b&rh<NM}^JsFa~2Ygd5O{?8@mbc&etTBKIaFuC#H"
    "=?SNN-_Ql@Ls?L1J(&(IG?yO%3&^_XCD$`7XiBPLG2s+L4#z<E0!9tcQ)<t^6;KGiYT-R#@FxnE8v=u<f#$-xg-SLcKe&0+`HKJ-"
    "j>Y5up)6<g2npaBK!Pom9_M1gTuAK$7K5&_G!1Nvs2EasV=TK{FCWBODpC9MV9KIygn6yYn+3LWz+@?m`j^$?cmYD)5{s{Kl6y|Q"
    "ek9B+1c<y8MtdPj=~7=B)%4BcQ2fzP^Gd&7)S`3`Mwd|F*^aL8*MGVzmO%LTjxNvms~wICz@USt_Mk+1xTv`py^u8-DYY}9_MLi6"
    ">ZtMn2V}?ZC5aqtK<kFh__L(zKZ{y`V8raP5d+&m_5EqRq%NvF2r4MXn@-x0*f6fGSzwmUSkw`r&Gvpm%@Bid>$248x0q-o=BOqj"
    "UYH25nqX?yu0Xq_IwoW;0e?ds`lwb)&wD{d-<U+HI14SFUP8K{t5_K>BMdXn1AR$Bbf%(yDpDndZwKo&Q|K&<0+B$qP+GdI=|;)&"
    "M*a>5-VCXVohZvD6T;16P}tgtlL2MHvs#y!!E#J%C1yFf!{VhfZ}6EO)Si!+9GPHNV)`ys0igFOT*wl?P2Ed;D066GN;u!5R#GFO"
    "7q4-I5Ve^sXcS2j_NY^`!Df*p)RETh0(e5g%WAEeWe==$Fdn~DoL$C5a?@9QY-zsm_jx(T*M+(E1)7Pnn{`~4>Ri=<M|Pz=Q?#PD"
    "Ygd$P10jDmFCHueN(Z-ryjWHaxRs-<MpmKFp_b2HnQyy(_PYF5)=$=D`$3B?Ks<e+3Dekqk)~#@-##%(Yr(4Gn6YGR7!yUH@xp&n"
    "Zzom->z@ADtVN-vPb6!QWsN$v4vhz;!`bb=2s1<tR_-(%IGkkpFd+}m&&<fCDAuX@*3Nv&>H28vv(mlAa60{;d;&X9p7NlD#$7Ee"
    "VnZ!Pm%B<Q=#}Q^=HOR~Q@aO!yAj(_^s;NqmiD>&YV;$I&)1}%gy|>WlztLPKmC8u&#y#397hI<?9VhTM?|z8Uv08#Xa)@`I_xfc"
    "cuV>+@A!_cci41tg;|gCO$@q{3c4Z#59^?fjo@QRLW<~`H55NbayiAnrPY~LR7#r~KA>ib>IaJ<^pz1BzSvi>g+#n^NI+76RE;G|"
    "9yT<puq_d{)SgU=TctL+9yqn<29BlHtO!nLwcmgaiRGfOoCKONdrT(A8LEFIiqu=Qti`{~4R3GP7c<&RE_tho7d~CbY@_yGAmDT;"
    "@O1F%WSIg^n)p#v&#*QOfFzWm4`D3!#pb6RWi!AV5tZ9#vnk=iF@IX^reseZ;nw1&7g*y3T^ago>Hm<giAXKS$F=-Q_&bc-Y08)u"
    "HJ#h0m>6<b_j#BLIH+a{8iS*G@d25=EUUXqB}m8}ZOFKZOkb7O+J}2{>x=pw>5c*+zXB!w++E39^th$q^3k+pPrayiLG^fvm6~a7"
    "N)ZnGQP>L`2VdkEigJ#n7X?~5p4))|-CULjQ6+v30Ly{{NVt)-8r#K%Ps^I)e|NczvZ|Vl+ehRj+;SS0A0?^7sSrK^Zlci>X-LE!"
    "j|fHVS;RNVS+cV7_cJ*zI}xhIx7}DSQO=h)B;h(>ZHUz{_A|dn*;Svptqnh=dI$&o4A~8{%Sz!BIlxc)EcLpOzC&1Fu?)`MS{8Hc"
    "{aB9p<4rV`Es_3GO`%$wOw29VX~h2T5*<<49-JvrQ^H1j(vQ=mmj<7O^&iELLfjYd56*~Cx(+pbsJ*|G+>2S}zFcCZ*RxxFmK2(V"
    "Kkp0W7ZsA-u$aEdheWO79le*_SzEZ~@SUd(&w1SczUevtwP^NDt;rIobu6f~Hh(WcrX4Sa`yBM4#Z{9!FYxD$#t>Kh3-sT=7*9W-"
    "M)@;GfHasO#V%HpB~@~yJ8o4%hIUFM0Df&&bZQmaCK0IgX~Pth*~aD-hY8u|NCx;q3u8cOsga}gjD1nqTcFZCl7-9tMp-*?kw*%<"
    "B3@arh@%cr!Nw*$7hQ^iNyof5_+(;9SykT~iyAGcE}1Ge1lonpVWnc19zrha;j1!t>`uKcKL~?}C&qV#qnPU4p{S#$QZJF7WwpAy"
    "V)jgUvuAj%i6wf8m0+<=r9M!7F0MI<Z=!x&k?XoH9yQI3%VL6oh>Hake)|>Goq;&{g6ANHZ3J8V`l~55yUb~+D2Og$J()59ivMoR"
    "ZVbBVQI|P-2Xtr>kcP-yW8_;JE^ASYhvV{gF<4-3!{KD~wPRV#VkBm%^%YG}tepr`Kg@txG#vHf6ZN{oCOLqgO5sAmtL*_BDhpWT"
    "*{#atkcIxcUm{f5jAfvLVC~>4^woe~QfftCTm;H{ziOdxLF4bu<}`GR);I)TMf|!>0o}*dQZ6fgvyepqx#nKS+4$3U*h}Nr7qcea"
    "Tj;N*Ybd=-3V`MJNeN*==%Vz12#&-mvBHC3S5m-IMqC<((>BBf)4mRe_Gw`%fWdeoij92IpB<bZ@Pufb92fQCywC-zLO;$rv%Fck"
    "GefJn_J#-<1--#~7Lka%JGeS(Jn(yPsuHRL_TgkXyl*`I(|5-l1PC;h7_OW4SQO7eU;JC(f6r>ADCv5Bam1^XJ;KiC6=xWPX{u8U"
    "s868M(!&V;PmdyYM^o&E_X;R$FnN5#V~BE9dXoBtM-dpTRic9H>tjlfXpR72y+HTk)jh~IQ4-DX1@;@4)b6VBO7dx!_wZ_Jni+GZ"
    "QH^AL<qY(Pg9RfXj6z)CoxSp0IBn*{-Ze>ZS}JFu)W$mFerTqwVu2>(X%ch31|Fza+yLlM=K%)+C&Q4RM4<5OW?bEozl5+DB^-h^"
    "(&HXVGx9`&L)u&(6LE_+L*j%s5D}0qxy6d_TQFl9w22G-zQn|;#j?GFiz!Fghfg0sO%Y;F_LqH_h|ae+i{~nBCY32tZKP|QuS2RO"
    "d-?cS$nyK)3S{w@(wl_>l6gxbM#|=AZ`zgFOm;SzpWPmEGXqg+usNEHCS~L2psGQh$x3y{;-W?1#Ke3gsYpd-DZqnRj@XK(m8o5*"
    "RoC?yaMI^RU7k>IAbWSIp4L#UrxnjDZcJ6MzVGU*?Z}QWf`CQTG2MKq(zPIP5E6<?%(Gk+7;MFwa~KyFTEvp7^#ZYLZn)W1R|aK~"
    "+*3iYo0mdq=89~xP_f7t&a@J7+ar-bknv>Q8_)<ie4)_L=O9k^!`w!#nupNa4>{6To~H8ggkp{r0f`I6Q8``|SJRV5sA4CidL(>p"
    "U}yJ>nB~)ra%Qhqr_7=m{M<^6)wgICsA|i_{;iDOw4!4<deVC1e7vkL7k91T=~W}j@LE?~v5qM=2Xsdu>o;YXcE{#uAXgvf0akP0"
    "bY~l1Rg;ar!d((E$aQCoBrvN)aHLg`ty$J~ahcD8Ph4kBU;m1$3NQ+Q`3f2PuA-NP1S>5jE^0{2zw~!OASK&!J}M_RKk8)hq`^{t"
    "Hp>bI0GB}!5(x)*rmGqUQ!feFC@N3C$pi=NhdQtuBan~-sd>Ku@o5j97>{1t!zCKJ{bpV!Nxc2ffL!X<-vV?2;C?g1vbC%~l)NW2"
    "3TJc5fN8x%?e|u7i0o1Jn-)!D{uQ&Bs5IsY8>sG_iJo4Rss-;GVOh3;WE{!~dPz#^w49)8h{pVlLDDqM8nzm}4u{#qee5gcwE1E+"
    "F|E7Q_2SeuCh3lyuiB%ky|);EeB)&?;~UeV(qzTn%U>*-w|=CbE~V5ZC9Qc#tf#_yB^srkGW*4R#MNMN-gfnX`=UOu)av07ROIRH"
    "tyyU-?$l-;EQ3zf7|?ElgN+K2xy<1%)n$KQ%yv4RKTx<`7Q~$53zD<_Gzl{>?c^j^(|vn^nbxoB!~djPtRs<TPZf<K5}`U+`s{Xp"
    "ABohqgt1gW9DOo_hE>TDL_Fz5F9+w1XjVtD!p-W~eJGJR(ZosY;~G%33`9|DG4kn`*R<QUKu`QE4tqf?#ve4ZYXycc7hL%~?PZBp"
    "z_fN1q+uBJh=q%18dq@?COxXUATRFqGvFvekE|{Ej3Scs3qjb2k0p3^1i}F9eoD)DmZtqQ>P4X_wuPlx_lsGDH97x6JEzUHJnZFL"
    "l=U-qB~JR0wJZIuP1(M}Ut?2}JiwYC8*WP8wJA}S<-I&~ZAz48aW8UjN*wv=%1ue5phvh^xhMT3@533|U{7LLY{-Tl&jE)J8{dgz"
    "7#TyHm-Aa>1H3}4mJvzZU9=X`SJ7$0@t1^sX>dGm)d*S<vtqw<(Lt(eHoiL-PpA~=)zp|;*AvoCGBxiD5riee*8~e+7mTCP4vIhX"
    "B7MPpu6lC`1-4nv9wf#ksj7OynfZ<1>+*+iC=Y-}V;)iusFv?3A$OvFZ6FH+slq;vA;{rjKQp~vs=`b2Q{^HIc=A=Rgv@R2cqEI-"
    "gK2?<>yLEAo+L<d1}*s(WX6?di%^ri`$R=?kb=Y`$%Wmy_?~F6(8Dv!iGw)Gfz?sJ1@ktF0yV75D71L{AaHtIfW33nqY05teIT<v"
    "z}O12I7xbWUze;gCAp;IHh6iO1Q~G3cnx%pIs1v9_wyb(W;dU+Jx~%xF-Wv1ZeJT2o>BV&Z%|HT+PJ(Br^@H+@}ha?C!a^4B=PpO"
    "UOAf#3}rO{*51qF_LUYN;94otJwKtEPm2cX4wiFt@|t94Z8Tr<p>`$j(#W|karv{rHmKMAu-A8g5&DS_FE(KczzT<R$Ktqqoz2hm"
    "W$wDQv?f$U@u>}`;kwnAbCqCEyP5%kei7zr%O51&pB-LaUY_YnP5rR%JJ5x@ui`yr9K)r&S){r{C(H4onvF{ZjVnaTpiU8#ptVS|"
    "TFGEMmQf2@Zy=>13$lI+l;0VDrN(H*PT3>Hd6dR67l=ilBvx!aI^CzbY&I+uQT6B=L`lmQWvlWkf?lp#<p<3Nt<Mp6t$MA`97SJi"
    "5%|@;HYa>R9!D{prY!FQG|1At52rZY2w)jh_UY?Ph&5r4&Q7V$@WJ7Wqtn9!T}0PH!#T&ec|Ty6K57UjBGSIyK5d5`x;|ohz2tUu"
    "jTN04p=Vw#UojSw=Rp!MAH2Le+yBEg(Cm4WI;amM_5YgGMj5DYfseDRSBDpHlwM$as_wOYJAh=lP#2;OO3{}4?}Mwu!3EN`lkc$W"
    "%Y`k20-TT~L7o7Q%(?&!;V^Op=z1`NGz)uKAA!9%JiP*j<OKGDRG@FZwHIeU500<6Ao)>qZ!e~g#TXd(KYRG-o3ZWJ=jUe^SJzh;"
    "gVReOyynRSjS(9=|FgHihTgZ*ukkHFdwKTe@ZuD!;&pJ-m+1PVev#jvjea2|KYx7*V&d}h`g}kw0o`Q!9Pi#S>STsJ3g4ICoM2UT"
    "@Z+O@e|>a7CEu<O-%z1KTd>Iz;~X=l+G<RGQ<BZ#4jp2@pMXZ$qnn8ivER?4q-%>?YIYDrc`u>~WyrBxgVdMw2DZ@XOY<;iPu*BW"
    "JX>ELU+sH3np%DurTwH2YI@wsb^B3<&Y*rLu?9gu43kY&DlqY)eg-<+C%z}=pqOJf%qnQcb3-5aNe;FjY(%F@80B#q<oSxj2KIXt"
    "WW5dLhRp8hq>VVs$#+M(ymP`h1^Y1U<(nZaNa83+dhE`Ydpnqyhcb;rJAS&N;K?S9`qW+0P}CeR`2j_XHcb%Ma5;6t+a&NF{jdEn"
    "Up0B-bw42Y=4vpSQ)K<<(<dtdn5oGb+=Ev&=VmVxaTiR14BBtsYG27sf0PTk)ufW!^3d=D-RP5lICXRgmDffC-HKEGblUFY$<=>!"
    "&a}9l7Po>`{qEf8$GH<f^<;Zc^%5g+KrdStobq0<IY{)>(~Uii7n=ixDozt`_}SxgT+yw~`qmGtTRzBgx+W%6+E1%=u(O@Qs$L7L"
    "hVNUEC%<Bpl=gETl#8O`@{`!3ti-xl!s`p~arBKR;KLt;W7SiaiKu@IPb~cN)#35kJ_h~%u~olaxNwC#Ryce8w{PVp>a<e4VS8Vd"
    "A9Nj58TMg>x4{XqV+S*Fr`ZZBO#Dd1)@&E`CMF^-Vn+`KQMgIG(-r|M%BYpz%YCz@wAh`2K}N5pV_B(wUzE@>tMiL3a1ywrJD*;0"
    "(Wra_w~AhJ2Up40=rq24yW5Bm*Ow5*Oo-aj_^ELlsy`Lalxz8ueGTs@Qm0B1c2uZyL}GDdkNuX2fa@GY249JHTtnn5!p5FII`?0P"
    "lIe+MeBBDFu|meS`jR5PT5+iDnz!!a!$I>y6|>+D^)g>IqZMRK=C+|$#wUkuFuFfn8RvEAgtB`uig^6Q%{B(3_XPz9jK130CC>ZN"
    "b)a2sZ`42i-4Kb%eo;#qb?%MVy4tMBcj@*K&UQzD8+=y`A4TCKQ$9JdeP7ha<_DrVtH~Bb2_=B+4;2?^qc4q`Dfs6Rl`uqGPNa+A"
    "QdE3{y!*x&3h_)`vm4J6c&62-gYp4OWx#8)6!$+=w6CP1Ipd<97q!AP(uMVo>?|XL{hQCH%{Qzmm=UU1RA8a&B|TE;uY~vS5XaR8"
    "ijp`gSwR7FV#OmngXD%XhRyw=4w4({$heMI^VX}KqlP*(O(t?RSP5kUf@(IcRiTJ-@e^R>o;+BA5mj+)Bmj~{EiUNHA&j^x<i7ZX"
    "t8>zUp?|(nTCG%IiC5S<a3J+ojxwM(RE85g<!(TkQk2-}-VJxNJmJsi*;{kv24YsGvH{({7N49?fssC%ajuQA2Hl+Z(?6Kpug~O&"
    "_7q890`)8vV)4;wXICqFted1F^&M&ptg3bNvE2KT$kjGf*etcDayPcJ=hL*j(Oj9dP={`21T1neDaMa{%l_9kol3=DvX18S)!L+d"
    "yPMI-7+9I_cT!B?iLM@`E#KzftKx}1J7B00J$liejSb;Xsz4oDno?;zRr(KY7dq$-vs*^0dWuR#CYvgvW50&gfgGl}-8bt*|Dh~("
    "Y=lKkuOgo^J_V=iY-uHEO8&qNthikjW_$*DEC+FPLEERuWh@bcG3<f(7Q32ZbTNhGvP#$4r_6jJt<zoZHHN8_Nl0oRWqMkU20O#B"
    "Bb#tVS}&&DE~>8dU6TwB#N3U9+Fs~qf#%kh!*D$>Z8FZTF!1eSytfVJ9u803QQ;bt=dC#Ots=mOD<i;%pAi8*lpi%hz(v3p(VUqr"
    "tyb2ZG5rM@(Vv`7tiN*Z?VI}S1AF_<MAmB~msch5ZkDNQ_{LhPy1}YU-M;wFoZgX}O@4Uu9anaC6n?VG%b}%>UQeMIa_vA-M#nBn"
    "V};M^_&m<awH~&!aLsJ+fk+2!W&tBtkeT40lOPTsJCG8k{OAgpUIP^gKXG9xjyA}|UzuUPK??cCTuS=hai37zF+{8iIio+|NxPkO"
    "D=5SH+9mZ)r-CFOIG7jS{AF4xdS0jtY|FTDX?R*$d;6Oi#JGN4g)DXGy6|*Nu5izK(FL4r2(Ek8#x2mgm$up0%|5oP;C@k}hCTK~"
    "4Xi6nS~ez+<222B{k{Q%@srhRxEq8QNBaXTFldb&X4aksY2V(m5X@zJ)INx+W}j4SrqBU;5E?fG#^2pQn^;eP)if5K<!RPj_(os~"
    "&h4$Iq7zdMRC^%mHK+{`e{YC=6@Q^AL5?iCxT^&w+l>1Pk$z-#$CTrWHuNgufdAYK@v?4(Ze|`QTR>$xP@O1lWuIGhI$eiO)>r6)"
    "fS$KIXS*9>ubnMlJz3tGi@IyA8#P@$YPyo2uK8F<b2}LEX5pQi7Lao<Koe!#!7`Q<b;hwpo&4v9bYPe;?$LcK%-CL_{JWdVOv7jG"
    "@KFPQ(Hf55SU8o8X)^s)-v?n5#0};Zrg6W;wgW#-o9rt}h<{NJ)za1i<@kH92@H);<1yj71}6Q+dB{FU=~`@PE~*c?6}c{cG%xl~"
    "21lo>NDIpkI|B{|SBEdpE`DC6^Q?#`I66HzdUJFj8_K%&yTAIp^v#?FBTdizs`WF!eS+=Wx#o_Qz<|Dq(@yXkCu3ze#s<qvRxdAc"
    "FVD5MEf>~?yv4JypYvQ?QR-N^HT*j^{Myp>(>U<DT=(Y^mAJlNiS1P%Htzj(Z}qc_s~2a-M`tVdYu$#qcFdN0?ccZ9IY-HtPI0pl"
    "xGf!b582iB$nCm&-2%PQ8hE1)^yY5t=367TTiIBF<&B_jV|gU947SI#>(+b=EC(&J2$Hr@_bV|Tfc+gnel;&ZrvP&uA+mAfxa!|#"
    "asHa!P%nI|#dYd}8*M}2I}LQnoI{fiqm2g4{q;P$D^<wJqg`-Cjd1i%RTKWa#@aU{t_EageRsenQt!3|DE{>TQihwiL#h&m7e3t*"
    "zU0?~Pv$pl2~qm%LDY=P+(P!Z?i<&sTPoGwG|m0ZjcE0{#7nl-SWQguEtHK8^U`t~HOP4%x(**vVxuEUw!wycTOuRhW~3%A!nOs@"
    "$$*85Z`hn%`&*D}gEp=0&Kvj%g0Q~{TkX44-z3k4XVi%PFw8#=r!X}(85uIPovW_N_>z?~t*chb=&|`^3uDi^uiT0r9k-v`*g`?m"
    "U88<j<<50lDI1N{>4n(Z#_hbi-D>%vYvVUvez^5WP7$$g{a;(uH{7e`yhf$zvvy&{1^&8i2y^=ohWR!uQNHccG}e#QWg36RMkHTt"
    "BMkZMaTvkp3u!wZW8GG$>NbiYrdvsC^}0)o*<dV(Fj|8E*G^<#vJ=*F@&;+9E#4M6Ot(*;oc+y2Wgp!iP!>eAYuTisRqC+u&~FtE"
    "c0~Vwwen8dd~O?Te^u432G-U1;??Cq;=1d(yj<^m$62*X)-cjYp=w5h24F@_qqT$UTYgci#rc77Tp18ao_<%%Hmgu%)i#m~*?1bO"
    "dXx3li|PE(=q(;JD~~m%XoIR+7_7&wLRJulo8n3%I1V>ode>L0*RQ|w)BYAHkl(Egmil&)sKod&y05N)FAY_Rzv;XfP0dQGYhqP5"
    "jYgHZLR64agF>;pG8?GztgkZ6Z02S~m~(JusG`$bq1smTCacpJid`)pG3TZHC|fj2cGuu?Rx;4hMAncO=0f9Xt3LZfqlWVpc1Bw0"
    "VT>HFMn&o7n<|m3W5i}n^wlrr%vG>jm0e`JS=CyVp{E$v=KGsgMR&qH5NS&$((M$nO+S+Lz}K(H^|>qsztIw11GvN23zcJKNwfR9"
    "pt`+wx>e3s{_s##7cM616(a~wKW}`mwFPufHowLmj<s>7=^e)iIQ(=i0Miv9h-YhnFyC^FQq2paz_I;Y#9YjQEga1|kR^j#?Uy<x"
    "nr=GPbhF7;V8?>TF`;9&j<*)t`Mh$0jrXP-5s&$l$bUATK9+NGj^lAjeSg&^IzGunK#mLQVse0~bS<DHUONC2Nr=svRxEn$L|qHo"
    "d@8wRJQ1}V*?3b{f2PZwwqi|1n@uZsXdk5R-E{ug$Qe3Uk&+^&-U@2OOEF<x>;^K9KFNaE{pxg2za5IVW6*EyoFcx62q=7AN5$T@"
    "qGCl*;pZ(wMrx^uGYsMl=utDWhJ!;evOZ-<9l>TCLd8+ZX1+PDCl!JD{g59SpK)xV--~Pvs6Z0G*N@Z4feCXxR2q{iv8eXpN9{7V"
    "Fq9E;eKet3tUCYM9d-RJqN`<)GQ~}!S^BCh#?m3$2utpY0$%~sSC38JAiVhNM2l~kP4Qdo+M`m&8vWRtHD_h$|HFt%c(av4HN53d"
    "qNi-=vkfUti1r7~NBYCQu0`A~x%wa!_$W?#i7YaN&CR&EScxxO-4_$-hQJYk0ohl=8+;=qgYlitiBhSaDwoq+$c!jX=)~TIg$~r>"
    "cXZj3@2P7gC6OC%aSm4VHSCM~fo~o-N6C)n3U>p+n|x5P^&g?&Z_a3)cvsvt1C4`<tp7@bRXL~dJcXkr64HS5lOXKKK*d_q0p+1G"
    "WDJabJLJp%YvjFu8@qXnRL#}SwN3Lh+g>>C++wQ&u;inQfva2twgI-@_I8XQ1@Cv>1#oV@vR0BCO@1ZE3H?~ap*d35K%^mOvMvLC"
    "h04+1a^~$|@KWOcj^}gOgw3C{(DY_g?$_3WqctT0LT{D8y6F?<d)|(0;lBC&Z>4$D!Z$7I_3XuTuDq|EnO<(Y&KP03dJH=7=K=xy"
    "*4k+>u7SduD26P#2tjJ9+_kkq5~$wpda)nf?0V&5xDh>w3CreYP)!b_GRHnH)BEh*zg&WdWD-(?r2bwSeGw6D0{mN7MGvm>Fqj-R"
    "e&?$c#pjI{Z;hHM23Cy}els1GorWDnQ(93*X5ExvS6op0t6o>tj&?;vl&+xC6#-{`#VkLUl>*$I==AHN>Okl#dZ_Pzs2wF*q(Dk#"
    "5vB*+bgbU56R}a(xffMup6R=g-F6#2SEyXGi5|T32YNtRZ=9uNW;zw)a=yS4t)RBmRyMii-!+ZD+vS-5wsbw3dr`eFyX;I_D%VE9"
    "=EBuoBYT~mpP;u?bP`dC`9MZzSJ#8{^W&ra!Smxo5maX)X}Z4wnzW4D6iea%+gN&QTF-b1piQMk@ev*K^7z6-otiGxJEmOGp#}R`"
    "n+>Ol&Sg^AbUvykcqh8h!%(Li>;NM&!121(dhEwB|1Z68dUSNvcpl~azie;b-j;;8j>)1h#Q*g<VSK?C9%hw%5-?Yd-@`b|`u$!%"
    "RW&<bx|2is6xt74*@BJ7Dsj+au+n+@SF?RhyKRm2O}k+Y`Gn!aCK<VU<FsV6>hPkfxQ(k3*t^nRbv&?jfZYGy<6;w(@EO9Nx79~G"
    "OSCZv>+j|;eh*OJ-|d`k`n4vUuATA)j>Q{iLkL?KtbKjj_(0cxl}4l4LC1Jv1z_=Iv3xN>pF^V$4<$a!a04#)#(x>@P}A<#JC2q;"
    "U({QN)qsn3{~uRzO6|lV$CR|v<=@|%HlFcN{PO)~RVuSM&9niAt0iV&wS)u7-1e04QsfPsRSr?y=>Jhyv0w#8mQ|E5dKh`&f$m-2"
    "&SfPKwAyPhWxeI3a=pFtgcUr#;ZX!W9#6$v)x<-U#Z)@PyC(IwUTc(C3q*Z2kbu}f4jp}>wi;F|CI=lTC4pUhtuG3%@kf1h^Qn(A"
    "{s?KEHAt(JB-ybqbsUCK*;g8DW~&FIW}G(ef2P{Uo^W)?2W@{WRz8sh(?w-&LlvId%@<m4zTI`WZ>$DBvUNB&?OD^A$!d0FzB_0("
    ")zR&9zV)Se3Hx)43a{vO7yNb%e)4=Alz=s@rO3e2!QxN?PItmV5QEsJ>K*OS3LeyHH;s*IWcHY0>W4rTzSTVYXmToo2<RwxR;Iiw"
    "f4VOx7!`D}oSZFzmz?T|*iAoaR7!JSt~xpZeesEEH`XzF*T_yT^k%CukTk4THKmd7FhqBb9!0L{wCZY>_7-RKAJxp|9Nf<kYwKdI"
    "PDi0nX*cK}IWEL~Jk(2rmBm4e;eA!UFO3SJooB;<5-YSii!pV+qoA;&%*`O9CYxvlhUGyR0@tTY5Bv1DUd14?90UYa&6`e+SH7L5"
    "{WwGOMc+^ofx=$=)D$UP2vP5$**Af2#Egfk3xd=M8x(0Z5m;07pT@p&45B&*xF)ga&1#a+F`)H<Zi668?*GCi_XRSzt%2}!Jj#2G"
    "FlDBAtwKLZ?9ne%<HwNc;QE6sHW`Mn67$FF1@%a{9vQs@LCaRT9M>a}zK{lS9NC@nu2oWblz{FNTjNe7@_0^iL1_517W|0|{-^<e"
    "3i>}~)~|xUA4O^0f<NhpK6Qb0!r$*_#Niz9^PCO%^A`N63;wtPe-`)|T|=&bKTWeN%-Zm$SwBfT;Kw^GKXSv*b2i}bx8ToQ@FxxU"
    "^B|4<HTcisI82i^{Be+{c?bMS5M*iUhM(uO;g9?l{J9JMv;luV@`J3u8vZ<t{4{98kHKR>7yMZgB#9e-p0fde(1O43f<J4(ANVmg"
    "I9#)Ue%8<Z)&k-_z|pmU6u4;IcP~Ip+E_u@TtVWyR**MW0M<m-Al23i`dJi2?IRqgxu0~gpe*ReQP{Bpp0u%osI`K?wSs<g1tAE@"
    "b$bx_Q5ptmdkJxrW}QpOqaf%w1!C6565`epLdOykzqth9cR>)ZTS6a>o?{89A;cX^$df4QckKet+E_x;T0-PnLeN}7;s<H6ZWpLg"
    "aQiHy{hoEng1(>hv#etYJZobKEn%FvgmKao#zE@$`}x`>^aabZmk?!XnEPEzNP{fzI?X(5V+k#JoVet1(v-(RmiTeBZV6$M<i2AG"
    "iJ#H(T}uF_llfgLg_yRnhL%iDTrxRn%4G6@tzAPDhI!wyhA>L<E~$pS$kM!vlz7_48d`EWamnSRDVIa++nldE(4c8%QCqVB^(INX"
    "G>afigCOZxgP7J{L)?<hiAy#oP1ziVpy1@mx;6CUJPzAyNLNT_U_4+YbkLHRwy}nmd`?{QIcdu0FwOy)`I<E(umZ=C2E8Lmqpme1"
    "AW)JH6;({zSVK!fr!EPdG$nMH1#uRvTSE%^nuC^tei8+p`;hhls-R;HJZ)nQEg7A<WOUM$(P2MH(r}HT6J!}+wQcDDxu<m0oomQJ"
    "5zjh=w3xQBhL(^{T|zo-3TeP&5c+GB)c_c47Pn~$^y#Ei+YaD31X+i<Af|1sp(UkLmy}MMQabYcaT>4Vty!G96xJ-}mASVeN|LT^"
    "5VJOx(2~-rOG>9<YYA!IPu8*4G!LREb+A^y`$T79lyyl5F>7N9Eh(M4q;wj!mH_{^zwR`oxbIPG34Z5c4&o#XyTGRz8{oGDbm|h&"
    "Y1}@{eSe+R79?Ss$JyrKCm?<Or1Ko(j1BNxvN?6h=Cmc7F*hpm*U7aQL|eEy_z|4%xQh+(j5hd5ODv}@v7ENVGKlyjT&o^|eHCs&"
    "JYgR9yJ%m`*Z{vJkyDpMPO~=newwYrK1}F4d|ut)V>!ouC-^vH1N@dS&RoJcZ3*K%0qtcS_W?o<{B#TO{Va*QXrE_nfZvkCnM)3*"
    "EjgU0{Ulv?bVCpTNwPWkAlvf1OO4<e8{oG@aOM)hnco6G55qKF2YwtT+b~WzEMXVp6f-u!Z%N<GC4IA?4SpW1wUN;+x((;?!65B-"
    "avqwo0e(yJW-iH_g>CS&zAcYk_Hh;_@fNg?j_NG#1RrN?fZvk3nM>+sQA=!L@=&_gLlO4_e`E0beNauiXon|kK;II&nM>$qZJ`TH"
    "AYI2d@%AFxT<G>QFrqu5rwJR-w`6YSlDSz+=JvrnSu3=#PHz%y4t)Z)Z5QS6gf{ePOXOxQk(;G0eGOFNEL!KD%hPNNuGt3=bH7Vn"
    "qX`?(w<K=nlDJvcR+z&mTxUP}863pTnPwj&zmiT}87FK&-x9dFOW<a?!|F<sb#xCbIo<;I*yKJ5y6vqbY0!PzlDD}_-e&z4^w@QF"
    "t#3LGxhBPi(C0y?LsU%IfW9SebC<ZyTNZB^#%Ug`^{o4#zibYD2DW0ysTC78pl?ar+$C-EmaPlCEl$_@uRwO@`Q~(=r%4!eLQfMm"
    "pl=D=+$C)DmYEx+z{%HM2>`JM@fOev+3bRzCu~69lC`-@*5)k>H;%G?w3g?fO`2~3eH`|?=$<ERK;M$Jxl7jOO<4=pPMEFpK==E3"
    "6l}qAGQXd7F-)GX0enl;<}Oj2H$`of21(RkccIshqsZTa<3t?k;{u-Nvw_cAk~Viq+Po!cGvHtAI8MJGu&uhGsPaL<?{L(L`5M5t"
    "1a0mTw0TR==3(Zqb1VSx+mKD49O)gv^L!29TXMGVlCybB&i3Oh3H$4S52HBVLO}!dy~`uT^EH5PiP_0=Ja&QK6tuCQ$4R~x_i3DO"
    ";Z^Yc#P4@dj+n3kf4m|5{idh|lU3Z*tY(;L7H(r2W_>^D*Z?tOV*$x$FCYq&rY+%=S4J<M4NP-5EM0LxV#ZHzKYjXcSA32EZhM7D"
    "M(h1jPbc3!`wpu_4e!f`;`)6#uQ@oE68noehX^{p<$&L!76HxmczH*!jwo_@uf&Mty<evHlX|Lq<CP*RA49`#vE;z@#1Zj4pNaru"
    "Gc`_!O6y?s>p}-9b2g;vS9o}Geth=x;Q<d=)$gunM&z=Ld#1f@0HR~5H5}8uHYlMJ6n|S#bO5yr7!~AiLW5}x1|&h?`ceh@ulTah"
    "-D5d@1T!@zax&SJ^-tgJbG7=vR5Kv&Q7N)@LO<lJ-s0mmETx*<UDrBK?PPFqaddca{rj_{)2m~yG+94R7WaUzp^<1ho7R=e@BORF"
    "+FRA_q8h#vDS?;!ug<v+oLchm{zGx&z3yH1ysM-0OYiXN#ozwd|FO$o!f%3fWeFB4U3xpFjEueW`E<egaL=a`#+3-A=1OarQBYQQ"
    "_lxUla;@RzteTQ5dtA?TVu3G$c(z*F?@#~GSlRi(h4*|sono;19hHgoeum@1P<nDrs~6e$%3fQtYHd-++TzyIT<s6^x?Wsf9sGyA"
    "vKQ5;9An7&WjU|P+Dm@tVI;fPwIlFgRDSfhD4V(D7q3qbK6hjDRf{M6yS4f)S8gwws#xs2zC38v*}r_%Uc<?BQa*Yo#r$2l*fYDw"
    "Nch85;QKDZM47ccS;C1saG$tK@1S~*<raY!Imu}=l03#_Cr{^&nJemEQrvaa($<<f+q&pgz4__PUeudng7Nwz@5R;Sp+`mXu#OUM"
    "K)vD04k{9*w-pdva|nB>D^Fe?MbYM~b+%UdMnt%B8NPcNPBPqJ%l>`~2~slnzs`C3J1%3>HLRhi<9}~3gzECXm;)QHo=-o1^qv5>"
    "e($}U7o!rkbUvG+qO*<2vOludw_0Mk_X*EUu&va3^V8w+e{`^jpUN>RKa1&vM3Tn^ho*Cn@vw=Ak_w<VP<f%&Li3fpFz;Ap7;n3m"
    "Z?29y7I`wAPw*HnKrVBV7kAiU>f4IdKOdKkeeADXUfQiyq3Zgse7t@r7xQW;l22}n;X)O+sqbYPH5P~6p8`iFy9j<-PAW#qgD4z}"
    "-Q)|d&jBd-ffeU*af5i`;|8x`MJlWhF<D?foq&t_>y@G=3r^|{aVDF~|LMD+7jrE#&~v6-P?oH}U5~ridlOK5_7>&*!4oyk$-bD4"
    "iy;?rfWN5rT+b@aYyTy{+!+?L8JBeU)1UtI-S2`B|HFKxU0A)>tQ*|xDE`aYJ`2wFSp^268W`RoE}tm6*Vu!%l!CRmnm)%u8Mj~="
    "QdSkO6YK<Ut}E4g6IE4A?$%pQ7c1tflAJ8!KNV)nfHSZ~<+ojLf|+aHX!=35>GYP9F*c3B+34L0cG8<I=R@oS(xc@nG6A;Sppl~X"
    "N@`6%YLH5!0NpdDiN(}I+t-7w_A1aKCV*!NiA5=*tert7=BwWCi^&o*<S8QwVV`&<;PlaB4@HY+N-X(}qUB69xBlbX9%4a`w}Vi@"
    "!Y7Xw!k!|I-*O=pLEHQ4JgvYAk@UaRp73ZO1tNZ_UeidX32R&p8YgGxrkK2wdG0lQwyZr->I3&4B;Et@oTs+_E-EY-IJ@DB2_C`2"
    "Y^{shXiA#B7{e6aPWf>-UXI{gw`Zi+stHyWH;SbwfOowQ_to$oDT(M!txixZ`E+E%0m+IUuw8YdKD1f;S&{T9ZZtqT9s^D*CR}yw"
    "0Gzs<zh6(cTka5PC0vc<S$j6#As6Q|*&J6iXm7~|+^rb>vaA=F{B2gg{^6wfIM78THeqRi)E_pk)-86L{_5es_{}wJOF@3Y$Pt^~"
    "{@L7hvrM{K4PEW}p`^wJmV4e65&_ffx1t7P8yv*2lmG3%{<|-jv|Cm_{hGuf_S68XQMCPwX+u`2UnTkG9n&AfafNLXEdYLyZ32jF"
    "4UikuR@y6AEhn4ogy_wZw3Kgs+7OgqTmKpITwZ~bd3Cv1P;Xx1k}lq0Dn)@)DcY7joV3=gj<nI=<t-&F&zEC4=G8q=u17kf2kJVJ"
    "{&X^a^tdb+m3H~hCG0zi?FGF(oC2NB7I6Olou1$~geN#f4`qRhvWF!`=mBdkKLQqzb<azB5tIX*5)cGpmrIzy8RnyUSb+GTr>KVW"
    "sb=`9h4%n!CBbq-U=TIXTs_Z_4ag5}9(gS|IKYKt@%Voz%NadF0(b_H089AcaV{22D$w{t@mPCxQH?yTT8MhZF1$EiKFqv&`5@L("
    ")jZ(AlttZWv<pvfK-mD;0a@66lTi9$Di$ErEwT6-C%K<~KwusTGYbJCFNM)w5EFuTfG+`TLQ}Rl6o2&7ywa~1HS-`UC57;NJA>sN"
    "A`kPGp6-ez5dOWR%QOCJ2OsYF`JNv<wFf2A!$r--=!K_C4tYCC^1U^tH!6qK1D5~sdr2Y(8_>F8GyW{;`p+JgC8|9zV)odGfo&*J"
    "8>97-x`<1yVfS$MLTox|Lt?|0)GMs;9;$j=7TBVQH`~MFBi`e53CFP{lE9j~_fsTyo};42b5%oUwnY8qKNU^WE)gN4y2^wLn$H4e"
    ">3J{6i_9ciknMttr<af}-kSBzgkdHcC{b++Q&Go~5;&izZwe=lFPm5t&=yX_E6725-Vu?)82K}vN!UVs#`T1U(;835uvpSbWhWB;"
    "$Y56F4TeJlv*1UMT)zn^5FgKg=GRKha&lJzI%OHwXL?Y3K4NlYg2~^}eg;cq&Q-IpJc`#4zfIjsd?;`S15|Ln`Faml`G|fLQ3a0b"
    "LkS^TH*PI3-l<2SCI*{Dl2At)xf`+$3F%`gfmtJaV5Nic_@(0PaO!WcIt&*?!pD~83xA(;ArN7%eSv18>}Ex1Vke~kq>V?uOnati"
    "MQ;}>?o&8bAms1n#e;=FS#ixkUMwgF&XgEsHL?nY4z>KZ<evGq>*p)M-^%)pb^$Bt0>sl7nlO#+=K>|x`ki-S#)3-}%Opwkl6O&>"
    "M4<6vKDD<KOVhc2`lEg1Yfnp`2t?`4bh+>{fx_GQ6htaEjc92+Yl_z4B+G{hd3dZsbnv&gGoLO=OGjJ(sVI%L@o<hZb~I?AaaRkA"
    "*iehD?o~ajzNI<%mEzRyLEmn~b`-tr+Onm6uD%-m$m8=h=_g_O$v35+MAA?HAN2Dp(GMvv=r!YtYJ3INc6_zTs-YP)sEB&+Nl@7;"
    "m7@HX^kv@h9SY;1_nJ;FS@_kUE2*F>GJp*PCBY+lqi7FFLW=0-6?KJC6!|%l%PIaXt&V&X(ko$8!w1w%QT<>sguXID!x#H1wvdQd"
    "4hcvKkf82{JZxxGVOt_@sXdt#w@PhtJ#cEz4IE3YSrMEHzVdEBhwORh^YRw!=$G?7CKKZf)jtwN>McTLy0zi$?fPOydkLy2dKeV("
    "!l&z)ZPeZi1e^{972T)Rfq6<=|6PgJ&W{L1HMchmfFzWm4`D3!#pb837BRhc>F1uava{P2#h$$NZDe<~|3kheuErf7*YYdj?`YK0"
    "t6^@pDJF*872a^5Az6EqT2UC4RI#)pdL_Z=2dTyGXhX(LWEo0nt$nyRx4x*~k?trE@+(l1D28dc=;f+~FM-Qxj;1Ah>dAw(O9mjb"
    "QnR+dQiQppYvbUHdYd=^ffNN=IW|$hlFRZS=UA0=I<BS%fMvk}B-}_^jqN&`2+!~WyM*mht7oM|(Do5|3Adbv<wr^Ca4LjPV2Y;b"
    "tmk#q|HC)QSt4cI$Qw^5ckI_2qUnt1@|hf$oe0(9+iomM5qWt-60QT*hFF!=3_pKc8-7Z6spMW~3CUg;(su~!E0*!rXq3HQ%!;9^"
    "L9S?I9|cpjkn{{+@@vvxRg;qrxc#JD@Uh2B!e4{8Hvo9XWVwem{>5n=m$wT+tkSjYB5LXJa2-*j@1E&WmT-04k!r?lRnqS@P}^&v"
    "dbj)Ap=g1Jp8m<O8drP`jz7PEpAX9MqFAG=!j|ld*HN9~7GZBYiUfacqvvI_j4!&YjAOSWiV9zfqQbkxJE}#6n>OQW!L@zVWa;0}"
    "I%z+OABBon$oj)tzeVq1QG0(W=Tk1FEc!=cAP&}RZiRjbAMO{@^*tS+Tjft&#hpyq!$Bh6j!`cesoN}R{<Lvh68FDv-j@7Ye9EfH"
    "+}or!vQ|-=)JbL5HyT5PbvVerDfkeB57lG|>lASf@`^^E^k0FCotj*d)gHxDw&g)vY6H8C%Jrp2j!Oz~Q$y!Swt(PB3%d0}7{%o+"
    "8EJ}mv4M1nvWOy0(5M0#;azkohbA5K-r$porCIT{!4!`J$fsSeo~kFPQ9kfJ4>|X%y5}L}{0-f|0jHHN^xN`-FoJnvd`Dakpo5*%"
    "8+s~rQF)u7R(Ds-o(XY??SJstR>VqfD+=!8V+(KXvRy@QqD@rMbwyn~YML3B#iaJe)nYLwt?JiPaR=h$3!Z}*wh?Uc>#wHB?lPxE"
    "wD429BAQGY0L6bdW;X`i^wzXgSSc(mtHxA}jzOy!EU*c{;bio+<CmmXgLI*Dq-vqc2-6%-!>t;|4*oWp5}58n{zSd*utQZJg<faN"
    "1BxpUs!Qifgese{2+C?Oih+mzIqZL;jXQDqEAM)%g}(WYzxV1T$mVK7*Oha1Q~Pzruj>@h9c(S-vf?-5)T6rK5RO{PCcWevh*^{F"
    "TOCPOQhJvZc+2(Jhn69reGz2so0ow`&m(>ohgqB?J<1&2ppV8UGj2tP+{#d?wV`cRY!pYktPPB!bIqN!t@apZS2K?r$e7J^j9);I"
    "+^N5*ZN;$+2clLMK}!E$w7?!x#DWpVCt9`|Pl3Sg=cweyeeoae)H5qdHNqaFH_O{w%CXY}d0rz7vhnn2Qml9`+j0B5X-E_Ef8IKS"
    "H)W(`-3WM-QKv%@xcjD@kE$V`(>vh|yN5$?HN_8f-<%-xxeRN2CXtk6KVVAhhaA}`EIE9jJ6yGTO`5IJ#RJc5HAxYQ)(?UXDAkRA"
    "QCsXu>eRHM-+C^$2IrwpbjB}Yw^cZp_}d;tcC2iL*&o?NB05}hx20Wb5{w1((U-~p6N=Ws@T)zhPEcqL$!##h#*m@;qaLp-$EGo8"
    "<ODP2{+7FOYy;`ecNv%iw$~kn1UmnZY~P&u8PV?-Hw(YxD`j_A@L#Eu`1(#xj<!vU;v;e<qf6*tjg09F*sA4B9F7wT6>2nHJDpOi"
    "N23o9dzGk%B1OgQT+!x)XjG<2-lMuNgYj6#SMP}+W^WD(`>t^CqMAoh(0d#O?Wv62p6sG)J{=)*or6WjAvSa}>*dYfqNv{yi)y^D"
    "Mnkdu=)JF)$AOS6fl)44-!JCxVK}_=6k1d@*{g@sS?OU<OXBC`1D6mT$;YjwgB`PXa$+IiasjFv$I#lNNv|o)+d{&K-=g*PRw5mg"
    "4|L@5{M79?41AWb=RnrQgrdjwNBn*zL$z@4NqPBz7?FYSq#~`JcZ9b)b3Jv8Q%4~CdsOD?Ks@HOh;m$kj759uNAGsIz_2pYngbo7"
    "Kub!@4n|G+k$k(lt*6ye8xSM#jUD{59+j++ya9~+J*_B{<~W^@%KWe#FRIxX^Cd;}qIC4p6heWNVof%8J)*cZaWekNk`WWxrBD8#"
    "y42%NFXm;jFgl%b9P0jkIebUKtEL2U{issz=xa`fSJr^>p6fUJ+lYR1NsW%)#|XaMU@3F#F*IM<e29b|bP0wvjg@h{+j%LMl$y(I"
    "$OCt)WsMTLewV#q;pdYAb7#d4?@M~2k1nJ=a7k^^ydPkl)!m(x;n=5&Vt6~6+0t8K%*y_YSDr{D^Zxc<|69@?%>R5|4BrWr;Y@a>"
    "WhdFLcX@>lZSM{aNNxS)jjCFEgLidL+lq3AYRX8O?ENR4TFwz3iTvrh0qpVB{!5xW5LU_gPkVT3h{xU<FJb&@n8Lvky)Ww@6=xS7"
    "$Ju=P@sWLs|K6T=7e+A`bKJEU*;I}i{_gCb@rZHHjYx`hyy9NO`fZdu1{)9n?$FB~1!zAt_zQg!^>Us->~T4ICck?E1_t)>_Wlk2"
    "nfQP3PG0<8O@kL3t*I>LDLI?bYF3WuT9MUyxaaCR%uP?1cN|qqj!D`f^b!y=8&9Y2mNSXTlfla)-kkQ_QkR8EQTo71fRFF0Awe=P"
    ">1KWnJZKL$rf5P(K$&+d1g;__0k5_3^f7~YM!*1Xm;#rX3L^Dp1qM!N8t7s55ICazhhol6P?!XGsl|AYBCf6JRljP(%Wj|O&`F4;"
    "_)Z_`qsfJBxxZ)&Kk}#{@|8rDxn2^ScH3&z4ilYh-%Bpz{m#QP0{_vJEPNgEOJ1!-p?Y}Q5;b%f$)SNStQZ=<Y7F~UL_EC`%0;&b"
    "rGJap=-*}{@X)l&O!Ldgd{!;%*d0^1d5^dA<Oh28RH(5Hp4fPPB)F&I7}itR+C7v)?x!Y0v!7gcJ~^{?hJ8vql5rD!zf&9?{%H*K"
    "6iA&FNt1ahVM$t=NNC2Nmh;I}*4{bae|czWC2m2g>ffxWal$2QqQ2jw`fhv7V3@T$3Bb@wtY2LJfgzZr{wO@GZ&&|i=tFL}WpSH!"
    "IT{X}4AP)S%`9wa(_WP1zYerfm-eLV)vUrXRgVeL-$TX0Y_R=a6otPI*qusWqmo2NsR->FkTC!8p{gl3@V>$t2GtO#cRVddZ~xzY"
    "x&=Cu)n|=w3haV4p=eK@_Y&9Xihm_~O;@VwvYySF3N&1ICQbs5eUZTTf;5*4h{FEb1>|`z%eG%a)@k%?M!bpgBmIMT5uf==lK2Ns"
    "KL@A%6%64Y82ucK27c$Umz9KC6@R$SPZFlRtgRHpy?*p7G1(yK60f=*kh^pb7wieLC}H21Vy#i0%73O|<bpR6MPlHMEMS2I3lGB2"
    "06*+RwJh{wSLES3JYfv{JTQTlFo(UopRGl8mi2;QJ7~$#kM)E$G)PXR>3Ah-7omIxjchs>n%Zay3b)XN@GFOn@+CHis&w~Ay6e@|"
    "iC6@fi7&wV5U?JUi=rBDW>;CaSC)%Q{biXElu@I6Ttjuk?(LxKnAwkb!R3&aBvNdkN67MYZI2Opcat8qIFQz8kO5)y*f(2@ed_dt"
    "p_|_Kd(;z8TGBxuX5!nXV7SE$m&==lxF=0BI8d3OaQ4O<Cd)<=R1Ere;keeFui?SkWB03Am&}UT>sYWLSEQ4_Be}XLbaTU3mSgRt"
    "o;c|DsLZ>f9^lAfxS@d>tRqfr>%d`ta{MR?dTDBylq-#ia2@<fKjDNgP5l8V+lKA8fo}3!q*Ya`a8F$c3+nV^Sh5s9d`U;Nij?sj"
    "V}zcAoW;8sao^dB7Ld<9j$2xBFMaeNW6g*}r?+0~J#Sb{M7fQ5Sp#9?_2i>h^WCqgy@3~#c>c!l;;2{@JuMAzw0#Nr7H&3izPufA"
    "-$=1ZPsIVl0tbbxzx{eLFM)FY0<fUd$sEa(;Y*F%;Vn*<+S;L-wXx@&4`dlNirIQA5C44n5&eOP?;G4G0Gsm_<?Ece<o%$2IG~Cf"
    "^O9mQDMxV2<NMoP!xk*!x4Ve#_>c(v0D}BsVAxH9%+X7KI(Xxu>%_<VF|T~MDJgT0T(dWi-l(jryGd_L*0MeN_VlPCHo-=d{7xQx"
    "E}zoCkKh9Gvi&!r7jpQ3TRUuA2?y)^qOx#yrwGdfVBw|+4%4WY8b^4Y_cHu@i?3)iN7dh5%*Jah>tvle6Q+L9qfSY3ukr{J&e=Cw"
    "tTTpXm0G8rkY;|58e=O%Aptob^Uyb&4!uGX%Y&Y!h=COwu%ed?Hyys~!kaWPFhr<zhgv|C_CfjMDMp)4aoIgZ5XPw7nTzQ6dwIe$"
    "lpD{W4V^si$35zWLaG%8?Iw(qv{>UC=&#z$Fo=585K7`A?)Os0M0&H~z@1x}g+M8($uJ_k4dT&<8;))up&!LP>4OP@O43gIN%KDW"
    "x~Z845qd^K>46fVR6;iutQe%=m5eGnDPVIyI-^!(WCt;36_cbddUdKkzoF{kNhzyupv^na)~}8m>xL@m++I8gBIHD0GB*W<25R7r"
    "c$>-SwsnGrV(>t;)*Ls8?i2-$tO-W(fEXO``Vu3?9x$(l3Q%Ln0tIqC?hV<~gRhmKB5-Z8AE|T}R#+2N?`Bl2k%MQ<%WO@HH3&`}"
    "+}1^=fBNq1;^63XaPf2FqW?F7sEb1p(1CZ=j3FB{RH+td>E!s_j_%<)i1-CkPVHTs?Qe`lJEF<LWaHxg?}kDv{1g#%Go6g~>c!)j"
    "%dDwn*V;saD?p>CtxGfLKpnsGWBD*!$Pg|1+5ZL$lmSCCQu>R!UQ&%d&;Q<2QFY8%WSKmQxY?^`<q-C5=shea6$Z;pYf%uADh0d;"
    "omB)$5ecBB>&=RViho@pJ-<Ci!EBN}1w|uuepVsNrzkhBY;rGxYi!0V7k0U7VSf)2ZY_?Y<X5duMJBaZND=EWJ1~a_G&Sr1^bgf!"
    "G!+@6z-A7NnEP}uz?gg4ENZ?mA4bN*n<c2NWnCW>kNYCtKFgy|jfP;@s$ls*Z7O4yx_^O_%K0Z#;l-#X&kM>D!uC;=9Z<|?WrQ*K"
    "K`*3!T<@nCrGfo~=x4tNnj!xFK;iWtu$UD+*n=m1>Xga#htHi2xiDL8hE;6$iy20Si81pmjCJ-3_q#bCa=(HkrY?{;QTxMwnuz{o"
    "%lRaD<XuMR4TG9eTsS|CnomLD%#Ek}%ZDW{mC8w@%0yi*1xPQdk23dK!WAVHQe)r&3lm^EFYF8MHl^ij^kE?U`Ru%$i}Y*Esh}1v"
    "_A3XRrKjHu0#LZJPa^f=C5Wn-YVO7RD_zqo_V*U7ZrtDpwEwv|#V^xJc3)H43>W;DxfCw7@J3}71yY%_i6-Q>#X6o`4&@4(ZWC9Z"
    "Za=zqEXlZeV;e-RzZ($xE(n8+0`@-}!ko;mPMV5y8^W&Z4-ID2h7wLh%#F4iP_79YZ$TRbbR;{W6}@*Av~IVPhSk02iSNRwJ1o78"
    "(A1AtfEWZZ)sI8sS3@5w;bS_e8bEQ6d!AbI$+%-n-F!>-G*l05&IA@>)XB9{N`}GY-dEFk1xNGeQuL$DSFAQBKFE_fcutVz(MqNi"
    "2h{lcrko7#Q6(EJL`8nQO&7(gOe}$9aH0f`PPhWhEDb-|(+DN0Yn~{J0w?OTd=-7h@h94RZ1IQ}!JM8z-LELbN>?sWRgo9d8DCv1"
    "J{>Yn<?kw0?5Z5zPp0GP9rKN<1`D&CS6GwH9#!^Myeno0q^64;D>)&k2QQ1+`AkT`Fjw7b;pYR@h;*-?C1H=KayFlimczw)MK>$v"
    "$3C5UOcK@s5a#oMuHRbU8?!_~0OS`rhcRAD(-@R1TWb*2`$gt4CDsjelTc?Cp7(pBAF0g78|ZeP?gTyiD|&&B$JNw~AAd%7ta1eR"
    "3qsjCd=EcJIV=TPjb$ZdC(eiB7ZJ`-(z}*!<!5_g+G?qaIgw&WCMMi~C}#m>iTWT=M0~KE!<I<m3mHPz`nXyGO&Ra`{k<U5@LW|3"
    "!E|0=779k{d-v5lbXIr?Ftfk?*MBFyM3_4~+~q>{l2vP9*Xjtv6fp<9B(kC2RVkHkcqlL6Bt4hMwrh>CSkH!Qj1oAeyIUbV2={_$"
    "GlU0;1DLD>7C(#oT?mihXmlZbR=uC{bqSns(vh$oP~?r^*V%Zw=teuP#P32o@%oL?9;AH-+B=t;N7;60kEs-YvLT)OedolyB}o^O"
    "VS>I3$uGxK&?3CL1a@?LOPGFh^dDY50~)Wf0590kso#a>7^z$Ao(s*<HfWB*sC#8;ur*HMAm^LmG|a=U&GftY1kzXD%_ruZ^nj_I"
    "OuvbLGh2a105<7Dqn~Yq#xU=9EhdP!#v)p`8&YPFCEZwzy3iQx1x~`enq$fSa?BNzy$|Bb--$g9WCMG9pK;iev=e>Nmgq|`TR+S;"
    "Lm#}}<}!XKM&sOxQJOOHT^KzmOHj4Sci!L#9Vx?iT?jS7c9CPS4L(`KZM>{>YYfBT2{*%V?&qBhCJOpp_>4PP=W%r-ik*NV{)nB!"
    "s@q#EkTe0KW++@(ZuBacUGy4lh2Jd8Iu{kj;pd>UzaiI*!p@ofe%Ou9Fm$1_@9&Ki8oe1gZ0E&Tcn>=9*zY1!veP#gJ{@Y*X9*vG"
    "EZGY-q)OlKZ*f4t?(RZt(!ohzU+(SSgW~GFEGOmrLSh)KClPPq#w`pNbkgXSJiyPkTH=;WAcfN;eX#4%oyVQbCrO>SrSU_ju)kc+"
    "(CG2@r^`7O=$w<<M7=lN?4b+c<{BKt9BoC+L5C*ATk#pl4L4MzK+W%F331qkT`-bj7j{)ODerJr4ZRo3`6KC4K+#9_yZ|d#VjNyM"
    "nirFm*cFR#stCze<eYS?;C>jeYouc|+ZUFT3*-j#5=1d6bhW0b{E>ZErn}wYB%{Dthuc5!lSB?=xTH)c`RDoP<79<@KJmfQ`_x@7"
    "n9+b<L)kj_%gVR4D#{`JNxV&EH+GRJCosV`pVqa)S14mn>{qqds~<AHX4CmXwlL7+h1gf9vw(H`N29E&Dv5oHN&FHV&_qM=LiIp}"
    "WI$UkWvP9_P#h=zI*{5BU6kXB-L~@P$sXXKyjfh9^Y@jwX~<(Ld^VD<d21RjVs$m$A5ZI&cP@&9H11`YfsCKfxpxb4-U<_ZzEqV+"
    "ga?x^A!iF}H@DEW&9FwpvK9pvsM0iE9FB{-Mhr+mqhf~y(WcVq>Z!{=>_nn0>{ALt7nQmwx9J@CNrn1|h<k(=_QJr=Pzj>BXd3)$"
    "FdEIVVw&zBS;<~6SX&i=joD!z<?<@THF^|Dx4s@fq7<NoXgSFRda0&)v-hOGD{6fmKFp}#-=6qekA=MF1bcPD(FSbH#?!}g?g6<C"
    "?}^RM<`tG7l*Kvy-88mGlz&Si)k7z1hOV(z_{bVO&Kuz7U4y6Q;IA$RJTC9Ih_=-)XXeX?m*?l+&LP87ir(($GHw`|!_$soa@wOu"
    "@4mXb-&1uEsAT)jzh&R!XK^ZHe&rhCw7GqKMTLv$2W&VmdZoIFF*S*iwl4=8KC!kSN$CeYMc`A=tYEq1sJxgi?y+>SC`{H~9Vx#i"
    "O6ko!OROCce;c2Lt*P)L%!tCGsM(-TH+wH6VW-VQLw+JPJ>B^Ips5BaL{PM->8NR>-$XElb#m7d&nV?}W89m`dW{Y=Bx0Ax(+|x}"
    "234d+7Pspa%f<9*H!7Jr-vQZE8>9zdpLclKCM)}6kfm%i*Zf?>QJ>9_>0<fVN2<srYUI_0`BzcDste-^86NA>l3d|Zi(O{FVgrHZ"
    "Op&Y~$SRc$dF?kZ15V0Og^d|dkOb|k0P}IATHjq2ABA90w^Apf_6?20A`;YTc=1h*Bx|hJQKSkz+@x*do6`wZ0GLjGBIQrr=|#@K"
    "bd4t!`DnZ(o?gjwsBWx%YL~UTwhlst#7!l0fs|mqC)0U(@i3~d?u&^mB#tkBa-in<qm+Crg`ri3t~P6YwjapOO9QL+o-7oM<$4~}"
    "Hb_=raRB-s+#h-3JI}Z;&oUli<HYj+20@nk9ERg=8DZSpU16UWil0fdjBBKHsbqGW2}^l0YO5(-EzG}#US&UbjUfAe9E1HbeteD1"
    "ZMj*hailj<zO40w9ddSi=vo_H!DOVEFZ9hbq5Wv`VmcoRHGDpuvei^nSB>|$)dYX7teSo6+SLkEdGW&ohOuIxaE+E*<WcWx?>V-1"
    "#n3Jc54n2b?T-skmW*0T3z6-NUf}0P$86M<Ab5oh3$}|L9r31^U?+x=clpof9-L?#wmH(9v$N(vaT<4w!?DtsmM<zDct@~79~o+d"
    "*$wUU(}U(5VTP`6a}q8pcDb0B<>LSU|GdldgA4eNYFywQU^DgUtQ>hiP3NEmlpps1i;fk+mp?V93nFy9Z8Kf7UW$9B!xP6YWS`zP"
    "@A|>oQ^i<@%|oqfy>jw9l}_d^7_d^R`JDuTV6$ZS9*WpZiq1&;amMx_CWnkmQr<*)8WK^)&p#<R?cdL36;|<xtL34Fpb#QQ<mfF5"
    "FDS7y-t7MIIoL;cg3y6E%RjJvHqGbld{0d;k)Am)ST0qT_<Ic^9e$=gA(f_==OT@KP*(-TOYwHlLqCqqXNofTVU%#n#4+G`;tk+K"
    "Ksi71b53SCT+XpP>>d!2hyNB&#gqb?KfrXO>4SKda0bFjH5!55bXZUmI(ndo<bXE%H4@O@8k0wXJ-NLm&|vBDelaOV@)JKK-ACf<"
    "`J>7cYvsL~Sz|_Bge#d|U{%o;oY$y7raH!T6|h!Jz>N21hQRiM;0W@Z$Ql#!Z@bn6EiU4Gjm{}6W+z_teERXD_XL>Dd++7E7@=R$"
    "tP!H-lqE#u->p(2jAu@T>YTPw*@b@_T)tXY=cTJox5C^{C3O>7Oef4SSsw>8)nJ>tw8)Fsf^E8MjF3|;=Cq%#nO}f0j6N|B<RcbB"
    "O@8O03g~s!GBenDqxzWwW<?n^pR)nGfcYG>hH|{lA`cR`FRm^RyP3AEh$a7CQyGh>Gv)lBmD7I_sdOa%4(~q{H>e?~G9&EnREtri"
    "$n2vfOOi?8{WbG|#Dn8FonrLJo!6+vrzVrN`sCm3ntkNM=4|T?mesrLc~?j0B)R|gzy6P1$52kPipZF81Z!6J*&9PXY6`q-hSed%"
    "HLA>5vW?}ks6nX>Byvj0`vht|QBjFU2HcG2L)SA!BL7<?s{CG7cN5YU1b+v9>g^;!FaG}Nu18$L+lhi+!hfE5I{_viNQwFa43~*$"
    "&qk^-lQr1*XovrgP$r@bhvjUcB2sCNIPLky9AVOn)EuGT%hVjN%3{2@XNwm1rBD9A)noT1z&v)`%kfX7Xc|0LgM$K%c_^Z#t+fb0"
    "r<k^t6D6=#6HzhZMl7O_3sTceFh6GQ?LQ7NUwSNOSi6#}mzop!a$|5OB7COuo~Rm8CESl-Z}iu0K@v%DC7NP$oBcNUXrxbSx@^EX"
    "l62J^jP58C`;0S2iA7kj6`Ga~C%_;ch33_d)(@Nr+|$4@Qj8in=o<utRWXL13}Y4O3DbBLdJqLsYC;||4e2AHA-@0$^$y8?<iUe}"
    "vH|Wb$_XX>i2K+W{59P-Rgx$Jx>#RFlnt5*^w7CL3{^iDK0X%<vQtTQ{|DkjSnB!%8x6d5(pkvalAsUIq(aX*<;t5#jo3!$m%pW}"
    "j<@Td3uPH~7~s#PxRX<DX@p~?F2-D!S-2+f$}a00#kbWIr7~+A?^=A+;*EqcWsJB`_EJ9lJjT7kL_vm~w;47VI1i<FQx&zD{5UC8"
    "q6Q`kkj<tYq&S6PA~AT_yVWq3cG0&-o+Q&VY8Y}(nYEBHO#>@In2`To(T_HLr8P?)WuyFtupFv|hgOZsfHM%q?WPMWgG@AQ5*c20"
    "h_~g$JbWQ;JX@E$w~brcI7t)ZhVt;mzHUBc-W9JODI%YVN|$IukdjbteHLZrSFPz&^1!YgCM4I>CwalI(xebc<ozk@0r~2<=M9Fe"
    "NVicX%mw&`rqO>N$VQyyUX3Dw(mh$D5gqif4$QIYpVkN{Z?(X=FFg$1oEKGHa@Jt&g~`pV8R@-CiH1S2;J)ETNVrHC9fE`{xqd$U"
    "g%?J6i!esx9bXAU*`!fUd5=n_N@xyZ*_l!_fE_Lu)R?70^<cJ8QP44WnHw$DDL|@SfFdm}%Nlu%W^8-)Fe`?OgKAz5)wk#(t@lQ#"
    "x-r3PPu}{_cg1dxXk<<=L^9wEAT!tmHS4ZqN*ye}kU2##`41<>kXzlZqnZYdG^wb5Kt?m<JJ`=AA{`{(BqFt&Og<nliqRwW_n}N;"
    "5wz}MWuIaU?`B9}=rY2RI!GI6=~9s(YQo};%3+1d4#&awlz$VJbjOW{CglervHC~vV)=h-yV~ZqjU)V5Fb*}L5{Mx{f)v?LjHM_{"
    "V$oyCO*`Yx<U~ReVh~^nQZhT^PX9yyVSh>Y+1)z;B;}Z{`o$JN;BYU`?fdQ(2;=sk5P9Erk6Iq5W4Zc`g?EdeIRYi!w7i#w2;&9?"
    "wG8}YX2!VW=Q-}q!=%HFt#j&<$cw{)=VJW#0xv1vpWv_^%UQRe_gP5*`v55BzK8fQ43?P#&w#<7%)(@G5!dgkIrUD0@3#rtcR#)U"
    ">l5IsrV4C>@2_!&BczraZ^gEwb%sbNUN!0!O*jrG%W;e>PIFw@vqfn2wI8Uq(DJy)Ul-o><n{P30vQs;J4d_#By%B^J3%NzFgWd#"
    "Vr^g&gEOBX<x&S`HgzDvp#jt#{A$t5ZT^#5)PpMX1@#=8L?Z<0?KyJ6(;V}QVpu;c6K(+%GhQSG&ex#XhoFM<tRCa|{T@t?=ks`$"
    "a8W3FTaW18#imP*cp96xw|l{PK=Q;scwWYL=1_Q6GcFuFMZ<pv`e+HF;`1Q7Sk1WDp^Kak@q_YJ&WXTz#`#*0GnV6qO@_123a;^o"
    "bO}PiL+pE;un&4<>0<40Q$BarNNF=LUV@pWt}EfMU*pL1>=r`(G`0tmtKG$WGzC#?!({}^Q(QMTJR>}kBc2JN+Tbk5;oCV5dz0#j"
    "E2iEDlf*KA<V#56rxHw_ixO6|Ql5blZt>n*Yq+T+Z@SzpR{4_<t7Lj?%Ws@7g7Ohu%H(H5pEKT%L=Tg~@zHd%!$ZSXL?Yc;{^)%R"
    "YlgqYMk7+Xh3>q2XFtN^6_+?C7$3Va*?YopIYPm+j75%-L)3tgvNHtQ84<a=wL*|f`=I^>U__+)3{kCdc1LK-^gJ2x>s^3dp&G^$"
    "=yGW_hob9=yqo6(Rk?%?RIjOF95DI$i1M1NczXX`5ziB)>z5A+(Rxw;#wTf#feCQ|peMjo%W~NQ6XNCLLaEGp;kneAB~6ThegIlU"
    "MB${6^VmjXB33gJ@JV_$e3JUb>+6#)IGiCZ(oAjTRaOvk9EwJ?qrhED(P(tk3ZW<dfa?Nh!ONh)2v=SsIvsouvRN&a>eLKA2VPh+"
    ">ByW(0rtrng~>LhT||oN(LT5|#mxL&m@!O2ew{zV;`)U=wVH#p4}M}?c6E5__}ibQ^jz$-y66smFi?Lt8Xrv2lB%&|uYhN%+7_pM"
    "3Xf%4&|c!^GK;)|B%TF;L(`fpmibg-Vmbe)8MKd3;4>x|68G$Mk3fMq1H>ny##iTWeXrZ&KmVM>E1LY{9fg(pteGOBx>}*HJt%1?"
    "0~6na>id{`fP`yEWJS7NqOruE*KG7!y=yOCVmlr0>MANmqHHVNG!MyLl9~+s4yK=FRvbbQtEoZ<OL?D_=k<&Lbtw2B=;I&Z^9j-K"
    "6Tlqo1?Gs4j>T%%iN_Ws7KD?N`aJsHHmHrKDPWTOMUU-4w+Pi}pD7#oEtkUsPl!Lj6fIEqnrg@)1{{RZ(eV!BAGD%Sl$wN;?>+RB"
    ">tG4$NftPD6!UlLHoZ?uQP3mV05NPNDR$c5>(Or_AIuKMr>4an%CJA3H}_n8y9$E;BQCe-CYZcvB3w%NX@I(PyC(o@fd~$4()Ub>"
    "BpuGT%ok#qK*!uIV?oXmSt;>89P(+202TvG;W%jXS9YM*A@$j}@c9-_u9k<o#W8<$G&ldCwN2IfT%ZgeYZ`Fsh_q3x>FLeM^d68D"
    "{T<&UsGuI&EXElle0C<y7q=<%Wi_?~p%{Is?D&V7hR=vbm!9~4rIKfM9;oBRXRE@sWWGIi=6cqkxg~9G&g!KaM3gelkf~CrljCbC"
    "atBwAOBGn;k1<R+IU_+!;Efi`1lmg&?ZYkf-F23l$J=#UQLV*RWJOV3H_}m(c}yQpiIJsJG`!_C&p*)8aglX=8S8bs0kzKJ52TW="
    "v)1upx^Oi)?@+{jS^nj7!LYi{hr;mXay_HvOwzsXjZc7b#vbrkB>LjB#mia><Q68C`e{yOYKR}-6CS6zlvCu=pfEVpaxD{5f#&cG"
    "Ba4R%u&$>mg05&Dx$0`Ny63zkg4Y1FP+wOsiC8d#5S1F?46#j869|RAPZo?-(%iYwBlV%>eJ`=^JabA~gZ6*^_3xlV;)YdB(#@Z|"
    "s$ta@-6xR}Ni~r2RHbIkyrA7t>ftem0GtTD6-wJW7|kx7^<Yu+%MxCnOZKcn#KHL@&KEiS{~R;&@oyhLzVKgYGE8eedog_RmG`47"
    "w)t9q7;2ay&#6SlW$&`DzVgo6L+@7(r|}5TOWZwwb^hjJe0kB*FhME&%t@PEp|{cLw0$_qQOB3qTLJ<$Q>n8-T=r)VnhuOK2Kf&U"
    "OcFuGi0Mms9w|kQAmUcIM~$G(7stZ<5%f0Ipf}BHpcmw;$6}tjk9SjvD$h#WBx8<OkU~=esPuvT<F<uH(B&@B4wxdfg?&8qo2Fxs"
    "fN7%|Fvvy}1bBQ%@A*ME;8)=)m#JxzU`pQ+KT)Hvqr>-(k>R+e271A%eF-^CEpL($s2ilh+1sv*iMn|<Ei6g7o@I^TMtCZ((Ny;2"
    "FIi)sS`6g|uQW|63F+$c8nkIJgcdmK6RD|dPtR^iD4u@7u;{a5D@tLHF|R^_$R2DmT9uh=0k$ltf+11+TQ=9+#kl!ueCCZ_zI^-Y"
    "?JuM2@#L~)@kj&dc1u+9bx4E-334>^@7;r(bS5Gol6zpt>4lXSaZQlC!Hev;>vnxF=!-eqGmq-6NS3tJNjf9K#bBPK2#g~gJrH1B"
    "<%|1-l$8Nt$Hraqz7zpZA4hoi`fg4061F=XaXTZLR$i|C8i}zI-3Kq`Apom`fZ&x=XH0g-QUuQxue&{E90VIfvHoW_z2VR+!|YIJ"
    "FO5HdnqZ<QXXkH5*XP*0u9`IMI}V0PN;Z&NT8!6;eKC=v>C=k2z6Z)qtuGKVzNF`HK02#n!smEYoEsZ^Tp$&eTpQ*gg}mvjtFlO_"
    "-T4GY>~H+{<OcSi*pB>3h!XHIxt)xQsadLtm;G(*$iNn(ZE5rUs8P}$k`*4A`S=%ySkRb@)tY5>TpcU)?hVP5h6r3v{YwGm1xpe9"
    "jagEd8&3Hb>gLv^GxRRZ!gJJ}ZeNWrF2_HNUyd%Xy^GQ7D=a!pki_mucpG}uPAc=YFp2mExuUlu5~uki7I2}W5I|0J({FbO`HXA<"
    "S24|{UUn41VFNUQpjyuU?#078B|a)KVK9!*N*JKPv{`U&6^(s^t`N6y328i~wktsoO%olK6wDyPWyl`_b>M7D@033u`JQC^W0r!B"
    "y;tU4qveIf*n+*br751u6YraE$`rogH{T!z>>g;i%UNEbEfiDtX(MX1Hy61k0Hin*i)dJEh%X5_ox>hMgmWP-t~G~`G{P=|ZflcR"
    "7BxUlI8)fb?}mN98})c5^;r9vl!jEer8#@L67UIpW`#skA-9cA*AIFT5>8{CQ2n4U_ei~fNhV<@7${SH<zdNiT`Kg{N`}KS|6M2q"
    "<AKJ~?gwrxy6>AR>A@m%m1{umbPZe{Tc#}i><&2MD_Qx~-R8|fz!oH^>u7qRKXACiqn?p+5gw{NpoIt)YM#qE$2r3xT%mUYxkgB2"
    "I_!reSKi`_mcdNdBx2@SOO_u|)L3{T2yl{vO7Oh!stD(8IvUZ4L>#d_ZwyMoBC?!yUOnz9;R@NjId+K8ab0kc(FZLT1O$c8)e*2s"
    "gTCXJhMndl`$8V2%|OE+*jI^Dw|o9+ugw?)lMaJ^D}tQzE9Qn}5<%vJ(E#Mxnwj)ZCR;<UC#kS6LK4r11cJ%5kaW^<O?Ul1H|=B{"
    "i|Ij#r*xW`NxMCX30H1=Zy;b;32pDtXm|8PYLgv>x(u=~M#{pYh6HAd9_%=IOqjJa->x@L&xMr+17w&y)nHrYMIFc6`OPw>ZHW=A"
    "IB<&(5AfD{U#YkM^iZ@xZ4a59+!lu_GO<fa`Avx@FKW7RdF0%+h)718gciKweqf@2^9MS-(>QTf<t*8AsN=&YrlspbKDWwgT|wdG"
    "-F_>CSCrI8BEwkD4m_jXj(EeP_L2AmU>V@VRXwW&hJ+%PJqafl1gsU2#6-llmt1Axipc*xL@F>w2)81naxQXfK%WuLL<`gfo@Cs9"
    "g$mJXiK1D<X{Sp9!OD?MEsagWX{X--FtLw7rgfIkC!67KiGavox~QxbKnA9T=#;7h!f1#!(oOBQl0hrHVc3OmP4_DVU=ai1^^msE"
    "7sBU=HwuG{wrWHSl?X5!0dL|>u6s%3muzN9W8e=$oL5yN^)<DczY0up2^NyB5?*hf0Pe39A-Y2k3Mq+Oi9H|Evc$8lkpnYkm5oYm"
    "O7U&4**&hy(Jp(d**O*nRL)?~2n#%>5~HHp$l)n8+|^?oXI62u8>4$e?>@u`=Rhw?adRZGX~gupmgF*pGJLQ}DITD`dGdj!m2RsO"
    "9jV>K_efM85G&$<Hhyi;>h+GemF?~;+0%Ap6?#3yMA^oQ9ADZnU}#emg>qXlrqRo!d_Azv3Z5%ULV|!N)KG#MqtogiIcBFbBMvl6"
    "hJtphePs0$Lb%Ez0#WHxG@uRS`UF801-cQ2xTx%9T|iZ$yn8(t1wQriS64zDBR<8awOvb8sRy-BiwhZ20Dr`xp=^l8(33Hg89`{B"
    "7NU1#wNdd?+fZ<yBolLYCr8tiiN=7mie5r~A<z>2g$eT^nQ=5ech<pZijW_!?f@8#E-v1jUtNv=e2$f-E&!iIP$6KXsf*9|IT?U="
    "6;1_0#3Uh18Fk5`eUaGtKE`uPQ&7%!mGCd2eEEOCGK35=b;L8!FcJ)SS13jErJ4g`QPI4haM3&v==+0u$^>uzQJUOkEbn@+##f_X"
    "NN+el+s1tXmx)_R%i5i}3Ei9PufB_NWhGL@D;GRfmAz2{N#<BYqFcixga*X)j3LXr$CTeL`y_I&;j9x~y)@6?)4vE!o-LDGj*DVm"
    "CXGyU7QYZyIK9sy{x%ERgx8&8M+T!ILQ4~bN1n_LOL=@y5`I5>JNiXG#5_Zf8e<30N>%Nz5$n5LPgf2#{Ikh6vSv&h3gT<3R1yp1"
    "jgl+%Taw;K+L=l#yscQ~Qjycin!eQ6K^*S394R!6I*-Uh0x=1`RTcz|pWCp<VL3Vi<0D3vYxH`lwYn9rs;n*Vb-9#IU*k1}RWLzl"
    "ix}#P^&MQQY`QV)l>Vr#i=59iHyI5AKm-qUQF^?pk8XW>gwmXzw+3-y?IfY$*Vk_**XJ+A#$(sW0BsMvnuuyu-oq<WStaiK&KG$H"
    "IA<^`x)61isx+5FM{J^QJ0{oId!?yIH=_t$TxbQb_FV(&Xi?~^e3Wu25Ng?uv^LiXFox0@99t1%p;xRvTkfN?Vh^&~#5m`bPjbE4"
    "coKnRC-j;qkyJt;ti;Pzf%}(W7_)d)vjznrP+HoAcz!_T@pZ}O5cA6(U1CR%utwHB_N<Bp%eNj(tBk6B&3683ee=7X?qy>^T=$pk"
    "jE`p(E0}C2<_;@lSH_QgVm6LC6Ac(gD+oHajn+J~kI>GDa57P44PPg?P_KlT`Q%E<uknmj22dIgVKX#469s^6oT5t#LeE)f?UXqY"
    "($2zU?<9cRO@d)nm2XyTLdPxQe%BTCtTZ`P<V!UqDCL-|vB%1iLOyn_M%$L6%TF6o*c`c48IC!zEa0CUZS`!ep2C?1p!=}}w6b6g"
    "E)l?Yb?w#}Z*RC(nYL(MB)j$2Ad+3t-G!-4<$QDAE-GmUe!u5vsCZ{-t*b?o^n5Xy`A`kfrQK;~_OGmJS=5!)o$)v&u^bbLy)&j|"
    "@CfvJB}P>85Z^&W96C`2Q7Bk5;$0l|tpYpg3^Dyq_>dNwR=nnpj;dWCytt1itMXf2`z`y4o;5C%GLi4RF;2@w+$`FmH=J=`Lb?bG"
    "SVUTApYEBu(Ux_F=WnoOGf-Kbf7@%Kzy`ERSIs&xVJYB-*<8u{D$-bee(>lC>%3>zW6X$X+`d!PXEmjqU0JNI`xS?fD3MmyV`T*)"
    "bz<ki=H^BKNFvCySW#!KURqg>okdDAKx$f~<uqwO1Z}53tEcNa-{dR9ju+ZlaH4^w!?$B!?qjs1rH1PHa$-VN2EcUM7ot{(7sAL{"
    "M<&Fr)hcKsQ?L<UjV~u}WF4ysv#ObG3#pE&Rh7sTB=|liIYykfz!Xg|i%G<qxQY;;-Kh#Oh<#~#)*xJ=V`3<<J?;-7JY+h(TMPX|"
    "ozyY1s-%ub(CYNXtf^)ei3R772$j_FU5#IBd2ftp<i<{g+P_mUG3*WjgKS^sO}f7#+vU@tvpGOJL1Vl7S8WP_yR|DA7qREe8tIbL"
    ")YO8&)&_8Pt76qG9hRIsNdh>{OXhPOc+DTj7e5|D&zb~`p-I;-w?41NM7ZIk<BLORC8>`*WQe17f@wlGVpslzt=diOF7L7%&B~}%"
    "lcY%EY<A{EV4+e7-DCH>?Xb@Gbx6~Del~vlN=6p?)O*<>-Kk0&TPhAo1RGI)gk{#zEP7qR;kM-=q|AkDDpcL@uO0?S)g>Z1Zph6w"
    "t!I(*q}Z-^yyh>HU%B5f>R4K7JH8RwrK)aK%t2}}gwExZy;22qY9DdMZS|S8SJeJpic$U!MR5~k^la+~P}+#SWKs=Q1^}Bay#}W&"
    "V}m`d#+oN&o?L$yX1U7Bwd&T_Dsn?+ENBTuwVN%>3ZXW;sxKS)>Pl48(mm>!Q^0(?L3E#64Xx3$cd=5(3IcW*%FcJ>Uu~7n1S)<J"
    "b-*-S!>a1rK}PjKp1MI!0vQZCvfo^(eW^&O?m4wGIQvRf3@^$|gC$D@*z~{s_M6S-*If4uK^``$gRTOY80!9bx=W&xC0BGs^2oO9"
    "lJ0g*?V;{X{c<|2SaNWqYRjN&@N-h$=`Z3)rK0#Q6P;&>iOf*SEVCjs-=dvV=?mWpckXm5JvqUy+kPObKhX1-|MB1b`cJ2o%axK-"
    "?g-IRkW&6L^klL5qT|ti=D)ht+mXAVMR}LK`1tX^KuB!u"
)


_EMBEDDED_LOCK = threading.Lock()


def _write_atomic_text(path: Path, text: str) -> None:
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _ensure_embedded_cases_dir() -> Path:
    """Materialize canonical cases in temp dir (optionally refreshing via MCP if MCP_TOKEN is set)."""
    target_root = Path(tempfile.gettempdir()) / "sherpas_canonical_cases_v1"
    required = ("financial-health.json", "investment-analysis.json", "persona.md")
    with _EMBEDDED_LOCK:
        target_root.mkdir(parents=True, exist_ok=True)
        if all(
            (target_root / cid / fname).is_file()
            for cid in SUPPORTED_CASES
            for fname in required
        ):
            return target_root

        decoded = json.loads(
            zlib.decompress(base64.b85decode(_EMBEDDED_CASES_B85.encode("ascii"))).decode("utf-8")
        )

        mcp_get_case = None
        if os.environ.get("MCP_TOKEN"):
            try:
                from backend.mcp_client import get_case as mcp_get_case  # type: ignore
            except Exception:
                mcp_get_case = None

        for cid in SUPPORTED_CASES:
            cdir = target_root / cid
            cdir.mkdir(parents=True, exist_ok=True)
            if all((cdir / fname).is_file() for fname in required):
                continue

            payload = dict(decoded[cid])
            if mcp_get_case is not None:
                try:
                    mcp_case = mcp_get_case(cid, allow_fallback=False)
                    if (
                        isinstance(mcp_case, dict)
                        and mcp_case.get("source") == "mcp"
                        and isinstance(mcp_case.get("financial-health"), dict)
                        and isinstance(mcp_case.get("investment-analysis"), dict)
                        and isinstance(mcp_case.get("persona"), str)
                    ):
                        payload = {
                            "financial-health.json": json.dumps(
                                mcp_case["financial-health"], separators=(",", ":"), ensure_ascii=False
                            ),
                            "investment-analysis.json": json.dumps(
                                mcp_case["investment-analysis"], separators=(",", ":"), ensure_ascii=False
                            ),
                            "persona.md": mcp_case["persona"],
                        }
                except Exception:
                    pass

            for fname in required:
                dest = cdir / fname
                if not dest.is_file():
                    _write_atomic_text(dest, payload[fname])

    return target_root


def resolve_case_dir(case_id: str, cases_dir: str | Path | None = None) -> Path:
    """Resolve the directory holding ``financial-health.json``, ``investment-analysis.json`` and ``persona.md``."""
    required = ("financial-health.json", "investment-analysis.json", "persona.md")
    if cases_dir is not None:
        explicit = Path(cases_dir) / case_id
        if explicit.is_dir() and all((explicit / fname).is_file() for fname in required):
            return explicit
        raise FileNotFoundError(
            f"No se encontraron los archivos del caso '{case_id}' en: {explicit}"
        )

    repo_root = _repo_root()
    cwd = Path.cwd()
    candidates: list[Path] = []
    for env_var in ("SHERPAS_CASES_DIR", "CASES_DIR"):
        env_dir = os.environ.get(env_var)
        if env_dir:
            candidates.append(Path(env_dir) / case_id)
    candidates.extend(
        [
            repo_root / "cases" / case_id,
            cwd / "cases" / case_id,
            repo_root.parent / "cases" / case_id,
            repo_root.parent / "hackathon-upv-2026" / "cases" / case_id,
            cwd.parent / "hackathon-upv-2026" / "cases" / case_id,
            DEFAULT_FALLBACK_CASES_DIR / case_id,
        ]
    )

    for candidate in candidates:
        if candidate.is_dir() and all((candidate / fname).is_file() for fname in required):
            return candidate

    if case_id in SUPPORTED_CASES:
        embedded_case = _ensure_embedded_cases_dir() / case_id
        if embedded_case.is_dir() and all((embedded_case / fname).is_file() for fname in required):
            return embedded_case

    searched = ", ".join(str(p) for p in candidates)
    raise FileNotFoundError(
        f"No se encontraron los archivos del caso '{case_id}' en: {searched}"
    )


def list_available_cases(cases_dir: str | Path | None = None) -> list[str]:
    """Return available case identifiers found across configured case directories."""
    available: list[str] = []
    for case_id in SUPPORTED_CASES:
        try:
            resolve_case_dir(case_id, cases_dir=cases_dir)
            available.append(case_id)
        except FileNotFoundError:
            continue
    return available


def _parse_persona_markdown(markdown_text: str) -> dict[str, Any]:
    """Extract structured sections from ``persona.md`` without inventing facts."""
    sections: dict[str, str] = {}
    current_heading = "_preamble"
    buffer: list[str] = []
    for line in markdown_text.splitlines():
        if line.startswith("## "):
            sections[current_heading] = "\n".join(buffer).strip()
            current_heading = line[3:].strip()
            buffer = []
        else:
            buffer.append(line)
    sections[current_heading] = "\n".join(buffer).strip()

    concerns: dict[str, str] = {}
    for line in sections.get("Objective concerns", "").splitlines():
        cleaned_line = line.strip()
        match = re.match(r"^- \*\*(O\d+)\b(?:[^:*]+)?:\s*(.+)$", cleaned_line)
        if not match:
            match = re.match(r"^- \*\*(O\d+)\s+([^:]+):\*\*\s*(.+)$", cleaned_line)
            if match:
                concerns[match.group(1)] = f"{match.group(2)}: {match.group(3)}".replace("**", "").strip()
                continue
        if match:
            concerns[match.group(1)] = match.group(2).replace("**", "").strip()

    tensions: dict[str, str] = {}
    for line in sections.get("Tensions", "").splitlines():
        match = re.match(r"^- \*\*(T\d+)\b.*?\*\*\s*(.+)$", line.strip())
        if match:
            tensions[match.group(1)] = match.group(2).strip()

    transition_alerts: list[str] = []
    for line in sections.get("Transition alerts", "").splitlines():
        cleaned = line.strip()
        if cleaned.startswith("- "):
            transition_alerts.append(cleaned[2:].strip())
        elif cleaned and not cleaned.lower().startswith("none detected"):
            transition_alerts.append(cleaned)

    return {
        "raw": markdown_text,
        "sections": sections,
        "objective_concerns": concerns,
        "tensions": tensions,
        "transition_alerts_text": sections.get("Transition alerts", ""),
        "transition_alerts": transition_alerts,
        "d3_text": sections.get("D3: Gap severity", ""),
        "d5_text": sections.get("D5: Decision-making style", ""),
        "d6_text": sections.get("D6: Motivational anchor", ""),
    }


def load_case_data(case_id: str, cases_dir: str | Path | None = None) -> dict[str, Any]:
    """Load real JSON and persona markdown files for ``case_id``."""
    case_path = resolve_case_dir(case_id, cases_dir=cases_dir)
    fh = json.loads((case_path / "financial-health.json").read_text(encoding="utf-8-sig"))
    ia = json.loads((case_path / "investment-analysis.json").read_text(encoding="utf-8-sig"))
    persona_md = (case_path / "persona.md").read_text(encoding="utf-8-sig")
    return {
        "case_id": case_id,
        "case_dir": str(case_path),
        "financial_health": fh,
        "investment_analysis": ia,
        "persona": _parse_persona_markdown(persona_md),
    }


def _parse_rate(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip().rstrip("%")
        try:
            return float(stripped) / (100.0 if "%" in value else 1.0)
        except ValueError:
            return 0.0
    return 0.0


def _fmt_usd(amount: float) -> str:
    sign = "-" if amount < 0 else ""
    abs_val = abs(amount)
    if abs(abs_val - round(abs_val)) < 0.005:
        return f"{sign}${round(abs_val):,.0f}"
    return f"{sign}${abs_val:,.2f}"


def _extract_waterfall_rows(ia: dict[str, Any]) -> list[dict[str, Any]]:
    raw = (
        ia.get("key_metrics", {})
        .get("savingsAndContributions", {})
        .get("savingsWaterfall", [])
    )
    if not raw or len(raw) < 2:
        return []
    rows: list[dict[str, Any]] = []
    for row in raw[1:]:
        if not isinstance(row, list) or len(row) < 2:
            continue
        padded = row + [""] * max(0, 8 - len(row))
        rows.append(
            {
                "bucket_number": padded[0],
                "bucket": str(padded[1]),
                "current": padded[2],
                "optimal_target": padded[3],
                "status": str(padded[4]),
                "delta": padded[5],
                "flag": str(padded[6]),
                "notes": str(padded[7]),
            }
        )
    return rows


def _waterfall_by_number(rows: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    mapping: dict[int, dict[str, Any]] = {}
    for row in rows:
        num = row.get("bucket_number")
        if isinstance(num, int):
            mapping[num] = row
    return mapping


def _extract_federal_ordinary_rate(ia: dict[str, Any]) -> float:
    rows = ia.get("key_metrics", {}).get("taxDragAnalysis", {}).get("effectiveTaxMargin", [])
    for row in rows:
        if isinstance(row, list) and len(row) >= 2 and row[0] == "Federal ordinary":
            return _parse_rate(row[1])
    return 0.0


def _extract_tax_drag_annual(ia: dict[str, Any]) -> float:
    rollup = ia.get("key_metrics", {}).get("taxDragAnalysis", {}).get("householdRollup", [])
    for row in rollup:
        if isinstance(row, list) and len(row) >= 2 and "In-scope tax cost" in str(row[0]):
            return float(row[1])
    for row in rollup:
        if isinstance(row, list) and len(row) >= 2 and "Total annual tax cost" in str(row[0]):
            return float(row[1])
    return 0.0


def _extract_cash_earned_annual(ia: dict[str, Any]) -> float:
    summary = ia.get("key_metrics", {}).get("cashNeeds", {}).get("summaryIncome", [])
    for row in summary:
        if isinstance(row, list) and len(row) >= 2 and row[0] == "Total":
            try:
                return float(row[1])
            except (TypeError, ValueError):
                return 0.0
    return 0.0


def _extract_life_shortfall_from_persona(persona: dict[str, Any]) -> float:
    d3 = persona.get("d3_text", "")
    # Sum explicit "shortfall of $X" / "a shortfall of $X" inside Life insurance / Protection bullets.
    total = 0.0
    for line in d3.splitlines():
        lower = line.lower()
        if "life insurance" in lower or ("protection" in lower and "life" in lower):
            for m in re.finditer(r"shortfall of \$([0-9,]+)|\$([0-9,]+)\s+shortfall", line):
                val = m.group(1) or m.group(2)
                total += float(val.replace(",", ""))
    if total > 0:
        return total
    # Fallback: check Objective concerns O1/O2/O3 for "Shortfalls of $X ... and $Y"
    for text in persona.get("objective_concerns", {}).values():
        if "life insurance" in text.lower() or "shortfall" in text.lower():
            matches = re.findall(r"\$([0-9,]+)", text)
            if "shortfalls of" in text.lower() and len(matches) >= 2:
                return sum(float(x.replace(",", "")) for x in matches[:2])
            m = re.search(r"shortfall of \$([0-9,]+)", text.lower())
            if m:
                return float(m.group(1).replace(",", ""))
    return 0.0


def _extract_unconfirmed_assets(persona: dict[str, Any]) -> list[str]:
    text = " ".join(persona.get("objective_concerns", {}).values()) + "\n" + persona.get("d3_text", "")
    assets: list[str] = []
    if re.search(r"home(?:owners)?\s+policy.*?(?:not recorded|uninsured|no homeowners)", text, re.I) or (
        "no homeowners" in text.lower() or "no home or auto insurance recorded" in text.lower()
    ):
        assets.append("Primary home ($900,000)" if "$900,000" in text else "Primary home")
    if "porsche cayenne" in text.lower() and "uninsured" in text.lower():
        assets.append("Porsche Cayenne ($80,000)")
    return assets


def _parse_iso_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _month_year_label(d: date) -> str:
    months = (
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    )
    return f"{months[d.month - 1]} {d.year}"


@dataclass
class IRLStep:
    """Single actionable step inside the Run IRL timeline."""

    step_id: str
    node_id: str
    day: int
    due_date: date
    phase: str
    title: str
    action_plain: str
    action_math: str
    estimated_minutes: int
    ownership_mode: str  # "single" | "owner_a" | "owner_b" | "joint"
    owner_label: str
    required_members: tuple[str, ...]
    waterfall_buckets: tuple[int, ...] = ()
    json_sources: tuple[str, ...] = ()
    inertia_lever_key: str | None = None
    completed_by: dict[str, int] = field(default_factory=dict)

    @property
    def is_completed(self) -> bool:
        return all(m in self.completed_by for m in self.required_members)

    @property
    def completion_ratio(self) -> str:
        done = sum(1 for m in self.required_members if m in self.completed_by)
        return f"{done}/{len(self.required_members)}"

    @property
    def missing_members(self) -> list[str]:
        return [m for m in self.required_members if m not in self.completed_by]

    def status_at(self, current_day: int) -> str:
        if self.is_completed:
            return "completed"
        if current_day > self.day:
            return "overdue"
        if current_day == self.day:
            return "active"
        return "upcoming"

    def to_dict(
        self,
        current_day: int,
        member_names: dict[str, str],
        step_inertia: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        status = self.status_at(current_day)
        missing_labels = [member_names.get(m, m) for m in self.missing_members]
        return {
            "step_id": self.step_id,
            "node_id": self.node_id,
            "day": self.day,
            "due_date": self.due_date.isoformat(),
            "phase": self.phase,
            "title": self.title,
            "action_plain": self.action_plain,
            "action_math": self.action_math,
            "estimated_minutes": self.estimated_minutes,
            "ownership_mode": self.ownership_mode,
            "owner_label": self.owner_label,
            "required_members": list(self.required_members),
            "completed_by": dict(self.completed_by),
            "is_completed": self.is_completed,
            "completion_ratio": self.completion_ratio,
            "missing_members": list(self.missing_members),
            "missing_member_labels": missing_labels,
            "status": status,
            "days_overdue": max(0, current_day - self.day) if status == "overdue" else 0,
            "waterfall_buckets": list(self.waterfall_buckets),
            "json_sources": list(self.json_sources),
            "inertia_lever_key": self.inertia_lever_key,
            "inertia_cost": step_inertia or {},
        }


class IRLEngine:
    """Stateful deterministic Run IRL engine for a Sherpas household case."""

    def __init__(
        self,
        case_id: str,
        *,
        cases_dir: str | Path | None = None,
        start_date: date | None = None,
    ) -> None:
        self.case_id = case_id
        self.case_data = load_case_data(case_id, cases_dir=cases_dir)
        self.fh: dict[str, Any] = self.case_data["financial_health"]
        self.ia: dict[str, Any] = self.case_data["investment_analysis"]
        self.persona: dict[str, Any] = self.case_data["persona"]

        window_end = (
            self.ia.get("key_metrics", {})
            .get("performanceAnalysis", {})
            .get("window", {})
            .get("endDate")
        )
        inferred_start = _parse_iso_date(window_end) if window_end else None
        self.start_date: date = start_date or inferred_start or DEFAULT_PLAN_START_DATE

        self.household: list[dict[str, Any]] = self.fh.get("case", {}).get("household", [])
        self.adults: list[dict[str, Any]] = [
            p for p in self.household if p.get("role") in ("client", "co-client")
        ]
        self.is_couple: bool = len(self.adults) >= 2
        self.member_names: dict[str, str] = self._build_member_names()
        self.waterfall_rows = _extract_waterfall_rows(self.ia)
        self.waterfall_map = _waterfall_by_number(self.waterfall_rows)

        self.current_day: int = 0
        self.active_view: str = "focus_mode"
        self.simulation_run_count: int = 1
        self.simulation_completed: bool = True
        self.simulation_choices: list[dict[str, Any]] = self._default_summit_choices()

        self.inertia_levers: dict[str, dict[str, Any]] = self._extract_inertia_levers()
        self.steps: list[IRLStep] = self._build_steps()
        self._steps_by_id: dict[str, IRLStep] = {s.step_id: s for s in self.steps}

    def _build_member_names(self) -> dict[str, str]:
        if not self.adults:
            return {"single": "Titular"}
        client = self.adults[0].get("first_name", "Titular")
        if not self.is_couple:
            return {"single": client, "client": client, "A": client}
        co_client = self.adults[1].get("first_name", "Pareja")
        return {
            "A": f"Owner A ({client})",
            "B": f"Owner B ({co_client})",
            "A_first": client,
            "B_first": co_client,
        }

    def _default_summit_choices(self) -> list[dict[str, Any]]:
        score_obj = self.fh.get("score", {})
        top_moves = score_obj.get("top_moves", [])
        return [
            {
                "title": m.get("title"),
                "action": m.get("action"),
                "score_before": m.get("score_before"),
                "score_after": m.get("score_after"),
                "effort": m.get("effort"),
            }
            for m in top_moves
        ]

    def _extract_inertia_levers(self) -> dict[str, dict[str, Any]]:
        """Derive all ongoing inertia cost levers strictly from JSON & persona.md."""
        levers: dict[str, dict[str, Any]] = {}
        fed_ord = _extract_federal_ordinary_rate(self.ia)

        # 1. High-interest revolving card debt (>7% APR)
        liabilities = self.fh.get("profile", {}).get("liabilities", [])
        high_cards = [
            lib
            for lib in liabilities
            if lib.get("type") == "PERSONAL_CREDIT_CARD" and float(lib.get("interest_rate", 0)) > 0.07
        ]
        if high_cards:
            card = max(high_cards, key=lambda x: float(x.get("balance", 0)) * float(x.get("interest_rate", 0)))
            bal = float(card.get("balance", 0))
            apr = float(card.get("interest_rate", 0))
            annual_gross = round(bal * apr, 2)
            daily_gross = round(annual_gross / 365.0, 2)
            cash_earned = _extract_cash_earned_annual(self.ia)
            accessible_cash = float(
                self.ia.get("key_metrics", {}).get("cashNeeds", {}).get("accessibleCash", 0)
            )
            net_annual = round(annual_gross - cash_earned, 2) if cash_earned > 0 else annual_gross
            levers["high_apr_card"] = {
                "key": "high_apr_card",
                "label": f"{card.get('name')} ({_fmt_usd(bal)} al {apr * 100:.1f}% APR)",
                "balance_usd": bal,
                "apr_pct": round(apr * 100, 2),
                "annual_cost_usd": annual_gross,
                "daily_cost_usd": daily_gross,
                "cash_earned_annual_usd": cash_earned,
                "accessible_cash_usd": accessible_cash,
                "net_annual_loss_usd": net_annual,
                "source": "financial-health.json: profile.liabilities + investment-analysis.json: cashNeeds.summaryIncome",
            }

        # 2. Unused 401(k) tax-advantaged room (waterfall #13)
        wf13 = self.waterfall_map.get(13, {})
        wf13_cur = wf13.get("current")
        wf13_tgt = wf13.get("optimal_target")
        if isinstance(wf13_cur, (int, float)) and isinstance(wf13_tgt, (int, float)) and wf13_tgt > wf13_cur:
            room_401k = float(wf13_tgt - wf13_cur)
            tax_saved_401k = round(room_401k * fed_ord, 2)
            levers["401k_tax_delay"] = {
                "key": "401k_tax_delay",
                "label": f"Margen 401(k) sin aportar ({_fmt_usd(room_401k)} al {fed_ord * 100:.0f}%)",
                "unused_room_usd": room_401k,
                "marginal_rate_pct": round(fed_ord * 100, 2),
                "annual_cost_usd": tax_saved_401k,
                "daily_cost_usd": round(tax_saved_401k / 365.0, 2),
                "source": "investment-analysis.json: savingsWaterfall[#13] + effectiveTaxMargin",
            }

        # 3. Unused HSA room (waterfall #11)
        wf11 = self.waterfall_map.get(11, {})
        wf11_cur = wf11.get("current")
        wf11_tgt = wf11.get("optimal_target")
        if isinstance(wf11_cur, (int, float)) and isinstance(wf11_tgt, (int, float)) and wf11_tgt > wf11_cur:
            room_hsa = float(wf11_tgt - wf11_cur)
            tax_saved_hsa = round(room_hsa * fed_ord, 2)
            levers["hsa_tax_delay"] = {
                "key": "hsa_tax_delay",
                "label": f"Margen HSA sin aportar ({_fmt_usd(room_hsa)} al {fed_ord * 100:.0f}%)",
                "unused_room_usd": room_hsa,
                "marginal_rate_pct": round(fed_ord * 100, 2),
                "annual_cost_usd": tax_saved_hsa,
                "daily_cost_usd": round(tax_saved_hsa / 365.0, 2),
                "source": "investment-analysis.json: savingsWaterfall[#11] + effectiveTaxMargin",
            }

        # 4. In-scope taxable investment tax drag
        tax_drag = _extract_tax_drag_annual(self.ia)
        if tax_drag > 0:
            levers["tax_drag"] = {
                "key": "tax_drag",
                "label": f"Fuga fiscal en cuenta sujeta a impuestos ({_fmt_usd(tax_drag)}/ano)",
                "annual_cost_usd": round(tax_drag, 2),
                "daily_cost_usd": round(tax_drag / 365.0, 2),
                "source": "investment-analysis.json: taxDragAnalysis.householdRollup",
            }

        # 5. Life insurance & liability protection gap (risk days)
        life_shortfall = _extract_life_shortfall_from_persona(self.persona)
        pillars = {p.get("pillar"): p for p in self.fh.get("score", {}).get("pillars", [])}
        prot_pillar = pillars.get("Insurance and protection", {})
        if life_shortfall > 0:
            levers["life_protection_gap"] = {
                "key": "life_protection_gap",
                "label": f"Brecha seguro de vida ({_fmt_usd(-life_shortfall)}, Proteccion {prot_pillar.get('points_shown_in_app', '')})",
                "shortfall_usd": life_shortfall,
                "protection_points": prot_pillar.get("points_shown_in_app", ""),
                "annual_cost_usd": 0.0,
                "daily_cost_usd": 0.0,
                "tracks_days_uninsured": True,
                "source": "persona.md: D3 + financial-health.json: score.pillars",
            }

        # 6. Unconfirmed home / vehicle property coverage (e.g. Samantha)
        unconfirmed = _extract_unconfirmed_assets(self.persona)
        if unconfirmed:
            levers["unconfirmed_property_policy"] = {
                "key": "unconfirmed_property_policy",
                "label": "Polizas sin confirmar: " + ", ".join(unconfirmed),
                "unconfirmed_assets": unconfirmed,
                "annual_cost_usd": 0.0,
                "daily_cost_usd": 0.0,
                "tracks_days_uninsured": True,
                "source": "persona.md: O4 + financial-health.json: score.top_moves[0]",
            }

        return levers

    def _add_step(
        self,
        steps: list[IRLStep],
        *,
        step_id: str,
        node_id: str,
        day: int,
        phase: str,
        title: str,
        action_plain: str,
        action_math: str,
        estimated_minutes: int,
        ownership_mode: str,
        waterfall_buckets: tuple[int, ...] = (),
        json_sources: tuple[str, ...] = (),
        inertia_lever_key: str | None = None,
    ) -> None:
        if ownership_mode == "single":
            owner_label = self.member_names["single"]
            required = ("single",)
        elif ownership_mode == "owner_a":
            owner_label = self.member_names["A"]
            required = ("A",)
        elif ownership_mode == "owner_b":
            owner_label = self.member_names["B"]
            required = ("B",)
        elif ownership_mode == "joint":
            a_name = self.member_names.get("A_first", "A")
            b_name = self.member_names.get("B_first", "B")
            owner_label = f"Conjunto 2/2 ({a_name} & {b_name})"
            required = ("A", "B")
        else:
            raise ValueError(f"ownership_mode invalido: {ownership_mode}")

        steps.append(
            IRLStep(
                step_id=step_id,
                node_id=node_id,
                day=day,
                due_date=self.start_date + timedelta(days=day),
                phase=phase,
                title=title,
                action_plain=action_plain,
                action_math=action_math,
                estimated_minutes=estimated_minutes,
                ownership_mode=ownership_mode,
                owner_label=owner_label,
                required_members=required,
                waterfall_buckets=waterfall_buckets,
                json_sources=json_sources,
                inertia_lever_key=inertia_lever_key,
            )
        )

    def _build_steps(self) -> list[IRLStep]:
        """Build the Day 0 -> Day 3 -> Day 14 -> Day 30 -> Milestones step sequence."""
        steps: list[IRLStep] = []
        if self.case_id == "michael-carter":
            self._build_michael_steps(steps)
        elif self.case_id == "samantha-lewis":
            self._build_samantha_steps(steps)
        elif self.case_id == "timothy-melanie-weah":
            self._build_weah_steps(steps)
        elif self.case_id == "daniel-emily-johnson":
            self._build_johnson_steps(steps)
        else:
            self._build_generic_steps(steps)

        self._append_real_milestones(steps)
        steps.sort(key=lambda s: (s.day, s.step_id))
        return steps

    def _build_michael_steps(self, steps: list[IRLStep]) -> None:
        card = self.inertia_levers["high_apr_card"]
        k401 = self.inertia_levers["401k_tax_delay"]
        tdrag = self.inertia_levers["tax_drag"]
        top_moves = self.fh.get("score", {}).get("top_moves", [])
        umb_move = top_moves[0] if top_moves else {}
        glide_move = top_moves[2] if len(top_moves) > 2 else {}

        self._add_step(
            steps,
            step_id="step_0_pay_amex",
            node_id="day_0",
            day=0,
            phase="day_0",
            title="Paso 1 (3 min): Ordenar pago total de Amex Platinum ($3,500)",
            action_plain=(
                "Usa $3,500 de tus $27,000 en banco para liquidar hoy la tarjeta Amex al 20% "
                "y cortar una fuga garantizada de $700/ano ($1.92/dia)."
            ),
            action_math=(
                f"savingsWaterfall #8: Pay high-interest debt (>7%) | {card['label']} -> "
                f"{_fmt_usd(card['annual_cost_usd'])}/yr ({_fmt_usd(card['daily_cost_usd'])}/day)."
            ),
            estimated_minutes=3,
            ownership_mode="single",
            waterfall_buckets=(8,),
            json_sources=("profile.liabilities", "savingsWaterfall[8]"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_confirm_amex_zero_and_umbrella",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3: Confirmar Amex a $0 y cotizar poliza Umbrella $1M",
            action_plain=(
                "Verifica que el saldo de Amex quedo en $0 y pide presupuesto del escudo "
                "Umbrella de $1M para subir tu score de 26 a 31."
            ),
            action_math=(
                f"top_moves[0]: {umb_move.get('action', 'Add $1M of umbrella')} "
                f"(score {umb_move.get('score_before', 26)} -> {umb_move.get('score_after', 31)}); "
                "savingsWaterfall #2."
            ),
            estimated_minutes=10,
            ownership_mode="single",
            waterfall_buckets=(2, 8),
            json_sources=("score.top_moves[0]", "savingsWaterfall[2]"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_14_review_jnk_and_glide",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14: Revisar bono JNK ($527/ano tax drag) y ajuste growth 74% -> 88%",
            action_plain=(
                "Revisa el fondo JNK ($15,000) en tu cuenta imponible (cuesta ~$527/ano en impuestos) "
                "y planifica mover ~$19,900 hacia tu perfil growth objetivo."
            ),
            action_math=(
                f"taxDragAnalysis: In-scope tax cost {_fmt_usd(tdrag['annual_cost_usd'])}/yr "
                "(JNK $247.20/yr al 24%); top_moves[2]: "
                f"{glide_move.get('action', '74% -> 88% growth')}."
            ),
            estimated_minutes=15,
            ownership_mode="single",
            waterfall_buckets=(14,),
            json_sources=("taxDragAnalysis.householdRollup", "score.top_moves[2]"),
            inertia_lever_key="tax_drag",
        )
        self._add_step(
            steps,
            step_id="step_30_boost_401k_and_hsa",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30: Subir aportacion 401(k) (+$7,500 margen = $1,800/ano ahorro fiscal)",
            action_plain=(
                "Sube en nomina tu aportacion al 401(k) de $17,000 a $24,500 (+$7,500 de margen, "
                "$1,800/ano menos de impuestos) y completa los $400 restantes de tu HSA."
            ),
            action_math=(
                f"savingsWaterfall #13: 401(k) $17,000 -> $24,500 ({_fmt_usd(k401['annual_cost_usd'])}/yr "
                "ahorro fiscal al 24%); savingsWaterfall #11 HSA $4,000 -> $4,400; #10 Roth IRA $4,500."
            ),
            estimated_minutes=10,
            ownership_mode="single",
            waterfall_buckets=(10, 11, 13),
            json_sources=("savingsWaterfall[10,11,13]", "persona.md: O7"),
            inertia_lever_key="401k_tax_delay",
        )

    def _build_samantha_steps(self, steps: list[IRLStep]) -> None:
        tdrag = self.inertia_levers["tax_drag"]
        k401 = self.inertia_levers["401k_tax_delay"]
        hsa = self.inertia_levers["hsa_tax_delay"]
        top_moves = self.fh.get("score", {}).get("top_moves", [])
        cov_move = top_moves[0] if top_moves else {}
        conc_move = top_moves[1] if len(top_moves) > 1 else {}

        self._add_step(
            steps,
            step_id="step_0_confirm_home_auto_policies",
            node_id="day_0",
            day=0,
            phase="day_0",
            title="Paso 1 (3 min): Confirmar polizas de hogar ($900k) y Porsche Cayenne ($80k)",
            action_plain=(
                "Sube o confirma hoy la vigencia de tu seguro de hogar ($4,500/ano presupuestados) "
                "y del Porsche Cayenne; figuran sin poliza registrada pese a tu score 82."
            ),
            action_math=(
                f"top_moves[0]: {cov_move.get('action', 'Add homeowners insurance')} "
                f"(score {cov_move.get('score_before', 82)} -> {cov_move.get('score_after', 84)}); "
                "persona.md O4 ($900,000 home & $80,000 Porsche Cayenne)."
            ),
            estimated_minutes=3,
            ownership_mode="single",
            waterfall_buckets=(2,),
            json_sources=("score.top_moves[0]", "persona.md: O4"),
            inertia_lever_key="unconfirmed_property_policy",
        )
        self._add_step(
            steps,
            step_id="step_3_verify_coverage_and_tax_drag",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3: Verificar polizas activas y auditar $3,032/ano de tax drag",
            action_plain=(
                "Confirma cobertura activa de vivienda/vehiculo y recopila el cost basis de tu "
                "brokerage ($300k) para frenar los ~$3,032/ano de fuga fiscal en dividendos."
            ),
            action_math=(
                f"taxDragAnalysis: In-scope tax cost {_fmt_usd(tdrag['annual_cost_usd'])}/yr "
                f"({_fmt_usd(tdrag['daily_cost_usd'])}/day); JNK $1,229.15/yr + SCHD $852.85/yr "
                "al 35.8%; costBasisBlockingNotes."
            ),
            estimated_minutes=15,
            ownership_mode="single",
            waterfall_buckets=(2, 14),
            json_sources=("taxDragAnalysis", "persona.md: O4, O8"),
            inertia_lever_key="tax_drag",
        )
        self._add_step(
            steps,
            step_id="step_14_hsa_and_vti_concentration",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14: Aportar $4,400 a HSA y bajar concentracion VTI (39% -> 25%)",
            action_plain=(
                "Abre o aporta el maximo de $4,400 al HSA ($1,408/ano ahorro fiscal) y planifica "
                "bajar VTI del 39% al 25% (~$58,300) ajustando tu riesgo de 85% a 80%."
            ),
            action_math=(
                f"savingsWaterfall #11 HSA $0 -> $4,400 ({_fmt_usd(hsa['annual_cost_usd'])}/yr al 32%); "
                f"top_moves[1]: {conc_move.get('action', 'VTI 39% -> 25%')}."
            ),
            estimated_minutes=15,
            ownership_mode="single",
            waterfall_buckets=(11,),
            json_sources=("savingsWaterfall[11]", "score.top_moves[1,2]"),
            inertia_lever_key="hsa_tax_delay",
        )
        self._add_step(
            steps,
            step_id="step_30_activate_retirement_401k",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30: Activar jubilacion ($0 actual -> $24,500 margen 401(k) / $7,500 IRA)",
            action_plain=(
                "Hoy tienes $0 en cuentas de retiro y te quedas sin liquidez a los 74 anos (2053). "
                "Confirma acceso al 401(k) ($24,500) o aporta $7,500 a Traditional IRA deducible."
            ),
            action_math=(
                f"savingsWaterfall #13 401(k) $0 -> $24,500 ({_fmt_usd(k401['annual_cost_usd'])}/yr "
                "potencial al 32%); projections.yearly 2053: -$227,414 investable_assets."
            ),
            estimated_minutes=15,
            ownership_mode="single",
            waterfall_buckets=(13,),
            json_sources=("savingsWaterfall[13]", "persona.md: O1, O7", "projections.yearly"),
            inertia_lever_key="401k_tax_delay",
        )

    def _build_weah_steps(self, steps: list[IRLStep]) -> None:
        card = self.inertia_levers["high_apr_card"]
        k401 = self.inertia_levers["401k_tax_delay"]
        net_loss = card["net_annual_loss_usd"]

        self._add_step(
            steps,
            step_id="step_0_melanie_schedule_card_payoff",
            node_id="day_0",
            day=0,
            phase="day_0",
            title="Paso 1 (3 min) — Owner B (Melanie): Programar pago tarjeta Chase $18,000 (18%)",
            action_plain=(
                "Melanie, programa hoy el pago de los $18,000 de la tarjeta Chase al 18% usando parte "
                "de tus $150,000 en efectivo (que rinden ~$150/ano mientras la tarjeta quema $3,240/ano)."
            ),
            action_math=(
                f"Owner B (Melanie) Cash account $150,000 -> Chase CC $18,000 @ 18% APR: "
                f"{_fmt_usd(card['annual_cost_usd'])}/yr brutos ({_fmt_usd(card['daily_cost_usd'])}/day) "
                f"vs {_fmt_usd(card['cash_earned_annual_usd'])}/yr cash earned "
                f"({_fmt_usd(net_loss)}/yr perdida neta; top_moves[0]: 60 -> 62)."
            ),
            estimated_minutes=3,
            ownership_mode="owner_b",
            waterfall_buckets=(8,),
            json_sources=("profile.liabilities", "profile.accounts", "savingsWaterfall[8]"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_melanie_confirm_card_paid",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Owner B (Melanie): Liquidar completamente tarjeta $18,000 al 18% APR",
            action_plain=(
                "Melanie, confirma que la tarjeta Chase ($18,000 al 18% APR) quedo liquidada a $0 "
                "con el excedente de efectivo ($60,222.50 sobre la reserva)."
            ),
            action_math=(
                f"savingsWaterfall #8 Pay high-interest debt (>7%): $18,000 -> $0; "
                f"accessibleCash $150,800 (excess $60,222.50); elimina {_fmt_usd(card['daily_cost_usd'])}/day."
            ),
            estimated_minutes=5,
            ownership_mode="owner_b",
            waterfall_buckets=(8,),
            json_sources=("savingsWaterfall[8]", "cashNeeds.accessibleCashExcess"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_joint_life_and_umbrella",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Check conjunto (2/2): Solicitar seguro de vida +$1.1M y Umbrella $1M",
            action_plain=(
                "Timothy y Melanie deben confirmar ambos (2/2) la solicitud de seguro de vida "
                "($610k Timothy + $490k Melanie) y poliza Umbrella de $1M para proteger a Liam y Josh."
            ),
            action_math=(
                "combined_moves[0]: Pay down revolving card + Add life cover + Add umbrella cover "
                "(score 60 -> 78); savingsWaterfall #2: $250,000 -> $2,350,000."
            ),
            estimated_minutes=15,
            ownership_mode="joint",
            waterfall_buckets=(2,),
            json_sources=("score.combined_moves[0]", "savingsWaterfall[2]", "persona.md: O1, O3"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_14_timothy_reduce_upro",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14 — Owner A (Timothy): Reducir exposicion apalancada UPRO 3x ($12,740)",
            action_plain=(
                "Timothy, reduce el ETF apalancado 3x UPRO ($12,740 en tu Roth IRA, volatilidad 30%) "
                "hacia el objetivo moderado compartido (60% renta variable) para alinear la cordada."
            ),
            action_math=(
                "positions: UPRO (ProShares UltraPro S&P500, 3x leveraged) $12,740 "
                "(50.96% de IRA - Roth Timothy, volatility3y 30.04%); persona.md D4b/O6."
            ),
            estimated_minutes=10,
            ownership_mode="owner_a",
            waterfall_buckets=(10,),
            json_sources=("positions[UPRO]", "performanceAnalysis.goalGroups", "persona.md: O6"),
        )
        self._add_step(
            steps,
            step_id="step_14_joint_bind_protection",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14 — Check conjunto (2/2): Activar polizas de vida (+$1.1M) y Umbrella $1M",
            action_plain=(
                "Timothy y Melanie confirman ambos (2/2) la emision final de los seguros de vida y Umbrella."
            ),
            action_math="savingsWaterfall #2 cierre de brecha -$2,100,000; combined_moves 60 -> 78.",
            estimated_minutes=10,
            ownership_mode="joint",
            waterfall_buckets=(2,),
            json_sources=("score.combined_moves[0]", "savingsWaterfall[2]"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_30_timothy_401k_and_roth",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30 — Owner A (Timothy): Subir 401(k) (+$10,500 margen) y abrir Roth IRA",
            action_plain=(
                "Timothy, sube tu aportacion 401(k) de $14,000 a $24,500 (+$10,500) y programa tu "
                "Roth IRA ($5,250) aprovechando el ahorro fiscal combinado de $5,760/ano."
            ),
            action_math=(
                f"savingsWaterfall #13 (Timothy +$10,500 -> $24,500; ahorro fiscal familiar "
                f"{_fmt_usd(k401['annual_cost_usd'])}/yr al 24%); #10 Roth IRA $5,250.10."
            ),
            estimated_minutes=10,
            ownership_mode="owner_a",
            waterfall_buckets=(10, 13),
            json_sources=("savingsWaterfall[10,13]", "persona.md: O7"),
            inertia_lever_key="401k_tax_delay",
        )
        self._add_step(
            steps,
            step_id="step_30_melanie_401k_and_529",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30 — Owner B (Melanie): Subir 401(k) (+$13,500 margen) y arrancar 529 ($4,609/ano)",
            action_plain=(
                "Melanie, sube tu 401(k) de $11,000 a $24,500 (+$13,500), aporta a Roth IRA ($5,250) "
                "y activa el 529 de Liam y Josh ($4,609/ano)."
            ),
            action_math=(
                "savingsWaterfall #13 (Melanie +$13,500 -> $24,500); #12 Contribute to 529 accounts "
                "$4,609.22/yr; #10 Roth IRA $5,250.10."
            ),
            estimated_minutes=10,
            ownership_mode="owner_b",
            waterfall_buckets=(10, 12, 13),
            json_sources=("savingsWaterfall[10,12,13]", "persona.md: O4, O7"),
            inertia_lever_key="401k_tax_delay",
        )

    def _build_johnson_steps(self, steps: list[IRLStep]) -> None:
        card = self.inertia_levers["high_apr_card"]
        k401 = self.inertia_levers["401k_tax_delay"]

        self._add_step(
            steps,
            step_id="step_0_joint_halt_diversion_and_quote",
            node_id="day_0",
            day=0,
            phase="day_0",
            title="Paso 1 (3 min) — Check conjunto (2/2): Frenar desvio a brokerage/529 y atacar 24.9% + seguro",
            action_plain=(
                "Daniel y Emily confirman juntos (2/2) pausar el envio a brokerage ($12,000/ano) y "
                "exceso de 529 para atacar hoy la Chase Sapphire al 24.9% ($12.28/dia) y pedir seguro de vida."
            ),
            action_math=(
                f"Joint 2/2: {_fmt_usd(card['annual_cost_usd'])}/yr ({_fmt_usd(card['daily_cost_usd'])}/day) "
                "en Chase Sapphire 24.9% + brecha -$2,350,000 vida (Protection 0/20); top_moves[0,2]."
            ),
            estimated_minutes=3,
            ownership_mode="joint",
            waterfall_buckets=(2, 8),
            json_sources=("profile.liabilities", "savingsWaterfall[2,8]", "persona.md: D5, T4"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_daniel_attack_sapphire_card",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Owner A (Daniel): Atacar Chase Sapphire ($18,000 al 24.9% APR)",
            action_plain=(
                "Daniel, ejecuta el primer abono extraordinario contra la Chase Sapphire ($18,000 al 24.9% APR) "
                "que hoy consume $373.50/mes en intereses ($4,482/ano)."
            ),
            action_math=(
                f"Owner A (Daniel) Chase Sapphire: {_fmt_usd(card['balance_usd'])} @ 24.9% APR = "
                f"{_fmt_usd(card['annual_cost_usd'])}/yr ({_fmt_usd(card['daily_cost_usd'])}/day); "
                "savingsWaterfall #8."
            ),
            estimated_minutes=10,
            ownership_mode="owner_a",
            waterfall_buckets=(8,),
            json_sources=("profile.liabilities[0]", "savingsWaterfall[8]"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_emily_redirect_cashflow",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Owner B (Emily): Redirigir $15,032/ano libres y ahorro a reserva de 3 meses",
            action_plain=(
                "Emily, redirige los $15,032/ano de flujo libre y el ahorro a brokerage ($12,000/ano) "
                "para subir vuestra caja de 1.4 meses ($19,000) hacia los 3 meses minimos ($40,073)."
            ),
            action_math=(
                "Owner B (Emily) accounts: savingsWaterfall #1 ($19,000 -> $40,073, delta -$21,072); "
                "top_moves[2]: Redirect $15,032/year (score 52 -> 55)."
            ),
            estimated_minutes=10,
            ownership_mode="owner_b",
            waterfall_buckets=(1, 3),
            json_sources=("savingsWaterfall[1]", "score.top_moves[2]", "profile.accounts"),
        )
        self._add_step(
            steps,
            step_id="step_3_joint_life_and_umbrella_quotes",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Check conjunto (2/2): Pedir cotizacion seguro vida (+$1.166M / -$2.35M) y Umbrella $1M",
            action_plain=(
                "Daniel y Emily confirman ambos (2/2) las solicitudes de seguro de vida "
                "(Daniel -$1.35M, Emily -$1.00M) y Umbrella $1M para salir de Proteccion 0/20."
            ),
            action_math=(
                "combined_moves[0]: Raise mortality coverage (+$1,166,000 anchor toward -$2.35M gap) + "
                "Add umbrella cover ($1M) -> score 52 -> 60; Protection 0/20."
            ),
            estimated_minutes=15,
            ownership_mode="joint",
            waterfall_buckets=(2,),
            json_sources=("score.combined_moves[0]", "score.top_moves[0,1]", "persona.md: D3, O2, O3"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_14_joint_bind_life_umbrella",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14 — Check conjunto (2/2): Confirmar emision de vida (-$2.35M) y Umbrella $1M",
            action_plain=(
                "Daniel y Emily validan juntos (2/2) las polizas emitidas para dejar de acumular "
                "dias sin escudo familiar."
            ),
            action_math="savingsWaterfall #2: $450,000 -> $3,800,000 (delta -$3,350,000); score 52 -> 60.",
            estimated_minutes=10,
            ownership_mode="joint",
            waterfall_buckets=(2,),
            json_sources=("savingsWaterfall[2]", "score.combined_moves[0]"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_14_emily_review_tax_drag",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14 — Owner B (Emily): Revisar tax drag $658.65/ano y concentracion Tech (35.6%)",
            action_plain=(
                "Emily, revisa tu cuenta brokerage ($50,000 con JNK/SCHD/SCHP que generan $658.65/ano "
                "de impuestos) antes de aportar mas capital fuera del 401(k)."
            ),
            action_math=(
                "taxDragAnalysis: In-scope tax cost $658.65/yr (JNK $331.66 + SCHD $191.77 + SCHP $135.22); "
                "sectorConcentration Technology 35.63%."
            ),
            estimated_minutes=10,
            ownership_mode="owner_b",
            waterfall_buckets=(14,),
            json_sources=("taxDragAnalysis", "concentrationAndDiversification"),
            inertia_lever_key="tax_drag",
        )
        self._add_step(
            steps,
            step_id="step_30_daniel_activate_401k",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30 — Owner A (Daniel): Activar 401(k) desde $0 (match est. $6,400 + ahorro fiscal)",
            action_plain=(
                "Daniel, activa hoy tu 401(k) (hoy en $0) para capturar el match estimado ($6,400/ano) "
                "y sumar al ahorro fiscal potencial de $11,760/ano entre ambos."
            ),
            action_math=(
                f"savingsWaterfall #4 match est. $6,400 + #13 limite $24,500; entre ambos ($49,000 al 24%) "
                f"= {_fmt_usd(k401['annual_cost_usd'])}/yr de ahorro fiscal perdido mientras sigan en $0."
            ),
            estimated_minutes=10,
            ownership_mode="owner_a",
            waterfall_buckets=(4, 13),
            json_sources=("savingsWaterfall[4,13]", "persona.md: O1"),
            inertia_lever_key="401k_tax_delay",
        )
        self._add_step(
            steps,
            step_id="step_30_emily_activate_401k_and_rebalance_529",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30 — Owner B (Emily): Activar 401(k) desde $0 y ajustar 529 ($8,000 -> $1,928/ano)",
            action_plain=(
                "Emily, activa tu 401(k) (hoy $0, match est. $4,800/ano) y corrige la aportacion al 529 "
                "($8,000 actuales vs $1,928 recomendados) para priorizar tu propia jubilacion."
            ),
            action_math=(
                "savingsWaterfall #5 match est. $4,800 + #13 limite $24,500 + #12 529 $8,000 vs $1,928; "
                "persona.md T5 (mascarilla de oxigeno)."
            ),
            estimated_minutes=10,
            ownership_mode="owner_b",
            waterfall_buckets=(5, 12, 13),
            json_sources=("savingsWaterfall[5,12,13]", "persona.md: O1, T5"),
            inertia_lever_key="401k_tax_delay",
        )

    def _build_generic_steps(self, steps: list[IRLStep]) -> None:
        for idx, row in enumerate(self.waterfall_rows[:4]):
            day = _BASE_CHECKIN_DAYS[idx]
            mode = "joint" if self.is_couple else "single"
            self._add_step(
                steps,
                step_id=f"step_{day}_{row['bucket_number']}",
                node_id=f"day_{day}",
                day=day,
                phase=f"day_{day}",
                title=f"Dia {day}: {row['bucket']}",
                action_plain=f"Ejecutar paso #{row['bucket_number']}: {row['bucket']}.",
                action_math=f"savingsWaterfall[{row['bucket_number']}]: current={row['current']}, target={row['optimal_target']}.",
                estimated_minutes=3 if day == 0 else 10,
                ownership_mode=mode,
                waterfall_buckets=(int(row["bucket_number"]),) if isinstance(row["bucket_number"], int) else (),
                json_sources=("savingsWaterfall",),
            )

    def _append_real_milestones(self, steps: list[IRLStep]) -> None:
        """Append real milestone nodes from ``goals.chartGoals`` and ``persona.md`` Transition alerts."""
        seen_keys: set[tuple[str, str]] = set()
        goal_items: list[tuple[date, str, str, str, str]] = []

        # 1. Include short-term goals from investment-analysis cashNeeds (captures Ethan August 2027!)
        for stg in self.ia.get("key_metrics", {}).get("cashNeeds", {}).get("shortTermGoalsNeeded", []):
            d = _parse_iso_date(str(stg.get("date", "")))
            if d and d > self.start_date:
                name = str(stg.get("goal") or stg.get("description") or "Goal")
                amt = stg.get("amount")
                amt_txt = _fmt_usd(float(amt)) if isinstance(amt, (int, float)) else ""
                key = (d.isoformat(), name.lower())
                if key not in seen_keys:
                    seen_keys.add(key)
                    goal_items.append(
                        (
                            d,
                            name,
                            f"Hito real ({_month_year_label(d)}): {name} ({amt_txt})".strip(),
                            f"cashNeeds.shortTermGoalsNeeded: {name} {amt_txt} ({stg.get('paymentFrequency', '')})",
                            "cashNeeds.shortTermGoalsNeeded",
                        )
                    )

        # 2. Include goals.chartGoals from financial-health.json
        for cg in self.fh.get("goals", {}).get("chartGoals", []):
            d = _parse_iso_date(str(cg.get("date", "")))
            if not d or d <= self.start_date:
                continue
            goal_type = str(cg.get("goalType", "GOAL"))
            name = str(cg.get("name") or goal_type)
            key = (d.isoformat(), name.lower())
            if key in seen_keys:
                continue
            seen_keys.add(key)

            plain, math_txt = self._describe_chart_goal(d, goal_type, name)
            goal_items.append((d, name, plain, math_txt, "goals.chartGoals"))

        # Deduplicate near-identical dates if vacation already represented, keep chronological order
        mode = "joint" if self.is_couple else "single"
        for idx, (m_date, name, plain, math_txt, src) in enumerate(sorted(goal_items, key=lambda x: x[0])):
            day_offset = (m_date - self.start_date).days
            slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or f"goal_{idx}"
            node_id = f"milestone_{m_date.strftime('%Y_%m')}_{slug}"
            self._add_step(
                steps,
                step_id=f"step_{node_id}",
                node_id=node_id,
                day=day_offset,
                phase="milestone",
                title=f"Hito {_month_year_label(m_date)}: {name}",
                action_plain=plain,
                action_math=math_txt,
                estimated_minutes=15,
                ownership_mode=mode,
                json_sources=(src, "persona.md: Transition alerts"),
            )

    def _describe_chart_goal(self, m_date: date, goal_type: str, name: str) -> tuple[str, str]:
        label = _month_year_label(m_date)
        yearly = {r.get("year"): r for r in self.fh.get("projections", {}).get("yearly", [])}
        yr_row = yearly.get(m_date.year, {})
        inv_assets = yr_row.get("investable_assets")

        if goal_type == "PURCHASE" and "home" in name.lower():
            for g in self.fh.get("profile", {}).get("goals", []):
                if g.get("type") == "REAL_ESTATE_PURCHASE":
                    amt = float(g.get("amount", 0))
                    loan = g.get("planned_loan", {})
                    pmt = float(loan.get("monthly_payment", 0))
                    down = next(
                        (float(c["yearly"]) for c in g.get("yearly_costs", []) if "downpayment" in c.get("name", "").lower()),
                        0.0,
                    )
                    closing = next(
                        (float(c["yearly"]) for c in g.get("yearly_costs", []) if "closing" in c.get("name", "").lower()),
                        0.0,
                    )
                    plain = (
                        f"Decision de compra de vivienda en {label} ({_fmt_usd(amt)}): "
                        f"entrada {_fmt_usd(down)}, cierre {_fmt_usd(closing)}, hipoteca {_fmt_usd(pmt)}/mes."
                    )
                    math_txt = (
                        f"chartGoals + profile.goals: {_fmt_usd(amt)} ({label}); "
                        f"investable_assets {m_date.year}: {_fmt_usd(inv_assets) if inv_assets is not None else 'N/A'}."
                    )
                    return plain, math_txt

        if goal_type in ("BANKRUPTCY_ZEROCASH", "BANKRUPTCY"):
            age = yr_row.get("age_client")
            plain = (
                f"Alerta estructural de trayectoria en {label} (edad {age}): "
                f"sin ejecutar las palancas del plan, los activos liquidos caen a {_fmt_usd(float(inv_assets or 0))}."
            )
            math_txt = (
                f"goals.chartGoals ({goal_type}) + projections.yearly[{m_date.year}]: "
                f"investable_assets={_fmt_usd(float(inv_assets or 0))}, net_worth={_fmt_usd(float(yr_row.get('net_worth', 0)))}."
            )
            return plain, math_txt

        return (
            f"Revision de hito real en {label}: {name}.",
            f"goals.chartGoals ({goal_type}) -> {m_date.isoformat()}",
        )

    def _normalize_member(self, step: IRLStep, member: str | None) -> str:
        if not self.is_couple:
            if member is None or member.lower() in ("single", "client", "a", self.member_names["single"].lower()):
                return "single"
            raise ValueError(f"Miembro '{member}' invalido para hogar individual '{self.case_id}'.")

        a_first = self.member_names["A_first"].lower()
        b_first = self.member_names["B_first"].lower()
        if member is None:
            if step.ownership_mode in ("owner_a", "owner_b"):
                return step.required_members[0]
            raise ValueError(
                f"El paso conjunto '{step.step_id}' requiere especificar member='A' ({a_first}) o member='B' ({b_first})."
            )

        norm = member.strip().lower()
        if norm in ("a", "owner_a", "owner a", "client", a_first):
            resolved = "A"
        elif norm in ("b", "owner_b", "owner b", "co-client", "co_client", b_first):
            resolved = "B"
        else:
            raise ValueError(f"Miembro '{member}' no reconocido para pareja '{self.case_id}'.")

        if resolved not in step.required_members:
            raise ValueError(
                f"El paso '{step.step_id}' pertenece a '{step.owner_label}', no a '{member}'."
            )
        return resolved

    def check_step(
        self,
        step_id: str,
        *,
        member: str | None = None,
        completed_day: int | None = None,
    ) -> dict[str, Any]:
        """Mark a step (or one partner's half of a 2/2 joint step) as completed."""
        step = self._steps_by_id.get(step_id)
        if step is None:
            raise KeyError(f"Paso desconocido: '{step_id}'")
        resolved = self._normalize_member(step, member)
        day_val = self.current_day if completed_day is None else int(completed_day)
        step.completed_by[resolved] = day_val
        return step.to_dict(
            self.current_day,
            self.member_names,
            step_inertia=self._step_inertia_snapshot(step, self.current_day),
        )

    def uncheck_step(self, step_id: str, *, member: str | None = None) -> dict[str, Any]:
        """Revert completion on a step (or one partner's check on a joint step)."""
        step = self._steps_by_id.get(step_id)
        if step is None:
            raise KeyError(f"Paso desconocido: '{step_id}'")
        if member is None and step.ownership_mode == "joint":
            step.completed_by.clear()
        else:
            resolved = self._normalize_member(step, member)
            step.completed_by.pop(resolved, None)
        return step.to_dict(
            self.current_day,
            self.member_names,
            step_inertia=self._step_inertia_snapshot(step, self.current_day),
        )

    def _is_lever_resolved(self, lever_key: str) -> bool:
        linked = [s for s in self.steps if s.inertia_lever_key == lever_key]
        if not linked:
            return False
        if lever_key == "high_apr_card":
            settlement_steps = [s for s in linked if s.day <= 3]
            if not settlement_steps:
                return all(s.is_completed for s in linked)
            final_settlement_day = max(s.day for s in settlement_steps)
            return all(s.is_completed for s in settlement_steps if s.day == final_settlement_day)
        if lever_key == "unconfirmed_property_policy":
            return all(s.is_completed for s in linked if s.day <= 3)
        return all(s.is_completed for s in linked)

    def _step_inertia_snapshot(self, step: IRLStep, current_day: int) -> dict[str, Any]:
        if step.is_completed or not step.inertia_lever_key:
            return {"daily_cost_usd": 0.0, "accrued_cost_usd": 0.0, "days_overdue": 0}
        lever = self.inertia_levers.get(step.inertia_lever_key)
        if not lever:
            return {"daily_cost_usd": 0.0, "accrued_cost_usd": 0.0, "days_overdue": 0}
        days_overdue = max(0, current_day - step.day)
        daily = float(lever.get("daily_cost_usd", 0.0))
        return {
            "lever_key": lever["key"],
            "label": lever["label"],
            "annual_cost_usd": float(lever.get("annual_cost_usd", 0.0)),
            "daily_cost_usd": daily,
            "days_overdue": days_overdue,
            "accrued_cost_usd": round(daily * days_overdue, 2),
            "tracks_days_uninsured": bool(lever.get("tracks_days_uninsured", False)),
            "shortfall_usd": float(lever.get("shortfall_usd", 0.0)),
        }

    def compute_inertia_cost(self, current_day: int | None = None) -> dict[str, Any]:
        """Calculate real ongoing and overdue inertia cost at ``current_day``."""
        day = self.current_day if current_day is None else int(current_day)
        active_components: list[dict[str, Any]] = []
        total_daily = 0.0
        total_annual = 0.0
        total_accrued_since_day0 = 0.0
        total_overdue_accrued = 0.0
        max_days_uninsured = 0

        for lever_key, lever in self.inertia_levers.items():
            if self._is_lever_resolved(lever_key):
                continue
            linked = [s for s in self.steps if s.inertia_lever_key == lever_key]
            earliest_day = min((s.day for s in linked), default=0)
            overdue_days = max(0, day - earliest_day)
            elapsed_days = max(0, day)
            daily = float(lever.get("daily_cost_usd", 0.0))
            annual = float(lever.get("annual_cost_usd", 0.0))

            if lever.get("tracks_days_uninsured"):
                max_days_uninsured = max(max_days_uninsured, elapsed_days)

            accrued_since_day0 = round(daily * elapsed_days, 2)
            accrued_overdue = round(daily * overdue_days, 2)
            total_daily += daily
            total_annual += annual
            total_accrued_since_day0 += accrued_since_day0
            total_overdue_accrued += accrued_overdue

            item = dict(lever)
            item["days_elapsed"] = elapsed_days
            item["days_overdue"] = overdue_days
            item["accrued_since_day0_usd"] = accrued_since_day0
            item["accrued_overdue_usd"] = accrued_overdue
            active_components.append(item)

        return {
            "case_id": self.case_id,
            "current_day": day,
            "daily_cost_usd": round(total_daily, 2),
            "annual_cost_usd": round(total_annual, 2),
            "accrued_since_day0_usd": round(total_accrued_since_day0, 2),
            "accrued_overdue_usd": round(total_overdue_accrued, 2),
            "days_uninsured": max_days_uninsured,
            "active_levers": active_components,
        }

    def advance_day(self, current_day: int) -> dict[str, Any]:
        """Advance Run IRL clock relentlessly to ``current_day`` and carry over overdue steps."""
        if current_day < 0:
            raise ValueError("current_day debe ser >= 0")
        self.current_day = int(current_day)
        return self.get_timeline_view(self.current_day)

    def _node_days(self) -> list[int]:
        return sorted({s.day for s in self.steps})

    def _node_label(self, day: int) -> str:
        if day in (0, 3, 14, 30):
            return f"Dia {day}"
        d = self.start_date + timedelta(days=day)
        return f"Hito {_month_year_label(d)}"

    def get_timeline_view(self, current_day: int | None = None) -> dict[str, Any]:
        """Return bidirectional timeline view at ``current_day`` without losing state."""
        day = self.current_day if current_day is None else int(current_day)
        node_days = self._node_days()
        inertia = self.compute_inertia_cost(day)

        step_dicts = [
            s.to_dict(day, self.member_names, step_inertia=self._step_inertia_snapshot(s, day))
            for s in self.steps
        ]
        overdue_steps = [s for s in step_dicts if s["status"] == "overdue"]
        active_steps = [s for s in step_dicts if s["status"] == "active"]
        completed_steps = [s for s in step_dicts if s["status"] == "completed"]
        upcoming_steps = [s for s in step_dicts if s["status"] == "upcoming"]

        nodes: list[dict[str, Any]] = []
        for nd in node_days:
            nd_steps = [s for s in step_dicts if s["day"] == nd]
            nd_date = self.start_date + timedelta(days=nd)
            carried = overdue_steps if nd == day else []
            nodes.append(
                {
                    "node_id": nd_steps[0]["node_id"] if nd_steps else f"day_{nd}",
                    "day": nd,
                    "date": nd_date.isoformat(),
                    "label": self._node_label(nd),
                    "is_current": nd == day,
                    "is_past": nd < day,
                    "is_future": nd > day,
                    "steps": nd_steps,
                    "carried_overdue_steps": carried,
                }
            )

        prev_days = [d for d in node_days if d < day]
        next_days = [d for d in node_days if d > day]
        active_node_day = max((d for d in node_days if d <= day), default=0)

        return {
            "case_id": self.case_id,
            "is_couple": self.is_couple,
            "members": self.member_names,
            "start_date": self.start_date.isoformat(),
            "current_day": day,
            "current_date": (self.start_date + timedelta(days=day)).isoformat(),
            "active_node_day": active_node_day,
            "active_node_label": self._node_label(active_node_day),
            "nodes": nodes,
            "overdue_steps": overdue_steps,
            "active_steps": active_steps,
            "completed_steps": completed_steps,
            "upcoming_steps": upcoming_steps,
            "inertia_cost": inertia,
            "navigation": {
                "node_days": node_days,
                "can_go_prev": bool(prev_days),
                "can_go_next": bool(next_days),
                "prev_node_day": prev_days[-1] if prev_days else None,
                "next_node_day": next_days[0] if next_days else None,
            },
        }

    def get_focus_mode_view(self, current_day: int | None = None) -> dict[str, Any]:
        """Return *Modo Enfoque* exposing only the single immediate next IRL action."""
        day = self.current_day if current_day is None else int(current_day)
        self.active_view = "focus_mode"
        due_or_overdue = [
            s for s in self.steps if s.day <= day and not s.is_completed
        ]
        # Priority: overdue steps oldest first, then current-day steps.
        due_or_overdue.sort(key=lambda s: (0 if s.day < day else 1, s.day, s.step_id))

        if due_or_overdue:
            primary = due_or_overdue[0]
            focus_step = primary.to_dict(
                day,
                self.member_names,
                step_inertia=self._step_inertia_snapshot(primary, day),
            )
            all_due_completed = False
        else:
            upcoming = [s for s in self.steps if s.day > day and not s.is_completed]
            focus_step = (
                upcoming[0].to_dict(day, self.member_names)
                if upcoming
                else None
            )
            all_due_completed = True

        by_owner: dict[str, Any] = {}
        if self.is_couple:
            a_pending = [
                s.to_dict(day, self.member_names, self._step_inertia_snapshot(s, day))
                for s in due_or_overdue
                if "A" in s.missing_members
            ]
            b_pending = [
                s.to_dict(day, self.member_names, self._step_inertia_snapshot(s, day))
                for s in due_or_overdue
                if "B" in s.missing_members
            ]
            by_owner = {
                "owner_a": {
                    "label": self.member_names["A"],
                    "next_step": a_pending[0] if a_pending else None,
                    "pending_count": len(a_pending),
                },
                "owner_b": {
                    "label": self.member_names["B"],
                    "next_step": b_pending[0] if b_pending else None,
                    "pending_count": len(b_pending),
                },
            }

        return {
            "case_id": self.case_id,
            "mode": "focus_mode",
            "active_view": self.active_view,
            "current_day": day,
            "current_camp_label": self._node_label(max((d for d in self._node_days() if d <= day), default=0)),
            "focus_step": focus_step,
            "all_due_steps_completed": all_due_completed,
            "overdue_count": sum(1 for s in due_or_overdue if s.day < day),
            "pending_due_count": len(due_or_overdue),
            "by_owner": by_owner,
            "inertia_snapshot": self.compute_inertia_cost(day),
            "available_actions": {
                "view_mountain_overview": "get_mountain_overview",
                "repeat_expedition": "repeat_expedition",
                "export_ics": "export_ics",
            },
        }

    # Alias for callers expecting ``focus_step`` method name
    def focus_step(self, current_day: int | None = None) -> dict[str, Any]:
        """Alias of :meth:`get_focus_mode_view`."""
        return self.get_focus_mode_view(current_day=current_day)

    def get_mountain_overview(self) -> dict[str, Any]:
        """Return resolved mountain overview (good summit path + failed branches) WITHOUT resetting IRL."""
        self.active_view = "mountain_overview"
        score_obj = self.fh.get("score", {})
        published = score_obj.get("published_score")
        combined = score_obj.get("combined_moves", [])
        top_moves = score_obj.get("top_moves", [])
        best_after = max(
            [published or 0]
            + [m.get("score_after", 0) for m in top_moves]
            + [c.get("score_after", 0) for c in combined]
        )

        yearly = self.fh.get("projections", {}).get("yearly", [])
        key_years = [2026, 2027, 2030, 2044, 2047, 2048, 2053, 2070, 2075]
        trajectory = [
            {
                "year": r.get("year"),
                "age_client": r.get("age_client"),
                "investable_assets": r.get("investable_assets"),
                "net_worth": r.get("net_worth"),
                "total_debts": r.get("total_debts"),
            }
            for r in yearly
            if r.get("year") in key_years or r.get("investable_assets", 0) < 0
        ]

        failed_branches: list[dict[str, Any]] = []
        neg_row = next((r for r in yearly if r.get("investable_assets", 0) < 0), None)
        if neg_row is not None:
            failed_branches.append(
                {
                    "branch_type": "crevasse_liquidity_depletion",
                    "year": neg_row["year"],
                    "age_client": neg_row.get("age_client"),
                    "investable_assets": neg_row["investable_assets"],
                    "net_worth": neg_row.get("net_worth"),
                    "summary": (
                        f"Grieta {neg_row['year']} (edad {neg_row.get('age_client')}): "
                        f"activos liquidos {_fmt_usd(neg_row['investable_assets'])} "
                        f"(net worth {_fmt_usd(neg_row.get('net_worth', 0))})."
                    ),
                }
            )
        for lever_key in ("high_apr_card", "life_protection_gap", "unconfirmed_property_policy", "tax_drag"):
            if lever_key in self.inertia_levers:
                lv = self.inertia_levers[lever_key]
                failed_branches.append(
                    {
                        "branch_type": "inertia_wall",
                        "lever_key": lever_key,
                        "summary": lv["label"],
                        "source": lv["source"],
                    }
                )

        return {
            "case_id": self.case_id,
            "mode": "mountain_overview",
            "active_view": self.active_view,
            "irl_progress_preserved": True,
            "expedition_reset": False,
            "simulation_run_count": self.simulation_run_count,
            "simulation_completed": self.simulation_completed,
            "irl_completed_steps": sum(1 for s in self.steps if s.is_completed),
            "irl_current_day": self.current_day,
            "good_path": {
                "score_before": published,
                "score_after_optimal": best_after,
                "chosen_moves": self.simulation_choices,
                "combined_moves": combined,
            },
            "failed_branches": failed_branches,
            "yearly_checkpoints": trajectory[:15],
        }

    def repeat_expedition(self, *, reset_irl: bool = False) -> dict[str, Any]:
        """Explicitly restart the simulated mountain expedition without accidentally wiping IRL progress."""
        self.simulation_run_count += 1
        self.simulation_completed = False
        self.simulation_choices = []
        self.active_view = "expedition_replay"
        if reset_irl:
            self.current_day = 0
            for step in self.steps:
                step.completed_by.clear()
        return {
            "case_id": self.case_id,
            "mode": "expedition_replay",
            "active_view": self.active_view,
            "expedition_reset": True,
            "irl_reset": reset_irl,
            "simulation_run_count": self.simulation_run_count,
            "simulation_completed": self.simulation_completed,
            "irl_completed_steps": sum(1 for s in self.steps if s.is_completed),
            "irl_current_day": self.current_day,
        }

    def reset_expedition(self, *, reset_irl: bool = False) -> dict[str, Any]:
        """Alias of :meth:`repeat_expedition`."""
        return self.repeat_expedition(reset_irl=reset_irl)

    def export_ics(self, start_date: date | None = None) -> str:
        """Export Run IRL check-ins and real case milestones as an RFC 5545 ``.ics`` calendar."""
        base_date = start_date or self.start_date
        now_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        def _ics_escape(text: str) -> str:
            return (
                text.replace("\\", "\\\\")
                .replace(";", "\\;")
                .replace(",", "\\,")
                .replace("\n", "\\n")
            )

        lines: list[str] = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Sherpas//Run IRL Radio del Sherpa//ES",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
        ]

        for step in self.steps:
            event_date = base_date + timedelta(days=step.day)
            end_date = event_date + timedelta(days=1)
            uid = f"{self.case_id}-{step.step_id}-{event_date.strftime('%Y%m%d')}@sherpas.irl"
            summary = f"[Sherpas IRL · {step.owner_label}] {step.title}"
            desc = f"{step.action_plain}\nDatos: {step.action_math}\nEstado: {step.completion_ratio}"
            lines.extend(
                [
                    "BEGIN:VEVENT",
                    f"UID:{uid}",
                    f"DTSTAMP:{now_stamp}",
                    f"DTSTART;VALUE=DATE:{event_date.strftime('%Y%m%d')}",
                    f"DTEND;VALUE=DATE:{end_date.strftime('%Y%m%d')}",
                    f"SUMMARY:{_ics_escape(summary)}",
                    f"DESCRIPTION:{_ics_escape(desc)}",
                    f"CATEGORIES:{'MILESTONE' if step.phase == 'milestone' else 'RUN_IRL'}",
                    "END:VEVENT",
                ]
            )

        lines.append("END:VCALENDAR")
        return "\r\n".join(lines) + "\r\n"


def create_irl_run(
    case_id: str,
    *,
    cases_dir: str | Path | None = None,
    start_date: date | None = None,
) -> IRLEngine:
    """Factory creating an :class:`IRLEngine` instance for a real case."""
    return IRLEngine(case_id, cases_dir=cases_dir, start_date=start_date)
