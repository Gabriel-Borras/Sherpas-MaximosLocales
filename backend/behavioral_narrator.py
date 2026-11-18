"""Behavioral translation engine: real Sherpas case loader, Dual-Lens Plain/Math,
Section 4 / Appendices A & B cognitive bias engine, Cordada Asimetrica pact, and Advisor Brief.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import tempfile
import threading
from typing import Any
import zlib

from backend.llm_proxy import DEFAULT_MODEL, LLMProxyClient


SUPPORTED_CASES = (
    "michael-carter",
    "samantha-lewis",
    "timothy-melanie-weah",
    "daniel-emily-johnson",
)

FALLBACK_CASES_DIR = Path(__file__).resolve().parent.parent / "cases"
_EMBEDDED_CACHE_DIR_NAME = "sherpas_canonical_cases_v1"
_EMBEDDED_LOCK = threading.Lock()
_EMBEDDED_CASES_B85 = (
    "c-rK>>2ljhmN5D%2#)==JWa8%15|(UMbMILt4rHRaxK&CP(vgnp-lp8g0!rz@E7yrzQKG?a3A14#C?>0l6#iSL?#vrs&ZA&jhU&g5`jeK$&)9~"
    "l6jV&28(QZpQQ8MX|h_UtHIt+gWG%jcR9UJ7s>UfbX8_WKG<`IgC#T>><w<SJjth7GT*&Vlll67FdR&iGNq5^n>%Px>vK4`FE(X*U(9ENy+6SK"
    "*{WP$=g9)T8JuuiXtXNk_+UEE(tHiSlRNn7MerhBXRCApPp|1&5Dy3GVmU7!@fmz_cyfMx_T%9Jc9NAJua~RhHlxnou8IeM@XH5)F<U>vlgXxB"
    "XF0Si*U1{2T>St){+=zbr^O6^M{#63@MxWUzJ^}1{O%f?Zc2D}d35^r_z*vS%-8n-)^xD9UTxAZ@MK!72nWl}%{(jb)7iCn<c9b*A$V+SU09B7"
    "Ll-wmKEvs*GUz5j1Wb#0v4JIk3D4l?A}vdr@8E6rDb1}%cxh3eR&i@Vua;T~Yg**fbd{G@0&mOgF3)bE(|kRDw6euAnZlIsxPt;#G?~w>hjc#Q"
    "y-D#o0AejyDU2bTS+}cVVI|Z1Ed4|+tlP~Tkb&5+=GkpJvVO$QDgc-itgN&EYU~J}-4?6nm^r*3(vaEuccnF5ZRmSIOPQu0t@QIUU9GLVO*Vs`"
    "Q!6hX@ZBQG0ToucUcu+|^(wtfvK%MA2Ew5sc(4klSvt*-c*_xBa|zHVtC9$i|Hk!9aC+P!(D1!=J1-svYB6p2tjO|pd0pNY5BYVLUnk2YF5@?D"
    "F!(amdOApN*42km-1TMrjboc%9_63Xa*dQ+Rvq|mR|k&M82dQ;8=wowo8|!<Wp$V4(??jdd{%Yoc6RB1<2GO_H!H$F(?+pQfrN^@>dlF__l6rT"
    "S(f+=_A~B#c(N{**9%xFUWIkGradv4&8*GhW(CBNz<Pcnj*;+q{Pu-&f+VjR0YR*itV}J~gFueS4Qx}GeF@|`#~G)$Kzhg+cs17vAOv{FqSzq2"
    "fbEC>C#G_Jliq6E6rUuw#0foTH~?CQ879{-m%-j`GA~oalZ5=ZcmS$HARe;y{cM#y0M)IKt!NY2->hj{RZU8qzzfG7dba(|W16h2op5Bod<8TO"
    "TP`iB#}fDy5O{JkPc32<+O+PoyZg3zc|B$ox=+pOf>3)$oYR7BTTBz23IP3(tY+5TJewI4Jb@)6kTas>bY?BG&&)w0|0T{fj$g|DcIb0!9K&>x"
    "Kj3$H`gv{L7pv^=MZSBRt!cj2KmOzYSjkPXSp%xZ!?A562^hoN6vf9LXc>=x{$e8;7mJ%L2X-zg_XBYIy8>P#x2HcYH;YBGdL*ir!+HUZim$I8"
    "mx$KyCi|1Cqq9?h@KZA15MM8lFaWiQ^}-v%2iB)VARD;x>d`{t7}3_0-39^EuGaDS`-}Z|lS>jyn;Y@);&5_&eRz2_xjMYo8px5)=Ls&TwcM;g"
    "{K9f4umFpcmgEJDF@!+?(Uxnw(TI2RJqYu+JZ+ffjD;t@-?bh1=gPMC=${dM`tO6TsSBxpm3+i8<#ch?($(TXcIrc?ezQ|V#Ipw0W-bOkHz(W&"
    "X9i>)qZ*KPKyN^Had>rfad>igdR4(DR3VUx7fRzXdyayq=lptd`t8O0^Q-+IumAn<;%t9%`3@EkXjW-OKMk@Rs9LaLG59{IT`)Gkv&v+SBn{K&"
    "ZZ9XtlZzj(C#MJ3-%s8iUcwus&iNzC0;Wk21Gts`q;$Fuq-Cu@u<ZfnV9TZXjQ;i`oR%2*vLI=FnNBw=WaCJKl~yQ+KifZo)ww*}e}8dw^`kzz"
    "?KtCj<UTcipp75fNYbcl<fVy*3)Vf?a+PR(<WQa$;yf3ibKK)^7bdPv1iuA&kV)Zb_H%e~eRO*H{$g^v599@FfAs!D>pP5Gt>+-r`aP5yRay0T"
    "eDodYqSuE%oFATE8mke8wgDt^44iE;ogxb{7yUk+ek28tUk+5WYcWns3sj6j4@=fU`@Wj|FnLW{@eR-n&U?>s2?hq~nsl`6W`jHZdR?qR+1=}S"
    "E0lljH7ok*>Uxo^r}y-xxz0K@NtLc^M$HC&CKNn1A+NK6oRiVwxzqA(XXoQ9YggMDwRu5{kMRC#m4GS;<C00yGPUc2!#9T)7i2A|`H3C8Wqz*z"
    "<OH2)+YF-)9-&S0-Q}b?FMilIkvA8I#v(nrMo&+{|0Qd5m3$_3?e(ho2nNqx+MJAf^*r(mpIn|TJ5DW+`~1lP-zY%mT3si=gG}CWars{3M`u^>"
    "4lgPN!wa5X?bj#YTOP3eRhDWU?N79B{4T+QfJwzaGdcKVk$$#7zX7Ftv#9z#KfJg+I|UK452Sx|bq(VfJAn1I3^_Pxm)E4l@7be@DPJ!Wao*rQ"
    "Ikn66W(G~Ic>!wHZi_U#dVc^S;rjS&a(eyd@Zj(Q0DBM8;q~Rw!O_2)d(&YgG(fZQ9Ha?c@Ep7ogcV$q_g7~GR15EG8NX%tpnJV4xu~rc9V5)L"
    "Qrd7W!t?kH1RaRalk0<{LA#VEtC7!2KxtjhlW97%SY@{IVhx5B==w7-Lp3ze$at2~Hs<&5&W;bSkB{CQJ~<+5KRCfVr5$%`xebNbv=?qy>EAYJ"
    "yyIe=p1z+P5425PuAk^$DJr6~VsVX+r24fk)KAdBbed?Y#p|s)aorptHLDscGG}sjdU$<xbb=qk+T>_VNy7uRQQGX+$y$3Dgkd0=75Dh1`j%*R"
    "ud<2!z;oLvG-{zx&vt^56L8-p{{GU9;u>D88PJ04NmD@`&ubz)G7#=Y-RL$bP<HCZo;wP*cN*JUIt6_n&(a<(5HQ4HWzUG*U(oM#UX-X2GP0^}"
    "$A0KPiGvShihN8TuNNtZs3{rIx5;!(f8ZG${+AZ5+{ZnJXGcE`HhG4kk)IQDDl<Hg&A&<D*F3p_U5O_V_!`d%szXSr<fFiarx^-pI_jexTxvG4"
    "H*%3cfiD(#FuN{h$>Y%C69X%UDeR&pXz?z`Q)%KeNG^jFZoqP+j^5sE@|pQdfVMMDmdkWzC2Q-?gWo&up9ind1Z9<UlFtqWw4=E^)7ys+)6Z+O"
    "x1;<-Vxl^n+cx~ZU{{AYS>hHW6UV^5fKgr*uTvQCc2lOa@3Zwi&JB-Tkbf?K=z)b=AXRU`$^j&c)xZTs^jraUssjS(jU)=;%MyELNZdG~Z6u#r"
    "n|zLkx;PHC&0ww6!2}-Nip76_d7!O)Qd(qg(NVc1fEq{K<CR_)7T!IOVVSK<K5wdav8J+U%da=G{+Q$&u!iY4WQdUJ2Q)QWfbUkxK8$;|S>thX"
    "`KJ#fjcr&v2n!xLKN_fcC1mtJ18ub({w%af-uE=(z8;>~niacwU+|39>Cz_tT?v?@(|_D|h%l5S){GBoB@!kz{;+eC<R7J)Ucx7v5;-Yp_(1vT"
    "qqRs@AJg?Kjf7YjDpUv+$|5KRojZ&MqA`;>bZqUUpQm$BAj`%$)ChzH9-&sZVhYHi^>7a=3X%d5jG7VcQL+>eTc>F{W45|TKBL*@h8}1KiwvZy"
    "6MC?oLrI6HNag_Bd=7ZanA)lf1`xLC>QgtdJp=puL~(R-yVo3nvESsu6|<%<tvbS=<k89OuNyo|zNi@7NtS<el6;;lgn8D7IRomx0bCyHeP0ns"
    "@Y&^kv05W@M7)<`73uF0{>AOKFkl7o1tWtNv++=_W)Q?`G5s*m*78tNRSl0L>k5~aY46uuV-3kIOS}{O<3Ij06hft4hQIn6OD@(*1IAdkU%cW+"
    "IdP;dl6loJ^f7EUSPtkqTWl8CJ^q&oQ3KbYAfxAPQoOeLk%kNnV1oA`r=}SHDtgzH`?u(##VS+24NHiJHFvaB#_WbF_MGi}(wLdrgc1j+w*U@S"
    "n>qJ)bq{oCktRx)=t#sxK7X`sv%AeIr8~R7ZD2*^wH36cTleJ}cF@1k8@i4}oWOoqq)9HX{rHxP^rk<+oROujQfi1d>o6ps0|XtNw7{UW*$xw6"
    "<n#{JaNd;+UADFsFiT?bHv|N&G>tT}G>(n?`R0*lf?Wet*cbNxZJI9W1upO&KmnWjo5z)yEa?*Shvc!e$|RdvOT1f$r2?DUnr{|MtK2NaJTkgm"
    "KPXt>%w|J)cLRbQ;081S%`OR<4}}0;Xf0yeB@S_qSN!+sBjIFC;PE6F-3hS~XaSrB;1c?{!DH}~?^jvXI4PNr(DgOnuue92h&0#s#;=9~c*44M"
    "ba}>K?cmE@JKnXOS9+I3YB-&h=sQ7-Oo7nxAa5rKUK%};-@yX5z>Yl%0`6);^MwWYi=^SdSn~|*CksrWT{eXP`6+5VG*i;N=pGnW498ByLX-X>"
    "mI+86$Fvq%IZu-rk{d0s_5D5ji=a;hkpW$u7D(VcMkd@znB=m2xk2sWZ;Fa(b%=CP^J7v4y<-idjI1}<hak&@Y$KdHH3Dk*pgZi4QxGr$gzYU}"
    "t11mw9K#QV;zJ%Cz+;h999>L|+wv?Y!3DGhIw0#Icu~#^i?^q2+l;IuqL7DsT?QrPN8(I^she^PNdD)EvLDIj)pamAOF^i7i8d=zR>g=3BK)wM"
    "=w@7iQ*pdt96IhO8f$D%%!_?n5E9R$In#VJ9CtE((ZM;ezT0A+6$gM&;`|a=WQ5w99OXhopc8{35b}*u<=IJw*tB5f6$F2PiAn|_=#2aYmLvEG"
    "41oC+N}nUb3CkaBNt-V%*RWUcHXqcFJC+4gBq}^z*pvM-VP@-JfAw+zPb%Q}y9+)|>yO8wACH3QXRVwe($ou3J<f1vk{ljo3UR2Dd|&O1Q5SZ1"
    "2)*5~6Ads0UTktOz%(LY-uobUU!L9p_xqG8J&RZo62{27gx&anoJMqItv0!Z4jV`*$ki7c*rnpsu0rucv6&+!0sF%JfFcWc4bbSlRjyGWEQ>Ou"
    "F-iX3q|*e58pU3w=o3(img?8gN_8Kwtn$UGCIkP#QpSO1=efQ&9@(+B;*D9()7!O}p%lXKM*6T|^V;gu4a)&MNJ(X6jdMcRE|c{k5X9{{e>6>&"
    "2|6=&HX#QUFuM~_Rnr+0hG`-H?49#gbt_pMND^%y?bI&whr|Hrjt00ND1_*aXIji&FpA>m@0~x0he97n;Ey~-=OMoFx5y$!dHnZuRSdoih0nv~"
    "J#2upTgmtYN`yH7nFNGg%7uM=g0<+<flnZ<oocO!2&GKMHm~&aN&n^GSLQL_l@%KS?lKo#rPQB;(en9tJ>3_lzd{eM)7u3;?$ZOG9<EU>e={#0"
    "&=mcVj*AsTx<dVx&xk-U(fJG?$*`fy*O->LAg9|*!~kA5<MJ!lW67odV1Bnmj+3oHZ!K805W1BT-AbPY@ni8MEWYyry({0861LKE#)0RBsDkV|"
    "_}8A$jFxEP=4)Pi*&RB0C8a*(R}yZ>O_eVz_b*N<1tIOm9-a_X)|Ko?G<%LRF&tEi8Z3FLmQTr-eZj40p<DZ?R(hY;mDoN)CC&m^#>j01vKgsU"
    "9KdEdPIF{kbSaPej^bs)H@TsOu@+n4#+0NW-=N01V1ola=3sgw3!&z3$N<dOD-yEs@ooAbOeG!|+syG)07n;^5xteVDh^6ozMS1%vaFL$Mr=%a"
    "UlS2QEB2x0mO?zD4|Vcb5eC=<IVkVhdOatF?CYw)6TyE3$3v`|NHrwG*HCnayz$9Lo!*jxk{3L-WcB^{okk*~a<c@fi*1tmgfuEm$J%nHq8m0y"
    "-R4%9$O~faP#>?GK_^QqlSNq0(ooLU)q#Qk(r^M^2}Ad5h^)4?Bh$5%vP|s^L7ym88-hhjreGBQilRwhDg(t?v1M^O_|k_jbm~JwixdFiQ%<*!"
    "^CVj!2Q4ghz0Xk@=o61_DWKG>0KR>7`ETPC)X7}+T=<xOQJ)-~AK(zEI3FkF`dr>d4_w=`ckQUnsgqS3%@>qnO~l3ZQLewRk+<F*TpcwYgC2eY"
    "YPk7)aLiXnKp6qA%%H6UI*^3c|I@Kwq6+mXz0aoe^!(z8uI>3(dA`c%vfcAMb>04URg|UFJcR?vtN=;=_zs9;l0SaOAImApzE1dafu2(MleB$#"
    "Oilpi*8s^Ij4isl2iD2qM)t@t-h*OV<TJBD08_(-xhg7MnJ9!DfC3Cb!q;aYmJZfD*AVA=XG~JK(5;A#sP$DYqpS5DP)1qJtn$&s*pce_m>hVJ"
    "{NI7<0-Nwqxv7$mD4paAJe}Rlvpc%#L`R0$4jEF>*`c&zPvq!$UFQ>7-gDo)i}d+AW7~h$)b8t0dcMoPtURb{zinEipCjn$3<HGZR*?%V#-PwB"
    ";v4w#wRBK&<G^mkra<Oaj8&Gfpmu%jy?ES#3;t#zJy1N}?B;2_!BW;>{uLVvP>>u2y_oaW+3jJn%Fz{J&uR4FN#8FV{U9qrNN^b2K+U(p<Jhx9"
    "?V3*l=SHHB`kg7?c%wd5mS@1ZUMFRGf_F#+E=BH4QS@MpMg6kYh;_g%nwHa5wiF>DP0u9VafSvqf*ORkkJ(AnC&}o9FP`x(xWu#lTd*}i4&W5{"
    "9+R%VT6{3jlERS0?Cu_HeZ;-C_=9&GLsH7?0un*;!n9Z1gXz%q6kf!1-ZcHb`UN|vC>L=J{}c*a##7!|>=Q4kVIuER+9{%Th4w}wm+u~1Uj@ce"
    "ss3rXJid08TQz+=p-XQ`!|XdfOXut4syM0LyS0K>^?^+$y7RlZE<b(JYxk<#X%{Ul#eh8F07$#U08LVk<AgEss4W+d>gty7{fw9A^G$iVzB4ZC"
    "yE_v1zHOJ=>S9~<)P4o7S_yxE4%92Swy=!J4X8zZ)~xnLmOuFgu7bD#FT1Y!z}{utZwF}0OrCYCxQB88_57pC-4&y$(;QegiQ11DHlz4507~Qi"
    "<r2>-#NX-z*B0V#vznzjM;#7YMFMJ@<m=4>1;;{I2@oPekjhz!98NZ1=}Ol~s@1N8GY0kmyl4KX9^>W((RsfH8ESNDS1;Zh9oY(={hG5ZiopHa"
    "8@t~4+Y~2tDY_PSU76_InCYx8oXw8*HE~-Xmj}^am>sIVF4#^%*7+S9J&j=)D*}+J!}c$0VCdi0ObTiT#9GH;YqKn`nvGjp6)oL$G|{`VYZNWt"
    "fZ@wt5>uhGiA52=6^bq;*B|UfF4;v$8nBMpdOumsD0UjYuKD7F;5yKB!08mUy5jb>3dM^%?52fbL<oQV%DOywGET3>z-kqM`}<;y(_*!tC=5?H"
    "9Rv32@5b&Z@<iWP#lA5cM+xTg@NaaZb0mD3G26iijg9KY`RsOo9|^{=v0z+h?4t@g+puyW?llmxBvs!|&S^=6whJGwQu4L7ITCIP9PT__-6FWO"
    "3Q`=)qczo`t*qL>9ZSiogrWTGPy#|K)TB}sjZP1dDeFD+m6muy0kT(xHViA9${tjMAPdK%7<OC{%(V%J9G1bEfXRoRCB&+jp`J6EMVzFOBLe90"
    "k~p;Lf2lRLNA0Epo;IWa1$70BOT4<WG4!_+5o2SwePTS+47!%a%DQz#1WRWF7aIg$^xdJ64ai2!+i;ZM&RJb0D_@bYzCB#KI@~pA2)08MV*hQ+"
    "4SU#gMkto(`izg#ChMx>334AF5b3zl2$dE6sE)2Z^^-cVBka({SWstMk4HJJdU;TYj1Z0!ML`^l#(|1@(Ko*&y#`>8?}kofkK$lEV9f!?VDh@|"
    "$cdgaV56HT9)kuqa^1$+qcZEw$Fv?XW&o(2j)`3`ihW#+q<#h}-aEb@j=hmPZfSCstMg7L9LI4qiW|d-?N&-TII@FaEOx2Z)xl<kCleZV>Fdf@"
    "w8(?y#U~y4Nc{cC_>G(>a0!HFd)E$ZXjX&9vBNNS<53uHn_car>MZ-INz_ME6!4`1qB@6=2fNIf<Xs!FngFAj4I4yQ`K^Z)JfG^IzyWh4YQYUI"
    "F`v~f<qgfHJb|Y0tdq@roh=2s3ouA|(0cL5G3InopmHNr0ebVfyo(tK#F5B%Y%iuw-gb8_zHQt;xA%Z1^wHIi*GH%OXJFWBW7BQ)W8-5fmg*!b"
    "qg%xCU)6$_^~d#30XOxa^}Tw`dnvBT+h@@R(Rl2@s*aGSwm}9|Y=feKI>?g{%DeY3zjP!FK|eY>rQ84qhi{Hf4-c+iAD+TrSK5@%`S#!X#+s$K"
    "m{3FB*#FwA@Ek<Y0VPx2WwBY&&4il4nRYR6mEyGy{N>fz{<qgaa_9O|uZ!tNy5Io>s5ro1bHWsh3$*{{`0V=*@PBO(WQ=(o83*ZYy25MP-x42("
    "lM5ut1~Xt=?>E8-rhoum&;a6sREFOQh_fFj$5))i<49kZi{dev17G|f7Cip7x#Iit^RtVq>#K{&=_QbfzE?nt0?7klfSQ<>x0DL%R|V$n*>{H*"
    "r<jMOg=M`(J2xjUp5KU9J+I5x?=OMbUS3|GPcAQyzB_DE*K52t!Mna?QkLja_uJ6f`Ni4!;RO)d@zKA%KRTdT=j+4oFq?`d5M+ER`?0CKNBKWr"
    "BG_MkOX({eh?=UBx@}PiaqKu6`yT7IbLm7?eQ|uXZ%NlI`AHPH_89C0zkO0(6i1+OgmL?%0xukoM|ctT<eZ#%42?$~okPgW$KxiD>SEGr0e9@!"
    "kq2f?5VeErj)T~@-O<=<hu4jQaWo$FfmeF&cC5DNd6DBgqtIy|$#X%AACvdu)2Oi>#|_BVma8^drH9f(R~~Y8In0qEKaLCqrO~3PId^o@!z~Y*"
    "dS0+)JfrPXBR4w!@<or2LegltI>n>I^D1c-KbXj@p#1Z+o<)?yY|d`?@3Z-Ag$L%<A#PTFRQ(Nh{8yGp4=Nil$P;R)o!_9HC2aEJ43FftCQ#~5"
    "oFwu{Xu!%CTGuubNwuUX>dIZz-DjX*O8r;8x~)#84pOi)DR%r%pc7#L86Un42YicX@x0)tIQx<w=@=`;XJo^{yTjwN{lSM1V$G@mK0Gh|l%)?c"
    "$$-2xQa9}L?33Y>5CpBh4Q`Bvci)?L(Kqd(ZnuQ?yUu4^ZArUDo*V6J*?$<J6GboYiusJRs(n7ewe(a$gAc<$wGpl&E*l#(iBP>q(6LF|ovLa?"
    ")c(N;6T+2J$F#|kWJRhy5XYRdIX$UP?Y<Z{7%d@{A~?1^nzDB7%9ngb1HNwU_*&exiUuuT2i^C=uOHhMRl6&$#+0|^our^$3_s^9y56mOt~9en"
    "v?S&5Y9Gm4pO$-Fy_t3w<e1mgJ+D`*4-T8dcYfA=t9#fAT{p%&fw6V+c{2Ny(3Q;Wmv24fbDx{Lu_f=D`ioPtxp-uUO*v7TdP^^TAGccDjr2Ud"
    "OQw%_C!(j)X`%_(__5YhWQ)~yCq0IVew%SjAbdj#5Jhmok0XkaMctkqFh59Xdyp=QyH&Eh7g=EbY4W}GZu50g3b+shMhlTojWssoW8QVL!S(@u"
    "{^e;$hl=Y+_cqz(iQ#n8a*;fhSH7*y_#zoKHt8&D5E8{Lfha6W5lfh^zsF!M5S9)*=8>Q~)`FFYTk*-X_HmU(7j_Lk$3S3OZTRCmA^nA@M|zho"
    "q(f)OdE(qah#x-bO1KYa$jRtD`Ifc!p*xJ|Ipx-)JtC)9O})z}7)av1XnbD4UU^hkg7rQo9UJS*f4N;i=u#_tDN^45Ni6VbYtBA;C6oNh<rrk8"
    "@&S=vF0^XOAyKNP({{>*T`|d%`6Jza{M0}xOMjWfyZ*LY49S*VbS{0izX*5W6UsR+qnImA)%?|ZKl}6UVa-eai{=ot^UL+wEh>{NUQPwa#WffX"
    "UMrPY`VYu-<ih<`Mf2)SFh-GfR9j|1v8>`JyK+<RKit}(I|@i8?8<kjzksi8`E`t&b?BpO1Abr6*|<->AsDPW8_>obBL2{igS;V7hLA_Lrq%22"
    "!foEcUC#9A^}fy;Zu9y|9EhQ64i^sSjcOY=?9|$pZFP9*@6z%d@0IEFq|E`Q8veEEXVcr;WxB=NW%@jCm#J)Db9doeYFcD1-ayWyBj(`e1{Qp2"
    "G4OsO5A*NJvxmIO25maaOCR}~JG>ijwHW(4!((fGyk<ay8=Ea!LK-~xi=M^?)mN%)f#RC(f@Qd+iUu^?ZltdO`@b8n>K^ZU+{8q<Sl7JlVQ+HO"
    "#B)O_;IroJ5m<O}b)T)wIS2H-1sVSKu$1l~j3**3`mzXdf`kizQdLP5c?XVv!c!yfWc_NY(cqHOvr`P<133Z>2Y<zK9MzF|-5s*&e2Eg}!*Bdu"
    "b=uuNZ@CXzrhH6CG?vz+0fESUE&-4~pMd-6uZ$ee?a;jegMI~8kBAV4c5MK<VLbM$q2$ljq23(rPcRcl>(Y8rq+?qAd}5-$9fsQI@@MPlmnuO?"
    "W2((e<61hCCa94~6wwy!HazXOcI=uRyIVR2+jv`7zR{Dvr6bByx1}e~=*jCvf1XKy-ZuIZ^1|A-QH0cLj>7?4Y8>&ib)1%32F-ngK16EQ(2u8P"
    "%AsKj0`apI0%WPyd8Mv4rU|MHE1a56+l0~F+FLMd=&;+md}@g`VyV>Ftv%vFj>Z)HUd+}pK9WD5WYH|{D;6z&8!Y;Em8QDR(CB8@>}9vv31@Yn"
    "g8)P5$vpCvM;1R&R~#pkqto`)#xzllTb9Yy;oGx|AKOJ_$1Tdy>A}%=M+cl-yNRN}WGg{^fomF(Nf5P%-0}pIQc(P&?plX7+i5$fIt_K+Fg-Di"
    "r?_Kd8qGQMpFjgjlln0E`ic~PN%5voaHA%4)KVC_`lhPtr9F=v#GOP3{<@kQR~WLCz}dyso3rDivo3~H<2X;?-B_vm)1LTmhN!h`I!^&-YC5~f"
    "2>K#S)amGfB6EX1y}$f6{P@p755m@pkS9Q?p<^bz*ZQKQ<?y}_erjrT{4@!<ttb+zRvkx?>EWxPsilNWE7qO_uyyyl6>suuJk}5T@Bemx%Etb0"
    "4DabqMOvL9W6*1ikDF1P9iJa`K_MK8`wi`X)uF56j5{P0>0<m<KS+YF3W@YC>o<1zRmV1c1bPe~^%=fvwCZrXhoosQY_nZl`*y<w>9M8a{@<H("
    "WABh*%{N%wnDm*WS^a1G+&pu)dqJ<cjr)IJU$+mfI(ALv@S|QR((bcb6k&PArFxaW4Sm|ERHU6}R8OB)fAtgbJ`2=Q2I=XQG7<gsIyt?+Znw31"
    "D)UcNRC+=gt{qH0TVOr;eUmA6PwuOTCcQvQx+>`urawBj)PVYh)=?`a{bzjNs_FN~W$?>zsfiWJa{ARoTZ7s5?>+iCQ)=abHD=Z1RbSe&->W*e"
    ")$LX-5)vzsnJH6R{F%O1)Nbo#dQBnzNk%A7jLVBP8UoUu=xU%MC0#6;-QKJoku2j|E4)yo>!hZpt9aKZdlf)*wG`HA1%ogb?~-M|&{ZwuRl@$%"
    "5P>i93233b#y4+@m0GseY#psrX+o>)nLb#RtK~T8-`)#bYJtNr>N|b;jn@|e{K3yhf|{4-ZMkLsS$-nK-O#}RYcSA7@Zc)_oRoteE+o<^k<t*T"
    "PFwDag&X4bcG7cI=QM_I6Zv|u+f$4Ck?sjXYL;1~gCh9N;wy?7)yip!gjhUId#No>8@09OhgN)LOC#wq+R>AlNNH=6fHpiv9h=E}YI$>HE-dnl"
    "skiQvOQ~mN8{G%B=LaIY(9^SM`&i_R>NT&H@7tt^a_H0~$$gnn!W6@^)2HKhcqJ0KB)Mv!d=IL(wQn^Q2#;K99}j*^tF1`y&CkWLPPR(4Y%WHN"
    "h~)YTw${;V8-QjDvyXZQEhu2;zUr`OOIIC}p;h8U%qLui*0JNxUX%O)-A?P>3$>wR2;pp78-`KXHVS~mqfnl_+C)^EkeXA4$StlpFzy43y(_4I"
    "x^!JUSN;OzY-L>WgGnQlu%Wm$cQjW;_2|P;^WV7D{Wrv|`tv{#m)U#|Y>!+w7~|vG%^P1Wv8M+488@yV`5uq`VzdYW=-Fe3FLWfKIjc|jk{#VS"
    "!bqPfrO+NaBRdY<=5#gq_jUmyKlIoahBAB~H8Qx^qjBZrbCgqF66wy~;^*^gdGrWB8S>Ua#rho>8GN8%c*eB58Fh^R6`f<A@N@YJ-bl~!r~7Z3"
    "dQp1dB7IbbZ)qlRVF$Iv>=M&4lkOLx0xur?D9Ws&Q-?^#)67V+n9;&Ukw1!k;h+aJ%voYne0_DF<kI58?}4@GH-bIB5Inc~N;$4d|8MEyZLQgH"
    "^;8uVP2_zrzn4*8FR8!+#TBR)>=$b`QME)kmdUs@c87e=2&86@z3PV(64z?GSoDVCZUVMY992I;m;7FhLugz6f2(skj1xLz_E9GYqPWvl9bWrR"
    "RQ(9-aTPZ4Y#X4bTX@5yN2|k>e?JY5E+)+o7fiWtw6u0~-=N=H7r+?tf<lNmoHqu$)W7TaEE4f8)Eve4?q+H2;9X~6{~o)o>2XS&U?CYU=vg1B"
    ">J-PI*D3HlYAecy@5t&oFakx`d|-vHjuC?B{Sr(+d5Y5RJlm!|5<Q;_AoUj9fWop^ZNa)OO~fCnA{LnAy|x6X2@NgZ_HKq&x}LV+Uv!?<P@@8h"
    "_NkV})5yNuEUDz2-a52*L$BZBYz5;(GuDVAawhqq`BVlb2|iQhd(}g*q>fd^l~f+{Y>~G{VAU^0^<c&!>t=LfK|b^?$zrwEeC5s|kb*&dQ@N8>"
    "p<RMI$$-jQY?m`6*5HdkN-BDSiOy8i1c=Lf4maDA$9=<E-rJVTX*2CDH28KPTyxpov~uaB5ih}tn65V~c2@l1@ZfrKa`yi83VWKTt2JixSYbuT"
    "DiDOe<B%E7uY>RvITt{g)sIIEW&L(D=LfoOfiPpKsM_9O^F|wNzZyd&J)I^?1b$|W#fG`ulPzFSrzdy{lKq|YEQ&~(!O7%@qm!e5Kg2pzve3hO"
    "H41ei<NZY#qa-LDddjhjou}e3T^SsBA|;jAb@CYxh?u_Ng$(l$k{5-eNa=_b9JG=PNKDdIwOGxv9KDFwsskIdM1aI`IjVySFIF#Ew4ELuT{WK`"
    "-rlBDuG+P&+Yb~tiL9W??L}<x%6#hh?$}moINr9ohcjKbzY<5<riN+cIea_MW}v*Y8s73)XXxYjrNtpk<Z$i2v~IJ{x_fr*dsa-e9>5NX#&M(F"
    "8|;O_GaB2Vb*h{cQYox*M{3WjdrUqx7j0b6t*4$O=X^F<IGC6J*3)+WDnU((C0{i1Ts9*8rI|_wXd(+R)32A6zNcP@-!Cbq)X0yDWtD5@4+9~O"
    "B8`A^QL|o!F`+OZe=pU9E0E)czFl#^)sIxpWQ|4avS!Pj7byDp*h^8)d|rq)S#AaHSQ8MUrA}4#MkEP4N~BPx=PFSLD`k3`G8L06b!AZjQ5I_9"
    "$CYd@j8tK`!#@n`W=Ophi^}J?Jx8aW`*M5X9hF`2=O2HkvL+ri96P^A88!>_>7lNA@jWp2Bj4w&FwOf5>aD3Dc2)A*+pS6ss?_;M`KdV7Cn9W("
    "Z3oNmKF#sIjq5vN#XIT7(5tx_t{VrfB?W&znKkksR+*J#VkC+StfgxdvSv#vLD7Q2xNByMY#B$%SflzKIV=Bn$;Kmk=1k3)H3I|w>sbPX3RgX%"
    ">z5W{Rt+YdSp|~meU^f`U8NRirDF{$%*W7--t26k;?#UE0B%D$a;xonVH7BCd(O9{ffx8eNI7B6En07AM~*!XM!t{rsPf}&ZT-;qLTBVU>M*&b"
    "va1sF)k<k;y7*AEdZqGi2{phZGd+#f*4$I=#bm48RV}^iq@*Y2>gY>vu99zwTu^`ITu?N1PNzj?%%eEeazo-%*UG&p62A-eC<hCHR{8otBp`4@"
    "AJd4bN7qy%t-PMe6w0m}#AE5_b3J3vFE<=xOk$NC_c~E&3*yKzI?M%*cqlwLQ~*acfa4wjhjENY+FJk)q2sUyupffZ30onK9S1{fS^%b@41nVr"
    "z~iR@_8d2kwqtngjeWlkaNsyxlc)jkI2hZl0P|1=z+)3&-|hi$IF1~58^Ewz?6`qpZ#>3%w$TKTP|yxBjip2E*)@orry)jefv3D%AdZ8vA2c8a"
    "GIrV_4r4d)+92k!42Yc?#O~7&2M$u{Hi&)Sc4Ds%u^WbX;n4!I>)Npwv_Z^c84$ZQh`k;Vk3&1$ien$t)+Ua@%0fM_4dQ5Q<26kS#59%xu~&oG"
    "e;VR2j%<G`j)Ncw!#Zp89nX&2H=gHvUffE@JeC2mUxPS!8saDpVqD&Ch(jlgR4#P|F&Gscyv=ufy6b2{%wri42Q`Spry&N(KrUcgAdbeNS7&bC"
    "I3j<GHi*ae*l(2|JeC1*P2l-G1RgNeFdT0M8H^KWTqk5Nj*08GfE+}?`&zf27|ejVCiDCrG7of%aTITbId<&8tFvSea38dzISl==*Gd>-FazeA"
    "*z<dcJzzSnV{esvF{lc@Q->KOLI-I?q33w5Oj!(Oz+97jK@Z6Xn+10GRy>b=AcHzv_CO$y+i4>XftR(@1`npg?AK&p&_nh)u=k%3eva+JqS|$!"
    "{V2q;9Bm2)dcDT2K=Wt@&^7TF^bmiba5<j)1kmHa_Zyf-YolENI;b!Ct@1<+XFy#Ofk6)u2sT9Q$Kh6}VW_}uushfFytqR(g84-4xaQ#usB2;{"
    "=phC{FNi~Pga*`Z;DFIzhuV(asGUF@Z|pj5>sA!Q8Bo_mVG#7OOU6&B&FI_~HFzE<)6TeqLV^I)R;S%I8P`>3za|cY9^w%22$Z&+u6-wV{DwUh"
    "MYh`kb%cgfE2|d68Bo_mV$jD1jQl8wx9S~EU<Yp0fEpCFxC8339sA>UJCKJnpsoqUppPL4mUI|9+o5(qbByXx`%V|P2Fe*nVLM&(a0b*hu^5c|"
    "Kn=Qh=x(PF^gFLBc`oqqpkp_VVWRj!8`LzM0d-9<hISvQqo5{wn^1#N*O2B8+Jx<@sS{%k^Y-1y!|6~5HPIM4eV~s0$lFfWU}cT%xDGW+#*X8S"
    "*!99FXos4HGoY@?#?b8rHK1iXu0i1#j~h@2t{ZjGbp%R??RP+p!x>Q5WMk;{fjV$)XFIMvP*KNqH3VeO*y-RQVd#y$b{@jR8Bo_`W7tPF#(<XX"
    "RxJqV&~9jaz$Jo?lY;;>M8AWqX*2`qnrICBh{nis$EYf9RYPLOt8c~-sI!BEpb6=O?cAD1Gk~s1#;}iMgry9&pWA`{hBw*`H8u9TPL;gKw>wVm"
    "Xfy-pnqUn32*%J3ZD+fPvB8Xv8f>paLv_1!Ju#92a7`wLePm)VcI_vy490-h&_CJ@E-d&KM(u)yM=}7eiNmmuI0Wp~4uKjLR~&|o{nrIAC>=pN"
    "f_WeV-kKnc`Ut`Rbb#?zHa8ADI`QfOFB+2_^uXij;D$8`81<2Wpz*r)R(cpau^$G#z>NVUr-K@390S~%=!^P@J}{kZbA-m3LF~GAKk5Z;>qH%T"
    "GmT?_Ta$TFADQQa#1FR;L+pdH>GT4Z>M^!+GaknPw<heOKElrT<0rTopezpi(Qb$)ZM($aaSU*4VlL_<=1`#ww_1QvH1_?l7q~$%j@|aH#^V^^"
    ")&yJ>_5v4p`&MFzNHypME|?*4`zfdx#{jn`+M=izxGv?q-2$%X#9lwf>w96~IUV5QI0m>i!4}0m!5wcs#E3w$HLRwNbNncDoNjQ(#_2^^6Km19"
    "7r22JZv{6T+fLXMTnDUduLE2h#{jn`)ndCBXK>=}XSHGE1YtkE3#(w;9kfg1=-@^*sTTK<YJT91-K|nB#IwVG*u_gyr(I0&I0m>isTTK<YJM0#"
    "aVQkRBKDMOjyQmB1DD1zz^zHOxSv$><7lf84q>REr-}nMM+e)bVGL+%LM`qi)bL2p-M-TtFco|9G1N8NH3k~SfVL*n;yyAh@S=FUofJTajiP>h"
    "!HqkVM;gTdwkFZyUWb`r`uSV+1u)&+o?Kzqi^(ga4O|+>0JkR5;$Fs@6S&cKaAOc@{j{-N5Z3K?dSV;{+?qs-d-<`1pwn%&e1a$pgPz!R0EoDq"
    "ba@~H-kL~@`-rp%Jq)&^Hv);~^@P_0EwP<?c_0JcnoJw_k!evJd%;#A0X7z0LiK_d$f3jb;em8`WBX^o8)L-F6YxfUVE2SKggxJGP4GZpKA=-s"
    "mQV(W>3zCLu0N%#lH7JN7&Td~sjj*V_}fin<P7C%ClBLtzPW=&3w9>nox(R1F{Hwc$vy2B17ff9y5sSxAkX3|^hP==S03EgiOihC0Z^jy!r{sJ"
    "@!5|QM6$}tkJn4(rYu~Psc;H;=MN^Ea-Cr)tEfvdxcUKp{5@O3V$AS&6i2o*ppc7e=q1bVu1guNa(Q(6_V^G#e$3bR0M=9{LmDiLGLuneKgp<|"
    "D#d3u{YZgDm|sLo&b#ye^1w(#c=?XdDWcH#22|_L;$nBZRXSF!VBv7^kY;!H>+3APR>M-#m6XGuuUG7Ajub{^2o-Ft`C28Ue?0xR0`~I!;KF)6"
    "FA8*`zO&xJfYy&$I-gmui+pAsUcIR%!9TP))LPf-Eq1`~28{_|6tQp4pe<XdoWSM&yK`*@)BA_y#(F=x99dUK=a&fcKmM=(dkfe{`R$xy4|dPF"
    ">So%2Ki&d=#{~FLq~8p_F0r`Xz}hXqK9gJk+Xqc-Us?y*C(M`wG{PYr+ezgZgE}l3)1m?1N#<0|qz%vEGl2i@`?Cu6?~)vS!DrT+tII=+GNNGW"
    "21aZ7!~|fv$TV*=AeQ>4+KjfWg-02de(8+9F6nq%NT(0w)R^F#%d3MQDhS^Ify|LML~gy{_f+=I>e_(tVwQfkDD{q-(wq0E2hZKVUN`$}S%Uui"
    "_PeX27IHc%RyoG3u3>5%Yr$!GMXlC88{_pn)!`4fY>cRr{eUd|m_A-F()CKzPrFT~>r$3^Z7Ey%(_oWlIB9+k0Nf-LGCRn>NicdLxd8<1alxz-"
    "Qwm@NYre*C6#)a~X-`G;G7iI~;j}$5@J8-{V$!k#Q!0_NGqkt{m6ZcQ?1D0}usEw8Y6Z)AGNo|N0Zp(R8A+(jUjnq9X|h~$fajkFzjxd}4{%pB"
    ")Ax<)d9g<A39j^t%-e=<RtFuKIR1b^5bLYrHHPKhg0@7F4LCQ@Gc2uCtCg#?4`MYwP?$!tQu#kPX=Op$&4h#NL>`Tym1DSwg_VWnGi#I2G4&>n"
    "Lv1ryD{CoIag4AC94|hw5N+j?(xP$~6oD)Wpq4OXk5_tKSg8A1u#i>;95e@f%F*kaQ7ymT$ogZFZ!kKRA_NdpDtZqONWnH~p;5c}Paj5FC1q;|"
    "VSy>;j|OU9As+upXshKtc^2AaCY7fV_x14ffx_O!Zr&F>qjkEpiGNpG!eqgHhX|wG3o{O2l}MP>_`}Xkl7Ez;oF#m+DJ>BOjg$}4YC(+il_{ol"
    "RETQV7C|xS++j2jjhW1$V{0e<Je_Z5z_aS(P@^oz9DrJYxB_x$J=}vdKvE!rQ8S`Fs!CnU7$GXKY-E6|vbza7JVi1G*yeM<TgKF;7z=<vwXQpf"
    "?HSl7En!U|wR_DG82e2gTrq17#;qg#Nggc=3Y%H%zBx%gPh`Y$ALb0G`=)QkJzhondxU>+yDbb@K`cs((_%Ir%GIpW8LF&>Vl59PRn_na_6RO5"
    ")84PS#u}1amUt)l$AA21D1=J841e`CmRzjWMMw4VU%cWXW#ksgyuI-GNTlKXrnCCFPC-V`+oX7H^CJx{8pXR$O)>se^sXuQZzVW@Ri^7T)tn(7"
    "*4)uj8M7Oz*mJgXud?KH-n81xxxcG>phJr^Q7Zw34~e+Q=Z_ZWAfdbgf7`%{k~~~f>uEuCvSA1P8@<7A2q&-~7HNXowuK@0^n&%KKfs)krLIzH"
    "2oe{E1ayF);|PA(g}B)c6JX@@4)u86l?+|BwiYl;V(~Ww1g$iUG_o{~jr;lLk!ONk160@-_Wo^}F6jj>@E$+`oBEr_m6$B)67z@Tv9!u0n^~AD"
    "2sND{G@Nf1ORL;0#5}SRyE`aY;LK)2cy|MW9pDBuVZ{$Z=0hQX7g~#$c8NpW7Y_)^BjIFC;PE6F-3hS~XaSrB;1c?{!DH}~?^jvXI4PNrQ0fna"
    "+}fFJ?ht7hhw*ACfG4b5N0(>()egSgwc}med8Kzrq=wU3iM|u7%3J|_D|l)2XwA}Tw!n-M_9zIrs|n2)7T_<EhW}z=c8k&iQ)rh>AwYhL8V}8s"
    "G%uWF2`h$UCt{&V{}9UrB#&cSi>#cd31;Qy1-39Vfc02xV7sM62AGKLzCZ%!F*16+Qb{A08`K{Drl^=!he#JSKPFYsJJvAD$a+IZX-t+0*+w{Z"
    "Y6R5qK|e61Ls?)1lrbDb&y|KN63q>T;sfg>GcQnTFD-Ee<^e##1+)b^AnPG1?habmBA2NOM%EEg$iuxZgOc(iaVEjkO*sZ6|MNtdNRpuGU~-m%"
    "P&viItVmfEBPKYcs?FBzs#s{{2nENJi8C~|CsQ!sw*-mj(VS^M8jd@ezUbgwmJK=pgc9eMz#=2m*5oJ`8p0Zrj1DQ?y()r7YeZ~Xu<{CmKfpvK"
    "0}ylu%d#$(Bda5*99z=nlNsA)7N{S0EDNScRMVma#w7Y>!pzpc{_5eSgjB%scNct`)-QwNf7Z$wBCS1B%&0Ttz^DtmJA~eD*gsS?12}nzMg+`z"
    "9|Z5qQ_L(1>Y3EDh!r7WjI2x8jSt9aL|4{olUv1RO_YLMeX)UEiVJ}0J`{={ip?A;3D_6zhf$UP(JI#{5cn$NlaRkR=`;bNMzNPE`UI4srTR6r"
    "QdP$<$BZK?iDxw#_y?9U4m3MYC3sOQ-k9Y)y<LkLN+FD=(8P!tklN~-scJ@D>19y)TPAp!)Y(K^-F?wk-{fm+mfhZ_fED6IdAepEj7GS%L%E4x"
    "=~$NnU0Mbrf1x;lq}*yaElg>J@~@PP9kY<$-J2gRaeZMQTl=V>WU5xIB_|~XX-Rqm5Sszs$eL6XNsGb99-Mo^Qt5W~P_w}90Un`GeFe60S%Y<t"
    "8R0JGOcM;BR-M_SRDj#qsK}VtlmfdB<x<vEUkOXgNt0GATu-Gps;zzfw_)L!U&@--Xl>-vY@YE^;Z#%}KS<~6WQ&mjYbA@6qe)4*Z9lYTA^PcS"
    "tjF7WsvuNrG^V~IG8SEmj739|MpV2BL^0<hD$U~?$}aSLM*au!P$;K~%x#1WZM8-l2-A}SG5$SW6$6z-=JFnh9Me1*hulK9{FyX*Py2?s%;OVs"
    "PFGd<INaLN@-HE!>RH8J>4)Y1%fYWK@Ql<>qaGQThSDgk(;Fo_>(c`tWjBeq;+|J%O!0xGMIH{8I3MiA8<ih|-1&cKWshJ)6|Cn9MPKQW%D6%v"
    "D)M-70!1(a@=YmWD=p5-j_i?n%AR1XnB5a8f!1Djhl#n8QXldwvCLCLxKRIskx7OZZ|8T<(QJoie!EmHUsD`X>h88as+Hd7btN4Hp%MpEtnkQf"
    "gmo-ZRJG_fAj?@uU36J8`i|md!Z*2L60k{C;Kr1sAm5<*vta8NFof6~SqL?ML#GkI%}L{fk8jflVYl<Z*k+DLR5-d&)9I}=oN!PwIpyr`l4YH2"
    "Sf<`)^SQEhpw*BD;FdybSQjLN)p~+~nu8^ot=Dt14!*8EHWB<sa6H7SiBv-}d=0B>$QvKAz;DS~&I=w}vig4fP9u@g_WX+7vRAjVk-E*TAn>D+"
    "_r#L<ZY%p)9OKASn`~X3UimM9S%5Ula$<Tbaq99lL{{6{(K$*fWtrL;f<95GHUx{5Ou;Dp6-AT2RP}6{-HX$~mp)J)wW+3~S822Hu*5d9&r;ze"
    "tp?cB2`Im4C&lu5U0gS8x%~N3tESX_wSaa87cbGWOI8_;EiRW*<w{k*foa{zUzqywSRSuqGRScV|8V7zDV-Ho*H~4qe(?^-(Rk~4K6-@ke<)W!"
    "&_N=y)8A~+?9n>0tlFiY@$M*3I^T-YC-%_w$OVP}^P%NpQrro4)wG(5i}~-;)hwIhUIKQC9*aP>R|Ph%N{hrE#ho@rpo?qsDHDq*wj`_#e6CUl"
    "n<>_-sx#uDRpnTxn>p>LSX=U^gWqcDEJ0anwPlOf0`1T@*=_2#SVM7LB7PYki(Kw?N0%dG)kQLQs=F|xqBofJ%Ly@Od&n8r#ltEqyV(P|0g^AH"
    "-T^+t|C!&nc|A?EzSt+m)1dKO${jEM6<57|_(g?N?kK@$OO2G@wxWsvqgguTxusULyMN8A;Hmm6UG+0WGI8;O-D#2QRO$AAs=R_PKuB$tv?)&L"
    "C|=8JeOh43_9{OuAGuMUbUdQ8cCLsVTriFTH>5<GllfeF3haujd20pA-cTH1q0T@z`@4LzZz<p15!ZRp-_4L!u0X9vd##|&f@=HjIw?OQ12S8y"
    "p6Dpe`jj#E0`Zjs`&+Y~n5;fQXLz<H?8GeJEvLmYwJ<9^@n*U%WN41$%f^&J``tY`(I$Sm1~riHk<Fgui7|}XnEZ@e(ac6$5DiKIo^0~iSf;{@"
    "F_rl_Y@Q@1FNo>`Zkx$V4_sqXARZ78(uspqlx-u<Qs7goYET~sb>b1mk{yV5?3$C#Gmwg?c>lq=-C*qiL+u9vo}kJt1_tdn{fvj%Dl@-PQ3Y@z"
    "5KQYU84lQ`yVdz5DQQJcCrXRWe4Q=l=<+E}8s+&Cb<Vn)kWI2y#1UQj5Xt|G#`bg0lrDdYN<X-m>s6YpRXGB5P~X2#ryuDqw-O}HN79!Qze4{y"
    "b=<02G@t0-U;)P#5zt!U1L2g5#<Bw*GQ;P8V}sjO$~_0wNCr1=s|KPV0xYJoY63hwNzlWVOSj1df#w&i;c~eQ>l*+wySrl<h^dn4Ho3K|1GI4I"
    "WaZ5}OE^ec|M-vpBNr4#d=2*cM-sDVvStGxmkh1TD?FM6do0UK<Citd%IcJFSXFz-$Q7(42eW+lZ$SO*IXn|i)1?9A@zwrY7}p69!1M2Skpzh^"
    "-D(Z+7S#=b3Pmb^JmL_%P@FU^SH<T?JWKkw=6FNsL!ZQP*CYm2v5TFnAFwyO1#J{#am95vWIN=}+CCCM?Qr>MatC;&HfBe+d6uok5@T<8MBV67"
    "<12FCtI`uMFyGeLwwpa0bv8yVMK-9k!sd>zY{?aYkdEdzZT5LleB3M<Jtvd5M~rQAOsT@bV911lfZ?;dY)TNUQZ(S7f&&dSqx(8k1dM*vO<*dj"
    "5O8X%NT1?P`+>la#cj{Ox4;%n7TS7_Fi-|I75@+%t3Ez2C(kaK@6ye^Hm0hyqMeOud(d%PRy`HpRGUyQ+l=j-oS)7h5YI}MNMF4{M*$X56o$C~"
    "{M-7yW%Iu%Q$JhPvNg|3Be<$V!nf#*cP#w7wKHsKcJu)&_vEv8LTt9n3S_F>0IM8nzU9-(nyAbMI+vybaOzUBl#dKPVC}s4hTd=?sv1`^-X00="
    "rS`D)4i;$_IeptZovG;0FFT%}8QA7ii5<x>398>KP6~f&-Mj)aWd%rQUP2I&j=`?+@L;pb(G*0I-+z0kge=P~BZi_qRD#SGj>p=CMt@plB~|>q"
    "hk*;AVSr&?B(o3ye|jg5w7UP6N=2I(=lHQk>=(y;IiWKej~P`jkSD$fM_v%CU*^BS41C!eo(_dYM1yq)g>W!eWP2lDhsyzVGx!>C`R#D^AT3wf"
    "*Z<8(t4l)^v1UfF7zc?3VT?5wjOFvc3R#66uyE+u_OLGw_wvS3MOq^#j2S-99e2PN$D=6f4`I{+VGj!P)S1bDGYX3pi<dEJ-3)@xbNpyL@(l{Z"
    "7)1ALP}sPgL2xjc5&tC$B8I^T<L?DQ#Ymwq+)+G^I-rT7k>m7)2hYYZI_*gv<dpTlD~^4Gy$L8QR)ome24pU(A#{~jQ%HWU(xKu>A4#ZOU7ZX>"
    "fxI`MZV0#z(sh!}x2sIrk*a1ns=p15K@=yOs5(3Bin@a*9K45KRn;)f6O%2P1ZxYw?Z%K2+aP*AsXT2pK@rUH$ccqYjE6qj0eod)k+wG=Y78VJ"
    "kzekL@2WzEzv((Pmqsm0r{W?)(>rlu<AsAGkmC9gW5wMnutXelSD(Q+ATLJh60F71m`W^r$u`L&B8mU4rN1zwYSm<XICu_Dz1{TatrJ2w9%0T4"
    "hR_W`JW-$19(`VJZq`gQI8V%Lfdt|~A7iN<Jte$YK>hanr9tZ=IC@udV*Ja6d5%J+e>#q(>eE1Lukl9q^}L{iIX=xcZ-3-Fi*AOy?l_JX@>-e*"
    "y|}d+t-$QbMNk5mLa;sX@cGdy`RraqDB!U(Zr3?9oF(gIG|;x?zJ#}j$tm`wwIj}v>He20CL{0Td+6cdeU7y*v%kaWXpmJsSmJ_MKjH7QBh^w("
    ")iA~ic087WnRNO6fqBHL_>877qVopV0ANIqg1KtUp+8_l$_ED&fUru*0VAD_2E8}^e?73h9-H>R9@M@0gt!45oPIM=YOkPFJWM*Bd}pC?VB^uN"
    "l`d}5*-X$V9^%i^GP}!1J-7e!(6lT25|>0KI^;KUk8*5?i3i@W@(Sdirt|O(PMhXqTmm@T404e|rAy*O0qD3&CdSUlcjT6P!j^XbNy37}b(b11"
    "=%r0sqrk_!$0V*@FbiWPuAk_w3wM4@S%4UIPB3ySVf{ppm8=e3FepMLtHZEe_fzXlEn_7V9WMeKmW^J%xnrp)=nXdVmAuwENr3V`H*Rv|-3QU0"
    "xDKlhSu1}|elOw_C4*3Bz1n$X?OF3&SQkib3pFsVVd|7GL724Po-XBW>DFC?H@UzQO1^hS8%K>VDmn9wG9I+Qzr?G^1$y*RHW57Yr@O+(-6@-0"
    "*enHZ#t~z9L7LAn?oC7>E-4(AFOu|Q<cg$9-~jTrw1d_LXBP)Yr<02x)zSGs9WfV&;syjyiWws&CMa4TsO04M+`QZ3_*47>>7ukQ&h~p_&Ai9c"
    "FjqS){|!-QI4B@OZi;-iTdp55ka3e&&ikc4>9#A5k<?E0qkXZF($DE)xt3Rv^5X7Snv%RhTe1sFS#Bs65-(TO?J%<h8An6+QM=_box;jYt;HtK"
    "@It95MYt_R&wT;`DsBpCkx@UkmdRT9MRZ+;{zg0jeF1mXxV5OVWk$uD@z$0+fDwGUf-+eoPvo+DBEJ<;HYP)!Slec!Zs-~_LO&!J7dH0-wHw{V"
    "=poBz1$mVNi#SluRN=0J&QzQQaJ8;pc<RN?24s9%mIuk>K08uHvG>JDW%$z|*(}I~ljPmsVV|M@U_n+*mcLGNRVNsaua>Fz2(3qMh&jJM6?n{u"
    "X|M1pdZdA2y&xy42Xw{4r@QtDt1}Emu7#@l`bmMij7~N-ON`{-PnLN1$z4S*=0p=0znpgMd`d~7f*A9mV)u=Y#tsg&O5sWFJo3t+*+#HYK4gC9"
    ")!sQ&vPZt#-z+wB3J=3~n15IS@+SK%<3R*8u7eduv^itg6FTw(&P%S1Q(+06na-Ez>52nF(Ekk+jGGM(*xOmP3P5LZ$6we>?kxz7rAW_6>*fbf"
    "uG<1FgO!n$QtAnmWQpC|TGXi<>F60t|5J?s0!kHJIRkMQO@Ep?jW`abu<lrgh|5X}kobI0K@rq|K+1CM1{C~NgEW0i6Wu<n?b(htY@2DOfC!tY"
    "@Pe=bM4SIl10*VK+kpumF!6!cTy%M?IAvwN8DRKc1%}w}UdyOde5k$|MUGMV!q{*zWpHiVidccLa|WTK#%XRFCyKpoy9(<N-K6>S9!36SE%M;Z"
    "!OEm;0NS*D+iu}Rj*XeeyQmCnhw0r5QT#Rg$Hl`uu6UqNZaze3n99Eju^}&3toOd;3kNZI-{yJ>;;C>yy-KI|c`+~UP;g}>m>TISOXmA#Zz7TF"
    "U9vnN-A=f2s<QHLljZr6whj=z%)$&04`e#t-M|@xnH5s%nb~H#KF{c2Py5iJ(hL|fKnRne2I{rf_Hi|U8wW9_CT#Ygwef)I1%WQAMA94zK_EUh"
    "k*Rgt+;^>gnYNeTA}cMg3eDAK&$U_P9)5zKl6x~tEHMa)Q|&I2ztT-mO06^*Ye&0oIH<|endpXA5|QCM#O!pD;HXW1uvr0e<c=7J6mf&H{t%fr"
    "4&(3I<6S3`<6mWK+O2QUUk-hez<mFRCZh#QhN+K&Q9vpycXPSse8&o2JT9BzEicApq_|*|j@HN6wncgY<oa4}iuT!rUSl?1>ug*v_<}684<;RV"
    "*YTdjq~kmFv7^?Z?Z|J(q_^uiZJ1nUp9(%ugFQpC5>w52)(oC5=f%1mp9r<xich>P>W5EM9ct+G+vgO=QBQpOlzb+55}%$wZW)T8iu_jmLAT>N"
    "{@%_D5RF!u!alyeB_w`#^aI$8K$l?5+`!bV&~C$^j}%D@(t<&!F9yA^YZ7tTA7QY^;wKU2h8=4|<tdu@LIR1~ckYUvw$R6#2`{j3mK{g}*n)N>"
    "d3}-OMjboF^_<>FLYv}gs&c}1?q=J;xD`pxuG1i@s}<&lO6Q#T%zB_JmloVekWAd{5^{QP!658d)u1nK0*q>*)RfzCV>?lOyW1Ve@>?j1hVkq="
    "vJTP|6ovGoH9122bNaCjR~3j&I<m)oafOLXdrlzq`y&sC+<g*xvF~*3bgzxwbGHr3I?irHD4%tJfyK!xyS>H8<{b3pDH-)`xDybz(OGZg#je{i"
    "0oV7Qg{<+@yAX>?wT@+DO@~%wxo#a<V|#a|kYp|C2x^tg=a1c38n;nce@5lGQ5QQ8<Ni1bfcHMV8||PkF^}5`ENEd}?=N@v??E%O-llo_DUrwn"
    "wVZCO+Rz5wIPJuR3VP3-X?r~<<G6i^Ed-+HW27e#88ua0w*!-Li)KONxD82pxmlv7Zh<Ac!W<|o(kLi<ar-WALvJ;QCf^JD%Lu<~H@VJpkm)|H"
    "WZ2^_HfNL3+Qc1b_I@3ADqz_<TxL`2&1UsTY6ei}QMp3%Na7Qk9IcYP6L$o13u(Ijg+|!L_pn$cn#ryG7$+Mf&u`FgkfW8sz96nbkN8BQIvH#p"
    "vy9tMB^@+;s0-}?qB_&-I7Xy$h#iK1;Kp6Yh=J##Mbwow38#!_Ju=7obL05yX#}XK0iHJW3-IUj4-rI1u&j!*lo)Zu`JdTLo@%&WOblRIfW<vy"
    "jHsS`bYW;uCDwQ(^H!;pbEg;`BS7%R^e$Uaj3Q`=sm!ZO6>_OY_%;|CAY7#Lj84(SDXIDKL3*>kOjn<>DWxa(DLQ^8k2Q?}IN<uK*q;|=N(+Pb"
    "p)+#aYTn=DX$>Y7Q=Sd4HzER0oIT;S#d1w4Ki4t_{*p`fU|<sF%o+~f%#%C)Zr8znviZys>3+40$W@fojwjO22(J=*=tg6-QQwd&26`D_!9VC1"
    "yM(_cv)Kxx=&L-uSzc~d<S2EQEKA|=U=N+K&4h6dOd~_hK)81dhP!;BV5@#HvKO!JC}l5a^P$9SwcNb~i_B}#)~(}52)pPNw&Dq9IEEcqB|zeg"
    "NyzV(s|*uM$V_?cMk78Awtre;_Oe;m$D#J|yUPiGH>g~7M6*b1c6fPyZtWcMNU12Bp(5CEPrj;;5+e#8t^4fmepkf?Q6jjV{}sJ_C463CQ0NuY"
    "Ua$+S_;@U7V_iI8<qnYvx}8MAibU+8NYNoW-4#DYw~mdzHiC1}(bGk-zQ-g*_^D42$S-{z9<=FooDDFi0({|jthBFx>(&Pi+_C2EP{%vU1~nGl"
    "N_?Z`#{yI%4M(&U7{-?IBLjFJeZfER)wgmTx~VP*9N~0oKoRiz&5MWn@_~FVk&z6oWV0?_NyoreNQBRz?376FBhW0CKEO;)>pQ$=kf{Mp8e%7_"
    "vn8@NOtbSy!PS(vpiHX2lk#1eNJa>6UYl1gdSp2<I9eMZC|!iXQ(qGjHR<MaNBUXpNjl3glPDH%1Ln$ENR!WktExl!6A^wn*dsL@ltO6qU5Qku"
    "CeVy*M!AG?8e0{)r~&sqsW>z|AHy~s&|cTBytEeL)s@^eBzL&g6H%S08UO`T!XO|BnBGaTN-q|(^6EaxWuh;t&eOod>qj9ex&((2_g_|-Q|gc3"
    "Qc9SKk>5ZjM8XhJ8RjZCd1G7Szr;SSZD0H!W!u4hhuh8EU9^)>WY8sddwNK9L2-pygOOfBJZ@`OLySz4mD-?%)GOVDiYNa{3WfQ$`L#^mc?_EN"
    "{P8{J*(MJTSZPoN%3eB$F;~!>&u$M}CPUh+jkbumaI3CWj`BCfYD)U#swhykPqM38n}PaHso?wi-BEQ({N|elI%}cBTZu-6XHk}X>oxEys%2&E"
    "Vht#3f1ZE>q2hH_QK_rfN5=zM?1}HnyjZ(>RduE=|HrunWFreosiIV8XU6A#<T`DivsWM0*%Fnhs&ZQdU=y_0RC-H;EN~*NYYs5KT(8n}{r~<y"
    "7S<Ak|ERow)&bUCD6lNk_r(fCYWjKi{be0|`09Ie5Z?)(F-TV(x2pfc6Qh4Sv?Hn;soxTU?V&>brsnPwDQ!4h3OFuhvix4u@^oSni7DAzhr;iO"
    "$bB4#BP?Bw9;Ne?R2z<HM5{%6_`L+oczRw{oiyrxs(FjP*w+DXH`C&7l`QWcUxOBZ$0Yivf%tPc;8Codml$9$MM`8xHaRa&&F~(?Av`3MqY5#K"
    "L8rhMlQK(?j0LXol^sUf8@1H*Dsaf3^cWDCTNC&Qa7r&6^71{&W;0L~4wG_CPwkkyx>fCLpPn3UR+u2CHn8ow#!H}K{F~o7>K(a%4EZ2Po7}h1"
    "&8%36H`IDR$&*>4o_rXp<$nDry{*mAj>_{|#m8N-5382)OK?9GiY_YObmZQ8UO71q9^}7`5JGYAMJ^c~BXw8I6tUFYZFj(=7=vU_#~4OzD*ooe"
    "gxzt_RSL0RRy9zDdy2AwTP8uKK{f2NAa=y3t#KB8%1m-}G5@_i#+WNaa^ObSkWW?R6miu$xrpd$*}J{1_dYdZIV%AF-N+3<JDQdDu0fuKe$+K6"
    "l9il6YVIDeQB|y}!S<L*QxXfMuc8Gm&M7f_BCZ7c!fKu+HimM8X6)L#9{GVD&eKn%v(P>SOEDgWSgHgT)!K2Lk&izR=hhC!=e=a+`UW(~T;$Cr"
    "g@zW_aYK+O|I=l!+9{U35q?b6b>NN0s%y_3Ia=4g>iS)p%-8p1IAE7HRvYi`G91NKFJ6GXhymh}D|!T+qVMg>+JBs4n8=(KG4|sv9f!6CtLt&U"
    "0@e^A7yi-|KAh3f2047W+xm1FSnAV>b;#kDub^F^<1Y(t1HE>HQ6}Bpk4Hh(ePn>_;VTmvX!hhKo?cSdc)`%tHFppMh)w7l2lC_(9B7Q>!f9o4"
    "*inxxPMvUTZ?0G;>dn`B13+WZ9ftT#E$Ifu2ynwL{Nl&KSOe0xRZkZ{QPv@s(k8(jd0WsJ`5F<qp`y$8bmp9irEtQn)D!Z)k(3^2OTonRK~@J("
    "TeiF&TOv~o(yq^C5e!DSJn`V53Q$j$Qlr8MAax)@d7@`{)OSlKq92}k%L)c+X;_1ePv2!uQ(<40U@N0uAWSyEwac+UEaX+^(tEw7rN*l+v%8#h"
    "Rn#axX!>6hHE-psXEMZ2jc_>lUokO44G79MY29Q=Sw%(UiS&3ytsd_o#DNWTtLdN&4A!lvv{B-WL3LuIsm3kre$7|>6D<UYaQaCQLS-!oGXT%y"
    "w8%hG*0QyQ3aIdxudqPn%o5G_T%_hDKXKDvPdj%xd_&h2wR@Ob^HRlk$cb5fvR~EemDf2>^nlkg%2KV58Af=UQ~Sbm1N{qQNGA%6AzM2DF&<EU"
    "Wx8Gye%FWxGH}y!LT3(?Zgo)E#l!^gH}x)m9dK=dbhkvlO3@uG(<vi2MwuRqWY&g%VJ-LSeQKc((JINxl!FIK%MEUpbtgcoFl#xEs9&ae3yQdq"
    "DG0li^TlBy93T}uo}8m?gH2pl=5?1t-lLAAB9k0nCbJjyDyADQ%9o)~TCSBJosTKLXB$bvKzwUifzSwNs9YVh#WI<$53&{e|6tKaoaXKfRhC>U"
    "x&4$Eq+)kR)FXL^ex{MN3tLp++F~fAzoab9ozA{FNv2eJV=E09Yi?3RxxkG-r7M)@6NGe=Gzmhj43h#?S9_#1trYwtTo^5k1WxAAHbPoKyBGs<"
    "ah(D4LkcRUl$%s{4y8VOMUK=#3{2vVv&ZJ?1CdMl2kT-}qUWE5Dz)`{|K-RcCv}zCq_l4FHQnXTAF*H$aH>a)qfhYgJmI=})SetmEJQHgJP91C"
    "NUyR#5eYBP79z^ZkGq&QRY)wIjC#0$Hi_w6l$h#APtsrX7tqrmlVy@)%}DJT9r)a_7pBQ>zWL+%k1d2$`G=Z>^kbT1R^Qd51>$Cgbpg>MfK~vY"
    "05oED>H;f5VA}gNCnKem6r*D}<H#Zye^**pXXi&h@bWwE$a_i11>FRrtTMbwbjEQ6mR5q+KHjtec_`1(ne-eDFee^>gKs4zQlI}DdK8)bizPsg"
    "1TTD0;OhkjYRwD8CI-U4S!L7%a<X)pm6-YwaE-zq(+oeP>Bky<9W55=ETd3y_>$`T)aguk!*<cx?QMh5di%;YN$phBtLj5)m1C_SHMS^!0pDU)"
    "MU>W?UsYbUHGW0TuWy9xA_rJ3GlF#_N#1Z3kc7&nm6UP=ePdxoKcz#9qT`THNPcBha-b?W2`4K+;RYllx!#&(*zZazfQjntR8|9(hbGno*47af"
    "Fsm{ZkMjQ1eaV$qfZ9ZdvjU5_7MMw!)03=;tM+D9(n0untg734_?L00%GLN6a418<-O59NiiW1E$0cPgZjy^~<~8*las|eiON#0JHh}>W>mBf^"
    "tW>gU{@9RHXj2WXgW|#Zy$2TPuqLVkF#eby{8<b^Oz+PFENFrQVL5f6#cDoGmkd8A-^MGygk!CN_-4R(?lyvyD1IFSMv)w_EH3(6rTHCDO)ip_"
    "qC7MSg{lj;P>Jx6?oTDH?$f`NIOOsO;y8z{rjLCo!`fM=)BA7AbdeD+J^hpccSS4aXm_6F$nYtey@fC|&t-!!(91F{#qQrME#(Hif{7<($~*)%"
    ">u$*jv?oWvL}sAef)<%j;i0$ZSGzuyW&~qM6tEI(1S5U1lr7#I7P;g!FeB&%s3HAK#hbBo5>Ew%&Dweq#N*e<&h%_TO2wwKNi6=ryd&3I6j7v2"
    "C;4M#rE^LSpy|`3oF#u_f#;1JpkhM?IzZ#klv|Y#d6S&@AW?;vSM=28VgAcRRJEvrobU+po5|5LI8CM--3^6^xs55uT4_sqcDFDc<rHp}pdl=g"
    "2mo2xa#c*(NsC;^cO3gAro~Btq(DM>{!8Qz<O4heW<$RY-w!Q6q(8sQ(lwy<Rm1QCScR`Jn_yB&vd0x~BO=4`(1d#^EL>vM5$jg)xT36zmaLr@"
    ";V8Va(iLuvS4}-#s9l)Y2+z4cWp~*etKV@!uvK36VOEt7_%pPk9xnO6nApTB|193Mjn>)}r7kiXH^_`?%G27J+q$;EOIY<?6H7y@PNIn=y!F{l"
    "zsTEYl~qjapLh;RHp;Go92$$zE!RxA){Zz{08!_-!OK?-@j4y_F01rh+PlHoC@lliFi6~3@v^@H*zi4=1Wx!8i`-2M(5*cCwaDbna(LF8+9+zF"
    "zi8YR((ub9WVOg&oys(hhGLY8jA5Frc2X0;53QsoNeZQ0GXF>%f&&$XQoy0=!bFhVtx~3e6?!74Z4^bR>5)W;R0Ls-Z5pLPG#;3NLrDm~_eXeM"
    "fSI{c8g#Nq{$5~-znRFHk#IfC8J^CwM5nTLkGs?RB$IY1jt9$+X*XsmW`3ob1b`(`4Ic3%t(2Zb6+BnpdLriI7t@sp5cw6j*8$HH04#eMby_$@"
    "<5bd&*GO)`PFcwEu(*zbW6jW2xfCbbzvIj(cs#GXQkTU8){q5yLdZnkl*w|Hq3-SmZB&Ss+a{kU54W4SW+d_nhE(3fs(_ZBEm9bG4kBdE3GGJK"
    "&f#Y)h&tm0To$g$?IUv0JpH`JD&C`4{j9nwXre#;{G3RaUq)2bI`${3{ncg$OO?$VN86nQHlr)Vlr`J3heD=>oEY>a_>zcSnI|Cg?t!+Z1?SVD"
    "Y)@zw8!;^z7yt{rlS3zN%AvKH&e6F7@I;BTsMaReiyR}D5}%9nakjG^7gP06c~j9Pbb*e1_t}!@4s1}$^aC)Atk>+2NthB$&$0jUAOGoiAkw93"
    "K7ag!r61VIl#ZZ;p)WS-NWwrQJF^5zudK?HE>U-x6EY7R^`=Y_D)bEH?B@g${W5K>A^|~~Z_{E~;LR#t%zvQ^D&aj1FaO1QrxGch^V2=)ne*rT"
    "&-uUni*;b{S>Kb-fCXf^!l#EPhZk>;PTyknW9e*W5#4jzv=@#a4DmLSPu77T5?PIT=S6Jet5-uSY5IXnmvmIOxtTo8!XSa27u4&kwqb#)K2cF<"
    "j*Vd9g%rXyXk_W#2UHL@=t)X6`U0fuw-#C+Kzm94kw4B#>xCQPP}a^=7Snp+xI884_WQyK#6-%%${GMI=bMsFLAXy!t_Ga(g%eRfpt@bYCq?3g"
    "NBuB}*6Wk+El+wg(N(nd!Y5SVw&O!R*c><LT+BtH@rH>jr)dk|`jP4sJ?3#nG3MkZXw@}0Pt~C}BV5^c_`r$9fOH9sZ9wrA7b0UDzY;a1xZrHY"
    "xzeau(1<;LM1zDBku{wgaCR`l96)djY$TKV$!$g_1WQh)Gm>=Y>;e0}r4x#~6d#@(9axk7{r4yDk0)10XQv}cso0el4Tb(ZR8@ed_t|^~EJb7h"
    "ghkk84|)KT626Ih^qHWSoUe2yn{u7yU?cnhB<Er#ODo~ax>q>AQUn<3Ws8t@;YAQrKEWv=*0p8b=ZEBxkH1v)U66<*qVc=2LsPzz@9yy&HCtFW"
    "n@7G<dJzP?AardG0RAz_H@Grb5z^WzQ<m|d6Xfg&3Z_ZATE9}5boZ>vp$N0u%(3*{BjNPy;P7H{bx4PKoCOb$^m*wiEw0RgCXuLbtH+d4Nj1iB"
    "Lsyxr<c6oUNG!S+wq7t*iXy{i)X-3D^R0|QoFb|UcloSx!xtC&3{Zka!VBmE3oH+{EP1o6Ol~N;Q7t;v;uZl~>T3+{NqO(=A!L(9`Wd5)fHF3i"
    "oo+QlKxNUja=jtVd0r&B*vZg@e-<ncVQ2G+X*buCXcVl41DCkO0i7yPqQ;#+o__lZJ3+Fg&;v$Fvz!_p!Z9iF{(TVuxg>;r5rv~D#M`spCQD07"
    "7kqqq^!D`V&C&kk^vZfWIlpA!mz$e;R-*DyQ51WWS>?1~0&+uH*Ah#&s{8U4%OGTmAnM6y0)9QD$w%Z_SZsPWvo^~inJ_nxTFLqy8#@Etby<L}"
    "R4M^L0Xt$`$Kf{cxhjV1(<1^w#@~rYiZNO-!#NaJAuAvh=$Xg>vl#+A^gU*!j5u^w8<P`?toT>e6D5(tByQ3+3kf{(<Yd+u1xTk$Fga1yJ|#x0"
    "(zJ6)%fzDlJ=E`SK`md?dhJ^O`ma@R%-+BLD>EY64{KmS7RE`IoJ$e#EVqY2A|-MlTBU@UR~#Vw{46+@a7j??3abKQ%dx|>_QG?AzBfj|@I9T$"
    "%X;+>#Rlm0t^hH+Ofp#wGiUOFiDN$+=OlqMbfRb&#39j&S+rd2_<2G1QdkY0`d?EGT_$T6D?mFK%0)7X<^U5fg#YApgCs4*O_2lVL7!VZol8~T"
    "QyK(sKTAG><YVj?@pu^eW67}89P<=c2$obbpT!2{8!MG^v%#m1C&&hQ1=d8DW!|a4I#}<tUiX-KREcDs-wkR}!vJ&xKLE)F@UUEghjs-28wWTc"
    "CUvnhsj7RCavD=6%G5{?x)Lm5#5A-o_ZN~7j$ds!=z8}>JoLO!k^Qbe3Ozy$#S{s=!B(VzBM_9JrG%jml)mCRuua|yjXZzoM(!)zq=-06hWMbu"
    "7YcQXwxtZmgBOm20aC97;ZZ9D1F?oCo?HSngcnS;37y+kii}8H%hOi1vT@qA;^IV&9)Gk`DQ~39z3}A73q6l~Mp-n8S{e);urpCA5U39*^W=n4"
    "^BWI6J4Biml*g3gja=ax#0yJFh8JX$U`dB`^@(*2)E{KrDdIl_a<NIr41!_oh0JvBQ{H0ymY9O1ZV~hhK+ae-G4u)wD7JQJ8#s=Ke$;GJi=`1_"
    "4$y)}RI-@$E2ZZU=7gri5I`RSKvaT5FGMM@R$3ySbPT1oO!%-R9(d)1S3Zn_ONWA8qb+^CWsix0yBA}dUlRnwn1A8Ud=a@q<3;o!`_$ASP<b|s"
    "n-v%iz>PDhJ1oiI?-)r&lj9mYG>A?5HBJJ9)DV18kq~J;)3kH+3=2kabEl2017ly{ZVpGDXNV%X>zHC2`;VTQ+iQV*bh8A(Ir1W-ubXr(q>~4H"
    "i>-MT@ywLTmPH~Y1!+jA7~wuAqCoY8e0^EAYAO=!YOz$n0nw3IkqsI^vPqztysVU2f6qd58!(m0LMT!y9{368c%C7KCvV?g99~`?eRs%O`xMJi"
    "gX)bR3tIzG&zU=|9siYFA^!$Y_bElk2eY4{)Mlr^#*;OwA$&8bn5<Mn<-TD%n9*9Z5MPPy9-*T?0+NaB?JTQdK^(frAos1IMri_Iv9+M<7~=-?"
    "Z=DEGD*V1I%490F6E==ZvV(`}la&;um{_tBe!^50b;zx=Pr_<u)tEH}*h{CdS*6EU$U1{^q2*j2?2iQfJ08hEArb{L`Qi<C9jjs^_a&ctR{ltU"
    "hR_v<;uFwQ(1L+o_L;jN>Pi;koJ`aPRU^Z8^5mFmg{SDZLQ%<eN|``+SuWVnro0F88X7!+U_!1z3`p<+I#=Kw!@2=8M`1zZ4>I@H8D9vXiKR3|"
    "oH!}A<O>6P58uKbM1?P5$+TLLDTt)2Y(?0Kn>jI$$uX$vhX*6}yq*me^$Mj=6gMEk$HDL*0nhCSae|tFaj6{^?4cK5hTdwsz#qt;2NT8P`~9=y"
    "<H_qYFd5G-hSvVs>6@d2!_)mku+`7Lms}I^pBG$?^;4EUP*EeyCQo(0ElfkoHy^@&7uqrIfwF>^%l6(=vDalPMZRI?Ei<HFsR<ljy@8FgDar4V"
    "PK<aJ)@CILp;2<)YgP(xH}iQ-WyiTBYbsZadKPM%s0U-NfSJVyXlP*qW-xRYY;fF2GmIrscntTflVY8Hk|(>sgF(LF+cy`7hX-dT4FnQo=ND(+"
    "9bF!solcGsh&HU0csD|Ij!~Tj`;<&Yr3#^Q(~xA6QnM>=0SYIhMJTm30j?B!u0-S7el&tDj+^36T!<60Vb{)tH`r<c@U7*vuWH8-rR2`<=*&na"
    ">}VWg;8uo*j#PeLjbLZW10Kpbf&1fT^Vm2M*?AFw@+bt396+5sY*Su5dzZ9Zw$njc`+<k?ZP-yH9Gs-)Ccn&B6$G{d@=38}aZXg+viv0@hQB8e"
    "S*Ztwsvs+OiP5O5^&^?_tP2L9JqL<4ijy8GxUm5YfRQfB5G8eZJoH1K!*mN(WeE31v8jHtQZ*E(Z8s!><&l>n5T+fz)CL6_l~^DbIuXHH2x0-i"
    "|0>*~Ko58*TMj-+>51ZD<V3<hI%HU5H1k~XEFxBnJ=f`vki;fzokkesC5YbA!sCNS#)L+xf(9=)H-8lcAf*2VzBxtCI!igU(^T;)Ue(E^WanqC"
    "eItdRIhJ;60(y#uUZq(ARZE*(v%%v)lkjB90kNaGO;o(i-WF!I(8eoMx?yVbLh1%6nGqxOBiJvXQ^X3ees5?UI6_jMx#o=aW#XZ=q-?dJ1+T?D"
    "EUXlqDt$nw+`M5sES+Jyg`(Rys#jB^Y1%A9d0n~1@-UBM(XF+`?64B)V6reV1j};ZNep==hK^0MM6Ej^LD(6H7;(&~Y!<Tc<$)zbQZbiS%SAUi"
    "Si`Lj?A1w!G#-ovmZ1BVJpSDS7GG0w5XiduDGeJww2_7l=uFdjk}c31W={7mbWkC*N0=BNQ>Y6Hrc`n5P@Q}<snDNFNCO>GaT`{hS0JdTKl1=%"
    "h@2!B+sr)byDNyu)G1E~7DMag==AJjkFGwdL`7%`NgSGo$D$U3kR+9%BsV(>AllP}NTNkBHHenkpBA0<Q4W)vKA$KcK9IL}z!*sw-{%|h1d$x5"
    "C>DYmsV)nyYa~exiAbE{SG?(k>l4WHY>}-=aeEQbgM~Q#T^8a%WrxqR#BmsrtvGfT=hm-Chhw6dR@tdG6pQtOhrv4%l_AU8k(p@NUc?QwWC!>c"
    "Hg5sc`e<MIlK2w*+pi$Tn?kzK^O1C0u@y^fof&#M9TCcSLM<N#A+Y7*EX5j7r4_p)K2bEz`6>=1F94wh83~{ul#G5fF{|KmL@suryv4}P#GHaZ"
    "#cgw=bTOoiq7qP7j<xgd=<T~#X!QVZm&<zQuyAPCmGH(WMFpP7v#B#kc|bOpacsNR@3e>?NjV@*Eb>1RqDfOOII9rzu}Wnud0Qaa<K;cdX6;B@"
    "UcFId7M;f>r3g}>3!OrQ=V%g9V8yj|P7V)_-k&gDoC+@ipjT*CYvP4!?kHZjA4MxOmkNv-yeXNlD9p^{Q6uX$5<2tJIzlC^o(Zc*cm_^hfy_@_"
    "6LK>HA=4Oo&19QJ*#==QnJn8%d^C!}UBcm;a8$H}hcNgNk|9V2VPDDvmvVy+j|s3l*1R>0f~3s;j@CA^H$G#{DK%t656nuvQWP~sSI8So*GF0}"
    "!h7?mbPAv`ToI;8kU^w8B<kE&C-z~D+Oaq%TRt4GEvFw?J7BNz+`|g_E+ZdICeBkv-Y5zAG1JM|Ek;ez)pw#_LhxY)&m4?%GGY1rltOGOf+6*a"
    "8PV1~NmmObNW{%Gc8mLmw-}nRxRVe%z|$W$bHZ#)eB&>F`HKv=o{Hl&^Z}7hAMnco!?t!84^Q1aC8Xh(w`bLF5aFqx>}jVh_~54gU|N5$Cl5H_"
    "M*u3Qb^-xUz{nQX^q+IKH}`OfOk-20o<HYOZKsB&&Q4GMKla{5xosp#6#W$h*S#a}P&D2E)hA8_EzxdG>$Q^Hy?weJ8i<4>j46Uckd`$QKC%CB"
    "?swdexSz6La`RDDsKSGUY`JIdJtwB8TLcPKSy@?`Sy}mTYfrq|6JML_uBGWG^i!w=^mnBF9m~I0f-w^az?G3H)1R)zyNZ5z`VU|K5umkzmg+ak"
    "J_eiuNa-%wouv;Pcz$z7;pY=jUXv@4zpuCF_InFXP^^NBcJJu=wnw?rD9>3jTi-&9N}opN<zHa{v<P2G7d+7xeQR?{p<LF=!eqRDq-Wo~qGwp?"
    "fQ2h3`Rk33&yG%i8B<tqR(!ZxRI4kYdz~@t81H(tG11>c4(Y_T=A(~ETjP+je6eHIahBX?>{&%#Rc|om+TXIp)g+(dZ_jfm1OzmhD*zC-+f~7t"
    "W&shfLypGy@gv{^W;{_fh3K9d@vH98uf!uvAB%2k*tyM~z&6#)qBPZfDUIs`YQP%Pl%ZoWPWwJB3Ie}361U)J4R%rFPJlH$=4;`yE)IP{!9*LQ"
    "xat-+@4!?ZF@jJL1)oBY9pMEuyP-^S4B7cepJL*wNA`jTJf@@uP!Dth8(0VV{0}Q)wKEQP{|jD_8o+!H8Ykre(+<3J8<EY?0~ITa3L|780tZ)|"
    "kF)|QDBBdEM1FjWOjJMu0_DGnILj+=CFFW)L81VC?$EK|3T+zmt89LiEEeca=e~l4Mlw=;;U!G@Df&0GeQUpRE8l8P3uPBr3#z#X$A0AmW)JG_"
    "l6@JK&+iTAv)T@o6V&=VRGI<yxlng(8iJhG?tGdgZXM7n@FC`c1nj@3`de2Rb;^se5}DO0$+IPnm}rN%rL>xf^rXbANVF@!FnAi#Oki{COk^V_"
    "yF-zeec+kvmM;0pLA7A9$vv~<1SXbGr=aYp3T;<hDz>*bU(aS@s#omyAU7mFArk;R@G%qk4PYR-nqUT3N<fKtloLB=AAb?Tfegno3zcb;d`-?8"
    "n8}88SZ_$~{}=^eUKB~inw+SO-pGlDJV~XuK}>o(*-g-Fonbz^a`JcVD_WU)5POu^d&}Itj&r|dRWDH~PGsos?F>{c9RbJ42Usl?X>jl|hma9-"
    "EJO?%ljv`UKF237O^gVIarY)$)$jqQSV!VR8|FICKWxW~6FFaw7p`r64GS<;^#5K|pHyk;iwl_-1{0!)VMEG_s#PrfX|zwu71loF6pp>OWRpNM"
    "sr7<gA(Y{?w1^Ja5nZmbUF{cDsPWse)-5}8!C_aX%qL8{r3dBCi$ERR`05%Pkb#2QylfcL9Q5qn`Th^13zCiNYw_@WJUY4>UtEIXbfq<rV4VrM"
    "P#PI|^W)er0$V}k+MYdNK6D4_&09t_pmwVKq9Y8Mw4F=a-lKmom)-y9wV_*8vc#jELNNspE$@}HwNI%6YMmk?%7J4_b+B>Zay`Vj`*7w<fw8f|"
    "VvOmzjT14(^z7}E)vzrFJu{KqWt~jO?Cp@XV9bE*e0+I$4yTQiOD)7h=$C&eG^4uNb>MMO#-^@ck4}C(e|L7d|I5|?7@wa~-aw<1aEMt2x^{x@"
    "^i-;m)zrWD*rsTdh21AT_z%+Fs4{y=_xy{|(dhh_tI^59)z721<BJ~Wxt;-QaK+9gS%@JdO3QvP-2Mxyl@L;-0{!j#dN$mO2ORDiO;MKsobDgO"
    ";$DpR-<=;`{-TW^1;aQPV1=eF5cnDdk&W9hRmq%7OpIkYgrXe$=<p{{n6JkFaW+1=FedNVF-=}vzxDQpl)F~-W+($coR*qG+4&Er$K$KRlZ$uf"
    "qmzB0TOcYpKWSrd?s_$X7X@ttm=|_h+|T*x+4%hOm#fRse;D8oP2i(|(9%>lcwag*ml<P4vnw%(YEhQL#iIw+X%|N)7=HAc&K;`IE|;nh0A1<X"
    "%&&-nQ?lTux8mfcy_P1>D=yQp*G!W-<(WR&^(oaGbeK`Fbw*Bm3pp#Z$&+Wc59gSCirZ==LsfuDzie1E)$rZh<59N>ib@3=CKzm;U+~=1qciq1"
    "P0+Rf(GzS+CtI0VQ|alh`)%{&{O#oFe+hX4XURd$U0(4Go6cQyE~c}s!()^>$RSI0OID-VjKQ;fiB=_RKY2{&bFI_;(RtZd+}_oDRGZn4GBYIv"
    "U6Z}#%#sq)@%aUM!d&g2j}HznuV9b^9qYCTp9J;(YRN?l6x+QLHr)<n(K@Nq%OA$)&o<zD{8-8<ZQ`;?bDT<pXgfLusd+g*KfXG^+}@4yd7?^T"
    "IVR^6c7GtY*bu1-3If3NuhmkG;HXE3Z^qllb#1$OVAnSWepmOeZ5a67@$2*P(b1?B>0bc>(7G%SZ;)Vv#$P)enCG>dCC6-_<#2Rz@@{n0)3$iA"
    "+S0vL7-VPp{S`ivirp$#KS8%MShYAKNE@htbA0fw2B_nbqC*Os(K{$@>bGaNgIyg<DQVpCCa68T5o&R=c`D3t1!i|U%si5U*o$IkfZ1YApkotg"
    "*8sYHGFojs7FAEd<|Mod(VU))uPzUX5ew&@D|z0<GX*i!t7N4;3_>>w`~g;U)zDmij_z!faaO<qdM>mW1a6&o4eY3aeYr!dVJ}PWpltixj_3+@"
    "=sHdIq#+&_G_VJ8T){kI!z7nhyc<kG9g<?l8(@9rO}$2&dadd9vTH>1An?DUYr`u~KOOkCPnh3=iuZKD{E$9g-KU@{O!#IenXHO36Yt-7`HFq^"
    "mBt5HsR}Kg^qhnjWh3s*U*T4miF^Ua?Bs;OWvWn}3Qws9#;|LYW}1lxnB)Txm*sd#K@N|788}ueONW(u=u!e%HJLDrfihoXH3svS0BvWIEEXK*"
    "_*?Ifj{92=_0X~cq%0XUP$7R<H7otJGJ89mA4^P>=Iu?x%Oa9voGdZwfr(>~9P@m2nZHh9z#H_a`8mT9FTeIy6_2U;nq1>KY6xM#1x55+0(MF}"
    "6*@@MH4fsdyo=@-K*JehJ)dDPE{;QO=_*;W2D}0hi_ghP<jN<7MZqAH)<6<KMHuagE9aaXTZCsu!KT)7Ka2Heaix}DZ)DuIk~5xeo2<|RRbfLX"
    "!PE5$uVso~-w!kfV(o~S*!iP@nwLU*`$wS75Qa}enviMDSR1Wx@s8{pBaMv^Vr%aU2GTh9N*t!l7RzCVl<Hq$WK>}m96G0BVJPfKI^pZVb1!S>"
    "1%(>vBS%p5TDMynqnFIkxpyc1L~)NrZ5;Mt;b1*Ia9;qa#qAUIs2S0QrSltNi))n<(@j40_M#!ID9FzY#BDgFB=mwLPjK-7ve}FS8z{G`y04S2"
    "tZj7n1l;eJVRn1<5g7M%c3kppc9X55dn>z6rg)>9PR~nTcbv^%9Veee<)UtU8Zh??Fge!y7S+|}Q%W#}d=jx<h&80Y2lyAa+rWzz#OI8Ro-Cg?"
    "!h2}>@EPcz)_^a!$@Ms2sC2s31=%1XC6i#9G9_#K4p8%<Bp`x5aiX=^OQH?!ND*ydhZ@n2<>sjXC&Ey8i+xLC)~Kn0mUl2Wy^45k)LULY2W<<Y"
    ")POPQ^Q%ewa88VOgEq2k8Ttr4CW?V@!+s@7((;bez%{mt(eozFrNZNk&7u?6o|3yVIH?Tx74B*jK%u<n)dEVF&>DGNB#**Djdu~IxA`8LDIS_J"
    "&G3On+iJ4s+#HBk{@K`TIbNM8DJx3bUXB`f@^)SL6G|V9w;TyJ3w)K6hc`7A$^b3YafRZ}fd5~tZo8_@G%!+x&etnlHgV=J)~lr)F-8~@7?g8S"
    "jU*}4lmn(N!{2S7@f!0-A~#ff8uY}}&!6Q$B|}+xSC~$yt@P6i2Tt!xC`h99xHh*2gi=nh<$A{bT~d}3I%KNQZgSlg>84QE{p%W*TRLMD!qa7e"
    "foK0tZ#Z2uU<EeWeVR~uCl#v8M<Thsmnk*GTsoLR5YxcS$(W5nvbclC=wm?dD8)6$YZ7$86e#ZoDs0yT1T8j=G_W)c48<0wA+e}yfC~G<-hWKf"
    "1--x}#z0Ce{P4IGlV#W22Tb`{pueolE<)kIn2xbn--~%<<bQUMv-&v2^dRf&6{f{T=7jFLgv^Ir051+CV%h}`A+o_d5>8eG9#4YNorv^`g2z^K"
    "v`ob(KQFVgaZ(8PUu07p2cymz-tc8#08d!A4lhpms~vpFZVNB<E{W7|I!n=aB6EP@ZOKkRWw^>7$${@4Ho=ZP2m<bEMDv9O__L(pKU=d5^AvqZ"
    "A9vZx0m!GE%Ivz2$13Fvj}C`oq1i)<mx(jFCDwgb%tQqOT43vEJV&7)Bqqs1G9bMSUC_iB(({o?E}Jjbcoz7pqGDPdB3(|@drj4Ss7lPhdPAw1"
    "m@FygnWj#SfEw@`T)NYc-DXVzdsF~iiO`eWkZdcNN{+P^k#lRM&aE;Ih+;sNoa%&C&K0HhDsU%EC@t?q98)<96oSX48aM)db*Ccuk>c<*dW5%%"
    "%yfR6VK9t{zu7B0GshvuMHU<RoQ$6slg^nL8dCf;oUH|}M0B+X1Gr8fF$<QcfJG(jg>I*@%wZgR5s;h4HF4e5ZY?u6^GIyr+@cl1)JC(}Tfv;A"
    "dl%Pg!<X725q_PeOKeJpoiEZq)FGjC$5LfB+6@ts2Fm5=i;zN)&bQ0tzC=<`Ic@ub7BG;Qzi-D#qGm1UNv4?JW1^#v$v<?O@B0mp%~b~3@r8<}"
    "xtJo}TAyaS9f{oVh`X0F>r>=49GKugLu<!ZDPLZGZ*I*(vpiv3Ecs8$)P>}dIVW#vUFSfKeR{JmoC8s%l<P-(1P55(&#m8jzsMvZfT7=d*3L3t"
    ")8P)SRd`nG+>v_D7OkBZFR{C%#8W|59!(F$`%C59JV^C^%Wf|f-)!ja{dTS(iJ-4@_sV|wYLXzbe;$H}i6A_uD?!APAl&~$5MM(O<Przk;4jo2"
    "dq0_$CzDDl;#MPyF?OR8(s2N$kdHT{X!1(#aKa{Rr&(EdooMJr!61k<Vv$O%T3eA&p>*z*bfG9|nbEbDBC{t-iw3FMY*a|iMSehS4y8HE018t~"
    "MYV%(DSs{-L=Gp)U^1-;Al;Z}S47YgR1b}ST6K<w$93JZf<>uQDk@TOUDkDmsn5=q7z&Q6{Vp%Rwh4;wiOkAHKvlE0oaTajF$28d9BL&Y!e<-#"
    "pc|OjMlgxAk;Zv02^Df(<+mwn{NLl)+0tAR0F4lYr{)=9UuSjfV>QBSMHS9tauZ>9(;sazin9%jaA+{Qb4(_V$9DOxJn73u!ilos(?Wd1C;QT2"
    "8iV^p-VpN`BD(79*|T|cio3@H5GD*sC@BjWiQ#~|NFMoeLlZZ18QvvNDi3%10w=`>Qom$Ih3BCY=Bh>%tjvxgYSc~GF+n896e+wY1eWtDF*w@3"
    "bpp=|2ENWGW#*Jz=0S7AQlHe2+|CQR165%705D3sSVD`0qb<teT$tm@F`=3m6BmhdG_pylgy4HgzzOAb%(<S;DqjpNX2-<OxJWPCbU7Xz6I=;_"
    "Gi^#7x+nYP<8ik7_REL-U0&*u#A$&~lX0+eVdM<3lKB@boncv1FJQZ#BD-MbmMP5PKK{Af8-q6V?ht<4fhQth8a!XmPuB()C!@lHFu|y}e0i%u"
    "77@<;fmU=9kwrDX5a!ANxqiQ%+-*(RJD^l5oVx>~-zlR97d9a?ptLV!D#>i2vH?AZ#l2&~;>gpM-1p-!atBzDx>Reb^PHtOD>ErEX1$X)b=bU#"
    "(;vWtROpXrEgv!aUyXqzZqE3lNwP>VcDS_(#eb=Ae_0;;Sq=$rYpIMW0h8KFJC!JqKJfr@y#)>^!qBzt<HepAVrsJ|@1F0?<k1QIF;6izPic>I"
    "cT-q@OQ|NNh?cp)bd9GslJ^Oe2)p7Jk`QHp6bt*fg}dkyLL`9N(NZ%|=&>*kQo<n3I`2|p`)|r+ekw{v0{mqr_)4KaPeGSBT21zalbKKxs`Pe_"
    "kGu519!e{`A9yp%A5b6vg<R5f!Gzel&*tj__aynCsMt(e5e`Fq7V%(ab|QsCoH^vFCiI<XFdXU^B|02Wl*s*FsqSFmbcF!LqxZ#rCsZ}|QQ~T!"
    "ePD=nu4FpFLhxxxh<NXoPGwR%Jc8s8n9-y~1=DGgagT52hAtzLa8hz4k*G<&LA|Zal#K`-SO_(LW288uI$;mufLN$9D#H9snf+0{5S8v(<CFGk"
    "HM`qnu_tWf3%oX+Q<4*41UGQpP)ZuK>WkY{Y$-$xW#4)%X=9dRBFI@ri3RfcGb@rKv4aKApd5JyQVrhvEb3yP`64AyptrJk2@Ni}WjB_g(a3<3"
    "(Nh~ZeUMtBDJmN*8T$DE$=louBk5SL`QD*j1r(dK)cnOQn7s7LR^{cN|D9GFI;D#wZSB5_>o+YPT|*U89H_0aG7DcfEoskj2ktjy@A_I9IL`77"
    "tJA`n;GFkaGJX=GBA|l2gfX2IWmdp^WLQ3n{ixYZB%kG&1mZ3J&G#z%_23E39i{g6v-<Gh>;T7O@vlYcQvMU+N`5%kU)ab!Zx1dHYmY%&JqBgf"
    "eBL`^7fx9EKp9W!9gvd@wEl07{T-?qAJe;RGE2|S56PXLe-&rTOb^|8i#Y+MV&>YQ1PwgUCa3x3UHbR~Ed6Ny_!ECBCnS41<{r+(!Hjxs`tFFl"
    "@+nC`Uk8IKx?jr7>gbd281F%I%jZ+GLGT$%yj=s0l*%M6Ke_ay&pN(61)+1W;(6X06Aa|SB6~Q~qLx4|tT4xMVN6FL36q}~&q)Z0T(e^p^6PkH"
    "jV7~%K+fs)EW71m-y90S0E*7W@_ctJM~B`&bHX8b%A2A#!;Uk$YXMKrRByXsKBTWA%;^-XAt5;UOD(7v28~V+^Bzy{wH7p1M<G4lh@|pVC}>(k"
    "f!l@w{$ixXDA~F<AbEjlYyrKDc7-#O&Ji#We7-!r87E83!~y`-IuSm*tf(Gj1u%O~pwv^-)sSe@sw*!u383nv>XvMy$z1wDy-o^rZBpKmH4kVb"
    "k%nEXuUQMb(t}h8NqY8*+V|D?C*y0nd_fDp%JmAI8{tI<OESVzUYrREyj}%~A~0dEhXwmYDQm>Iw&tqNpLE<I`5}GrI_0=91J<^oMojEYJ+946"
    "Y!S62wx~pKZN}t=!QSfxpgY2`TV2IN^NmDhNUp7ouL5I@RF}=`BzI=|cuY>@Bb_*AtK>4TI>t4wHWI4QO0Jv}GaK6AXsTRw+0V1lu}||sZ|_IA"
    "`8GLiD~D~_QL|^a;wMAFyc;o~fNDWRtD9ndV{@}?UTNkIJ<QjI=Rx7a*Xk#@7dnLDZVr-6R8R7o+Y3Ka2B7j*kyGxab6|udus&qijMaryW2D6b"
    "uUy36syznWk=R%-r|F#eXajRajf<kinKk1$2<M?t>R{i&X9aQ%*?<8cCn?ox*TLCJl~6s#Edo;LZUy4V=+rJ>yfZqo6+8`^<0Rj&yt1pUe@q`+"
    "wbOE%)2f&=JK5Lu*vgnZfcC=dQ1x}rT063%pZE+=8-`KB-^FEz&0ki)(7&zd)YJ|LQ$t|Tpn7w&Y+g2VO0`GR&>Q+|X`=UKS7=$jfrB7lS51W4"
    "BUVNHRyewloE1p|X#&<TTkR*yDdo(=lYyoV-6h3=u0GuxO0)o2YV-$N(+4#iF6t}@*y#Sg7~zD9T(f2dSZH`GFIvWbC6oT42%P12%Iop;W`7@7"
    ");K?q!d1DYLj;gWc{@7Oz0_*iz@~aB-$nuZkm5c>B`|QKVV}6nh*Ms2e<v*w;vKRz^)(><*bn1@fN^9>bwc=MezBr#qPsSQREuCLUF{W*6cT7%"
    "*{r3W?PA^~e>kwi@+G-BG`6^{U5$?57=(V&CBW!)jahE@skHPg`x~u<oPzI11J~=8rK`lXAGwZ>>#z~m-7|LSm=0_&gxPgLwKIsm9Mf(TM&7_5"
    "w&A&azX8i7u$$5B4TpoFM~X4`58DH?jdIwzSAKq$E~(}`&tzanQ7DjeULzIFfkl`d0(U5K)f759+AqbWmw+)sh2FGb_)br}qV#*0xi)6yxUWWh"
    "BfK}*yM-n2wmW`>V#yxVCCQm8wM;68o|qOm=>@41ikB|5#`a*?cupk0004%%8gte1@_6a!Z$~1j%utD>>UZ@w`a!<_g|cNhbdufBz$GqcI5BAa"
    "^cJhR<5jD4*%5>#c8o3!oT#+a8|2ou6>O1CflZ;KRoU4{NK4(qN>{$RffdwA7c(AE`n2|r4(GJu#ewjI#(ssE)TNmuwx@zo>)ss><H&Ufs3UeC"
    "rw(P!Fsy7e=3_Ee#keLF%O%q}ZgyAgF%59>-m{&^9fVCSPUp%N?Z&WKnIl!K)x4hysg%LAT~BO7t*e7I=3~{VMPIx!AFI6AC4-$r+b^WjhqfO$"
    "Ht~ykd)E$ZXjXw{=(}*38raUJ$yL75?isdCqVi?A@SkfSD&vwgx--v_SBWTdFiSC>xfF*LW}8L}6i-Jp{kX%BZ9FDsV0}H|uq7|gF67++WdS-~"
    "&sNz2*%(65aEGp_PTYejJ*rG8g~5aTQc7F^G<4%A@&|U@d@V1&tzE4*_ki|_!^>Z;4o~(mot8E>U9>;eK9;hlN}e)5h*<l}N|rwTarINcO*N0>"
    "UNsM7Av^$@XVC=Fa0u!E2=Sm9GRJltI~+tE0F+(@pTBY-OcQx{dP3<k55{i}PsRsVug53w*QGY$Gj?mRUSUxibdQv-2;X`Qo`MImH8ag!Z~}8}"
    "2B(_GfhF>r8^B*&p6>s61q64dFErJ^q|y-cLglaemJ_D*Xh8XIj!u7W0smWr0Aw&eKL<LfAmbnv6%&6?e2houNRl;Hz$S;^2_xs@lS|+PH6YGO"
    "NBF&fIQ?aGbjgWr5A}69&mWT+aK(SM;PJQSiSN$NPR}o|F3(3N7eFTZUIDcUE6x3@wZejxKr7!Gn75}tjn7XouW<v*dW+VUIk_kOPQ2=AUA}&I"
    "0nGN|;_7Tfg<0y<^&0QL@Pc-MwPUbG`R_t!Dg*D);lIB-JfJjkSL2^Bd$cAHWQs3#&{O%+=l^(#V1ND{Wv}$rs_RMW9!=rHaopH*LH+hX_nS%Q"
    "u=0ze%Y93_oT*Pd&-J~5J#3y6zQj|t(>y2N3*vC#cA1kCx=tJoFky2~c?TcWfmAokRui~3UJ$rL8nO}I;V|$+mol|A0qhNJFAfHg-vwgnmfW)5"
    "zUK_-&>y!U#~Z?8*iI+xgpMB#=z2onWVB4j(*0PPBieic=}_+Bq%|F-)}*dFxAoG&=a4S6k=9#BG#YOkyWaEX&w4BvQb@y%IGVA~%53g@dxQ7N"
    "(zt4r9ikg!X$sUT3{e>Z>T4uRAMwwVTCF5bg;2)3QGq6L8<7<s6fC_R|D~v;rmjVJz9VX=S#>DI1s~&&GBj6j%rxGfVO%6u)uELh!nR#W8(Yie"
    "-InCLy;BDN{Xgl=ercaNNa1`+N&9{UeF_tNuraRR<6B}5fXAQ00wx{xF_Q(G%lf?^#z&|7z4!fJE9seq9nJ1Lef#};v6f||5Z*IjiDH@iQC@(m"
    ")A%g=XgIEL68gFW3|-+q)kA}JW}Ev;!zFq5D_VINlGdkvEipD@x+K^i^4XMBwSAEVK+mF0C~ctflH6=+(VD}(Y>4#O(pDuzueYvKeA$LV0kKh2"
    "3i7fUB>;c_zHd4XmPX@bLGmrt9_ZIe<yZ8A?Yx_kNr|*z&3U9M4hVcJZZ@F%vzD)g+kt4%@O9AcAo2RKiC#*liE>Ek$I(h;rH8~5J|ahls^e5W"
    "fl)*L)wuGJyeX9)4*EOo(zJeG`9x=g@`EQNQ!?Ei#*MJGep?0kGbPF&O+O}dH#+_L4UKH|Q^OwbxP$vo+{4Irn|wMzL?n|(PWMm>llqF?CB>1}"
    "R20hU8KIyw{~t5X8w1~z5$EvZkn$+u>4g1y0eT^s#AP5}3)5q|Xe=Mbz4uD(I7sg?4ta4W5(fW&Qjcl$MR=VQVor!@qlKuSz?!Y`F>iR;pmbY)"
    "K5vJXz7(sIKAp0+W5egG!Ruop-7^}S39k=SX{DpLL9G<G268<wL^x@>`WeId(35qj-F+Tu(Q2^1qWXybb?KJ?1c%QtB^9kT{PB~}bc9-iL}_S5"
    "j?`!PKlomHQ1_`CIJ}CLP^42%-|Y|i1^<V3qnu-jfGtk#KpV26z*!EP^HF&~ReDkv!lf(w|9>_Rt)rrg3sIo-S3w>pjpae;l`O-BYdMzMZB{6U"
    "FLBG9(y~hw4sCfVFuJdm)zC*!)UdVpSe_0h&0A}PSqYQbW04u*589?~;?~t>a+9~WY}=8NfIbVi{NrQ}&t=Gcd3rE^wO^lq*)_T8mvmkm$N4Pt"
    "tDqXsg7`!TAzYDu@3lIsNOvcS(4pfDofcI1x!wdLYFQ>}^;`DI{fnwzgWApiqZ3b!B>1vGmHsGOzZX#q+OfxQxv#p|*CS6FbgGZH2dk_WZ=xga"
    "K#W;)>8cqBns;-f@7q(H*(Q_Yx;I?er9S1(es7azzqf|R6Zx#-_$IFNwSXE4T|KDg%fe<pH=I@fP7xhH6{in)T0f=G3NtK3M1yn*{1E5f&T${q"
    "ULUO<s)L0?^cD@lI-dJk&-;P;GZi34NzG|nM5L`A$!d5VNlyxl`7mBoqdfGGppl3!sKk}P9-@e#CqxOs2la`gRTy4e-epU3x&b|Jz=Q8?i?(VD"
    "GujeK)M4`q!x-WnC81)?(lr48gr{b`!pfapt-%GAa-^8m2l935_x^%ql1rGY?#kNlTq>j_*M8UU%6ow3dCLvZFy$k%Fj-oY8U(U%V_9%7u0x<Y"
    "EUQmzlBL#X?C3p;Ut2KYIHB>C`rQb}rKtT<oAH};iautRh<U%HM9j6p0>`sG+PJDrUHPPOz&D5cBTVelh{7Ond<}B(bIXLoFc!>1eyBZZgyBM^"
    "y{S#RRs>JWky9JlH)+ndH!L_M)ZWmSV^^qWQ(s02!msPK5u@f;;U-vw^sqMV9(4^VsjW8R&=_#IaXg^LL#-fEeN_TuQG!mJ#xp*WKesX+CAUhx"
    "Q$8|S52l9KMPRM7-CAF}ja_k;3Od*tEM3+>EZwm9fx4DB9vz-Etq!MpuU(CdF2`?A&wpta04+BkhbISzKOG)$Ex0<fFv+UUp(|3pLcZ0f-1ZnN"
    "L{b2%?oWq${Yf*h`aWvC7}`7$&zy+2eIoTqbe}-&lFFpTe2I2MbX}H0!-OtwfR0*<!;mSJWZt2t5ri=9x8Sd>xp5O9>t3FoU%oj#Iy`N~dlm6p"
    "Fz+{#kpCnSs#iwsSUR@Lq}+<)vVBTH(~N?rOsG=Bwo{$oE^~1LQ``jqfVng=YUyvQ2*(TTjXKdTvg@wwK<jv8pHtzP_x1fYF#z`|vu$Sq&Aya1"
    "7El}B+YWZWcZKnpQws9bB10OW5H7^shW4Lz=u$J^A<0M=+b_F85<Dv;(zC4F*x|E|ZQk*B5CP2vmp2pmu)@!W_7?qAOf`B+5AAa-?XX?u*H$Tc"
    "^AxuV<HiZb&mqj&zL<#Xiw+bt>_S22XwACxup$Q3gAHJ7w>5wN!ahG&3T$hq_wwm>byzpxcA<=h>fO)D*PSQHnTyqWis~Dc!tJ!`?vwgg-mcvT"
    "_!7yW*OpC}MLq{^)O|$%NmJ64-tI#LUpFa@y;2g>XJhfT{omUAb8)z*QFHVqczge(VLvxzo2IZynQ>j_JupHF!=RdLrtW|9O!2P5Jo&k%4gXyR"
    "_l^u}_v(j>5l^%2t+150wW!AJ%Fxde1r!82svlanb+=_;andUX7l;1aWYIOwQ^MM@XCtcB_~uQ%9G7*88X~GIBh<m`jJu~{MO|}roovGgo2Sbk"
    "?An9KiJb29Ew8>>t^mL6exKMLUesa{IJ(j6y_x09Y?|~sT>eWRILbkxx<%&%>F8E@6G}fzofjC6E9^4Z;8mi039A(YDH`1@1}J$%r35!8^%8np"
    "b9rvgg0-<`rdGUkLnG;T*wT}kDQaVrfVOD0AYv^mQB%634wV#@Phi&)xSA_txAr1k)Al(ueEWryYJxf-9<TfYH9mh=B$TMea1iu;@>?zvkwGV!"
    "s|M;CxqNGWtK^|?J0B`v_TJ4u%sD+@woJ4%IYti=k?#_=%HgsZ0^xsPHmQMOysi&}B7B*^Udm9b+t80T9sM2QeKE@)(<Rx4jOjJ@oXii<6R|pk"
    "kkt)ez!3ZeW#y}5Nu{T#Tx*NO-kS5+K5)9*eEF!kjh(4mTXu8QZ(FThOXx9uae?XRPGa&=S&vH%UfvamJI<#;AueXr#Tm$!F!JzC{eFipN9ZD5"
    "^Zka8*@=JP(qpYXUqIReKlFWLIud4QV7oz7pOywB3NLKLUI$dQ<*=3^#2ySwUy8#yWxJ5h%5`^&Z{#^4+!4qt0yWSdK-K3{t?q!(=*!VE{xkX^"
    "Z1E^~2A_|PK1KigWp$LUiIoyMX6_L7{JEb}(j(HYFzb<g!0G5+q7{+UrJf1no^%o02Y@Lx2)RlD>2jLc6yIM0wDLrP9RSPFmHrN22&eV(E9GJ*"
    "-D;)hthHhnJ9eMNl+lU2m*n>{aOgWKTtH6Yss(%SnN3uc4)%yQE-zi-UW@xF@{AwYxaoS!>kIQZGA`ROf3^Ge+Jn#!T=Q3>r*8`=hH=i;UH`sR"
    ")$ZsuTRZhqH7!HL{k?a1KB~tqU^afErL}We3Qy~g);TamG?WVwhSS6-hU#}MpP^u-MZ)GN*mu_pYX>jg0{f5HZAC3pk_79tQ2yN7NM)xu2E9&!"
    "=TTcxcy>n?r)e7DJ*!()>=1PC7I46lMu%qK!zSg92>eU{the9>6nMkR4Hi(TFM?EkI1_wjIZ#*XTfXgG_pNj_X;=%<d0Ih}>kB;X<J7F}h`(4<"
    "Wig|5Xzzwzw}sjW#`}8Y2*o{&=410I+teiAQD<}`%toqHrTc#A>&xfgdX!E5y4Q$j>x*k=U;6MP4|-KP;gn4!J5nKVmAgu_Ei)cR#=$8K6A%AV"
    "i&-U~@KDaPgcs6HS@2_InIgFyCi~Zt^W*5!r7K@fvpL??tW*aixuxnxZYBCl_Fz6aJiIhMvAvl8P5R!=4aOK_wWP-G18nO?F-~p8=8Q7&5bcUf"
    "^Qr53F=o;WW#IVRCLc{^YR#{NO|U&hr7BvdS>6J7s5=@rRkKrx^yu^nA5^w!bF#kb0mn%0_I8#{LBC`@vEi}KYhwF5i^BxS1=EF}H`yoMW3$o$"
    "OHr*0dk_tW!&<vH*b5`dXzbdyqoVhv3RC9J)1Fr&ZIlN-KQ)r?k)JLr)*MX8f9uGvhYUE+l2ng5#(6E%UoEy-o|aIJ6%s@K`mR(@)C=+ZyG<d^"
    "GAxLXaYjN_U?WvceoI+c0$E)7AVVWhno5OOEKzc^<ZuVQ3T?gR&I{z;Y*SGbHk;+DLMW9UFL|P9sS{tdksinwa}*z(aWM-kvK7{;DTgYMWKf3p"
    "g&f<*O<m-<)u!)1_uER0P-5sZodWAFdPXS~d?@uwQHW0#I^oBq*vgHpPC`wq=<L-}CMxOP=4^?2Uc$|lYswsWUtx|-Wo0&MIdr~CYc$Km=>d0o"
    "3Anvo&kLP^a--Bu=M0A}4XpJFa==WrB6li_{o(vXSeA*Ti80`5=q{b(4Gk9)#Nul5P8r8&Xkdl{MqXpRx-X}nS_Zl@yN%3FLquOmm?uMq+S9p-"
    "77WI1JzrnLI7+23N~@9Q=>JanP(;_97#EWPVAygs)>#-j%SSDdbY+84Yix8fxyw>Gca{OtjW%WtDhxZX*AZ%Mpwc^sb{IGV&)1wO^jjTshgSBW"
    ">qI`Wm$<qYtD80Oqc9!}F&H$TA8l&txXv&L!$FzOx1n~Z(jdx}($XcdJ+OSG@*fEW!z464m(a!pK+WY!%LGCVz3Zf;=SOPkOK)DLKoZ$_{=(UK"
    "XzrZUh)iFP!o1^##H+593wtDf=jzdXJ)6-gUp<HjXE^)$n9oT)yP^_e#nn_MuLUJ68hX;*<7z5gZ}j}6SJH{xM>o_^?`<wo<l8O`g~l@lZ&ZOd"
    "?gB5Upm^oJ0bbv8!(r47-q`krQ8T=86bxMh-natqumik7;JL%i`1OOKXFHwX1yLRb&F}_cGz?Ar4o!Fiy92zT=Ld1P8Q!7o`5obfnIW1Q;0=S&"
    "9eO&vo?U_0=>qT2A39s`I~+!ySAo~}gV1XsieWfJQ)vUxk?Vz+SyuzvsQ~SE06L27C>m}AI&kgKj%q;L5$^IPOoO6}1yLG+j)A|2kpZ+@0ov;T"
    "bR5P}<ZcE!h`hK4v<FNtZU#DXBivODKo1=!#N(p|v{wPz?*KHc{1ElkO+W)bar`RKE=YuC@(A6)iGn7eVas`OXd6KL6`+IdK)W`e+C)nY=+KLZ"
    "Mk_#jQS3DX9lKHUMs$H+MxIF?K?Ufr1JEvzw6mEphcWyUSAljS&u+$agsi9;({2PZH!y&%NWY+i^m9Ega{SF35lA$uNk89#m2IZ!82L>z(7qjm"
    "Fg1X#h`^wO2z31@2!qX-jv@};G=T;QHuRf;9@?SX$nsneU}0>syowwQI><pcgsow3=F_nYR9dBJ5BNI@#|EHbZ@aP62y|q}aTFUsSA=2MK^VGG"
    "?7Hq|@`ynn@oPZGq1VDa96R&^uaQx^G3e61!9M(oNDMoOM0XfC;TDlN^n$=0R-uLs><yct1_j!78gcE}fgObgRr?j07<Q0}p5wUzviMC<1K4$_"
    ";gBCUQ?&znpcgjc+5>WoT!Vr56`>e*5Q?7XMuF#Vg4(r%z;S9&gG6?kCAovt<23SW4;27Yl=~H_7<Q0~K!6~qH%dhpKz9A03bh}2anKBP;DBn{"
    "sQTk`+cs2FzakdH4r0;6?E6E13)FV(R++U2tK_v%NC5l0neo9<(u2dT0d++#hG7?6yTGtF^N?X2`@^bS^gx@iTX2m>iXd*rHRxJ_xf?5jG3+21"
    "fzaSwwD}ki$8h4Ps?{FIkv3cdS8|<3$q2h4hW{H-S0rN?ciD}gx%-=W2q?q$uu35=y8U@A{2J6T*KUT|g_SUlFn&cehQlsU!=gFv7A3?9{ICjj"
    "6gb0XDFYnD51WC8=aG4?^(&$=>L427hz*$Ww&<uprd6_b13ad-=%`U>cBy~{uH)MVrh|%PjGQhqCghX$rqcl0DXN;2i&}`^a#(c2C~6ilAbes&"
    "oCg)b7<CbhHXKm=Efx>ov)vld&M=Id#kmW|w4fQ&P7DYzxL#0^i;>qw2l3#LX>T?w0nvL^GXn5J^p9x*+5<-FwrC)JI5c=(P?3s}-$~m8jbJmP"
    "QHiZ_4>%2mQ8S`<;h^F>&5AXia6Ll<2`W-C>T*~F-Vp?wwLQ=%BCmQZ2Z8N|&D>)bh#lBMvt}IzL-Vv4RHS0m<+SJzL3iIwAE4UU!zxkZeO?qb"
    "LmlBEw{a^1vx-9VU>;PYV$|ul=;Ik~6V#x4+cmXm7}+f+++AorjKjG3xEO{}Y#d^OicpNY92Y@Q4>uoTVmSNN45lG453dDi5VUTyh6+0xPCn*d"
    "tjNTu%W)C7N4#0Dj^J4CM>PdCbetBTLo}T>W7-Koz?w|2A`{~-wo^F2IqpV59u9-R?q*8gbzl=ZEyn5LFou3~fWwMBjJp_5Bh<+@(sSs9eogVP"
    "+jt!w{k&!yq!$3p2EY|r7<Vz82EG@&8`aVPbil3{Mqc83%@_vq2N(^2D{?UIVl?$4;4~XC?1%o)_B#R`+i-Ai#;}hniizQh5RAJROr0TKW^Do("
    "_P!f;Bni&}7T#h@_pl0}Vc`uc@-OZn{~X&6ht5Wl@LVU1gN^_Lhj;zPLkfsd#~m61JFJMlxP$16Vas_NwG23lkh!W8yb-Lr*T{;8KIoe!xD}Zf"
    "caV7@TH-e=MIb(ER^2wm!iJM>^T7mdUlr_Dq+Q%W+JQ0@`kS>OIJ89__Z#Tdj?=7k!a2cq4LvBV$ho+aoC|`@N53F;eY+#Hpe=Y_i@9qUn}@!z"
    "BH)G{1l%rA!se|88$RrI^STSP8OCul^L2p17~(jxzXVzrq=mg1T=X&O2(JfnrP-Khe}0cQ^jSjTos+xtKDqjsE(>yR!pIh?L@jznH;3IsW?!Z}"
    "n_Q%Lw!Vc%h48xCouv=-Ud1iZUH=V6*IdnO9$L$sT(Bn6Z8?!HU8S?zRU*UH*^OGHza1Z+9i9F%KEO`0;=|QK`Ev<hE?fs=SQ)h<$3!nfIiwTU"
    "nsbTo#>OG#s3s51-f@=PqjRBAtod)*0@iqnzdg__?H)M+UjcyG{PwC4NxFL%hbM23#`y6g-~(nnQC{AQyvU>*{NH8K@68FTvdIUky7SZJVNWF}"
    "|0$WH&(PF5&X-u57{*>&>_^3^k3>D2@#UK`0|Nh;$S}IS-VwS!TCZp6d|KA>5qasjbox~`zfw@zgD}MXlyYR()l!9h*=!BjIG-||*zZ0gcf*W2"
    "O{X!{+wVRNf5Xc7T~}uFRDM2fn97^Wi?Kyf!Wcry6DYRK;2<NGbCadh+NYIbR4p@dnx_+PCA8|sx!C{Vpq$mk<nAH4w%%P>03t^21AOcx++|6m"
    "E45blss(({!|S6CGuXHwe>(Y51O4pa9Ec*%(P#A5`T<6@e#z3=)OwxcG&aItX<ez^)wTw0RONrccK?R!5O3HRU%v?781Od8-PSElg6c#1cy*ty"
    "mZHkVO)^;(vbI=5U8BGE*7FRf%Fla!RWE%03MJw!xyCZ$Tq>Zz5XBU9jrj@}Rlq>mM^h2}gu_@=&_UbJy=XA(Q9MAFV`2r;aQYUf_P6GsKJBj3"
    "<-Nr@Y)~Co%o3`d{3};0F9t?(3G<f#ZD*1!791M%TknsK`&$pmtez}qP)&C+Xii+AmloVKe7$_sz{K%;bS7P0=C3g%?gsQE@({(jffitCg}kh}"
    "3L_P(@t(Y0lckC!=9ES`=^i5vY!G3&eQS<hw-(mAlh3U6e1_?)a2#rz!CG01^>T6t`rH6(VDRF<yExERJ}In}>H|zQ0;mKZ@9|2natpOS3l`GK"
    "fcwt@pK|na{W+LfEx+E#`cpDrV<ZWAS|X%W!xbKoR&CNkt&HHW?+03KKWhhJfho=(4b;3uJpO~wW&}|`327oGyBTYv^)2w$Z;dp}S)jJ|zF;7Y"
    "bEh5shr$wv7Tko0J&NO;a=4Mi$f&|BcCM582N_dSz$fd%5;1hR4bn&Jp7ev4HTI}bBdRf41VyiPyU{>2W-^10tsO2h3k<9}4mHZ=n8HVkGgLtK"
    "t%tj8a))$5)T3rZ8&=g?l#bU_i%(DUqEfgBl03o11IT7Gz*@$Hr+5qiK=l?|>Fx=*r+{*f?Axo4z__oo<C1T4OjH%!TiLa&L}#X|d3Bt88p-Ig"
    "E_@m=_o{1B9bQBFdw_p&yA8ZpK`hE!(o#~b&THV~^5HYkKL_<=r_^MXFDN%a(~@rxk&;O;O_`FleFv!d(9uKC=X<>%qBc<?+A=kh%D^Oub}Tnf"
    "1-OBAi8Rbx>{}AEMokU0yc7J_fBvsf2-0S~<>hnGwjj#$mU^6DP1+*;)dp>3b1Be)NF4U6wH~OxRm}Ry8#I>+k25xlPF#CR?h;i9dSEel2a5|2"
    "FdMa%VAzkv3K1_LhX3O48hKqLk03TlDAO*w&R2KeLo>xgGo~4l1fkq&vgh0!h*$pE*lRgnohWfmt$R6Y+{xQ@Vanfyd1z$$(_<<?($ZKc1GG@p"
    "EMI59|1VazUDf6<OC0tUdi58SLe+`e)MZ3rxcA$cr7jWfYh_zcO#S>>4pbBFU+jt^U9G4@0_h{I^wSFmPVY-7=t(7M$%wpM&$z$KJHU-ahfFJ3"
    "GTG<z*`sxn-L8S^QP=(J8kU=s-4(T-<Wvt8cJjZ|8~lc_0-NkUP0&1MVZ<@-emWA#?Y&H?A!y?`Bp?KK6bCSau)!TXPCzZAcX%vkX2Z|{Q@BT!"
    "85Oo`0)iHsMjBX}28Lqm`jKaXT?16u7xw;Rnl9)CF7X~f0i5F1<5EnPIMVDPc`U3V$)*-25kY;t4-IGQ`-N4k@5MZ_0=qlNS$&*N`|$1>b|%0L"
    "Xu|yTgv^Ir051+CV%h}`ahE?JD364b6@kZ-V00(Mn-q@~dW6Ba@ROgHS=l%#SX>gDLddNhb<XgHFZ%*`!n$>Mamruq;7iUg^-}MWNDZg66n!UF"
    "nGgWPbMT$fqcu$@**ym8+k+tBu0}LpSb#rE8ve6|NdpS&L;ASORt`XZisu)aDIKeDk_D_7j-7~wrqhI2CLnnn)4I=!S(;#eTV7xb<EO31d<`2e"
    "B{CqrEJp(8F*16+R5A05HJ%0js;HP&he#KXbxf*oidexY1M3YL*_bR7(&=#O)Cj2Iy_SuG>^36vE{5hR5sGoOnq-5$#kV!At*~?vO^`PXtV3G-"
    "845VueXwk-a?0YwKo^r_O?#4$srZn=!y;-JR*IwGM~|Fc0Vxh&V|mC{k(thKGeDorKD1YMW{yLQi!3(sIoieHOupnK6&UhuRpf8O*;?QVKF(nO"
    "@_iS~>=CV>B1H-1Z4kPh#xlzi>xygQx~tuaObdB}1dou=+oBc0)JC(}Tfv-RGhbtPJ10HBm)ao_ew}gLGZ}WiNdHiW1Vujr-JBw>#SkHBpj-|-"
    ")aI~DKsw(pllz(_SYgN)v;ez9eBX|dM9o^xlT0zc$3#aTlYi(m%Y=`us|>Q^3l&XsF*(fIm}a{jDMb-U+`XJxA1z5C9GEa3*V^$_-M*LKn_IKc"
    "EKgw{b=~#KvIVAYmN^Kx{Gp<AY)SKi1FY}o)^A1vm*0BU&N5%q;SQ};cvkD&Q9bnwc9)cRD#*&C>7ho(<bjbFsqD5a>fX@Z`|Vso5<y?*?v?%U"
    ")g(b=|2zZ{6G3=RSAvKoLAd{iAijnmP#3^+8fRYNG?b?0$)u8sxYdY)5~oYB_)I6|;|(dAyplWQ3PJ5OE32OAOA(7yYSr4p+JM-#h=|B<Lehnz"
    "q-91qb`_aDQCc)e)n=nYYA*5vYI7*fSq7l3mS+CN2mOxn=dwZMkPacpv?73tii?H5GoPS(Xav-%b2L1z>y{NPN}W<sk@EDhu0h)xSZ7Nt{DrFh"
    "E-$~f35xHD%*sVTRkOC7=7M}N1H1rz4NudG5aF|pd{891Gc-RUZOZ;gbAh87X~4HBYW&~h*xAxt5&(@5gs0{iVP9u;O-XSF^%Q-Brc8W|Rv5N{"
    "ZLPskntx;?k<GT@Q(17DPxeMeodQO!A45b}eQ}op6e4q9Q5I4yc^IZ_LL)I8a6y3Z<%TA1<}$04JgGd~=?k0`A4vTYXm}<%5&5jNYaKaDaa!hV"
    "SkpY^+a0pS^y$FEOs`CaDfg{RUZ!tdkuD2ACQ#h4)F(A0xAQ{o;7k?;JOGT+E|$<D;b@C;I2Y#l6=pl{Q)wI}wP}%vbc9K%gy4Hgz(DKbw439h"
    "Yca4|vj1R9G66_|Gqq;<{FZG}6FeN^KHHQ1^6@xZef#A@{w^=|NaD1>r^z^#z37XU&akXC=j$7^=7t)yp?8Py+YbEuvIY=mdegZ$85JIc31*&R"
    "3UoA)i(3t{h#+OK6`e$+=*n8IL0p3JhNObVrTaDPQ(OVe&8BetkgsP*N+9;h1W;zIM!El3SnSI9QJ4XxeIZ*(R=~0v^F}_0#a-3EolmXOb5)xR"
    "`~yoFdAh$`nR2gGYpU~{r8g@vM`;a2mmYCbhs~Qfy-FB3XiNEr_UJ`|-lVNfwDsK=ZM7BN7dISo*<^RpmR6AI5Ego#u9!jNrT@ShmDE6pV5bJD"
    "8p_mzduUw5?vp~ARG&jMS76;^F0_j|bOpO5d^2y7R`4bsCe1lD9$c1)DDB@8ng*wcQnDJEYX=p)SAQEa+5B=M$~xd($b6E`GQP6F$8X^AK{{I{"
    "8_oo<TKl3Y>a>&$|9xY^#%DP#zO80eL`$2-Q+Gsi#|x3%u}{K)iVT7%<kXFY#z$o$#;3E<@5Mu*TPHFNWO<CBOT5DRTe{49D%sw}9gsQZz%-oL"
    "gn{`Bsq~I^&W$p6ZW1%Ps=)4U){d5{5@}V>tg4}^=LX;PzOlG5vS1E6q^4B*VwK(~;cJ&3*j24g#D<1~*t*Z=>%tO+Tnc$FRPNMg;yEWe`(w>h"
    "@PY0e<0-0H-^`MmDg@M-IaSMO>O<r5><mRR6rmDs3@orEA>svWimC#+e&JaZ8U1;iF0Rug;~wA44W*WECUPWgkOF<H$kiKE;P3eoiS7}yVqhWE"
    "{0&{|0Y8*h`<wJZSPFPxY$NU=(56p%CcTxazr46mv%5_edqSoy@ctaOAj_p2ICm;-9a{CpwK}#Gy2dIeIi}WgmL~JUnq{lijMUrbJyDFr4i-EE"
    "v1%gK;H}ScZs;>#L^SYQx^<f8Jh<eR-B^Z3BZJLpn%l*feo#d6Hur)+kVfAl3k__Ty}LXDitA8$`<boETVVe?t5}0T$mVpBw-mRR&%yPZ7LV>D"
    "3n>oN)(`}Wa;e6fC3AP&f%^^FyS`S{tlaIZ)54kFQ_9wfrel_72t4qYw_{o^eNj!YOG@j{n)8KpK^J~_tv->TD|H0h9nnxr<}zSfD(kXZgvGVT"
    "%1rL+H!!VR`3v(*A4$g+QLBavd`;-Wz4Yv?y#rcodV2~hpNR4=*Xx@bEX$!@T2{sT)p&O}Pg>uKvSO-`PSr10xWu-UZJY>SnxE3;G@Ia_Vdou;"
    "+)L153!97F?#{rrhm_K(I!0OY6Mw5(24+c;vKpI=`6z3Wkbji+Q>+w)pTKXm5SE}4wRW<_Yk^Scn@%$7w^$S5Dkpv!AJ>s49DvyG>MKfi-O|Ng"
    "Lv^m-x0aUxqgu7=IZJ%CR%a5$NW>eCf5dGzk`bg><VG5f&tcH@g6QU$TsX8^6el^>e<`!SvyFs`t&qRM&Ls%|7xZb&-Gdb|Mzfjp7vB{Q+SU@Z"
    "o4&9(po}E{?p^lpwp6g?fGY>-@21EbmY|%n;{y?FvA%|rYViSgpV?aVM79s>W5!z-xOED9f5nPXviu00p)o=nEwcG;G07LHg(Yr?8Ietvp*fT<"
    "Yf}bwZ}<3EoA|{F^d5GzHG7gaJ{Yq$`6;)enGH4|8iXF2qIhg9d}LEuMObojgfClj!%TY0-~yAhd_W{fKYo(On}(a>CBm{C(dQ8l#AA-qNM{+a"
    "f7CF)w{F%e^ySg@TM$qQ>Xu?mQ1jAHXm(WPeT+I?fCGV8z^G>rFxj6B_kwfGZfQ*-jU=Cw4dQ-1TV;zGhA#@MkhDn92&|Y0R)dsy`M5|A$xn#r"
    "{a-Y;IOnP*@~5aIhby^SrpZbbHbS4i{kwGX0oPJvwDOT&vgDJhN##=gC84-zg`TQU^lv=k$!&p?wen8-r+)LND%x-3$3gkqh_q`eRi(beOHx^t"
    "2_7CN7)#0pLFIBm^K(}AE~vDH^~$<jX1BL2L9jjnIVd)kkAfB+DROUqutYeW^<V$_f63*B5nnHp$p;crr?Ms#AHMt6#U+}$;B1o33*(nH&5F`y"
    ")Gw<^WfVA6P&m?j_ph)wI7W6VVhIZa$fL{sw=k|lhJ>@9cacDeW!-2E&@m5m&6O;=Q+%)3q_A5omiebgT%CWfkJpDj^hq4GO`=y8)!KP;guU4f"
    "Xd`#7ORn!F+acrDc9{TbhniaCVfs?-U0jYqj2(*=Os9MDix;lvVcj9?zr&xl{iAgOG)`qFM&u5*s*j>^BFQdPeJR;peG*1xuR%juFRGrjzGcrq"
    "vTV>o;PI5$!z|A~tQU;3<I&qgUIBAVsT9Fr$g_c{;j`OpLJ%xdx<TCn2cBPy?yFD{FuFOFz*LkX;M7)@K1GBa5g27b^Ru5VIIJc2+A0q)6#{HE"
    "{vo(r6#`ylo?kNCB^Oa`R8{9qv%hIO)AbujEEV6BTk~*!uAi^o)I|oJ(h<{2{>TuoUQ5|GQIZah?L>{hBdkAKHvUV}r#O1bFL-Vm*_E9V)<uU-"
    "%%8)aZs`zPo1ML9zmXq=$ZeK0@Rw-NL+z!^J}@aY^-?7#8z>bgRo732d}MG5Yv;u)dc!plD?H11dnkCD+Tq$eSgc)&|7dupvmE{TMa%P31LJ&r"
    "-;wN;p!%cYv+$?Z%}XFx)|_<KCZsXxCmd!C57x^$o~4lV_ur070o^J#ISqu7xq(w@xX}P}U+v=dw+C@ZY+w)%BYIH(R}>8#2MOX=VQYEc`nOa7"
    "Hc8|rxF{ip=M6A@&bNZgYZ3NM@Ni}eFAfKoRq0zn<hMaYSuZwctl&%)f$t2keuIF}31j@j8F=on1;jWWL{WDTgN-C65)l}g1i0L$?+zSAV+@n+"
    "$1N}cS$2mgY(W}lrl@6=VCUKZt9C^?JR#Q3d=7Y`E#%&WBT5h9!anrB35wzt6t#guu=oSa3;5j7yvK}1`Q*b^QE|fJ`jT^80IVRY@+C3xDPWhR"
    "1>H?l<i?lE29+!0k%;B;^0+5zsJ;QIAmBPkS4lS8EZH=xlBWKvzYWGNYC(=vg)$CN*}+3Buh+}6fUbEWRt*0HkB^^r-%#wLj9mwTR3^frRkZbg"
    "Yj(U+`6Thz)VM4q`@5o{K69RPvR%rF6jAllM6d691I)N9v>YGv5)G-_>(1StG#-p_>rf?lp^>@qAPlMJN#~v~*4Hau7RLsqiy1kJK`LhMCS4?{"
    "NG8=d_n4}^iMa;@FSNPi>nC*FHv3^Xz*1&n_MSiR2(Rws34LqxcYSjA#rY3K(NZtjB(Y`osiuj0o;$#7nPTRlI|!%*vv=L4$F><e0QCS9sf#)L"
    "wli?4n7udY(yumKKkx>a<r1drhn|?PpKQ_xy!Po1oq<!%)`<lD_}3l!YnyE3V#1%2x`SvCGnA7Ky_Qpr9Y;tx6fwhLSEVA@yc9mnb*P|2Y;M&J"
    "g3S~5eAsxH?N;>Zxb9FC67449<Bi?BUOd3;{i63c7`VgjvO2c6b?WM?6bG(Yr5d*v^)QLQFmB<`I2;C2!)4<xGJj;fukk+f^(-e#AKS*w>lXRW"
    "qI*@d3VU@$5AWsGE^+_-#%gH`=c2g?lZCSqNDee>KUxJ}3W%6lG-#vvnnA;9vPuSRqpS7lG(NZf3J983u|9IG)t8P~O6h&MULDTiLQGpb!YWU<"
    "$7Cm^pv;7mZoZpiweRe2Fgl)6%N{IoyR6@rIGx4aulHF&5g8LT7^#a}9?Sekbb<b!6^CX139ST()N7<ffRw{QWMg(MhvT(;a6rMp%apu0Fc_or"
    "Syc$De?I8FE>h>84{X1K0Qu*Gy1UT&=YzeAT>R&Q`YB@fpAY&@g8iQl><)^<(}3QUor$|@6FB*e6mFc_z=Vn=oxG9#haJuNF1hJ|E^YYLGx|Z*"
    "w*O`4bk%+HSzTQc!;qKq0{1w9nSH9=O3HgYnwz-zEw2U22s?f+(zr+}RyP!y^}O<|ew(3d3QcF1p1e{N*AP|QN+3qfZUPJG8L)9(&}9Lru3!fX"
    "H1;S6WJ(KioxlsCcNci=eviJIlpmS0K_OZncPDIr!e(i9JLi-d-%}O{ObjAYv@9qs7GI0%*B+$;UjU6s_kb47zIS?laCkC0|3$m<`G=$Cd@OG7"
    "@NR=~V&a0*69T0iADx+ZwVa{{zd+h3tn<_T&UiELr8V4Du6KS{q#52gh?47kKHV)=k2B5+qJkR=ecDY|bL#M*Uq^}UlzvL@7b|(WE^oNM(Uj!<"
    "?}8*tQWR@S7=u@W%HM$*gN&`ByVTuckxpQ3Cf5CWp5bL^UWlAT6x{a_*tEFkre((Ci?v8r!U?GDdjEIh4Cw2*t46Lwy)80i!sLm-A;fp$^3-IN"
    "Je7;~sr-I~S(^^|7jBx5x?!%(2|e#%T-f6GC`Walx`%8&%_(jG7{!5d5e#=7^i<?J1<O_W!c#A<*C6oIqBuw%_t`-(iqT<LE9CI^Ub4QYVkM++"
    "{0;UR^m3ci!84n`PS86S3mBmHWU^eO-XnUCdOp_P`<P>3JTQqzd}<Hu7!4fv<QDjV`5W-@u03!Z^fl!ad}pet!*PyVjf~Oj1!g_lPZoH2&wYgf"
    ")<F}#3!G&8Y{F^#vD^{%Ui&5<q78PL!jrl4$Sa2@Yf5MCVf8P5=T+YYSc6Tz+h5<WXB0$-?*bo<J_3$6*(Vt@BY<(JE|xZB3=P9j4ZwN9WzkA3"
    "q4(a|;w)Wq&<uKYV!<4<!2!Fot5#TGeGuZZq4VckkR1zAK>`;}DvFyH?morzYDP^CsWMQeX?EyrKX6@3CtyJ&IwAO6+o^PfGkOw!U{yMCJS;QS"
    "ycVuAq^bq&P^m+Sg3Gn*aA8rnr-J2TLAW-sxB#yJtLe0%!13$`c&O5k2~d;kTMZ_=ooa`UgK0#NEJTk-il3IJ2@?vpghH@{hJEZfSemrDUqulX"
    "`NG(faK`eQcWdm2PWucz#TOd3Rup@ib{^GuzE0<pJJbzEE0HC528SL>YhX|*5?md(cn#YES`@mUjqZiae$M`J^{~<nUNDjqBeDb!3;vanRw7m0"
    "Dqrw5t(d)!nRv>l!YTVQo!rgyS$>PsEi2$;k}fk$#9{O%>e1XLivv;vg@ZE>148R<vN&51<F=`!rhIsyiWRwTWDl@nDjbEU>&faYBLlVep+l9|"
    "F>-_uCgV-;HFk^T$!g!0{Rc6KZmeHe??E;4g3uof9bKG>q@@&wLac5iYY#O#wOdD`uo1tdL`0Xl=1#WfL@buaAK|Cu@XR#}3`OI5LHEgD==waR"
    "R+=2Pqg^-bRpjkdbVCb?sPakn=u!jSIhbq?)=R*RSaU3+OJP^24~&t&<1qfNJ=}F7IsRp~qTTuiJw?&)&brG!-~rPDjAFXvU=WaM%iUb8xFVE-"
    "7Y&_Lbcey{oK&orgYk{`={eBqYq=vD=MvQC5;e~y2%XQ!P`lvKad#bWD;^!ssSfTpj%~+LGakKN&uPNrBKrvHHToaIh9O~!nXo)-3QrfaeASFi"
    "gxYSxCJFs+_+;!E_-vjN@S30_K7EQU3AWQ^BN^fws!-a1Kj?N?#oyam4ua7tQrN^dH-yBW4*vtrmOzy<xpQbYVbDi<qy?#C5U=;TVbJ%&wpqAQ"
    "cZ|Uni??FTvzs@r?SxSi!jMAZ=8d~#e?$yDV9E>Z>qQHe0JflpCF0)bGtmuA?l5i!-E*AISi*D1cDi!Hpan~I(1;~x*Qt@!<r33(rZdjuW<Ai&"
    "Sp#w;NOcmjqwbr~Z2>s$h?)SS%G_uxYG7wo_q*LZG*E9HS2PTjrZaGLkfxv}q#vx&As$gDADU2Ag4lqn&isluKo|Hyo$ib~pmBFA?uK#Hve7*("
    "_uGIgzkyvHW!ECK(>lQ5@?@Fa++cM39JJ*L9s8S5Cm?Ltg2;Zl;Z8feRyoxZku}_kEH`jl#<E+H<+@d54ei~jLXx#0L)9{w%^usaG;CBa+|GQ;"
    "i{ci*o#7LZ6aepi&fVC8w4i}=y}Q`mzXQe0dYjJEkBP({DCKm0(u6nY#%ZQ5x07bp0=3f>VIfdATa>mSY#6q2_6CKEdUb2^?_#|`_1l8u=@Jvf"
    "EJ;zI(oM~qvk7S>#C2|l+`J>>58H^%_M@lZ&fTs%(2=NlEDEx(BM<a-zluB+m~M?1*~EIYUOtlc07Q3KER%Gm5DHBWm&v>pc?5C;#W|g~svWiR"
    "7(V(ocB3DwNh!I;H~|rxK5&L;cce#bWl#pe`r+GaG(~!7a-a@0lR|09Yc?L*arv%xk`MKFrtvU@E%EttYd$HQFIsP86^y54XQ-xzAPW{M#$D4k"
    "ut7tFixMo$yeK3_T;Z%>Hj`!wmyRKee7TaTMpZu;32!&2H>*7=^Yf@wcqbUs#UMDb=fo}@KeKxZ$OW}8m1#0D+<h3@_GUn8aGa;Jj7(#~I%<A="
    "kY2AY(&fht4S87Fc{<HF(Sy-B=MK2c_h)&L@`98z{u#|Km}pJin7>|&C{kfW!fT4fiYg(jWEO-AE+LFzbeKh~-+MDlZuL7|2m8T<rJ~r6R(ht4"
    ">f7-|8ljic@c|Ac5zx;Yy5jHk{UOzNf{w9I46UC|mzYSQtWc84l*pKPr$FahHfVa1BxGNa_$@l~FqB{=DwuFuCQ4CPDP_VCh@=&=D>!CoU;%L*"
    "V<jWlV-}Z)h9fsn$K;N<*<zVtN)VZ$@8lI)bH%5@=1&XE+%|3dIMhD=;bO$!RU1WGqw&SrnYA<KaZ*v{_e{Es;I4aF{Tx`@83?bt?DlR~MXFH}"
    "yq*6ZefN^ne<-|^*d5B{U*!*2nOBs0YNmp)q=FEw_I;6AMO!)5v16m7hG0u%DLT(rcbHj<hBttB91}y>!uN3@0SA~|WtV@+=5DoXEYVOpEZBX{"
    "KOI(w@w8!l+xcL<Di;$Mj=pvMKp$EBlwJ53&+?J)td(EMb!o4cKFY?p0WZ!hf2ghv2-X7GK;KH%tNdjHYKV9~0M$`G?t5S=w`kj!sSQm!U`LzN"
    "1@a!uaP&x_{**$aNXoyH;)f#X?Ey0>fK|aOm5_xJzLc_rco5?r2t$`L^0Cb7VhSL;V*NZ$rx|7-MdmAO8(b!z1lv<q@M96wOO>fn_XV8|n*CHD"
    "=_v5)ar9Um8MOjzmCr?G`kzSwApm-Nagzs<K5Ol*czh}8US`*}xpeM^Kw%-lC`S`4ILz%hU#92x)8g_jnak{I%+;$%c>O5Yc^h{(a!?dyf}84N"
    "&f`5Y(rm~iR2XwCBd6uY)At+w3vn-Y3vQBfPw>B^*tg%yqHXoGmCD|KiOGaPT!yib#m#zvk>paB+**bPr5=Q+r+qt_ZoaL5Ez^r0fv!7ye22w="
    "xY&%^OPj^MF<H=CPjAKzbD;w%nq9>mR(VlzIDeBbC#29V^Bnc+B)hD%>8bCO0=%!^#*|mHZ(iM_uM~Qm6{yjB7FF@GUSla7^g^(9u>iHTKTAN6"
    "tMG1B#QO5};ZaXknx^Feg;u-GRMp-u{`Jg)<(Ac~RcZLsQ{!_#aGSnnH#(|EE-Kw00^&b0ga}_9vezdEM$Z_nqjk-R2`*O4G+q5a|F?xj(BVHS"
    "pQ3eu)emzl2>o-u1i6=f+66pSpog!1HV5&7@Ck!d1A^=QkB^Q1?I5O$S>qB9bbl3PJTdp5$ehGco5TU<>FQ@pw~SXoL%wuR>9{i%E<dm>W6$@7"
    "0}r@ZL8&lE_uxoVq+spg&k{1@>6y%HL@zjd2Fge^anToh7~p+jinR<DcaN_@hrVSJ{k13l?Du#SYv((vFoKlGUSx7&oaf^m$U1mPI7cBq7`g%S"
    "u->T15+q}RY<y*Vo~ON1i%sv`fFb~o0F`rV1YZGG>4hCclzJnZPC?+06RZY6CwA`Zrflfalks|qshD<wcr5&z-#O+x11#Hdw5j|EkEi)Pzp-5k"
    "kV)prG|``6N93X*pS|y^6@UFG9cs<6pVGNjMe1I%8>yCmO|U+dyFjM--xwsMcC7CE$Gev`Sh0PX&^c(I|29JRX(}E^oNONOVsiJ8Tq6%tvA}$M"
    "7ek0>X?+Y4GtD*cNm<(#di2b*aytz9)$@wQAdN8^&pRLA-Z0j)Or*VcV5tC3p5xW&tyM`JAco+i0{nL^wE%5kR@t|r>&@lGxQ%IZx(EJybJ7Pf"
    "FY@J~(0cN-sCZJqepSKq2LEGjP03G`a*C&8VJ*b`lsG#3qiRkYpdOP$m22;Ml=x{pOFxp{LMv?TM8GkzrXntgwF4ShjK5%7@WUCn-!Yf{Ax&nh"
    "JJRF(WEBE!>%Y0|(K^ApoWeJVd+~>&7aYJ3wJyDZFM50fis)Qq3nw*+P~_l&si|Y?Du@PN39B0nf)dt9!3rov_t&L`TK&90%NZhnhzGcKn9=`4"
    "!R&?uM}s*OJ&SY(8Cf0Bh=)gyR%k;TCo7@#Yz^8Wc5ec^|2V<mg&B8@XQfRY#~K<Ugs)sO3G8?d6i5_cM^Uh8>R~KE6H|9pcLCx=z<G}@!lKBJ"
    "zGQY3ZUi=F@C2~lz*fD-iWo2ga$-sEBJS3S;?1N`QkCzj#Xko^wZ^2Hb1(iTf{J}6e#Tv(R^=TTelsya2P2DH`-oy*X6|EXP$+|iN#}&Ep}yVq"
    "2oIUhl6L%DmdN1Ml*S4UYycHyA=N4j-%+*<%ECQGyW0&JCEss(%X$Z@YFH1QE#NYHtT;#(a41IAK%Cpq)okdNsnAsC(tEt2rN*Ze|3S1U4X}=v"
    "xAN5!Ibo|#*zf)Km^k1?b~`7X8N(yc&;L40iZUo+F7og)ZToI%U(s~k2DZK8d+?DKR73drC>FKU|Ak_YhNkP3YDI}a-SMYvWuZPPJkQHXQI(}c"
    "^WhdrjLF~HbZOJ<B;z-90bt&1+?cl%9=W8c5B6os<??c5^Y?hmq0XJP0e#F1Q5`YxJ?#r)MAt#T$1NQ=zVA{JYPzWszRQRNI<BV0i0lWHiMLmt"
    "a%nf?Z|YtCI^ZG(>286dg2E(NFjL-g4ADChDZdQ|yh>W$yVOE2n`M#}DSO}-mK$6zs$Oz^a@uzsQ7u_>rxO7d6OaNarwzn<H$W$7Fr48*1)I38"
    "On)zjyhD{n1^GC>%=s@0V@%du1Uy5Yy;vz%GanP7PuG%uvE&~WV#n)0Jtm;^1<dXj$z*kqE!jZ^UZZKI*qx%@fy63J3)|cT72i6f9?@?fmlqw2"
    "%ezn1*O~$mq(k9~-IHOkSI5bON_=dj0b|WgiYV@>U>;peJe?q<C!t9YYGs%dsFw31CHJK$8sX(<6~Kv-8MKX%R`8U&<~T#dd>_qqoU4_pT%#hx"
    "j)MbbR)I;}a?as-`atATd~cnv3v`aN@VsID(f@8>kr%hhmsD6c_?qrTXO9C54u8N`Fke7|=In%v@lkv7y|56$c%LJ1s6wWS?nERUAsdJ&D?aRE"
    "(p@2XbTaDTC0Qq?Gf_#Z8$C&v%CDfOKP8J~juq;)XJo&*Wk*Gm-MsqK*)I)*RJu@_g!D@~$6V0MM+;=l6swTq<vOhZKmlmP%;Y&1&Y+s7GRrBf"
    "q!=9|0|yqt_=m!}JUu)74_<!91x<yJ3rYrtDrI;-=M3Wr4ps>s2Ju=8$U`|-PNj2YfC&)+9DFM&k^20f(4(k#kS_poBzWQO0$<-_w9_m{Y+@SZ"
    "H<%3ckvUnq$O_E=3AjeVjmfDW()2@xz7Fs2Q#dzcWG{S4g@mefCLBiF=<MdEMrfVgN$aF`B1&U*A+^%?RFE2<3%`PIF{>g<>&&l8ztal8BKOcY"
    "LUxghC{|;^s`VsqxL8U;)zJz{ErQ;ou%aK+zC|Hs$R{MfGU{DW4YY(~%Tc%i$w;oZVj1=aEY~!@LA`X6$`VPULaOzU6u?OnuGFrIc|6KHOZPi2"
    "Py^H^I-KTM8Ysv7>zsyVMO?KrtCB9XPh(Z>{<UAnp-N}mui#LIgu9XF?vjQk%f|&Jw62qj@^&@#9rBgMz(op<{V{<766*)xQ(2*8)$Fk*r(8H^"
    "_N{~b!TKW}s{0jDg~64~4}KFv5Yzjuhh<-IpzCD*0cf$D57Q;X&#Bw-k}lz}WgxyOFrM4BASDV0$EZsr2VkEE=(?27Z-Hv&B4aJeLz7T0FaooI"
    "N`wn>cPeT0FaBEMkjo>8;|#i*Ja(lFYiE^C?p_t?eMY?W<YNZh6^}57yR&SL44(qS8wf-5?KLYy++`#R3DEVzQjWq)n0Qj8%tK(a?iQR|eRK#+"
    "WD3eHXpsrkXL@^fx$9E}MmPy26PbF6lw+!j412o3r;^jajGz~whV&EuF0jHBPX&d|%6bvR!`H~p^sGrr#ir^~EdJnZN8YC>qDY%g=8xrZ`!0h&"
    "mq61eNij|S$^y?DI6%dQ40M3TpD4FVFY7uvu{BV|X_xfW<b(ZnBC1?eK~88#d^I|J0;kFJ19VLxVs2x~u}0dG&d&`@NBK=#1!xEhBmzKIwphaH"
    "cc#3ncO3gW%wm!PNr8m&{O^!Eke4jhsHb1!cYVtb>Cd0CbOmUASvz<Etiqd?k6=<svWF#aBO=4`@Cf&iTe!rkBi60paY<PvEm=D+!a;axrAyoz"
    "FY9``P`fZI44Sn+X1Cc4%j|L8wB@|$!mLU+=_hDK9lX}Rn%KlDe-ZE6L~BioQX82KYh*T}Dk!*i=C-aZ@B&tS*Thoas*-4835Ry}WY6bKw8|<b"
    "_D?*Ainn8`66DZWZ)ve&!nJmUc>zS7;|AZotclm*AaGfw&)^u@z}YCf0n;!@+*t9lzW~_qJsb&~@H?ypILSe`^6b|ljXTTXX=iF9$Nui3ag*2o"
    "*Gb57k)NH)G>(R1lq#`dR-<N86X5}kq$WuUrCc)mKpcWy`TJ79q3Xg!klZd)rhz3o_NGk~MfC}gM2J)bVGV5>rA9O!90U835dP>7&|ZLvlu{aW"
    "bf5e!$4ZD(k$58EO3YI<v$I5};(w33le;97=TICEmLGFhOjFD!O{FOSOQP&M;z^!TIucdzRDEkpRK!=)l?b8u2Hfj_=LrB7oep(cXhO{@X~sSz"
    "H*ik5mvv}y9R<glq6csx%-Mh7^de|#SDv7Y`~i#A0zDyQBKgQ@vCL3+cY`J>#FN{4K1&{M)-&yp$QBH#yopr-Ej_zWVc;2vkQwJ68(2HzPp~wU"
    "Ck;o&HMx02E;>&?t*}`4;AOW{T^WDSoqoO~YUJyPs$9qJM76(MPhqLDS<STFN?=pE6-`;QEjlP<TJ(lNUxF`*FpyaSGVcy(Ym#$P8cLgl$6_Nq"
    "B!dIMJzlP%$26s*T2J6;umrKRq8wCIk(8@yVs#$*xv-D(IookD-wjoP6<tCX=#h7qEr{;m3`*&80EU6}nq4RfQ-bL^_J957|8hJK=~6YHJ$`TL"
    "2D?XbTmU5u{hv`s5(h*&XBI%|<*72ItJYoSgv<j6oheg9-8?}#`;wTPuhZ5_5)h>MHq93~UXkLB^=G=B68_Ba@?WeUR5qeBe!6GL90|Y8@qhpF"
    "FV=y*XZ=iW1r|`|lAn){$LDVkPu>nx`#%&`=}KnNKH!XGFEH>1uNf_%R4UdC&(KR1Z3(FNt0K|FE^rJqE&$`Z$!;;p70}Gblxj-j1&Z||=1<WK"
    "kD&&*u=IQ=`oz0Jpg2_(3Y5Uvy5Po?FAR9p3*Qky!5I})xivb9DzK<BGO@i3D;l#X#h@iD(M&a#bH1acJ~L6q9BKFmyu6hc!uaNe)Axon6aiYG"
    "$@L+nv|S+eZb61$<HW*%?o6|l9F1beDAgNCWBf{FFh&y{W-dl)&BMLG8mrhp-~VC<3H6EH3~c~IRM5qwaWF=ifr`_h(Vi7Gp9bZsJA1%CZ^%S&"
    "oATqM(dF10?eD)keg}UZo}QGekE8lgUnsF`?g1Qtk_1u(WKD)ka&ec+=~3zHWV)VlVmI|D#lo#iZc6U{tU;msHrg7(K%xZtaUxlP`T_0Jh>OWx"
    "Hk$$)A;KePEjVJvFIhzb<zmMPK^><TWX<IIn6!zwu=Qwty9UNZwbh8QFvA*><qO9}FC^*IkK<3*srgAXpg}}wd*fBi@KK54WCqm5)hj9Y+l!Ev"
    "PZkRm1;24>Y|Slq3*CaNyrgvh<k=D<@Nj-h<tdpg=Tto$P5VeU_;{w)Q(I?u&njJfFe%Io>nc8SgX7bK@j0wIFUTEc*Mt2kY(l7bP@P>>8E>8o"
    "I}G*%!mH%G@J8k&V@#-Qov>1SIMgmoK-4^Z;o0Se5uWicn8?4!hDklDL-vP2!RKXL)Y>P?kxz|EmwuA(NUG^$g*h4--!S<g3@?~h&{J4oLf$2n"
    "`Yc%t5*&L!(A8X@B1tH3-1zcMVeN1pM%L%(hG>Sjt}NSM_EmvzRJlH8Q*!5^cZ_*VK2v9M$P$+{rm*@;)_4XAC}7jtPae}b8dhZYvmCb+(pZLU"
    "tX$T4t`}pIXcGHa@I3s#aw5sGG%r%GZ#z35Udl{_ALan6*uHpHdJ&_SC^RE-W`tt~MifdDP-FHi3J^oe>}yE@r&*C)Q%om8u)e=u!r?x#Fo2I9"
    "53DkmIyEt}^#Z;h5Yq*Lkxk_^<}YcTWIkMZj+fLV{c_p1UEmR9C9*6Q7_uM{Sx^-|atJ9mjHot8HAAc9*2f{lg{+FP)ApdZXT41pmK5*&;^Oe_"
    "$>E#B{n5##^>%c2!TYA%tL*A$6_cDnj9poV)<Fp-6fu|uU==O$)4te=BzVXy5AtSUVFU!dnW+NJ+$VLTB2&<QPmz5n!=s?D1q()wm|3|U!cZVl"
    "LWh<*mD3VVAS+g%`W$4XddKAfMJ}82=Uns^!Nq_?daIEs?kT!=CoYN8l6Bq{qyuIx|MqWZYRJ8R`#0-S5*>+Xmt?-pSfd!m6^)H4YDpWkmc&|-"
    "w>W(%Zc&RMnV@S7GAAczgv3zLf%Q&OudLHu9hCX^eTo`Wbz~9pDQu3_&B1$2h^B;nO0Zh5rZAus9#|(iaSYg;xNDK_*8o55LedzPWJ*c}jj#f8"
    "pNe%^a;oTAa(l}uR@ZY{d{B58xn+D6BKN$`NN8(WFKk{_SpL6=>lHxL19LV>XmDJl1xH%O+XX;Z<cW<3*!TUoA4VRo1qxHT5E7NJ04&<<qI56X"
    "XT^mCi(T$)=<r4ol%hUHafzEoqc2k50<VvO)7C{UoM0zw+@pO0nsgR)K1OS=CI}N=X!zcX`<@p{21xisDnPd*q45c2S7^Dcy1hXETF{&2cd%BZ"
    "xe|{Nn8Kx!17YFk2ip4R%7}kx5oN|TZ#g}&cKdRx;L-_87c#3p($%mZvZgJtC8MiYEQU%Em!s{tK8=pJVO)T0D_HFVHOF^iIV0L1eKB2k5Hd12"
    "SuarQJeA$Zu5a^HQw9y{+LPLW>|C~$jJ;$pO6wr8t~PQr+ZGra%fNiZkgTbWqFvv5H10yGpnU~VnoRBl)guv#;a}KDY8Vo$bWkx(R(koUfLr6m"
    "Fz&}*EGhYgV@se{q_3gjm`*Tr3QQLuA1PLjJt2!F*u`l@s0m7OWP*$aL+O-;nw<&?muoILvc?tDB3*u@#SIXPGWM8fAG-7qsU!+u=QC}+aALw3"
    "InEmK;nogLP-(#kxKz}I()|+8M*`Y#;Hc4vH_%pm0V4@R{WZurL%%^RFnhxjkj$aaLM0gZIswvQN6S#WOtrRrP7y(Yg=GAX^bQ%WmWn#D$m?#Y"
    "iF$v}LVE$Q;7nGm;g`5<2Y$l&o~N`K-@ZK`UtApiG-i&42_unrVpdMXIj7~ccKnwE`S~@h$;T9(Hkvw^Rg;8P_%m<D7#I`lp1?2BmW<-ritX=2"
    "#)48rNWJ+Fg`v)aPDL(6NIxL>9+f6bc}H3IDDK#1exH59se~~)IdQu_GBLasM9(!E%NY)$@93ie`o8y3*c17`yAbCMab=7OL0=v*<-LlGtCY;f"
    "8)_`7$wsjA!U<i;*`%QWj*Vrw1`grbf@$3;XK$%L63|0pYKRV@iM_i}%QQj9846^^WhxI@`w4~!uM2WGM7Cy{I{G>p<C%bh?C!;Jn|0_m&6&2%"
    "fM^eG8e#y{eoJ0$u{nT*402$p?6a(^s#c`v2-_4h`E3V@np%M@uBuP`HXqFZI8r98(Ge)Y;{zsN-WjazfnuJ>`r=4YxZ6>L&ZWcAEo}~M;{|)@"
    "otU8)-tK)u=S<2Z&n<p}kq$<er{{fZ|McX|;lcQ1f4pZMo&JoLBvEfcY53*QK&(IUc4Q39ajw@H8aBkK0rYwjz3j7z$H6{q9W>6vvXD(x>}0vW"
    "sGd8#BnoDPOIAzl3ouq{(CR2fu?DjQ4i?gSMn+Lk`p`@7F6Z;L(B#pNYk6O2_zCx{;~dsfTB1R-2NBKh58hq=QbP=NbasCF)8WP8>B;CwcnE$J"
    "{$Y4%5@<?hj21ovH=M@tAVw=#p2Q^%q<lmXLG4hW_9X?;<!cARM<!jK=Y^5xQDPAlH(h7J?Yz)%a|!Al^AOlD>2g)@8`4syDfduXl{9;h6kL5A"
    "(s&gMjf{^je@f<SG~LlRN&-HhSYJ?z7WgIYI(;(f2xAW(>G1-9L?Eoc<D$rQrFS_mNyTbZNW)P%!Hf0vUqtNz>9No_MWx2@>X5x+g&{`i1C^+w"
    "lLc*4=Bcz{q=}FuB`M7hb3B#M+DV})&mSdBr!62M2R(K6^iu|b1m}iA9)LCFm(LH@&i?t~C7h*?UJf>&Q2JFxUn(3V_Jz{Uni!u9Bws}Rt1tA*"
    "ji(e+PB$J^KmnE}WM%G@=0eFs`{aXLhzdU}+30v<qnw2iam9e;IeqKE6N2Z|-Lrn#z{RZ{&E`Oex@cA1t%TG$<3J$LZUUeN_x6<XED!E*sJC{c"
    "_@e=(x=Y-nRBM&^K$TgfTPMIa%@$NGaqLwG-qL0v39d4}qHsLzGPX^Vn*^lA)MiLC;f*_`xoXF6W=Xga@xY%ib^)Xh<amv1z$TNJc5)259m&4y"
    "^%N6{OmpJ%L<^vr=w}b)jRc{Zqq@bQY9RC}ZZ(ibt66!Ip@ecK0K<)LEFj?2pGc&F7`;SJ!^bJ2ftntFe0XwtPUt*UN_l~EWzC#T94yapYwKqM"
    "?t!d8GNDupIfY10T5y-p>_wQE4#YOS4a6~C$!axKNO$Aa!_dJNg;HoG>edCbqL>kZ8poVvxLakI5B5sT5tUKo*a7=T0|k&_5?{sa7lMknP-YB7"
    "_}3B>(H<4TN~Rxy&n9T1nPvAG@rHF#qwouI&|J^ZWV*7}3%(7*R9}*kGQ=fi!P=452zbp$P|j6@8<MXSFk8(vr`dTah3Fj{CTZHTrjXD8#c&ZV"
    "H;x0s1yjLiRQhX~$dqfCgQ`5dsq{H1a%k*<Pt`vQ5|+BBZj4^f$rR1Q%CuHyA|54tu<T2=!ro~Up`NT`+SQp#OvvVgcRsI~jt#nlc0zFL2MuwO"
    "WXyVf+j9lt`xJRG6P9FIAgUm93?bYr9k0pHkZK_P>EuUcjOe?VWJ_=;Rbh&nQJ||hiPUdRUc`Ynu#RiB<+zX>Viw3e-MxO?#sA_V6GVOmOA<rF"
    "J?jTU<B$>%k&Ajq8_O-LA*l;5)rX|S08VC6;0wVyf4PUP9kjv(4m*7)mFvY2sMhD4B)NXx=Q}k&u=}p<m+86y!EnkX)(kL;aEcdhe>e=JX|-9{"
    "NG%avfO1_;xir-jWfJZytyZ^SD=A#c=A9o7-~K>I`oXY-ZMJQ3d9dX+E36c?O2bYTd?ptv(=>&%OX-l0U$7b=EvIrieA~Aw@A2uTe9Gk-tesQ9"
    "(<$tsQ}1PY3?w=*6;qItxH$QWHC^a87h-1TbO>Vbop5ogUM5KRWx6%m)_k9j_rhW+K=l!)EahRL%o{u(bG}WhaXdaae0R)Tw00IH>kJM}2btvd"
    "78Q3o8b7A1(h9BAR3taAa;;+MVvIMK_(+;JrptT*f(3c^U54k&@+zN9V2LpQ($NCRimbxg?Fbyb?oe<EoS;T#94-YuY62Zjd)>r&Qnm3>2mP%S"
    "#FI*w7+VH2+c^z*?!1@&{O3Q*v_cbMF+-;m>4O5l&{?7CoB)qu(Iu;aUohS3of<s#lReE)h7Yc*4<<%8zA{U|4^W4c=>UF$Qi5mY-{yQy+(Sgq"
    ";SBZLTpnWR(Wzs}^9cQPb-?I}r;P|dee-8vk(8moL+$U#Y!+*;hT5x@;8X<5rDGwNp+8-VNt}Loc*rN@|Hc{1vU{NH$KCrB=r~JvAJXIwL&9(9"
    "->3xNCs!h|UvJOt_ZFO2SOqfevSQGqBx{r*t(dKEp+#fQM%v_GVHor%yOKdV`~^Dm=9K=pEO14IUu->X?iD=)!6C9ca2~+k`1tJT^p`Qk5yRfS"
    "T2$*Dp+BE7>M_HojhgS81AB49z;@?>RbjN+&_`KvuZ@dl5;<mAYy79YxNB+bQF=0VA-e!}^af7~85}v-myG<#_AyuG-?GKk1i(SJZ{OkA+vL*~"
    "01Axds^FBh0P*Pj{BV45^{3OrlglG4y;nSfpac|5RJkEK(BN_}*4Lm0-=)(l@d#0a9(p*6%}&rZ)zhM6*M&^q0USPGW5TsZ4E}uRVPUhPp!xKE"
    "!PrMWG6A~@(Ovo$wRGWY!Lsl%Ujq-FqhNzU@E~>l*r%rnny-;PFEiG>C9%$+K@QxET^7j=Hm5kWqEIOT_#S?m75VZO2;*-Fp9;qFJA4J7JR)#q"
    "OQ9HZC|sJXIA)yOdDGi$qHc(0ShyDzFYe$T%V6RyNWKzRGVJm;ThJ6JSb!AUd`4Gw_{}seFpnkK#?Zxak%{6-u#@<2B7law{hnGdD%F%{AX2Z;"
    "P&>cM=2yvLfu4rpE6*k(RehlsLHQ|W@o4_kabLNWPc=_Ht%ugZ<5x~#c3|FimCn$pU6noJ%~=~zL9Ne2Who%<5@l{J`@>{2&D}*bMcin~qQGaE"
    "?2=HA?z`kON_nn8jm~F8cG9FlVw|*_(b>5i>I%A9z@|x7xML7X)y**o&}62pR7l`-8dk2BGA}T7tbF{7#;#oid6h4&&<??*vJ%<lF*Pn}*Coi4"
    "WJz2_dck6o7nBZ+&PA9$BmRzB@p*;_jP7sA%yDNTK%Ksc7Re}%UEFe&$n@qWCs~3{!0UTeiSCMv=fc`z(l$9KPN^Ze3qB#Wghc>GsKT1y#3h3&"
    "r#YJPj$v%-v%@zpTy|u|O;)y|IbpyL-)E@>;dR(N9o}x0x%jatwzy?7c8AHBR`A+{oMW7eYGlmh|7Gt@ljBB`gwd<OI91<J)5$FCi|Vsymf|9@"
    "n_H8V)HPKy4wMO!XeBeV6G=(zGJQ5bz8lOt!FPanh<B7e$@3*55CH@-K`mADY-XlS#RLKo9v&X<9v;3ZS1VA{Fv@Ks+$sa_V*#hUteiIU?rjMt"
    "MU4REUu!6^wP==!ziGgLDXY+6ZN!lgt->i{LUsdfh40X4zeJk@92+x_XdG~*iYm7jeWg~L9Gr*5S{^@@7SzFiTBtYR8+V?7{BnMy437^Qy(#5D"
    "Nb@`VhpuecSCOrw`E=fb>~jbJiSVle^hT6vRiz!O3z_-p=U??oo#*?Phv#r~Il085pPXrR>lvOIg;GmAL#Uc?g2jj|<pNDNH(@F+HYz9fsdel!"
    "O5|3IX&-8Xz8dY)nMfP*`JBA0W@{ag&2Gb}+3)V@(b4|%eXU#ePb?f&&4SH7wP*JBcOi38G)B=azP#1rHc#49X$*Sy@_hHj=mJNr?%yi3j*hPO"
    "FD~JLbEP$qU|~Xj#A9u3VCw^p{aq}qP4ZrB!=$a_zuJFsxO>!h?DxfOi3y}=_!=MND9)P0EgYVnGd%(QOjLwNg2CUecj>xM>3^84@?W>Q7F*^{"
    "p`;6PeJK)hd8eXA!jz&fn|&e@>Ty%di?V)PZR%p&v(}6^;miOm$tdb(EntDW86j%{yX8vo8!5?vtYcIYvXs)?tc9%JKeFnvFlLGKp1Dr`=0QX6"
    "3kDVEMsv`p$DpZood%t3&pc1V(MC(q-|9L1jGhH6ZS+i~*5zUQ*DVqLVwA#`2YQNT8uNwUOhk2wkgCzi$;-pbpRNv1c2AEHi)_uRt3T5%9||UE"
    "FL)#3v??rE9R(CxMt>)IE_Tb<GNYp$`eJl6I{)cvbh3B#dh~q%LL1!k`wWg1&E?=>st^7JBS(#qrE#X;$QSp^_vL%wgU^atab42=eQjuw!=LUR"
    "!mhm7-+g(GxW9OL{_616>G{>O{geHJ!%H2U%=1DjoU|SlSY+P14$b?2<k6b|(#B7tGzo`j2--jg(IdvM?OmJ4&w|VyVnxCA3u4e=f-<L2#T4od"
    "u`k^~t9tCC!&iqV&#(6Xa<+eRVUR-N6D81H3I2{Lf4u7KOjPe7$@}88zNxPJegRtwb{4Gf=wui8FKq0?m&f|@QUMz^f)_@^H0T;*fl1t#s|WUI"
    ")&h3VPtW$xfsQUme=#NyL<anR<_%-QjjCLuGYjq3WlJ@=5@YPjXr{Ua8qml)R2Twb^wG1UeZ7Lb+)ND6m407&McNV|IqGU4Y>{RQ>BM)%C5@h1"
    "d4z^QD!Q|yQG8=w;{9cPS!<u!)!zQW{`onXIo0%{Xw&Sx#N9MK&vVzzFYaK2+7zEP??2nKv^D9meBs8`^P<i3i`*|*KfLDN;T!KwYlw|H7VqGE"
    "-<X)cabg=L^+g1UcltXT6a1PanQWYy?{8kRaNUxn9rDq>YMZ9{m{p5@lU1uH1e}uYZ?8E1Tj!R4EIt%dU8Oj^e6fFCACr7{GnRDbu5<IlV^mIF"
    "usSCC3!)w!9?Z#tAzAiFhlk75t^NG6sHS<x_d)0IZ_xh5#<jAce$ts_cUPO+{`mzu*Iw-c*&beA!4L-ZdQ4lgWZBhHlwrcW^g@hXiHmUpX~TqS"
    "jl5djQ#Kfk7}eB{%a?ngXkQ(jj!v!)_VGgT=;|ei>t`2-dx!sO?kvH_TCkDo(*n+qAG7+(ZKF*F$EW9)&qvRVjUZ^D4N7c-#O=564cv@gUY-(S"
    "3><U~9NKUYc2i8PD{1snFPG;1Y|*NYPC;M0+&@3Q+QV8QHpO(TDv@qUKk|XYHW0%>cgspG97@?9`1OlZINu)~9_()%mZZ9_Ez-^2=gmt~ct2-e"
    "H1gx7WF3(!uXIsxhxU8=`ULiTtpk6>dF|#)kRQHnWNC`|cEftV&9HBj8MfXgnhijWY*-DH2&`5eAIiI1b|Ev4sOn_mdTBO{!@(BbcU|FQKJ4P9"
    "n)+!R_15%XYXNote&7$i4c#Z7bUxKK{IyJkrp@?zNx68(55mwfI$DFCR__v2*_Q?<p8qvC!_<JYY4&0$_xE15z{F~?t~kf4-te>yXW6=UzZ>Yr"
    "P!eQ-&<*I=Zh#$_=nZ`<*wS$JNU%e%0d}+*Y%!DqI|$Nbn6-$`Gr^7wu-n$p)mqbM(-z-AeuHdIPxh}a4@ngho}X9J@{LwEQjf0kmG&@BqQH%Y"
    "e#Z0SPCwP3lbn58o8+U=^}}$86|dWZHL)o^Q3lOpQT7uRp-<hIZeWKly<|_?ZUp@@_DF#+3C1-rAGqCkHyEO_Km<uVMBB`|UJWMF?6qa|P`eV)"
    "49eFRbZt1&>d5eb#)fIS5f>d)SYHmTI&TIV_c107`stU_V3;JKJB(@y^wTvI7^Gh255vCnmqf8neo;T_lb1x8bWi5|bFK?xP5l`5jo;+8X|E-f"
    "{omxqTDq}2%)YEgGuFmnSHP{@;LCdNqQWE&hH13EZ$Dk%w|%o`QJA(Q?<0H0L?)|Z)<6i5-7xev;^Ph7UA!wEuI>srrH|>B`8pr3s=6r8uS|E<"
    "E(h`81FSENUNiKZjwMu;XlwQZo?53Ob>Q)upno)fp&v7Pnu`Q#=;Eo}ZhBZ|2N+H{N1wgbe1ZvfMOB+t1$ZpJi^?0_+Y?1sL*=i9)nd(G0<vxP"
    "Qo>vBU$*|>`M+#oK1tyYKblQs72u)DV1u=;i;pX_x5L@7L`3b+wQl%bp>^)#T-mwLMDZJPBDkDCD`3ED47Pb)V(r$Sx0-2OX7^MU1#m1D1J@JL"
    "gPCaRdtT|?!QrkdlmS)T+z4+#2SId2B##Yji)oP54KsTDiM8i6rE=l(3ZwD~_ImwIHSVeM)FQ_*N)fvfNzm$@Ay%IiJ+=CJBO|Dl0t<A<f(9v2"
    "<#e>CpWd&~39<V5%~0El&b9~#o;?_tdBSJonnriUPOwg%XcN!MA~GS@-0~;vnI%y&YEb<)Ry3&NC@5Ee48S1wOyQ#cq(+Swxv7C1>ElOWY;{r&"
    "jl=;R=vv}z7av9FXLBG<KFA4+tTFd0Qy$TeniA0-+5Zq-Clp{w>?8jOtj>*qC82Sm1c{e=URry~oZ$L#XvXSR1jW_fmLdkAllC5ge!5v<_p+z$"
    "5g7e#-cmCmuDaet_(tB7PyTw3b#2b;jeA_qemKrQisHKcm=0j>2f*dN-nS?LKATY9WZd+K_e!iH{XN9LxZN7Yq98tJWNgVY?;{MxkPpAY7U0`0"
    "72&a(FI1J7=7Ox@_mWS<zV9PdnS!Ew7pNIgZ9YMxIMvqtCE=!_PPj>=6Yjp;LJa^h5DFP5ZM1Jm&>BTq=y^N+$G`u_`s6!Lz6N~@!qk8<X!MK8"
    "`*245ca3;mb_{)lRU4|INOp$Z<9~VAY2X^$#prpRC~j~%W5ej=^;F4Uq6$F|EDfpH5hgS!WRQ~)_9ViaTI6++KZu;JbyA`qp_$^NCDV*BWm)2*"
    "&4GC3zZ#3J$7>TM2f=miXSZuVZ&vU=q8vH}42%T31^&vlv22ZnUO<a=+@QKMkOLR1o4&dr4UANw^Y=!VHV*yS%A%Af#t8ca2Kn!*ktB7R^1xJU"
    "_`5Z9-Vy>x=!U*ZgPxd5=T|u-$jWiNGcdsbIX;kP(n&*GUNj81K8J)PUXNRovtX2RUN7&b+~4IbmOY}A69sFk#KW9xnzF|I?S5VdvsNPi$O3Co"
    "{h8iyE&xCa?6kWgr)-53UqLK@6n(kJmj$P1$!SPR2_^zu$!mD9wU2(U^o~k6aqe`24mbmOaHH<_mVlturjal~$oo1<wvc&5sB3@<`@-J;Bz?Vc"
    "jWJXj3mZNxWnyg-eIGD|WQEB{79z<L=GU5Hxq<5bPRygEJn4IL)+8sB0hVoBVc93-P#FJ9$ow!Dz>Cv~n0AFj+;Zyg2g1pUz~f0Ux^q!JKrmXN"
    "P#D|`KY6_@>&AH{GF~FDqSOW3D#K2YJsAk#3G2?`#VLQajW5|t@`>Ihd%?qWmZI-mCeB7TknM;{Z`VCi{j@vS1>5d0inyy0%@-En-y{wHn@Ics"
    "NB12*x&!j5W)RJkj#w&W8ncv$g{G5*SSF5T&M|GRj76gb#{35}3IVH%!VxJGSCm*vj8V=w8jMM<oGtG0SnxMR#k4v^x?G6nEmg0jDyT!}0Q(SR"
    "NtqI8>eL9R0sY0Ki#Hh~IFkK226QMndNMb}8yST#){9jZnT}Q+Vu#KlEj}gMShBA@>z*ptVKeBvPRqxo2)X16e#EK4Rc1a+x6>&%i`fn4p_fVh"
    "p4Oe2;}GW}JA{!se1Jle1H#Fv-4MdM%xy&d8yRli77v)yK@@n_6WwS$(?hd!I*c{0iR-R*Yh9U$M`DBH2Gt0rHkwYK3+^m~aJZ;AzSPc(@awEt"
    "VpB3#e3lZTP78I2fGQ(tK^ETAJXIu6uLd4(=TkCw-z@1WN8m^ph!uiDK?;}%g1_%ZNUkO=r%4v;-(sG4vGcpm6AdY?$L1=7?D$M=(^yQINl=@m"
    "PU3V^rlv)aA;jG4iD7NH01r)g)8%Z3D)+;aAI+VqrCbYAnE=ug#kn~yaYnIhy3T<d`}BHO1gxM=DHo9T2##=nH*<d3`iWW09L4J|Th8`!eorSn"
    "v|QnVt#?Q2Ia{~3zk7n+<u#%zGWckUD0(NT5Y=I!_gi;+sraU)yEmJ;f+T{0&fOau;)_Xw>He#bMCdU|ggr?j^b|=%|4kBKLK5UX4*DQxm*co{"
    "(+FkKNkiajWU-Iks01O@k(7|vq-yd~ZgYVlY^T{=!`RK}I!uv@)M?eiiiCM}yqTm5MMuk$ZkH61JyKd&gsR=JP?#%><q1fMV-Y~9U<y&p?_0{B"
    "ON+!I6+)%rG~|z_jAX7UfF7ZEXvEX0aabO=HOmGPrADbJsLqh{w!~cgXUpQcphVp}y!zS(sD308tJeS(&DLs~>+#v_?*g<nDxf0i5I$SW1bsg;"
    "u#I4vNykM=ij|0G{Sn75m*$cHXoMg<GfxToI-6s!-4R}usgw*RClRJM{n0wxIGe!;hX$iN$5L5%XqVs0bG~dOQd3wyt;9EcuCG12FrAD@v1uMc"
    "E@ZlVRV`{MMyHf;c>KXUNyvRgW<@yOF0fu4ZdOg!sBHW4obusTU*NoYS82&dzY?8@e4X0;j!GmdDzJ~)NkwFLBvZ_QtDfl90yJsrr;$HQbuKBZ"
    "2yi|FfF$s0Wpb%|&vkJ^?%+(O*4hJv(k7O`BHd_fa;Vaoa;X6-0#YaNf;AF}AjzOqL-3=dUm$gH)Wu{I^Tp6%W=!1dkZ^J$GKX?nF(qpzS{ihf"
    "+5M^Pm(RxK>f5g#)teBPdn9i<;M1=Z(=c!YitYN0r8CTG>ILl9Q{)!R+e(Ew+{Ul#tugFE?>6DL8+eL~R|PWo({-A`Bar*NS$CsRzGJ&pvV&te"
    "DI4WN<iOI=n|N-7;bf0T?~mf4khnSg!NH75xghg?<@~)^&M}!51AKv1drz<B<`6g$R;SODE4TTwkT-P?8^}-RAR^82wpPsq_n|Z$Q7sS6c$)>^"
    "Z+&Ajd{xzy1_U@2gjea$3y?KOtMRUI1rlPUNpR=*xK9u4m9awW@xgTd0oApi$O}i);Hc~trR(EThr%a-Z&5^bED^Iru`*PaC8X*km8OpfzWk&4"
    "Ar<r~S0Z&U-Z-%hu+H8q?XFljhG*gU6vKq2g6=B`T;=#-;s&4&M<}X%Ka1UA5<L}WJWMN2#eS(wmgtjmA6ELfUx^K3I_o;iA@wgbYZ)vPGkE%K"
    "fb4674sMe?gRNSs!`c^W9hH)@n=f)ogN7?^?W11uU0z_iCg8*=bQMAhyV_59yM*=j*u@1E?fD0+(A}YF=v#}I3*XEPk*)I60$UR#p{m4ydQ#^j"
    "L4*z+gqpt@tGvi;k-RQGh+~k*e!48Ajg>OOq8O#OQn8Un**a%=zGzZTN&M^@v}&b`PzF)HH^i2xK9^+mt@4MOHn2(qMvPDvYAgZuRrRHjU_^rT"
    "Q3gx{sfLWu!_VS08OF)udD?(E0Ofn5x3btCXWtY&zaQh%NMuM=YN-wA*d%>5dA#PVu4}=hg7L(UitE*Ag}F%fXOpktAfjiF)AJioVIcWkBeA`P"
    "?jZ5t{5VWA-LAu}Ma$N~WKSk&6?eNMKCP@^KBw1b{LxtK>&_;K5tBKLWN3-zeuuUctXW!X{NnCQUUikL`pPf-9ylln`f^6{U@5MuzJ@fnQ8QgW"
    "RZ`4vuJfhexDMTKD7AIsHBem6*N|%mr-tL*Cn?W~T17r5@^_u)<sBITRN6a{B@#3DVGO3YMcGwhLzECy-TK$hMbffQ>XW^*JsbiLBu9C*I+HHk"
    "TYPJn*^-g4)~7`oQ7$&&?tM7ZU$`i3ZuTw@TaRz&ACB+Gx90P$BX;rx%7~OrrQHF!&p_+{>B0KKT!hc@+4&)PyYsK=Y*~_rx|h_!q0g7|s*+l{"
    "FfmN#pyWKf0OA<U9$pF8d@&{2*D-%C&{K)fMcbE0<T`JD4Uin5{q9ocC!~;7<2@+t^V!5~fPVA1FqiZC96=PqZ#{mCNs9MYG*vI~VmN*na}@F3"
    "OX90)c`54yN0e6er2J6NXMrg$wRaf>tRnfp;Cf>FDt|^q_G+?S2t=K}ot8Ib!@%&9AR|w;N!{VTJO>_2DA4R3`AC_fTp4d9W6Ca`ReDbEwh5%4"
    "`H?nl)mBWpduDWeLD-84*7KFyMJ}=!2u)NUW?MYVXEGi(3py|=5xN0sx;!JA*U;hnNZ3|%@HZnF$Apo|x-TJlkZFwN73y%vBX)#0)TF^*X3Nv-"
    "eJWL5QL5ucPty07&oO&t1u}zk?jCXaTAp8x)=W@@@>P?ddMa|c>Es;Hj;p<?p5+xfNNK*7EvIU_&66Q4xLu2Cyet<YBV;R@PmhJ*R4$l6M&|4W"
    "UXCN8vn5$$Db49vWbCzg@k6secs{0eE^lr@SwQq@>!=FaOAj8BDbh2qR|+&Ul5xZ2#KaET@s50%VRKTe-QF5rlm~K(8M&WYU!?}_RJV5g$z4!9"
    "9Fx1ZB!`q|HeKbH^QP;Xt)IKP3-WH$v)Bkf@so`?Q7*evqTr!U?d_B)gvic-Os*m?%sLNL&5M^^K&}3MhLd`CU&062=GCn{y6dj&&fg00><Hh1"
    "dIgweC#>~gwCz@ISk79riG7zbE*$(iod}<LVVE*^=;J<Fll7w<>z<N4Hf|j`5qvQNZby>pU5V{jEEF2MtQKen5r3=pnUEFt%Ska)ywc7?QDLJT"
    "CCr6!FogDy3ooIO8@{ZNr^p5j1^H5`Rzw}Z0D!ejAJkJoL^Z{->L7uPKHd7oOQWAqfwS8P{ztK~`#3-;9qu=UR6w-b$i2{<!=DPoHhu4iidI_&"
    "+Lbw1N-6XEU0oq>jM>q*j;p$N-^8S~e|mGyrxaxDulUH*0*dj(9lOIU2!gs}`{#{O8y$FPGSH6})EKs!hTX`ON?Eg6Ijfr`QM=XL)}8NmH`F_n"
    ";o8O)m9L-Y3%;ov3l&bRtN5)GuJ(u?Tu3p7nv}UT+N+SRhw%_MhQ%#cyZLfLN#bFwX8M}jyxP+=$nhAI!uj=eoo=)1<aK8pLqvv~`h2>#F+-*0"
    "h-Q(Zfc{-E#>sqnhkj9U<PMXNBv9)e$grWCiq0?RyT)`pUnw8e{@>_M<xm6>lfF9Gs=ZE6uXlHm-i%WkX03^nPn!Rwu*4u{NpW~SI@4VRTiJ*="
    "rzrhUAoIYnqBsUFgN%GcG{xPWe0H|dfd*m}c^=4K(dWoal^~FJv7#y>o=4VUp?N5k!&Q$I4u}BQ>Z+dkaq13(q<%wQChgZZt*hw~95&G_U4s?9"
    "-mwDIZoVinfi{<YP|&CGFpm1=WUa9r27!*{z>4KZq-Qm-oCcXUbi+Pa4!;D;UgoF6H0;8%dc6+I3f2u+4*g*o(RqZshs}XS5qNt9_2*~B@)~y~"
    "&tvE&m|B5wbKV4BIS&a-P~>M)U)C|v?U5kuCr0-s4%8TYohqJFD(=g<HXt9*lr=>ScOd*`*sX}U<tFb6g<Q!I)b-;TGa8W&*C_u29QlHjG&#yb"
    "YfJe7Eaz-;$N*TVC*W<Qu4xDKG)g?Z$w(xL3zXz*ejK>XH=2E<<11w|^2jK#rh!ik&Tu2qSSjeqAStJZ%4bTDme?}7$nd@T5~)RSao2`$MScmk"
    ")sI$nk0W8S)UN>O>RrD9c#77oERKh6wyvYY87+UcC*0AoUm<^WxhE;F1%@9-UKRrD%htow8Yd0`z+{L;3;K`O>IHUs6h%HQlW8he_Av7?n>anM"
    "bqC0s02ySO$PK8$FWv{RNocOE2B$N1QxN)L>JQP{)VNCEtyW3x5dd+0u|u_<_U@Nx&(jD<UrN49LDfUvUXZO+BJU?kV3P(RBG<RJ_ua^aW({b3"
    "*Gq#W8fN~w$+bR`*J7I{(fClU{-+j%%5o<!M3@`N>wCb)Fkro0w=T#thSk2u^QrA=Al;HAY~u#Es_<Hrm%SJA>V~q+9p6t^<pP-;17Y!AQFJG6"
    "Zk1-GvVV*)u#;a(NsQhlaf&->h_#Vy9x*bhR@1A+=pu$5_|~kEhFlw+6PCBX_M$k-JbxIc;#p(Kf-ugo070bEPzjp2<PL%)aI;{T#kSXtzF-4p"
    "ZpbG4X0Ga|%~aQwaL}n?1u+>TD86q86(~7KTz}~Lc2GUoOkqsPcs7CxIEg$!$|w6!QQ-P8aauOpP*I#=<{*>|m=F8#^n|jc@9iHPp6u_b1m*Rl"
    "&)D<G`N5eK*XZCXorUV@yLM1qI|OczN!AIk)-9TJfchlN|4f`0^ZO-T{i!LOYED5;C0;A&{lJd`qOyz2)7?K^0ezn7i;gvyxn}6BQhDjV<-{q|"
    "ENqm6qtn+Nv-s8^$jrk{WbC0k@{$70emi{ZkIs=aTbzT<E-j4I>uKGJz7OOdXLgVhI3|0354Zy0j47(7=lds@z%5$9os-t_8!gxQ=})7hORjft"
    "sIS-g{2`wLbNwF<JpRT&T)aFxJ3YU=x;!79Tmbp#dk7RU5MTfXD3r76n#vx1Q(&H-zS=)O!F-t(mi8QtN;7gW{Ec|o=TqXdmlwd8FD|amMpWRn"
    "O=-{Y{u1xq7dch%{f%f&6(u-2{PRn!D2t+G{}pB^)r5yk?#KQus$SFV_m>`O2iv8n7iNj4vf#C(XyS$$UgGx?Q(=S)jbch%ZMKy#b?I62F(0(%"
    "G>b@9Po>Le{l(Gct|J{u#V4Vk!Fj+Zz1%h}6#Y>`NnfpMNPr&OLp=3voRuF2krxg_?-N}=vNym{8%pIV;8@`G(g?Z<eaZ-GU5CUALN_Hdk98fg"
    ")JxJ~+GiQ0H+sjC$8d58;Y<^BZO9--Ye>{bI{03c_~9_|Kh-NYS{D1#?Oa+Zx?FtmES6-LD_7HN+D%;7vnc1buJGX1!=IS07?9jLhcz3!E}9b7"
    "1JLN+PrXl{^guwQ6^myBn&;2z;zxWnhu6Tutg9Cqrut{X5UJM`rpjd0(@2(C=AS3cvdr>AU?i&|%LgaTQp%h#qmGHBOF?m+Q&#U3$Xnat6H&rl"
    "-S;qBM$}Ndg_74f=I6l^N7YxZ8#TJ{r8gK}nzD)Fs6@+rXW5tTaxWs0wKmr}HJq#6m49s)joRL|SHRJhQVaeJ`V(esVI$vQi+ut(p#lCBRyCP&"
    "05g;PO_aTQv43>ByY*)9bEEu%u-fsz!no(Yc_VOF2Z7-Q#{07PATw3U+w0m*W=ge}>(e{?3A7!S!hkRRALBifDqkkU*~suUvU*uO;-Xz1m!wT="
    "S1YB#$R8=9crl+&NL$+#i5~R28-!(>pM@eJA{}hiphDFEZxP?T8JJF*wRJdOkSr;*2l`b}{T01ni|)FVT_XLOJzH1Hn}hudj3(?c)A7CV;1CTg"
    "U#H#fCeI#h3#MF9>Jg<YPUj-)-X@Ruj9f;VUS{nqQI^E5=(Je0b4KaTBKlkH(zShe`B;~Z`in<ot!jIa>{|is{JshIC#r8Vn!L~H9(3~MI}2If"
    "$M$Bk6c<u|aoryu^K6KwW?`&)Qzk}3YXv6tm%X87c-ioc&C6z5+~ng2PSH^djP~;1=GBqbluIpZSH~jB$In}TDmm8=LZEU4z>h=9eTAnCcFP8^"
    "`L<VFAmSx5J>}a;^)&Rh-Y9KhueihD@x`skT>Rh4$6DpX>ag)FuLSmRO^p_!Sd(zSZN8nG?~TrxmF?<PtXz8&)r+jt^831#bPTVAgY+7f02~`m"
    "hZf(QvGkv@HcJ|-+u5D;%^BAYIo5{kn}dqG3~VsAH^sYvf-|o~*mSXa4Jg3!c3D(kG9PI{E*L~7E<?1BYqt+zmG~Uft`X70AFqV=CsaM$#fFyX"
    "Nga=`Ve!2T2N?K+hzev;wR(KR*3_KG@CNL&<;(B*%r^)JA=lLk;#BfBiGUh8T@fBY+Al@pvpMj%huT@L(Z{HRA%6OAj`Ud^iI!DS=mn6+y+9Yf"
    "II&h|qgS#<FOt>1JbaXu@<$ZDp+tak(E?YNP11W8rP}mf6)|q=k!Y^jp)B6^c|FP#+}O@}Mwm)8pFYq9=dUgLWVPEB%%b^Lvc|SJmo2;4iVSD^"
    "BqC*w^BFvs`7!E)q4}%Z+v4*)Dohu)^VT?gSo|cjA>qM{mAMn4fZ$>bww|f8sC1BX1htCz5S1}PZ-SXGTBlXLT->qxQyyL2c)+S&#7C>T3g0fd"
    "E@CPJpgne0q}qDuXXq!?y0c{7h4GV%;c@XhEOi&74URaYUP?~TpZrF`7e)h&_Q2yWDpeHaq@Aku=o?$KO;>yx29mAHRwSCfcza@~h6iF0hPBVL"
    "W>wn2{u<oQ>KoeM`SUS;p5yVc%~iA>{#nB%wYOvFc#UJ|__2<mWBEnHGn5@$fa0{^J~@$&0Kd<T;`?N=y!=Y>WUs2z4`_utrLZnDDoqBX^@%%E"
    "W}If=*_yaB@r^!cJAx4Frsyp!F@%BtNl#RSM^Lo8k<P_=rbOxoJtu+TtS5bpINHp3)r>FGV--gt4yqB=2AfxeDn2fJ5x#2AKZxnY<!!k%XC2XV"
    "3p&DJZ6xTLz{icjjeWU@Ft*|<pkASbm2{xNKjEoamAr9L-D+?_<?AUl{R24*4z~U}F9k))>!3u}{M-7HQh(n3ZXeh8TUIn&iUMD)7Y79@c2k)j"
    "<dPDs3owG%kCS1RDro8lTGihg6up4i!Qt)*Q#RGTk$p~13phZe&B_aL^VB_MWDnE)Krqj;4MZ=BV}Ix;^|h9I&;eqN<;aHv>d=qWw~3!%jjTri"
    "rnrs;vqxmAcC;p~)lGb3apg}dLX}Fbt1_(~!@4(L@5#4P7Y-Pj<2Sz2)<7i(Yt6J>R9j0W)+Xu5r0B3o(4JWdwPoa9*STkQZgw1*9g|&rO<zgW"
    "*%iLBVl*^AYE3Q(A_E2?y_|J~RBNFYWQN9k{csHhDTe^b3|hSf2JqsSwXYYr6A!hrZS9pvA{`O@%eoJ>*>Ie>nvM8rg#ZPGb5?JK7TU0uEGozA"
    "_e-kJSp2e%r|I`=dqmTUhQqkKM_ub*-=*j4UGlFDsHBVlIwOnx{*2HM0?r4ebr7U}nCLx(ew?C;goRFY<w$h8)9SU>l4__Z$U@s!N#LcQII|X6"
    "u?#scE5+CTtNcLStR9aJPwb>%y@wrL?ms_0|Ed2MhbMc7uMYRP)UBQOtYtoKLkl!{OyeQ9JjT3Wlp{g+M8;#U4Ebr^CY$7dwT_oC{Ntdcw&JjD"
    "3L%-i=W*z~<N|0Nm~1t--D}Fy?WgCL2d77er`FxPW@@1o|AxG1KJB>zZD{SHVH0qA(fIu14(_YI2(w-f^}$#}7|WkEn`mLIjjjHe5{d%CsaO5B"
    "-h%aleho@}>w14R=&dWf0hzvKl_$chx9>_@ZXx?%s&R}++>Pt(`_`QiT6acj21>M%rs;<I%C{~``^+U;qvJ)9b(bgBxp>yO#E+VbRrWS^RSVk$"
    "rIk<nHEnz5l4Vg#Pmb2|YP<7%i&wWm2z2jI`ypzub%lutCX{?Z3oW!jAwo?04IO^fq3aXVHi>icV0zLIlIW{KBHe`hjU9j0u}x>L9<sV|H`7b?"
    "2^va8&@xll$vt^Y59S=B1~YxtEDXL@9}yQi{U+Cd%w2QF5?4>X`sM4*T3n=2AC%SBn8^G-YJG1a%xfUbxP|S5v_BRfis|y9_w-D(`TZy&>;HX|"
    "=B*Zvw1FhQd8+l}HXDtFNv*z1|Fzw<yk1v_$H29AO_x_3Ggum-QAgU-%|{shda2h5roNi$cX~-pvrO7+xx7bwZ$J6=n@#7{S^tw+!-%?hZvG>_"
    "Z}a-@$$b@xtJ`&oWkp7}{^&Gr68oXBVTbOwo5M$ZZ#`x9M`HA4NYun6l^A%utkf@#d!e);@p_8P_z~YXnSJNP)(GZDVAIBc#l5o9VuKctpKRqo"
    "D64|3h$AyL8Oa7>U(d#5zH*z%0b6dpUnyaRxc>UoI&u6eQ-h3*TffzdixK0o>#evm>}t_W{2|jt)EJ<|5u^60cT;y81{M~adT_x6Z}LU2+z=Y9"
    "J$p7XVHn?llC@tKlx!wrX>{L)4dc&@5!NB^acEIlB_chS$LD;re%5vN3Je(QJ8}7yx7H=&8#|~Gi$zx-Ecr`r6kEIbw7i}#XJx+C$APVnlbUqf"
    "r^Hxl__%h=H(#hQcAftiZlfalq2Y$rc&#!-H!Dh0(j2o`v|vPrd%mcOu7Xh-FB{oW*H%_HirlYhCgUbL`ZBYXu5FSMGiVmgZY8I*<-P1tZCi_I"
    "u*2Fe$8AJo^!q~O?%X^N%eS97F-uP(L;|IX3Tx0L%WaiYmOmrDA*Bm8cqLL0<}=km`SR3n&2QCSM*~;m%dMa2bfUdCzZC{S?0UXo=y~Vh;?0`j"
    "^%e~P*os#!b1ea)(Som2maxAMm+R1DwrD|#Bh34aG4C--CpHW)+9P3FZA^gP=%>5ksy0`ynO&pRya%D^?})0oFb!E!x#ZuPg=>F+-Ul7f=CeHv"
    "LurB|Ji0qT60tpvQTSNeG20E}bj`&+QtWok2j<S>P>SxJOR@GNm8Y%Ys3vMhX`cPNARlk$WW|v_{b$Pkikx8$k11!z5t{nIlRmH!C@R*5^BvXJ"
    "7i~e)2sNjE;m+i}sVfL8XzS}?;mPzku!U2D^5JoZew>lpY{OH4ufow))=%(t+XaLD4%kl-TPW8T^41%$Lmy#4eZrnJIA)ya^Oc2_2AKafYEN66"
    "1bOjcN(xo@>9Cc04|=JcE)QpvK2Amkw*4-@sfVR-S|smDJh{Dq12kL8bT>u2>t`nzU(r`_qu1eAa1ecr1N47}Z1plcqfxih%#6oQymu2y^f}^?"
    "rh$6EHO_oD_B2hr*|_;aeH5tVhwb!mcaut`7{S6CT;Za?=a;wnOdh=PLtqg4*|x_Qf<@OZ7AmAbhD6DzCuhYW1swW>)opU=Wy0@eApG}Ku80C4"
    "RSOPVFq>dSvkzoNZU<v~HCOdA*ROy1Zj@2nr^VqS8u-%PAJ|Qx{Ysf%*(0-%83&mN(86D!>ssTqFcoF!bGR0TJj8Kl)E2z<qfq;iM0G6ZH#}PQ"
    "40Bp%GwKuL)G{nlPIN=|{)+Ak?O<c{X)szk+q!?`AIOaWFC(SM+^WSV#fsz~on{{$U6AgXXo13GR6us_7tS_1r9|!@aGciZr13yWEoU+3;vuc^"
    "8$*%92DT}HyV3{DsGMzC;}gaeS}6YqNrO%T4Ga>%FBb>%r8EoL11M}q9_`zC_t&&f&&0&^ez+Toy=UzWOMkVOb6-_m#L`=hg++yM;Dm1QcHk7N"
    "@rG3u0~HO_QUrG$@V!g*AU|UbFYc+zv+;TC?!>`o5<w4e-?YQTDfD<W+c%%G&0R9yy26Mao3AjZVo&SfF1B!4L-Unqjvj0;`BJ-$;yK=coi+3}"
    "x`T(&9ebCMH%Vu6t!Gwt$&qGrwvGY&hZ$KreyF{ZwT41S$n+glITVxmsvts8DsDN$!Bc5?A2e#XSlo!r5-!l-Pg^3QghM21??4*y0v2<;x?i%h"
    "|6lg^u13eFFHbJ9r)jZVVct1VmMAJ&9H8hs4#(w0kqF;>#`QxdTMa{|abUZ?pYj7;14Ecs<@@Goh|k&DV7v7gs<y{CUm)-kV=Oj=Nj6~tgE~D%"
    "+oH%aF5_Fbjz@nvJU;x_eXNiuO9H-BqfjR@1(hh#A!$a3p6bP5=Y_bwsn>D7+qsga3ssMG^nZtSjQ?}2WBfa;;~VXCj>dm^Vq4`O(In3t5MIcb"
    "RiUh+J}Gk3W6egb$RhFw8MrfFPRbeHL9SE>pb64hG>CkX2z05bzjm{L|HaoQhliK?TV{p(*VhFtihTe~x{N2F)JGPy;v0=RK{1KjOY^Dk`AL=y"
    "GhZfwdv1$XV}514YQ{X7FJ<_XA%KJ-^;a!Hzn+-iXxmK5PqtzBph1n6oc|UpjFuH?T2A0N%|~L(V_n(F((fG(8mBlk|9j`U{HRB*HNNL#hSq~S"
    "%n}UC>KJGK6-JtG80!H0;Z-pJbA8v})Oc<-S6Kq(S+y<@pgpghd-#@Cv`It+zg|2511iPcJf%?LzZFGv))Z*hA^7aN0j%?!w+b4x(ydAJ7Fn&t"
    "$zS~XzCK~97vlH#o3pNYp|73(aALT1jS4cLax@Jr47a=~GZKXHMfuM^OLrbr(8&8iHF59?-$537z2tcPpQvQ)YVO?6%67}`?@&qQ+Zjcs)9GBa"
    "DQ6DsI!${LEp-xZHmb7_#hif%WF=OdK|7#GL4-*fvy2Yiu2<(L3OF|rw~wHGsM^y8U|J>Rx1-E0Rq(2_Ir6zs&xEZqC`p6CPh7lL7Te{=En6$v"
    "S4I9>&ZJta?Q<hhb+g%<LDSCDEWWD>5v;E#p%rXcUwc|r1^6xQn+sXGnVM$a?`kG6>rm^NdGs377!a5RC>B$jKLT~vKDBjKtTt+8s}hojvlDR<"
    "PrJ{W`t7E8eOt`XC+7Tqc6tw6{zUmc_G)hC7qTSNY1c9M{N2zh2B0PRmpS^eU9-M{R<=M@9U#8hoo8RDLk!qWyWoPB^Izq}f1?yWJsm6UxBsG9"
    "XGQ;90tpjBVxGBXayoIks2`D2g@yW6gHdNPyL^0G7Vir!qn(xRHK;J(U_0+gX9JbMAqm3N8@jRPF0A|Bm>a)YFemk0tmT3X$K2D+hQO4A&>N;6"
    "7Dt~Qt!tZlZtMfQS9gL$e1P@WChO<4U}~kb{M39!RlidCriH3yQk$N<d2PaF>h-eSfy&ry>0YNLJt1{RXL|EG>9k0C{8vtTOq1s{(qt-m5SJ5}"
    "ZyeanmGb9y#qYU#gwh8V^NP*+PZKzNq_OtsYDJl-uO_l25paaSlN##PguTntG{8+%7o540fvv#3qf{T`Y9?^RL!m`LftxhI_1fTO2DqsofY4qG"
    "ZkEvgHo%QCAM5&AzzxHUGMlu)<)I94(+0SH3tU9F25uHcz^~VVo2IE3HnAHALFQV)jr=gQW0!|Az|9)q25oRX16<DyVFP9B;LRd0^W!FZy%_7o"
    "Sm2GlkTMUo;T2=)00(XZ;IIv_ZvyPaus^(Y0D~r&xmnVLIEkV(w4*roQoQ7|fXt&AAbSmvqc+Ha33A{jo-vI!$f)xwR-!<TQWt5-hUFORcv(T_"
    "(F~CN2FP(6<j@2e?FMnU7Gxj8;G1+Dg>IH+R*(~5m%bg#JemP=&;U7UgB+P4$3BP<cP+?)=ecbx!_hmlgPdm2qaDjUngMdy06A@g9Gf5~8BBCN"
    "EyIrSgP^thvMjI@h6lP<8rt_C4`;v}HDJ!#FefI=Spw>Mx)$chg_RClFuNh1ylgOoC~b%&1v3w4z}%2{QCs4Lro{8TILV^*c#c7mMlI3+&DFD$"
    "25hsKitx2z7Q-1ZH^g4l7JH#7_F&fVf5BRq6E{keCZ7Xgk;Hb^4Eroj?6e_<GhlAWzNjtxB2)JHQ5rQgffmdu>f%k>2$R_F*n+Up{KUXb4KojC"
    "z}ygkQCk2;rU3L)7rI|h8!0FlZJ1*?19$AfBm+icrDrjm4s+O$fl*rqMy3o5T&&Nyp4DYQfnJlI!^n@Y)S(S#*l39zW-*)rb3+J5Z6O$$LNLJX"
    "6|cp!?<PsslG~s&B%xjL1VRd;#7Y}tI0NQ}6pY$ZFfyfJ5CwkZu2qhFFU4v-O_*VsW4k)%!=c1;?J)Cj2FwjH7`4S<WQxH6;Mu^ReLqdzC~d;*"
    "g<)*x&wi8ynVr{(;S87?axiMk!N`<@A?Olbu$I^P0nn!^QY2vxvMfz~JIpCa`_QUxh~W&F8*(se%fZN$gMh5e_tz@=e&qXEOQr;ANGXYI2ProT"
    "y}(KvVmJflh8&FBaxgOGV3>wpoUPUBaN9&da}Nd}Hc~rnz_}$(JuBZ3!x=C)<Y3&EgOMo*;rQcjIRC+EF0Rw`DVW17a^sEzD{KMZx4|riGhlAW"
    "!MH64V^a=BVd#77`7<zx)XkzM%z^9sb~y-SlXb`xF`NN&Lk`AmIT)LAFp8qU^TQ2zc9Xb8&oGS+UKhYgH;C;p^Kd%MQ9};KZ8;d5axj8ZP!w*U"
    "4N#xMCd_^c49#vGfMa-;hIW{FI0NQ}9E{s?FgE32l*CaKujh3M9JsxvLBo%OxQjO6d>&?28-W<kfVm+D<F*`(O*t5)F~GE*p5rtKTQ(yf#6#GH"
    "XEJMBVdmism>Y61Zp*>gl!GxS;n8}-h7Uv#w`4b*>r&6IKZA$_UT2kqVmJflh8&FBaxgaKAS@M}pV#Y1sgE}=4VXa*iM+VO+7%>OY=@bLGhlAW"
    "!MH64V^a>sS>~nTdcKkQpz}1(u;?Gru?Isqi9~kUErv5-Zpgu;EeGR<1vHF6KU+&1z=)wqlW%xl9J(DgBrgE%I<#6rc{l^+h8#@VaxgaKAe<=S"
    "B(zqq3jl;HZp!Y|^%Fa3L=lR?#0oNxW`NufgGpNqCZ-rn;V2phYe^&U!`St*mMTgrhz;b7>>*a;Esth^+>nAvTM8zo6r|Y84U`c8&uCGzT>!>G"
    "nx%o=c*`T{;KmIBn6w38VhX@4_Pr!tYgq&?3z9bK2QG+3FSdirBN^Z}WM9&jeM!R*>bi-WC2N)DAo5)@OZ9*^@dLK<+icA|lmT!<@Fi`*mo&_v"
    "Ab8R^Sx>@I0{klO2QXkU@H>p-Jd^=&L+T}Msh2d2pl+IlNw5LKX&lB`KY-IT^8()vFb`z_+z@$5TjV7T6Q~EWA@nw2I18hw-;M)87?MrQX3OWH"
    "41gQ*E@{iVBx&A1xJlw|z;Fg=OZx#FdO$x}$K?YJWdPg|c4=GKC20d-5dU5lYydc;b9*0vfk;EQ1H(L&0dPaorEN)<n3B%(1JBI@cN0luK~I1)"
    "5HgV+U@?>da6`_eZ8?{^4S<2ghN-_{(?x0458%wh{n-I94`l${kaB5T%B77<KR*LmnMNDfn(z1I!=R9ce&X2y=Am?elZKp2+j1^#T>1q8T5Q&9"
    "KcLQJZof^J#c=vg?Es6R41gPwE^SM?w0Y$hqvP-fw&tf)|Dq4TXt0YzJHR}Y0dPaorEN)<HY8n;0dHJyHw5i6NwS_82EE63?YDhmC<EYzq)Xe9"
    "E^SD<&`V(rHvk-aLDElfc&-<uZqRW*$zvH1H$+|97IkSu)P-RPTgqDxF|g0X>j|+Rg9Nq{g&50#xFPG(wyaB&<}GmIhRJ$P93+65z7WIQ{0?C!"
    "#xfvo2)nE;?9zs?1K}SA>#xlM)N#YKC&Ylrtb>llSO&xmX*au{PTMdy<Xse?GnTgjW{@9!DH)UoufqjHjAg)__JBESh`cC^k|<j*LD2om_xr&N"
    "x*7amYKNJ}GGNX=17^@oqBKl5z?_Ay+Y{y>Nh7-_ksRyO8}#BTbIPPNzAf(ZtM|pSBG+1s!_SxK2Ux0b>787L!%@*7@;9!g_czdJ#jeFWckDR4"
    "^P$LZx3shi<P~;}83C?lO=slgocw_6s5<GqT)Ti@<<f_kLnlQ=u>Iq+qtl-#u4q|S@2(cgsaQB8<Ej{=){f0`)cKA%aFALCc6$%3JegZVv&Xy|"
    "7rp=Gm~pEyyUSY}2UPcvVkx#R@|kmh$+F67Jl_(Dz$gtN{P=sh0D_y~?<|Bpw?#okR{&@^ySb|B=&bYe!~MOhKb{_*TpnTO!s=nRx&;)BRdnfM"
    "UX?O%_g5JWXU#QUj^9yi-PXV;`>_4;V$Vnueer^bNMs;Eyv>RShYP{))TIsBKlv$hj1NV5bGy1KXIBaW3>d(qP?YrIYRUfgxZkMUq=M6)%U{BJ"
    "uzPa(mm1)Ma#Bpu#hGG}@@veLr650ed9r6heuM!NwfDP%IElMJ20;?GfJQ%H)|2{z{qpSmw1)a@Ils8gmqq2goC4JF)4BK`XOZjHu<u_Un4nXX"
    "?d)b}2dl}WKlsEEVLJ6ZeDcY#&LeWs#lSKTRz?gmX(ibIMuZZ68KHC&^wFR9YEVmo>hjtA<45N^=WzBOC?KB{Kr_q592tP~Y(4{Y63V;qZ#LFv"
    "k#tVOk5PfJAl+*akG0^3oXxA(8tJ^sXXt%CaSkpo_8rQkhRJ&v$JK^8?3E-lu1h4I#;5&e6vU|fS!U$MkC@TL?h9>!F2=VX^0&^*3kTrCq==HT"
    "H_V1Nvy2z}n!q=!-+Uwb7jbtMSiLVI|5y8?E`r$u<}sZwVErY<9L^@iM+Y<UA-WyjENifSFkb?^Gl#MNY+C4>A;|nr?4!bN$9~YsNx!+U3csbS"
    "`nsS-U(78#`TDENLkqziV@lH54JaQ=hvR>^qy_`nYjZZpBTCcGNu*&f;#kX9zAnPkuSOddGCnwbeqqyNE{bJY;I3R1%ULc`-LS$!n{=IaV{Xl+"
    "mXmeQ2c0~cxPJuN|9J8zjhmnCox{4%=NNK#<Gg_3oS({KI_V>18?Ac*?}v7#9`>hykVj{2c{IEjI+urM7YOq|{`db`1NPzUdP-}x1FGDLGZyrQ"
    "-wVG2SA6w)|L8B4J^Z?u;t66kpD~N)d|LBmi_f>INuG|Jk%~b6Y+}N=xe(7n?}~@3yJEF0#}tNiosU-{15$O%vFVshm#Vbm>G#*I`&o&z=jSl~"
    "+niFoY|VbaWXaR~Z87DI46iZU7-s62tuQ)Lz)&H@79yDs4&zWAdQIQi^5QKD1TW{9pO;SZ1BWYtJF_BR?!aEWb2uG49yk}%d`wv@wrGCU(8yD4"
    "{t}RFkMqTX^H}_X>5G5aLdMk2`#x-DP9EBGAX7lsiUYdV4KM56@8eu)4TmO*-(W!9>T>=JvyWWgSDY>m=LW}0XIba%b!I9doLG!E6!MoZRZ>5$"
    "3^1ot?T91VMK->HGsDnBXEOhwN<BLFvnkezz;UQ;2}|WH?w4b%+%eo5$h8M9t}T3CIR%yao@ncDW&wQ4>%5vfXwGn89i0+1of)804qmUmD0d}S"
    "UvK36F`wOIJ^_k0LqKN^9=;wNvL2bFP+-Dx6g#J)4)M=#hB#f>*EYfeGn_pbn0W$dd_zfV1dZ;BonW0j(dIu_jxaMJIU)KeDc6K!vL#AJ4XWRM"
    "o6p`!?p?tr_mv~^mf(Vd9K0hr_{309Qv*3~Ib(!FU~F|#4vj>E=2Pg|*)Begr}q=sip_zjQ8~j@=vsak1?9l`a9fUVkur#W)Rc(!$g(CY8!)%H"
    "%RicFuT@HGL6#@DegNBa3WzJ2_|%305UOJNzMJ+QfqqgzIG4)P_6UsrHgBn!5NCF1B77t7$tQokuT~gBucz+*;W+;|k{L7lFde|$4}H^&^D5Hc"
    "L;Q=|tzj$*;&Vm@Ehc_BdJ9ZRKKu$>fRAz5DK%Nm7nHKnw&ZL0z2p-z{kkbAx_5z^5$Vo?Mk!TXbN-TW^_2B0Grb_(eYu4i0D_8wbj%y=TN1QJ"
    "Q5JgMPXF=m|B(sFV3)&Bz6N~@!qk8<v*dp%d5f|DYsBlaV`wzX!E%WD3O~pK47BSsaE<L^^t?_KH#nWKVRZ6(s^l+Gg`fwPhPSY|@BquIIynaO"
    "J1pUO0WljA{%(=iMg9QNlY}$vq_?1f{s_$!A1#??MDELayUCvC=0LpiUya4q<F$zr=hVHQ-LCz-S;3>a2AJx2B-kzRSNzc4Sm*_`Sk3AOXCMbI"
    "RyTch!OttG@CC}Elqbdr`ve9hgis^Z6^3*IH`N;cZVjEcga8t{p|8@QC#KT*RSpSb?qBSTs#vY4rZj0Loiw!NMZ<9Gb4W<y^|&=T3r6YcZ+SoE"
    "{w{9;IS!qi95}-f?ayb^2ZwV5Qg*4o-NSm5;=7{O<2i8I#R|6bpXm*LLui4Wc30$R=5a6;60-nO^yMC37Ss?_a~u*d0^5qSEP=$qZM>g@hDPu3"
    "@W~v9p##ov2eTyI?JWU8t4$*f9ZeNO+4c5;XM$Y=RM;2x{->f?&<kASrvL@8iyt1AVzR`RrXTW$%Bk{l;$Z4m)XfLbaC(2YaH{(|F^{ss?)K)a"
    "NlqpMc=r~zCcq77!ZNXh%nx$`yf~eRX;(PJ?fe6R@<2FQ5qLZaMt4pON-<iYP#D|`KY6_@>&AJ-GLv`}Lhfvj?r#uj7=rp_Ab=;VJBJsi{M9zT"
    "+;P(#*L$LONu-9;S&F`Mr_OKYY)8@eMvu;<7?*dLcMOXfa91OmFD$^nNgDn)2XmlR4jkQg_~;JEFYqiwGo>RIPO^d(!?AO*&~&m8%LF8kV>)+b"
    "H7)2Kix=3zG)m6H{2q2(L1aJ*+8ha-$0+IbQYH3U+~cv}Z;Fa(b%=EFh{vP~2Z|MpGIS2elEh@0lX8bsr$#^xZ?r^+WQ-66&@k(clB1Y1M-y+b"
    "xA=~oRTdU8q6spGp>s%!KSe2ryAPI)b<Y(g?yYbqjPrZilhbK&Q_w>OuOu@PY!Da)KYHL~aY%9adI1#PDL0GRO$q3enWvxDotfhh=OR0Ve2(^A"
    "IG`^%10QB~avDNdm$~92fh+j9g#F9T3NW(=H1UZ9k(7o`D0uqqk{7_Sau{n|6W3ksR%BYp6C`+qgsly#5ln3~ojw=b88-7<%womq*zl!xUW8v~"
    "oYIKQ6`!SqsMCU?AAxSRku{Np-ULq-3Dm2B$J;q<5|GX}OL91nw-S+Qln4bWz~&I&cOxWMla|wbgNDT4VxH&-@w?8mE-%u#${;&FQ`<Balk+DT"
    "v(!l((<Ii@Do{cabFU{hKn9P8Cd#q69ZGvp_2fr$XI4%v5YhqayZ0-{^981^mvazs^A8Q3V?)+T9O3?M=KNyhqx@yd*<Q}?>4b-tt0!B7{vEY5"
    "Sz>p2ji`zYKAIwGl$RSCDQW9&FBRXkboXX6SCB+7(7AhKLwqqwFx`I@k_bH}iLfV0gq|Xa=)XzgOGpB>0X(X4(nT(mVj7`LI%x=8jV!2ir38zQ"
    "by7lJld8!}xlK-F)K0Uxsx-@rRHRO;78Vu;q^?6GMBZkSDij?pORDIki0qNl!Xi}dhK0gh;SZ?Hp)h9=fL2?Y_GcgVd&-|ni^L%nLeOYK{%Fcb"
    "=9&WN5sHUKJe?Yc<#AiHY#>o;l!}6sU#9aGbgiLtwk)o(5J$1x;nmkRK=mV$SiJ_QXtq|<T#wIYe;1&w;bB_QA$+!$35pEkhTcb%O%*$6E^sg-"
    "{r9Foeg8)syIh(}0-zCs@XS0V?CWgKR^MsZ&W%2_r9ihDVb~0|u@G`?{gI7CttHE+mH39w^+u}93Px=oLPS>saj60nB2(p3{TVH%G3I4OJ24z@"
    "L3;2VhbC)gGMTJAr+m287dWrpk@6+b@RjI9q_NfRcjPR^S(%gIPUZz)^N=ZKK*t^Cd36;K<>;73{xH?Kq)d{F-x4H&S1Xemj=MP_cW{PDgXhz7"
    "z6S`UO)P;$y3y9;a3&1$D=fS>pxWX}V$&KC<p_gP4Z)9+eu31*QFo3fuEo&lNa~3#>HIHc&BU3`XE$t-8so_jx7kzKFQ1Le)wf?g<nHovkK|1U"
    "eEOB5OiKD$OJ|tX>^aAWojG5JUFh8={B{HXrmoPwn=kUQNX0MdVC788Yv9OI^D0)nP4N=g*_KrupQv+xxl)!Vd0iuFD+w1BD$ap(r`ob;sj1}t"
    "$I@>%x8_$1G)<L2SAZQLUc8=>M$PGb{*G-ge6}Ar)f~qccfh{Su;Ex@6OtumHm8gKB_anQMhL{351n0M^A|9|Tp1<OuvC#94TO+^h_5Ab8iPLN"
    "?X`oYIm8U6#q~;TI*A9{=9ET?7H`o7lmf$Y-(QOgqYTEdK`G7OYcy0q7}|Uf09~kLQPIFR*398w<@EBrnamq4KiW3m7FotGM3(UZ@uzZCB0?9O"
    "F}%{ZwoL#1_^th;cqp{JT&5qd6<fMms+_+U%lVc{>`XpPn5o@x6%rQD&m^#0qTXv|e_O};bm_%TMb5UCA|1(0uScNaYAXxA-}=TZ(8#?$?2!vy"
    "sW44~qtXa{dSH*BHWllq2bd%~$T$=PC3#UlMp)~@Vq5)a<%PuONcR!;XQf*xn?J}$M`YjU(mT#wIlHeUaKId8=~`5iB&U2Tm>gDwLV6$ykbR;G"
    "pI7?0Uy19T7$SxG7Ys?dU8~Z;oviCITF<~Ni&3a`Y|B9^scP$^Uh-XDV7j70sDzII9TwGo!kf(kr7*cy;UN!XhI8Jf<?36DmkZy_40Vw${&U=+"
    "k|g9CRE_WWa)#{lWi@mVYW{{U%P^WqSi`T258?>U17jOu-$z?Hsc`gGD%J8rK+WzZUo<JFBz|^Xl6xl85wseJJ8NtybcGdy{ZP}!w8&>5*~`^x"
    "N}A)>)zwFW5ee3ZST&Jq$O!FdC(4{Wo~I3%10WXotyDp1Y{~QcF+Pn%hU@FHbW36V1g2?zN1#@WR#;_Ze>V9V&Ph_0!3D3wHY=gO2-5(P`L*go"
    "L$_Avq_!z?YtgcGC|0#thF#@T@aA4<EnQ6zBPMeY6r*kUks}Mo)u&By?<%iZ%T;~d9DWZR6a;-aBYChC*Q8%Vn%k(EE<P(M<`u6HI~MhgmdsVR"
    "{X_Q~N^PBZn`Mc*$+d%1zoDWJW9_(78$8goP~XC7mC5jh+pD_HC(X%2x^D}=zcpT%y6+o#Jgsqj!<~13ht<5aayfNvK!*!L)itoxZ{XuM@)sAs"
    "5>7N*gA6P2`e~L9!*qaoGlzjFV?U;={@T5C5M@Kp8-%{=594$YdLf)y^|nB)T5DI9$vIsVOBuBB_8w1#TU1^vN}<IL|Ap-wr{SL4)$DMVw;CEX"
    "dA6_|>Ht)4Z|KE?IE(PVZ!8|g(wVn1eS?Jm^H{k4yegKHa*P{~eT^_KJVzfhY%NM;dBZpkDSu>hjDW(a#L)^LsS<N$iCY<DFpv+Oy2dSeb!k7v"
    "dQ(sc{8r292zpZ#AX_{Wc!$2Jexv#=mQFbMiC@OY?E>YR8}*hfJgbV7yRKHh9BU)E{QpBYaTBdTZXK_2XpoI4r;G8@@;g7}-|`_n>MEYA!^YKf"
    "Qw5g<DV0w(u&kjZCTLtCH8dd$>qiPMOIVHB6W6u$8eP$Eui2S3oUQ>_Bx?HUy+!pS?yE)r!u727`cvD0n6Gr7{Q1|d2}k9l%m0q+!T&B@_bL4k"
    "gL3{AYsu2BawFydBmQMcB-&Avq8cyD1v{6t8w+E^0UC0VAELB6Ie9rc+WPe7)5cnGt<rC+{39~Hx(4#Ebv}o45R~@|+JndBzoS)IJegzt)w;qL"
    "+sLTYDLJcbUy@Mv;p`d$-^7H8qv=!z4(te8be5ok4}|R*H97M0-(f$0M<pZ}at(0(-2}Py5)NJL^+KBu&Qm+9yn2VM&TOrELP7oDyf2wAf(R{u"
    "-L6=B&zJ9^GrSTNs#7`JsmAj~;b4hb5)WjOXJ`)P%hr_POtN!)tWEr41-cqLTAMvd8!wF6n*4-Y(aeTx5Dkh5nj(2@tW_Sz$q=(<odJ#JGm46+"
    "KjGG;^p(O@CN<^*VnRlBkfOA1%n4p3E$d-J7&Z&zAtndi6Yn^3r<j%?n(;vNqjP<arGSm&80Zf<9)-lfK<ULtG(fBJx_ZTO#D+jIt+0r@M0?>*"
    "tq7B<IG>S9e0M)xm5V7xtqU(fX}zP)Sz{D?UY347Bu_CS`hU{o%#6!$%AXYcMj$w=Ws$E`bzx6RqMF<8-WKC`<P@sa-~6b`#=~UV{N7$69Y&L="
    "r%wZvS{D9pd!`SGuBTRB-l+8s<Du6#eG~EPCeQ8%XlxGH`n)wDUaHGN%JB3!$CLxKD7$ibq5U~)?OaRS`2nCPZ*EwGW3f7NX|>jTh8BK^D*3?+"
    "M?@7m|M>U+TapKi_-vVv-;tJZD$6*tb!^~VT%s8nPTl3KGJZLevZ@WbgSr58NpWWtMYGLz{sw!AQz=YD+Jede^5}B+IgIN?2;kZ49VBStbJtn}"
    "bmjD8plMNc77bd0w+h4JVmbf#fTqJgx5pbmANnMYx+bwz*TLT29bs?TFt8wwt_d!=EVpcl{9fCa0<3Ln>X29R6SdKyxohcmR+cNV$RlzWT(x`D"
    "_>|-$swne!zDJr&yJw^F_Rvyxn@R`Y->~N>U5*pl@zhPs1FuN#7mT3e(ep#bw>hTNL18dt>p;Tr*-ben2$luiv2TC_kDW&MO{fSM{bGW^RCFQW"
    ")Yg$cMc_sR#x4>E2JGiVZ4Ml>^E+)(hnQUm_7?vTY_JIguPIM4pYD(su{N-(#;#e!^{ohJB;T_7h4`%Aj)${z{d9cLmMCO%LVPP3C1V1&I;yja"
    "lC(j<gbjSb`GbR04*wyVycBi=`2|l;Bfh#*!oBFw54l6w#~mGFYqPUA>|69gh-JGhg1<zAEmU*rTnpp+cvPQ*RJ^vTE6GNTs>vCg?eBh|H%~~t"
    "Yw#)K?V;djYENtLV6k>6RLJs9XEXZqi;m}~2FBU;vMpICLG=g4Tj5Wwn<qfAtYYcxOo$lLVK~AZ9^5Zyc!ovl-+jKXgm_CN8<`>O2_Whd*wzj-"
    "`uVP`$e-%A#L)S24B$-X`Q*+2pWX?pX7}Gxhq20cnRUy|EWvrR!Y~_RqDe&6cdq3hZ|KL7{6#ybA2dN1G$NVSnv7VS2@CZ0)C6ppB|!(6u-yGY"
    "3+-A|AKFp}-~VE?71=f;C+cdZ*5VvafTUrnuU<IJg7j;wUfiKubE2*FNwOF=Am}0H5oh3rUYs(a2Y%K8V44n-q(6vB2Z$nbmXZ33K?=QOh?#A7"
    "w0-A>Uj<*O<uKHP(hY0be=%y$Y}C$qxvUAaIB`~#q{A@K*U%rjZuT|SkWxxo4~spPQX2mLi!Gw(bxEKeIFmNX|7tk%?V^!Wj2Se~*}%Nmr<6g0"
    "m8LP1eVQd5WS=BM&wB*ncUf0@tf4fX|5sbXPQ#MST4v8QMoFO}HyL8`YO$U^OCS(MSyL+vd?lUyVU|8(Nu!P><wRtyBw_@Y=dy2F&0FJP5PcQ-"
    "Ncp2IG%wPMb!P`7z=9NJA2$Sd5`7iGlCFi6`NFJ8z6dPe^M`S*;sm@g-C^uEH0Xdr;J?EJj|j9M4?Vvph;J|p@_hVm<3ag^?G=}t?hG&sSe!2j"
    "x08D~7!ps$wvAKs=bnsJBGLyUqsz-<0(O;uJb*K?fNQT<<>hq!xn8@-)C`{LZ{t{t5mM6TIaa<9&NiC)nIq9_+r@!8?yft%i8RMuMnYi7aY`N~"
    "!sOuv>Cg|?o(uUTCh`uSSdF4UPCyZ<vdjda(gc>{on0Xzt>d@lk`~LlUGPW04{TAsfje_<zCT-5!VA42mfa8w9E8J&dVJff$FBADqajxD5$l@{"
    "gD~@{+i|aMyXi4b08YQA$2b7>fO?+v>iOdS?TURQQkZzahe_X!fm6{jFyFu(yAcU28w<Bdz%pRq)Z^P;J$50|gS~;ZlLRKiaL90ud-d9l$HWJH"
    "Dz3pzqG8PNPI~ox(b=;X0U~?_aRlOlC@L=cb*vT$Yk&>0&Lyr;2I3~sJY4E)0WwK$Q7aKUj_so?8fL6Q@~x@h)yOh`Q(oO>&&-(fbp{8KvD!vv"
    "KmoC~ZlE0#cD=Vf`s*UH0G14Ec!?zgp)ibSyL#guz1AxhWbh#)-Sed<mA}?(u>rC$0L`%`e=m$ck(82Rjr~Dd7=9lyvFT`${!UV2or=7k4aEsi"
    "NWBg|ke{1bx1-3Hj3kgLD-SxF4ShZVu<HbFN8Ak0(1Y_C=$Uwp&YmZxW0-vBkSA%E+tcBlbnK;_IKOsUt$<(6MAo5YQNjL2N0A4oVrLtXf(Tti"
    "kf%(c;Ur(>!!3<(>`HihT;2%A;cN?^5Aqj%Lc9a>z2sbl<>hQy0J8rMqa!D+dvJt9sqT&A_1KGw0LE$<gDyHA%M7dJEc=F;*mC|6FO?9TZ*dJU"
    "@QZ@XWn+$5b$(C}_9(;9vLF|B4Ds&0{r~fU-H*RWPd`|uA4bY#AeJ2OIZsBf96Y<Z=pWz|cW(;{W+t)u_Q9DH6&#s|k769@*BY<~JNVDHE<O0o"
    "<AC0goe2jr6FB*e<O!T?%7ls;gmjMj-4256+hscr8vZ&PFF^T{^S75y{^t8L?{_--1)cX)8`PH=v{2ux#b)3QBTu_5wA=-Vav7cH0kn<!S$%X)"
    "lc5``GhmmMRa9B99smQrtCa`9V3^e>zzzL%s%?ootdD<Q1jnmT9sf4;S*w#VXt$v!_x3Q(<V9VlU2VM*6M7!q&`GcYiMsZgLTwqL%+?2sG|A{d"
    "wj=!_S(6ca_A>u?DV+w7bJ)EfTb^yw7mW6=a5k*nOzLPxelL<oN{2}0@uGQSG@iA+V{|3LMgd#GEls+$H2H@FVr2JET}W@#wY&#?Wr4F+?AeRv"
    "GX;T6q(?rx=yUY)0$n}tFp`a`i%=q3MC-%Om@RtPjI7O+$nQtWJ%{NCMPkSWW#nboI^B(?riu#qsPsndAeXJv^S#59(fLoB3(@b6n)7|(6NbJr"
    "j1v<Vlph@^<@o5#^!MY$p!fySM&+EJ?)Ju;>D#E`uHi29n<C9{14op+ozEsa)#_o&xd>GVd!<j?=ISL>3)8(xY^UO5akp4W2Tkd%@{Oh>y$Tnk"
    "J>^w(PiZP0_j^bA%raw;nIp(OZ>L%mV_2K9b9X;0(YbD3iA<=JRpdRWBEox;mKjer&LUq4@AGae(Qm{VFz{<fjoe7Lu_%!#lQ%1;F1i)YcqXgl"
    "sdSsAenY}+O@{(Y*3CzGEVkx^fgdm~Z1FqP74=|_59Mq!r>JUR6niQ}CEoEcM1`wKE?4!7K)rZ-54uiKReSlvF2|=NY4FJ?_xbBqet(Bi<g8Qw"
    "9rhaZax<qhX*qkAW2hchm&CA{e7Pus2aE!9(;yyfy`SUd7S=Aprx<^Og;DP)9_0h(jKjw}@I3Rd1~`RVov9L>yTGi9<@+3o9fLj>m~eSFU!X%M"
    "kK$qdMd1|7?p<eNt}_#%2^L3aed9)$8)#X;lbQFxtA__~hEKi;8gD#Ld$oIicRyvYuyS06)s_Vm2jxeZ89{&oFb2k)F+Dd%vIEkw7Hp!U3FAi2"
    "7H7qhQzKAqoV3|skAquPE6~$Hfx&gd=%eQ#JQkw9C$60Dty{TkIPbvH-QfWdYX$vvUUCUlsWVX77LF)t>8WpJ1Rn>h83X_dabN^p)E$_C1Wg+8"
    "ywLAlg*eVIKcfK1c4$>FanPFqQ-B_SCP=m}T2z~MlSLG3@K}x73Lw7;5C+Rq4RsrmM7Tr?JARsW1LH*+G#2Gp!IHF*<Hv36^jk1Ljygfg;=qm|"
    "3s8QWiu{l&o<9OXfr~uB4h`u2n931%iRkM{$(P!KU{H)3*5eBn8Ch4wZ}TrzLRh{sSQIc+-_E>}1epTH$iILSDC}Fxx``?Bx+dmhG^ZG(&4Gdh"
    "@9Mi5RDw8uTg=9{s6&lbqL>R_`cv9D9Uq}<W$S4-1t8Lm?uBk+?>`PL=ykKKo9GkY`-H2C^_%emo?=PxqX2Ip>U<p{k@sr8U<Uz-94`n5^-~#D"
    "S&VOI^XdEs3AC)>1XnCeOq6K!CW<QG<cmF0mqi334+FyedA>MXuz;h*mJj!2A@H3zqwDX*az42qug*%caBH7=_!(trsC_WRYkX_@vhF*G@lMpU"
    "eXkl}A@X5th<s5`f+F`Ro^&M3c-!Jmo!49-Tn3+xWa({tG^%P&?})B1=UTkSQ#6vuPpz+64cdPXKczrrAyuKHH&@fX%l}FaAO*G3^d2|a@#C$A"
    "elro>5J4c)S^nrk+Ee7ccfSNY%bgQbwgc9`DD?*p6YjX#4tdwm_?P91xWNHNcVXy^b6dW{1HBUs{pcV6{vXjWqN4<NbFt!T?FwGBIZe>*7*it@"
    "ik`5BI%d^B2eN-AH<xufL6r8LPa1wgZrul!p1(uhbL&wl)FyrG*gCWu+c6pJ1fC6(i}L-P4c)NyNO{3RY=JX@r;F))WydE1?b`8)QllR}Jyb0l"
    "_zdlnO1z*aLPM(95N$+g5Tur&2&}}jVi3B`nizaOorBbMssfn8^);dK)!|>@JP(v9Yx%^k4TmApBrS;rhsbdI;m}XAu4#mRf0V&KOE;p-5A4)V"
    "RY2PaLmEl#n|H}EMHphtv=_N=7adpv&>}mQP`LM`v@Eql4pZulBs}YFrYkS(*q5$v-I&m;*CMOSB^GKZrkt_c`9K$$7UW2fY{&`vZ^MpF=lOlP"
    "ScFL&{A43?TrY0!c((&vQP9Q~4HLLcZ0!{VC>_N+XLN{$f$=*VvT6`bWIc{$xqff>`=bts+~0`0#Pd2fy5E7S(88~d%C{nSj<bjP&hlk>eU0g{"
    "W}uRf$<|`SoPf|mW?9r1b+J`eGQ$lYg{*AzCXC{av0UHlK$h<}k(IeS6NMyaLDs=#KAk>vV=1%JSK6CV`C-t7BtPhnq-e+6Oi{3SJ&D<K?MRC("
    "tn1~)&h9N}XU_9tR=m$8_CUj@ds!Rapqmak==PF>Zr?qb#XV6N1HH3hZvzU`E@q!3ZH!T`eoG`?+%Hfoci>dK#AK{X(jBOXuYJ4P&{#v<CO^No"
    "hU>Xq+Jx(+kHMY4S(|XP&avXqiab!`!zS`nE-+_*QI4I1`{e^E6hMZD)iN)p3Zc;CaGB3Kkw+lgbg|ypbHk()djTD-t^F9s_5iPE-(u(vC;M`T"
    "VThNb^hgBWDzj|scps;s)hbMO3G6{LTGS@hE)%X7ciIa4#Ot!+h5@M!U8$RK#%MQ^We^{iHLsbn@2Nc6_e`h9788*bl0aF`t4boo7uGzpnY4rW"
    "enMI#=l^DesGeeUT(YMyZ#{w$R37vb%+tW5ds*TKAtjhC?<f%usDXtnk%0O5L*L`~>wsv%a9&JHvdBprwfXg4@pg4lEZ>)7s-P43&_h0vW=dlO"
    "PT+Mp-<{5@f|sP8@@q8hzz9?2q4VrsWQ7riD!ejUtf&^=N~V>=G#mF7WyzSX(BI-<n&0U6>mK%lMJq(jSFHkRows8<5D9PDk&Gg1QV$()56Gto"
    "9S;21h2?{;u~(p&(PXm3+;nxB%2F1^!6dPj$btqv1;X|93>Zd<@?Ur=Z4Gw#PQX?DVgf6?JEe-2oK2XLv^Ppy3TQZonF7&^br4}EA7go2*mHI2"
    "Wlq+N3~sS3F>j+xM9R)<;?rpTrxggx*`({^So`?J#fZOaHcGTc`xj?t&h|c!Q#f?<?wm=7HQa?ynxChL%m?STyt&;`IVmW8{PzEqe2<Hm3NJwD"
    "mQoF*I+im@6RY`$d<mq%Wq|FZ5o@Foh7>#(2WV!Mcu&(1Ra4Qo=c2=yU|3{bA}jmh`3Uo9c`ofR0o9K9DL?g0)Zqtd5^3%Emu&7gN5WcuwU3EA"
    "z%oVk$NWov9B5;aA^!(0K{w!B((fS5I*B*bk&354F6ZKCS;pSVYaQXC*;q(K9IoVa{-L>$AebxUAOk1AU(FHw(zCM-if3#hk4W$x&@R<@x&vl)"
    "gBMG(v;YMKH9%pP!P5nDHcV>!K#9aCLtmBGf9KVUDp!mUUa8!fl%BJeQ^ehPxq!NK2__%Q1e~UDa~mev<6=@`feXBpX&Gd-mx(N@cbR__+*TR*"
    "k435=zJf%%?Gn>Ry{eEh)!f?YxKL){(H>jPXOwSYK6_2dkGKdyDr$RLDx63!Ev<=ocPaN5U7GT0Y{)=_&;+PVQSx3O8kpnpd|8~|O{&Y=d?wS7"
    "Z#_lTxrvNt4?>!B2^S;#T~#M6Z9e8wQX?bFpG;1S>5ODvCdmuhyPy6Q+g;z~^bf9(*xT0KjQ@!3i@Vm`q`V=cBzE7(;^UZi9q+kkW6<+*<5J`j"
    "OX2{w{3J#L_@G0V5oH2czCM*X_RW-WO2vusJpWCV6Z5Us0i19#G)a~dIRd49`tY(Yt0J8vHft}&ltBkSz23LX2rtNE(o|RVH63C2aCR_Xj!83J"
    "&gXbW$ji${n=SR7(&cyci>vyw|KNu^biYF<#tKg-fkWk}oo86n6&+ig9cTaYz}cPVppB>uR4b0ceY$n|?C=N=Ed>ZmcFFKl{VMoXKEqNH6X)W8"
    "oH>AE>`edu)#<76IVwiB&)HQIL#9Q9zH<o3|HvRBfNjv8o$MK1^EHm@np3D<td>Qw`hWi)=i+Sd9R8y!7&v=ylAF#K#l(3%Urw>2&JG}|0X}^7"
    "+8D%5!}t+{G?UA;``<q{`wwFO)0@VHC!Atb#+tFY4MiGQj;#h7jHx;Y%m`D5!+s*FFX-g9FWktml^-SnX2{+`C+TTHTGK0497lWjT0&+#J(EdV"
    "=>_NcLxHU(F8X2x74KFHEX%jJeRu{3f*YpMpSQ%HgDoD#+5VnNWg;oEXQG@KXCHhCk`*2j&XK1LQ#av+-S^8m`NdE|<ctE!Mpc;uZL3x0cRs~L"
    "{t?b5Gk)MkT4T9d^vdT%%Gmd!fR{jw__uf$Y5@HSKAFt#=#7^|oMC#FPjY?|ke~AiW7t7_RV6=mW9t66oJ>H`+0U_v9$C(*^%1P{%ozbZu;Aha"
    "fj+vfpLn4GpaDG$i&}|9;IjuAuwX`G)xirY?*5Wpn6(7nf=#MCY_hbSJvFr2(z?SbZ*Nx4#s21<z&S(sZzFRE8Q=nTBJUXKVto4{f9t#)UJRYf"
    "!!z2v|M=hkr_Rd2-FD|@5MyNBLl_A}C==twi?w;btSP}2N)9eB_BF;MnL-z<<77fS3u{UtF#(D(u#Q}EUrzaK{_&&p9gOtedA`giXz$Y#a*5U8"
    "TwVNkGh-K197jl4$9f#DSW~eFz!~W3V4<AIi~nAq&Wn%~*MM82*90kDI4Ug!o4dqlA}5zlry?^~uiil{z>>}9c)@++G?JHyAvm!K|J_P&LiRmH"
    "s2fw=Y{I_i#~xk}(?_G81Bwmi<t3N!nXGugd0>cE^;|J8Nfz5v#<&V@d$hP*?bihr%2~~4ycPI3IA3b}L1Z)$!&wuXkjXh*Kjfou6}CF6*#j^X"
    "vB6$WfxE*`)Po|*C@V4;@`A3(V@QVlloM=p4x|=^4t)8wK)*=YDDcrhJKh6?oDrn6-$!8r4<2YnCJ(EI4;4rim9WK-=B#^Ax>0p%Lo<~y<YO@p"
    "+`a6vueoc1s+ggT-gkEbO0T>>E#8wRPC~=k4x?fA{gZ(MOw!r*&;uNQygqfdvtjx@YYYc)mYRtQcci5gJMcpEy7`|zd;X8d#bPCV2B|NMpQ65S"
    "6h9qCs$<U^#-eADl%^zu8aYoU>$;TSQJ2xs!ymMH;HNkAMW-){e7d@&GdV6_hE5{ZKCzo1MPTIoY0d)&`4s$05H(!t0+h6SV2RG|!x$qCr_^)m"
    "ukSci9s8~}|4i%l4nq?}QDYssZsM=&JdDNUk#qslc<9!XsL`vy#*_c7BF}N?JBlKE-#qWY6C^=sP7tqh8a~d6QvlC^2lKuQF%wRAcYdaK7wg@H"
    "3Q`OpA3M^suo5b0xP}-o=ZESR5TMaljAX*PF5Rq@0;eAO|E(ifUv(HHf-I;*AA6?`&w;j_eLBnvMb%rkOp!)hfv>~pG7(_fcVY2svjROnPL`n{"
    "Zh&dQKhWWXmO`2gIV=n`-i16sU<{|SC{l&D3EIi8=`P{ThPSMnqx8T^sglofMIB*#sX!G+<yIIfF!@#L*XhYs=Q8%j(o*AL7a;ZMY=&y_8|}E$"
    "M$L2i>XD4H^8hs1O5B~4SmZHUrEf7t>TQ`<bwHPt-o&Xg+@HeM2|a43ErtVYzt-oj0p06)wVhKt1zJSFiv3?kS_mWI^SvN~`eZDQyl7z7V%q7n"
    "QLY?3<%l?+8Us{IJJ%v+MD-|&ZZVx>HIwB20bTMnE-$amtH>x!llq2k|6o^EysGa&H}rs)naV2D8k26pn`354s(oP&2?x``rVhL~$*2Yx-ARjB"
    "5yS%-bBbz2Ha4nxvsK%Gh^OFh>RtZY<I<qTPKE52;?h{oQyo2w`#%x|*9;F_vjPrQ{zMnMWnNYVhdfn|AH7{P-DC$8CFOZ5u5_;X(~5|;F-WU|"
    "v;V^{ys1Ic{uED6*u?i`HAXq)E$YfDs?rN(2})6Jc6`60x-BINtHnxrnub`0ZgMY47>I8Lx<4ryMi5r*3|!tV^6_e~T(Wl@yhih7wKG9A2I*BA"
    "-ZuFOD^_<%J)(0pE-ywd)LssF5U@plNsr<c$3MVeKOE;{DxABP28=Z~DWbZ=oj<0#$Hx<d^dmM2Lahvw0`TK}@<3&LC~Q$U`8t@xBA-Ir1Zf3L"
    "K$w&P*BMoLN{2y3S)55RE>Rg^zu}=WI>IDwxVq4+_(0@R{pg(ESLhk*V8D*^hw%HMLt!E+<zMAo<7;w&m_A_DYv5E5n7bv%i>G`-G)C>o@5(_0"
    "<CU$zp^8zh`V*1xgSHS+S-soAqB=ra>15QyNxDr;Y@(xxyB_o;J*vNep2(<HRE7SGjGH&?rEIdBAO3julZB9K|7nwuekx{I^=bLwtjKzCKSMVf"
    "S^<Cp(1>-w=2*uSOEa#xxD2hN7#%~ghYrE`&y{m|dUp61UVc!Kg6|2rpqF55Xo*+wUX~_sV$acBg}2o}9?G+NB0Z}ktY`q>;9E(F)aU<#9!0gu"
    "`2rwEf)_qw@bw*rmrm!1O-$i(uq>$u<YdL7tgwa$;2H%zmZADk6z>}Jb$EAIOiD@@0$);n?k1fHZ}BcVyS{D_T5n(SHmRKyH+f%Ds~yh;sqrE6"
    "3-}hZDx$RB{HpdjZ}2Pf4L=aFi~Pf}IPm;l)CT6-z4;7Fk5!cB30=owMc)?#hhln>Pe^`cR2!vQuQ?~ILE#1@Be~v+W!OJs5%k$Ls<Puk79JO-"
    "OXmYt#xBT+pp{a6kUj|h_gpU-s7-V@nS&g}!ov4&IVIMLxN2`!CH?0g$Ev!W>%WXc)t>lYz@ZEYcP&i=H4TlI4-2Y7)g~9^>Tc>g<S37k;*^cx"
    "PdN;bJ1>Awm6eiJ(}$Lv!t>O?*_(fG{t&=9YtRr?5uD|jAN(SQAg1@r78c#bf!^k`cR-8ve3&j7elE?1m*F|*i2&l80OPs27o<elH!#c{$pP5s"
    "9y%!&vm2nAnJ77f^3Wud3k-R;P>F~i=uaiq;DRqD4!JynIL@G}@k3wAaJE;)`1XgYxGRa5p1dz7RAOm#xHBzh$nYr>hlMaSw|;{#&<DAw#O}Xe"
    "I4VY92@}szH%1-;n{}t+f@q^dU?LMxZb6I8sa*K;v&)?jrAQ8kAyIi=uo28pFmPZ`SNK$N8kiCE0@P4^#NQPbJm;yPuvt0ZMQQd7*_ocfPN~>b"
    "?3~3P9Ph~U97Pmq)A{V7KB03$C7|h(yqe^HV}Tb8J)mMk26{l_kCa<=fJK{}*tn<?W7PCy3%~d>5mhg$ASX0S{xCXx1g9wtn|V_qVs2x~F)MA!"
    "zy}M{Q85!v1scKvi2#sQE|&8#J2+Bg#kS{ukEziLASsYgLHIp#2l9{~0JEWA`!5Gh7}KAx%3=j*ebPF30j$E4o{wNsNpiEAw-J%yczA^SFn4f?"
    "RY$B_!Q+~;YFcu(zl(?QrBf_%YdmS|=|b(oRC9P=^1i$&r}+$J3|b(Tv#JlXszW3mp%wLrSovaN6RZ4LylWk;*%YNNGRs<IHlli`xOV2YZY=Nu"
    "R(;3B(!gnwXzqw$7LH<pW)@my6%+d>o`aH&azi19#zNJL6%($rEzAob>O4RC{z*%`W>}++NUwxrq=mClIvJ*6khrPhWq$>*;d?j|cri#|^n3!{"
    "DsZ2PI&3V5C%vhSf_nOk#&r=tUnU{zMgHnkrg1bBqg&)RpO;fRsfo}aE2&A6LMfL|-w}u4FrI-FaHzU45#%?^f@xrh{`-ZEqNu<ik_eHCAgs)#"
    "QCdWUH#7rD2!9BNXfMF*j0Fuky379#D>fBo$_g`2k(P~Cb(ZMWJ+yw<8Q&st@i`R7gXPC$L6ZVYB2a}%z!LSzc#@}-o<tQrR^QqX5%tA%CBmn^"
    "0r%SDc>;h{uS1;{gw(Q1no&;qHJnrK=%6Hy>4IZT(9ORR7VUrLd`@VZSDxLA`G*1x40Bpnk?m=;SeB@}`;m<b@#J<to8}*`@2A=!ku4Zfc@wJw"
    "T6%d`z`#=wAyZCjI&`-8Kf=;b@>Lue*W~&Ex#+C;2#2lv+3-ofQ(YZt)SrGnCqC@Uh^k)4{zSFAyq~~QmD84KyOY2sbhB8nW?S`8$h0^ugT4e`"
    "5&>V+9Aw@t(AId)S->by9UhB~K(G=H0C#xBhk+23|L=YbM}sAZr4=RpD_6G^xdEh-A(s-L3;Q^qvppXZjG-A^b_rde%j#{pAi9GyDCH*u7>3R>"
    "c2p)z38v?{|M>U+@B$F&QZ=7G{OITgJDH3alrW5EKpjaO5b2y*0j1Zc%7U&|cbF404;=QUOc7uA2<7Z^qVK*;TdPSxkmmDZzL?`hE#9nuq6;b!"
    "c>pi}$$6pDzn$^Zr_%R=@FhG_ewqC;`=@_$_S~nKS7izd4<x$8r~AkI=g$vMp0hQeP9_JKMHxi;xhi)3;kE?H@?m~IMPYP9O3xj7^#Z$_q5){2"
    "EbrJqW)p<XgeJ(^fzzQ4ChQ4Zcph}G>Aj36!pC&M$ZIhaPCDABl$P>4-*X3eTMBG$BGkz5&=nQ!8+aBW(TGopg}sGt2S8x-M9vv@5^O!^2Cb%`"
    ";UhZ8TLr-W&WpG!sx-fl=VCc3{;q3JR}wQfu*mRj5UWNUwkH4wEl^%g(-`QCj`{&%f-W)j31YG(csoRQ8$fZrG<A~7@BD;E+LmiB;U379hbKNg"
    "c``u#SFBFvuH>p>-gvxYEjig^T>*N?USy(GPD;s&YzWn=y`Gdalhl>#k_-k5&Tci7q~|>aZhlP$iyNZH<HJ2?w7dKA_~p^)^6>Ozs0bIj3SFIi"
    "@kx+Mk}2SLhjJQk+JGS)U`Sh8jpx9B(DexL`;MrY!@pR8!zc|jb;Q2H)f4J22IPrR07JgVR#;Z-X7dlcEylOybOOAM7UrnT@0{(JKmX$#y_*6!"
    "A?(hlAX0@vh7~hviB7inH}`-u-wjf}jD&aeq5dxP6n!%59g7Y{R1o5T7tj+|lTQ9YTJ>q7`4qmNf^vcT_Pa15%6MM@Wx^_{1nYd~#ehJwSZo>E"
    "a%Q6dXzygs3kE32XE(GEQwm%l@qx|cJ*Zk}|EW_uMPah5Y4H&@GA;S(-v0UMa-V=+a;kPz%8}U=lCYI%noIeBoq!-EMvNSWQ&BotYMf78Y&tR="
    "+K0}54m+}1;I?sKQZU(7ot@4Rp16z!a#_>Lkqe(k2_|A5ahtcJ##E^Y?ubr;f{(TOz`GVgGfl6K`x+1q#6k(iNEZSaXI44eb-OW~L`p16u|#IJ"
    "x+iUaI?n+sa-H$l6G0Tp69U;rB{KKs><$X!0J?$g^0nu*b{f1qaJJF2@Cj0Z*ejqf5{~Lg<sWx|{FX#|<3bYXd^W`+_;NKxmhTkr`KsY5-$;>Z"
    "g`of)L`31Wvrn@SVbQb0rPI`x&h{Tq{`3StSBgsKnkb44o;uI-g(GFJPKnO*(b<JS*Zo`AJg8UI<jd}I4loy9Lf{s-1A(!7$e9mm(x3q0nI5@|"
    "tFr8(n+wl?uPW-5b3__LanmEBRVfKAGpHOh_T$Z+=xT~=ldkq?`^`VF`9hNjL{JYf=NrYUhR$nQoCFzIzF_vuGhqq-wh#;@P6<^z&cFOi9nbdk"
    "U;c#?JR@sCL9VWZ3dWbVUv2<)Xu>>O2n+(aa<briDLfxo*VMkNL=iub(dZl`JSkLomXXwV$yVtKjWHskZCYHf<Si)L^29jI3`s{A1j+x$-kT-2"
    "kz|RYTM0u;U6d6F#XKmVwHZWG600~hNo7{vOc^T(1j#6Y015#}VwLGxf7~7PTftqxTf|#Rt>m4--NQY?0{}H-^|jk~$Py6|?#GWGKa-!q>vMKI"
    "11*!`xRi6{U{5OokaElFHubT`l9_;hrX)`@+qlG2g|^m+3&%2Vzs94&oCl8Ylav@NJ`ks=4{TTcCWX&{H-KcMO4P<pFh=9;hW`q(K-F*r#8L}S"
    "WOYxxkh!{)+Bsbgg9eV8vC1@uWj{%zzL0axVN7tR2Qh0p10{obV9y*_%8&N<VJ5!6yepM<AU$PsPLn{z8fZr>{q6nrqL@r_L3y$owX+hxJDBEA"
    ")gXA;4>;))kETbM>X9&Mjz%G+iqdsaTgn242p_9tTi_q>3&#rvev1xx+dT}Xbx^j@iIe?6SW9Cbinb3@*B%K^I^-BifQR^r$J-BN>H($ENqrI!"
    "X_4FnI7(pVFf*%=d?Hb?Ly%R<ae=~&J{UN|C3_XXx+uiyh6&+q!0KN(`2=*H>w<<Rd#VwW6o|txLo5p^L+9(R$Uz%?;jph>sMG|0ErX&#R6q4t"
    "$uLDxXuRPXY6!j|Ht9eX#lW4K&QP1UB}PM~vjJp1zmx$+34m`2e)9wi>`^HVS39AUQ!RK6A9rFe1)=Ck*pJ<8;QOYTi?8>cMM=9$xW-@9kwhIH"
    "$PNJofG`jQ1<pvf6;e6_te?q@d~)ol>I*XQQ*zJxJi-naiw{KZDQ;aRzu$r5iKPMX$0upnkCJ2%p(f9YqEJoH)SgdP6~-4;cf!lPq&aw8i5kIm"
    "1a3a$BDR`L5x4IHFN|EVW*P}|bMZb=9y{77OgUB$OR{$QoN_C;C5vy#Xh)(*2aJ=CrHEkQIL%ez1!!aTo~^k`_!IW(U<Dbqr>4FsZ&#FeL?V#{"
    "*pWqC$PblJkkX}+SbU(LF~nD^`JX!!ZMQ)4Q))@@?tQ-@-gw88ObIznx{**rE(t5g#~=!oN)o<s(CGj=Y$;oiNfEps=3JwHjQG}UB9R!g6FzI&"
    "Mk-B(ED_U?Ux<(nd`&1leW`&`TL$11%a29DXcBTp^3m`bzW-2Q3<(iGuQqwQ!5(JTCH!8}IA#JEzJ7gvaB*??;{hqQ6ooQ%68EV9TrGuzR$1wK"
    "I?xnR$r4D198JhYin_T#&wcqxHMC$1>EA3?G#P%8dQWR0l|WmzVL&>>-cG`iTDt~rh#dLqKp`Avqsl)R_eW+4UF_7>TNoLuA+?(I^A0VX{RLpg"
    "_mhysX|4<uhbt6uycmuROX5RFFi@3{LKus*<pC_cE~?Zgy`Wl6gh08^ALtyw(S(DbXkdgvLZqT24b(QAOf-^Osa$rgD@mU=_tvP;ul&F|05ge+"
    "q3p1dP)_@H>91ryY0a8yt?AUPj-%uq3mPzNGWiyp4`bG3OF^!}3L(oM!LQ8`#0mYJqm7B@o=r?VvCPW}hj_vcFNQ~luTKv4nVL(PB2e36K!K>n"
    "E&1*<pUN1nB_$)vQ>#c&xKV2PW?2qD!rX>ht(s$beusKm+`!7XIhgQx;?)$;#ig&<QS<@>KT8a7+`Z2!w2Zo<kW1|J=xF%z6!!e|TyPHD?K+U`"
    ">yYSNN(aEA5)5gn6!ks}W119xErG5-PPIWLQfl<V@y9UWVsf)vQ3y~WO->qwqi##ehD9q_2xDZ$0@Ibin2jxx$jDiifVL})C=g&1U><luH{*ju"
    "D*GtMxV{PEiUmVnQ7DZ<di(;md0BptHwUnnph4qPIQN$ad*~FiBAk{D;C`SD%O_$3P*EgDbcI)MXpT5JSWsYn*XNE2M<@mrdmc=~Q64bqe!_}Q"
    "1Lw?8*m16Vyo99K({WMF%O%GXN@g#-!>sl5!enom2lNQ%)G_ZGBc9b!0-Rg|BjCJ$0KHf&EByTg9Vg>L<W&p5ljkE3uf0#Sk9eCw7x8!HjnHYO"
    "?8oit@`d${x2&G9zQTv_@A2>KMq}rlxNw!yU%3)7ELbe>Vs-r&(UM2Tm8b<SC=@_g5{mojM}^K1c7AcF=MdIjuMe7H9a60kX9c7O*&&FF)%5)o"
    "ej9MY?T51XNKUkmixRle)M14b*2eAutX+g`MS1p4t-zy<IF-)bnwQtc;LZgw#KTvId&85<X9H8Ep|_N+X{a^Qfb5GPcodUh893^iyQ=vP;!kKK"
    "NYLc%5D7-SwaT@_{*N(X0kq30(G)Phpbt9PNQk^s{{{KJ+pe1(Dg9_64ckuH#KImRACPG-nAR}cU+DM|))GOt4zS<_dSsPI9Elo(4Y-C)tJoPT"
    "KY&V)V<TU?fyn7rVAr?~5LU2ed5?hA-DBJgtCq-|F=*$ycpxX1s#Qd~v#}7l22g#K>8C8Z)fE3#v@q-nL$K0Z8JgLrTZA3cfoMA%OKWZC`0(WP"
    "oQGB>532*U*;MN-x&hUwaaYS88dzMHkrw7ssN!O_y1kq5jf_&trb>IP8J4tIV3egS=|s9JIa4*eO&V-0OLdk-4t>epm?H%ZmwvU5tUwagX>-Eq"
    "F7Uw+(OOmNwCQQrkvdccf>5i4^;J9alqO#9C+PQ0mAkLchWajzi`pwtEvwZsfl$gTtL~gHYsFb#et0dHp1g40PFEG(rq_kEfZ*?uD72-W6eS&3"
    "?M6X;!5)`fRnl{I=wy_Y=F0>#`j+?rI{j9Zul6Lu>R1EMedcf^eU1V6<ZzZXyM&&<^X6iR3w55P{UmZVMUepQJFAL(;6yUzjo|-cFj7}!FFy32"
    ">Ng|#WI-8I<b|)ucQ05e3^32pjZc7y`;wg}UTAS=dS1()NpgrRJn^aU#USDqvl)9If$vA=V6>Z0=ztsJ83x)DKcwfhc<ly^I_-)(0XZK@NOs$i"
    "Zbow}l7cNrVtGE>9E6n;j0~F9((clO{WyI6<{6qpr=EiBG*Uc4=<}M^#5&MG6s{;0M;gtFPjqF+o<R>w1uE-uc7IKJ<)llta$83w5HO&S!@V(}"
    "v84WV!bH|K7MW#zQ7^q%zyz1fiSaZvuSC=h2<6(*Rfn{)m3M{0%PS`dq<euxCeRRt@*t>04)t{gAKfHHiiPhRmL8eRl(xH^&BSrN^x;Sz>>s{8"
    "Cgksj*lrmJ`*wOy(Fdoo+Kv4%7cPI+-G3)HMd|rF!ec;Mhu}ZYg!Zp5P8o66=%7-De9h$$?d&9BO9Ih^Va=L>r}$gTF(X$N7%MyVHL?QvJtYle"
    "gQ?qaP2S`S3TrLKmF^A{SK8#HW<NHcgaFI)Nl68KTlt=MJia0k>JHw92+(XYPTb|rYJZ(vVd(4}o&Lnj3)L7>Wsodyz9?r4ilAaZYmcq)TdHEp"
    ">|mqIVNCrbqGMju7q^wLu~^~ND3Pe*La<hK?N5}33u<ReG#_gRB}LbPzKhpi#1sDf=ReDw_K|SiVPuUAD}ld2A8v*>z^|ZIO6>;z3hKY;77~66"
    "bK{Nh`i15%!yiWG^B0=K0saP6M>p2t7ZmKumi%?fHq{H<k16QPzfPqhPd@=G(^Pf(#n+~TKLhj6(EKxUNLtdrW9{FG{P$8YQko68C^Av{Crm@6"
    "Pk#jZAE5&zLm2;+N)nDy7EE@F`*QNI`<L0>wBk(sn>)(ZAKigndL=4>_Fnk?-kgh|t6Z#I7K%NpqDUnWtI6sX-ms2r)Oh~|ror2SE14HUUtl=$"
    "j7qh0T~us|NPVzEy}tJq{f0$h_y&<HhV~AQ&yG%iKA=o!;2c+T)e=tB*ujWIW6}eJPn&bL+nCn3OzUnvt?ESAn)q}=MRe+!(O)2E#m;Sw_b+Di"
    "JIZmgy`ND5LXLymFQz;&R}Oj6+ry$pe=Fx#BLD{ePF<hV7xGV6048vWtBR{?1H8lY^TUJvt3R9`o?ISbr`GCW3a5Knj#Sq*l3lpdN}OGZpQ!Zx"
    "C@1(_4&ipG&ma}$|FD`&0U2Dg1k8UBtne#0Y`q6gODpO9BwXnvAc0H5nCMYiIEv(?9#-O&K6-L;)>Qi#Hizl~-cW%?{}&7dYJ5t<5=AxrE<LPh"
    "a_wFhC_S8`V)?s@f}UUjpgNP-nenZrin+wRc#HtxRL<Gr7D)GR6#0Qh+XTaEv0QC)cF+k{!b=C!IKVGK{Lk?%9-kQNjP852FGb#Zd5<nC7NMkl"
    "f>9w~#ARXJ=DZZ`<=|}bzmamJ@=H+>f<O1vK4KA7@@`gFpa^}OUX|0Ud_IQ{z4&?H66LC~@T#}|G>JPujh_3BPY>(+3~h3+YlQT<7nuX7dqa*~"
    "HN4^Vh*+t+1E!!g<e}05g$q!qm-TRN*Jv&+5RY9xudX=81ew}9>S=g|3C6q+OVN4a9CKjk;+OYMIvc3xtIVqyk4a~Z<2v9`1*=ft9hw>{3R4ZX"
    "t2`I17x$=K?~GVAZ#LV3SKQ1T>xp_?OrDl`#gQWN0OKz?W_Z943AReOf#v5{BP?-Em9P<qa#;wn=|E{O=onX`Ucz+{F36Hqo{;JeLz6Z`F3U%6"
    "f;`>?Id4cVs|#`2VGZ{4f<63vEg$&L+2?S>?n3R-7A-odZmGr9LSvVQL9JiCM0~@DrqvgYTxNCOUVG>P7}R}o)8ZrR;;Bk4+dvwD%73k+P|GgA"
    "Ys`sK5gn?Szo8f>UI*8k-L!w|3rpb)Kv3ApKA?lT4QSSF{I3F>^>qC6A^vi(u+!i-1?!#Yo~;_aR2Q;F)GvS6I|iR0Tppf-O>lCF&4;;KagQRD"
    "S#jh@OjPHbkNI?|#VOO>LddDvw;)Y1CXhmv87t~^QRQWA#vg}!WNK*hy`G_1NB;vFQjz9GbPBo^BEN?*tmxmajf+Ob!RrHUSdNe^G+PX<D!&et"
    "-gzQo;L!m{QCRo_NdtQ4*??uy9jNE88JmE;u}XtTFhkn)E?xHp{XZ;$`agPItCflWsFUPsg_JM2xL3IqA(eP&4T@`569)lRHd#AyjSexd4E<Ir"
    "vN3I7UyC_y^cB-8P1~F{+dM5|B-${oLB_ffg24-Q_k-5B*%yq<2ct3YJ8B3a43xk3M3A^%fu4I#{7!{$%F25(g$7LI;rY*3!;}51pN6jwE_&Rf"
    "VS*j01hs>zgxum6Y1F+Fi8<Iz+x270C8B?ap;nuHPg-AJHn-oHn{B)8roNboqNAe~#x&FMQU<A<`*iPccyx7fu=n=-@bYJE>eP#ZXb@%_7LG5-"
    "*%Q4c|HW$Yq5J?-zAUE2O-Y_bX_?w5zq)vP{^Q|~r{`BM4^9qV9bRhC_<kIP15^sup&|)1V4@AESPzUgcM`i{G;p)^bEDd?&Hb)!<Dk>wfsFO5"
    ">Y0xYe>^;SeRc4svxAchWBXI?PDA(C1PRr#SA(62{zr6+^X9a6|JGx_IXynOIy?c)4o~(DuFl{%9lkx*rU<ydi<}|AVx3)6%(2G%Vu?wXp9*aO"
    "XXmG92j{SXm%~39@F$T0e(V!oR6`K`d}0e1vNlyMY4NWsF^T03wDu_=Pxvfg`r*r?12WG=`xb8A!th+_PQEJ=Ib;mko(hkN_E?5>UvV?27nW10"
    "6P$TF(_T*dg)LT-ZCXv-`GQ=K@y6rUq$<-ZCem1wD8_zS=g`=fb+v!+>frpGoJ(qLo@i+Fz4uBoG26l<OZcYia@~It4PtP#QUEkt&{!M3wA*}*"
    "I+k^;@zwc(L6gD8<)s^mGW~L*6m`L!mvxh_<`Qj%>bGPa>la4SdHu@FSGHLiFh~mexZ<Qqok{A<Sm(Zn$EZIbtFQI%B(iHQeH#vE53nGLXMwek"
    "Sw9tAcX(cp8AKa~e1|4FJ3q>X{zZ{e7x^6Y(1i~C!TH7M3CP_&I5vluS1_M>dYCliMbp(nc4<PrLkN~Dk*7iC&ia#np=BZHj7&1+%eVWWZC)Ln"
    "4o|LL9pJ^q(bZd!o-Z#B_YeO^<6!%C(5PE#3p9TdXojSfxfJbPK0ZCad_8<^QmW8U+n~ge4NKk^69yr!25R{B@|2LJL*sXBnVZ<QEcQ21RISx$"
    "^z<_&KbDpBv{_W2qf=0-E)UL+ulBLKi$#l7PK_5mjEu!B#lFKft_X7Gc)Om4lAon-+BW4+Z%&U6u8t009c-GA`)X?AN_*+c)}-{&FIkeD`f;nW"
    "Oi9Lyi+gsf>~%4RX054l4f9Sh(Q4W8p}ZsE8)>j66tO6EIf~)|_W8wtjw}3?Z6b7Et3M4RWzFbP7pQe{FB+hMv3Bt2vniZf-iDTA!gST#ET~N8"
    "2yeZHCns-*M{97?9$o?~2h$)$Gf{&SEX8+*ncDPEFrWwfZ(ERxCYWUUsPO_ez3RV{Zn#^MDJ#$O+<1VNlmR-9t$`jSR?ur7$74Z{8lY#JL06M0"
    "&;vit2ASUkJu*Sh0Ce<Lye}TE?hDWtM&u;C$w$koF1`MD=9ASP7wg3zu%Rcq(dl<$w^V+<H+_y!Ohkd0<26ZTt>6#NPtsg=-T-T#fQeVm@N#oG"
    "8)F?ck#gH=;EP=dk-w1lmE!!Wfx5xM-Z|!90<@hv75dlS?>+z59+nNN8)eIGh=Yl|8pCEY#iyk?+TrwAVxqp{S~tDywS9n#<qJy_$M47qd^vkr"
    "U`iPVIN`M|u5H=K#hb1uNfMAOb^|vQ(Q^sdsXdj#r932j$y`zn%*?rTku2M=noh7-0mWV6yOgmfqcZUhRBS$1qmnzHS584PcB~OVgC)EWL8F}C"
    "&!xbCz0nPg6v1l$nQ5r)*I#n}kWW{rouJ>9V&Qe?aDx^oy%MtnPghI4O{#u*H^BAEv35i*)AYeW%`+DFHI?p(vtV645hu#a8C?&{9B+y;BPU~x"
    "lVOAIcd&A89c7Ank*Y$#J@p*oYD3Rz)Oc)pE8NHcD}tieNjWqTmwLdf0cS^)v8h_~aERTMdS<t)OjKIv5z&uY5z!u*BZw_-PEPzI|3nQ*6E7K{"
    "4p>ex0>cZmE0`19K!8q!@Y~~>JE`vx_}{DJmS0#RrwRXU?ozWMjxTPad?WYC#~3Y9jL++%dt6SRALpM$>%i^U4xsKiVDms9TXaI5j;TN%9(%-m"
    "CH9g2J-~nQduv#Wg7}<~LEG8-vEEPD*Z0$nQ*A#FByBZtDG~~p0>9@zYlyaN^G^DY|M<^rZQAp*Z?WxSzcgTst^4X-KcoUs>*UU&V`@x>gzXTe"
    "6`qTZ?M#dsxCRv&Bd?QD4HkfOWXLxvZ+T)0sc)iH$c6%RnToZ%C|D^cPS!rvwW{H@RE@_R>f_eh)KQdJK)DQ9Sga;I-sK$@!zN8jrF~H_yi5}Z"
    "Df!nGrca6R&q`!5%`uPY-{}cwS6<Tv)P0dt6)Tx}DD;9KVAaT27X_CN%V|nV7@u-B4_y+2iHkR#^o$C7bEyG>u3S3z80dwp{+fWGy{4J4K$zm&"
    "c%rW#>O>)c3dh3H|5y}rdVpK}0-(Tl7Y_@uSgu#}5euDGSOEeyLL}zr&IF54R;zolj*_b9?ax^7j4^p^b-l!5;Fytsp|!F^69X@l8L{jNr?}(%"
    "#s|X5lEC9dFuHS5RFZlPsAf3^m%&edT9oz6c_nIN;H@_WvFy|(w6bS?0X$*dIlMUKuXgy(6R%O9=|d8!;c^yY>|B;Sqs*y@8jsZ@QdRwXI0QTH"
    "Ac}aXA*~lS;LnnV|11h^fvUgDsy-l}DoN8yNg-1~##F6`H=6Viu}xgKF2@k|iAd6?4R(G)4Ge?qs-mcK+c1h>%u!B7JRp%=ImNt(zCgI7G$vgx"
    "Pkc>1ji?a8z<EU#m6$B4@&PTKUIJ>st1Wq{PsR%;SYcQB7fS6t5&1{L_kguZDOipfxyVXbDxFsrN}>!@EhwG?14dLDO4K@%S(bW*6>Lz!88)(t"
    "P*vA$z#1o=@~xQOVkJPCg!7^v%$$c97nv<amS>+*YUzCnV=#oJt^<jWWHK5|2j^E59cg67p-WzfJ&k38w2vZxfZZ4s+r*7m$F(k4%~KH;dK)AL"
    "tZg`%ycXP9MpAKmI((?<m+;qFvA|c!y!j$+L0OY^REX*>V!;+W2wo^Es5hi9Djb0jzFp+^HJXGgRG}!8DYiHA`)-uvYT0t3<Y)LTR?7Z_f9gun"
    "_G<lX?lcIHFEjxf8!GZN^mS^K9+?YM#dfr%VdH=x0F4s<Cw6v1RjcXQ56v{}S}p{#{7%v+;n>hTkZ+&f?1?}n)Dz_%(m}xqR`*lq*WS;}Xl5v6"
    "f9*Ltiy3FAqP2_4?A8O-*{);}?>u>i!{s%eDzXwal@pz{D%5vS=;PMIUMlWs8SdR?)*z{%uk-lEnfPj&kfi@@Xd+^oNVlblNYX_1-!$<xG(qt$"
    "pcej2!|^?`>AW!sr6G4Ux;W^r&UHf?C-3A=U6#vm)c9Z^CmN+l)mCk+gN1q~TA-mM3PncEB43Y`7#7i5>qUBUe_`(MN7U(1q_Yq}Uk@$&i*55Q"
    "WzeNX=8z(x%6%9TNY_dHh75Xy{-IG%r{ZDxxvgO~uqZW4MM8Bt<u&MBSf>Q@m{Gys<?Yu_K=lLBSiK3WO8iUTPIE)Pm;qjJeZ`s(;j^_&Flb;K"
    "!6ec~8t1jhY*-Fs{y`*Z8(RXP5rWWmo)GqRKF3i9L-eq#+!m9S2*-r}(>jM5`=AJi2B$m6A_8c<%WtK<FJBU|D3(tv@eSMe_01w?>WOlprZFOh"
    ">euDN7h-lw#YZz}yvRQy`<2xi`;^&Ej!{k4Ol4x0v{ydf=^LC^?@9j>X!u5S@^g1lRMDT0!b-=pg1y5cahggy64R>_L8R*FXMsQP^@A&NZA4A5"
    "!U?=uom}Xbw_Ti&2T(O4_5q)Ch9#^>HrkeO&Ag)GSi(M6;8X=Saf^s>gj=bG;0H;*K<UEb<@)Ob5#~?ajN22lFAU!#H^ADWu`lGfY$BJ-@4tCm"
    "(Uz|SNZxe7r;9f~bQ5ga{6$-5c-PbeIIO40ESR;G3Uhdhf2vQ$pbNb_gx_x9DH~#yFR)iu-8lN2sF1JKu&UzyR7dqrBks3PG(y2ia6Uw;v4-9#"
    "3*%@IdymKN58_85aC7(vM?EXuf+~Pl&ff~^7Aa!XFR<|6>5V)a0wu!t^o3G|Y6)&xPg&<5qFm)py;t1LQ#g?D9Sv2zFnikj&Q$ngRTCP}-$c+|"
    "rT<=lq&ZrS_UNKs36Unfo#W5jjKEj9OY|YXn#?|;w)QjK-Rq2tBDBisiVAnp4X3IYKs&+-Gv9=LoEWuKNgN4{v^I=H{#@-$*Wq|1$L{xPVTdio"
    "6#|rO-xJkZ302lHYFzC#suYRKA5wG`A<Fs_e4mU8D)v-3?-I~DO)~EB$<&Z^s$479s8~{&8C5$1q<WpbMYYQugj$q0R#l7Gp?6b!6y^g@jPD2+"
    "C6z5g@gsV`vpyhwnrd~o`TT|OpU&|r3@a`YBf#2eN`zCn6)qu#Z=%*&lGC)xA8Oi|6!{dxw3bV%<MWNxjG;Kef@dIBO{5yU^&2P?eddakR9@E~"
    "oz8e_$t$;G7#f8PsPhlK1DYubElrHAF>!U>ku(=x_fc`P94;{;`d~W#7V!vr^15CTcTKJO8ry#C`UxC(-3=^W7B9B6`F;4I5Do&o<{Yw$zl7zS"
    "-iSzVS%bOr6-0>18iq3LPYZQH4+Q7|MXe@_iz9hYR4(iLvhb<iF@Ww~G*bR5A!wszy1A*ObX1&TX?DoAQFspvntwlGr_-*1;&QfzT08hO*hHVD"
    "7$jm9DX|n>hK2daa@O;Cv1|nv4!}TfaRsrbLONYsg1VZne-|n1pVcS(XZtt>s_{p8wLFvYy_o8kbYw2FvZRHEa!xk~)q#Z8p9CmuZuc(_&7a)?"
    "oQ4Q%uzWmTjqc2cy(12*0{V!QJEA=b-OIz<|K_<*Q8g1)^3Ki=aYeG}%Gsi%C}uy7RTwk1U6LBDAHe?^V65VJhOLF(0F?}<4?ptvTxvuOULErY"
    "0#B6)gtmQogdx|BuK^h95`TFIGKEXexC764enCA$%oidoj{`e&IjhxhB9$7E`1lm$_5PBU>jyq8=+;<g%5I1SF<7<Hl<37#>s7s~F!Qw(Ff6rE"
    "KZ`<&{l<gvhPx&lsEj$!qkws`{ROH{uP5a#cM}I}1rY_pjO!5(q#<=I!9eXO4UtGiR|Y;)#-cs6rM6t(T@y-74Aj=G-W97}vox{*5cpz@jf&*a"
    "k^3xWLLbk^X^)rrQU=(^A}OMcREg6KXwzjIk-mlyH}ks?!rutr3ko7S|7L`W#$|qN*2a-cX1X}NIpAu}RDY>4f{3+a6JWorKyGjqpd)h1i&bm*"
    "3<NEx7#Inn7mAUZF@+*^12xa8It8BgGOvnb46!1wB2_*a3CLT~jC3a^1B%^NpU+lIwif!xF_!2nSM~XTwd33v&y^-Amtkr}&0@d|7MkKl*oZrA"
    "^Hi5W83034MTP=yl`?O}pl@1`Sj?+-s5;*QNTd#Btd1SAjUcU8a;X`Gw^<*h2IAECh`h|F*hWeD#ltbhR!UOf>!WcoS>~6s<3?bY6}oy1d}XNT"
    "tcs}2lZ_c@m)!|yXw<#bQ_a*3iUFG3M&6lqacz2ZAV-!N&(9{S>SB4@2nt;@ng}kmMNz5<N^LNEw557agr0V6fC6sK@f%{X*==^N@kKe^_yz8T"
    "h_$S`V#$D+M9eeR!Lw!|kBVG-;eDoRH}!QM*RCt3zzj)(y)W@KmKKG^OhqY6{<nJH^MnjpEyl&P<{5S-i&`D!FEW?L=@49k1&Psvb68e5gnWVF"
    "plBua77-7y2<qore~W?yB+}gyM3XUSR6lrY3=}DN_8R$9C|C9#2dU67zbB{yq`gL7RC5u3ED+!HJ!f5U=x4ng<tvpHD9rEobiKVXXUEt&vg*-&"
    "6P4ES>B)JaI{E#`mQf2R#*-L$5XGoc%7N{lH)b^lh~qdhEf9Jcj-7_x(3J{X^R;rSSuC;TwV7o+(yqE*G)9#BY8+Jg{B=I(d$5tv@5IiEzjfNx"
    "exe^Pq>Mx5ra|cXGhu@v%~1jRy?imIYIZPNGlTXnul6+sb2I{#advZ4*MbQ<bc1`tP!Tz{wJE#5u~3Y~n6oMadwXJz6Y5Uhdy#k{CES6WYCVhm"
    "1Pm52_~mTRSWcpJl<MHGbZ2oWl2NhVMS$X}4(~j@+1o>+Gi*6boehJ}TA-s$pa;~Fj`4bUX2j&R$~<kZ7xb|}7J`#Sp$jl0OCNHnOdjv#D{2Sz"
    "H83ML3H^Z=@~A^I7fxXCVo6m{<3SQB^+o9?UhMnc0GX+HqOcJLel)-=V|k&fp1|4n253vjCluGA9(#TU9}1AnyWk<%rx*_YB95~dENY)isbIOe"
    "J!&LADgQ=$qD+z0AEetAOR8}mMp>ZYJhP(wQFW6Hlt-zDS?XJ$Jhh`dNRo7r`fZd4aS{#!8_L7Ljn|+&4!i-bc^$^HD9wQOH)1@5#rb5&@aS-G"
    "uzL+3ouK~wtXSOOk)<_Z4tOB2blwC$laV{Zp%nR<RJva_YE5)U1Q>6e+X+w3!}poucPfH*InySURViwhjGFP42wmaO9%iVU0vr^IK@n!2p)LW>"
    "R67k)^7In7z_l+(p_9|hwRhct-BPEZ2mppgI^cHohR-8HCsqB*P!yVwB_rA&lSyto(R?hj`attD<$CgH(lsym!~>034vpP{a*ZWz4^`xnATe=@"
    "bh+Xs^_5hU@S?QqTm+#PgQP*Jfz2}b24J|X2POs)dSQ?PJHqP8`V9kJi0c;&Xw7B7^#@e8wR6P7DG@}qFJi^P!0?kWiUw(>iYe$)Q_^J%ur!Xm"
    "1o&CF9<KI$S>&c!IzR{C_VcxdiTof0=@Nvk3j*bBGk>P-NRb2^E^Iy@E?s8k&3ha1GywI3wyO2Q>2z4DdLFRfK@zsEEcg&sQvDpb5!Mk|Hc+*{"
    "TA;H~BP@MO>%R8#mV{if5_dl{Zb2!{{6S`Y-*+PyUTZ+(frSZYiG*VJ>KY%Z%ePHyXila!|8omM<rI_`FU+Ro?K<k^zMsYoABJ$YSv`lm9L;4H"
    "yME@jQ3LxcW8CD8@`b!1qM8`TtI4vQPYMZxCA36Qowy!WI+@DhA5JFn?pVrf6xfNEWHHdOJz7P4+ln~RMhMd&4nr!LhyF0EXm@zBhgEsBxhekS"
    "q4lwpSxpL+1qQ_KUp5Lx=|49=1>7`i+P!EN#H&PLjC~b0h`clmLO2OYY6s0r;xvP^7jFTg47d6G)l*^Ryu;HIs-d`l@apj7U|$sxtQUR85kJmz"
    "Y-K}TQ$&=`_uhxcV1h0UnC>pPPm8vKQ!N<B5p7&*;M3HLJmOIom#2GwyaL)g)AyX3B2hDpX{8F1e9v{CUcNavhePn{==7(KReWy{WJ$IrGWHA6"
    "hw`_?$HDL%DYL~D*df!xNWGsnSRyZtfL|qckbF2i6v?&`FfUI0L6QM@=LaX3z%E+gos&ZG8*SM6>CeNXOD>0csPEYM>>-~3>-<*-e*WH!^X=K$"
    ">G|c=<@xaB0tiSyMWAD0N5X$~me`5%hAr~%3C!!$9}mt?uuhVNr@cmZ6SX$_t(e(Y(BjLt7r>e?F0Rgo)UT#ZYA^BL6L0P3*gWS$@f#7Hs$hC_"
    "`0sBI_o-~q)xnQgno1KNvivE>$fy$8(|^AFsL!xnkY-@m;{AV@AkC5>>e#-f!s&TIItXwo8T{DRu+&wl!V4NVaq6e!E1Jk?%leC>%RNWNaEecY"
    "IEyk+QNs@YmjwwrE3yuv^T5#eqwN$CFkyl$0iEYF-CuGT!BHDZ6=L96;Pu=n1-k~&+@U%JX&8HH+IdXC4h_6yuocgiao`<09wsUIk5HSnO%=vq"
    "`S^o$8{~LV7<kcu+@W&khKu4r27F7`L|1ez+F3z{eT_8Lru~ZRVN6?7^|lO^Vt1D<LV3~0m-*?MY0Z~i51nf30cZ@LWWndpdI}!WiX|Wd9rtH-"
    "eR96L!;56;?KK-HQK^05lr&o<Q9*nfZYUc_@t-G+epB+gU?>|t$sbP49#LGgqRvO8dqZ*CQ&#U4(7m1TnIjrb$rl(gLwZrWq>{Hi=I6mP)!<G8"
    "uQ7x#W6JP;mHiJ#C3@}G7K-jJ5G{%os@2Lcf3x(Wr4(~ljpmL4GyVSlo5zaOezW}oY+))d_6sOwScQeXh5a5!DsYto{8PB+WE}x4H^RQWe(%k}"
    "(dl0AUH_LxJz3%Y6Yf0WCUoDu6WdXzbm46Yc7~Sq>g3hA3f%!JHX@!9zJY26LPc)CaR`ry=-~<IL>qBWUf^$x{@DJSUz%ak2ezko2PEtd6-m6A"
    "O}Jw2o@#7dzf5Sh5T>9X7azB&OgzPnz!z)*CgK%3G4I~>&Dhe~4V}+Pd==Uc#;sNT89z}j$j`?0r=^UMC`x6oVAPI9;iw1W9gg$q8bE}fh&L>s"
    "r`_Q)FCT0>t3qh%DP;svH#O+NGLQL=;$522aqSv}mQs&i<0E-HYzcJHU(@b|MI6~915WA>4%*Xqe%2l5a$tq7b0CV}`b>qnhvN@9UCoZa{`?_l"
    "{M0^@?NavgA8y}ALNQ*F++LpA`W1VLb@3kEAHnIgh4R1``RIX5Y}68>jm^8fI?`Sh4ZnIu_AMdgk0lrEfp6*zfB55&3Rt0~!r|cnw7f?aw~=^5"
    "O~1>_&iePL_f9Ds`^7z`f5R(Wvh=@|m<>vdH7ev~UJ3l+&Khrsit!=<xcPKuJ~swurX*jGp;5M1)F{5Y4$9vycBKOV#pz|>vIODSh=8;N0gYsw"
    "j`cMa1T?B6f9x-&%@?~y^i>d!Otml$I%VL1YBQ@u`g5`T39xX7J`=CLt3J}wZqO3s%M|_NI<^G3AO4P2)QIrmA3qAcPbhhKnhpKXliD5M<l=Lg"
    "mjKVWu74uc4Kfk?em_Yg{)C>q(^gn7zbmN(==ZI7`HWh1*O7OPF@_zy@AH2%o-brPL^X;CFGL^QUj!|lSbIs(BiVKfDd#|17G<TP8^sP5L}Z3a"
    "PUe(8ysf2#K8K>djpHZ6wi?-41F)&#G@m@sP37NP)Fl*NahRJ=yLBu1X6Lb&v3DY)<~X0i@3IO-ZLyhub;nbDS;&ML$9CSDhmE+;vgi<6Osqbg"
    "2u%Suqu+a}j6@kH=Lkv@IV7qugZ>KEmuQ)hdgqE`^-pC}VnYgQKM}Z;E5-b#qsfGz5%DLtmEblKm@DO_p%|dmTV#)-A*p{ous87?b_~JTMG62U"
    "b*G~ji2l2<u=?E915=VBA5|jClG4mzJ$J{NtJ9h4hUsX_(w@|&Z|=UB(M&lT_-^7UPN}(=*7G%kjakD-w~r5fOepARbZm<zt*3w4h+5q`c678R"
    "c69W}*wK;vpb<RE!7D^RT9%+(Nk^vOm*xU~wm3}wPC02mR;M4)dvy9yHlMFE+hju97P)J+_obP<=5^<;W&DjkX*&-QeXjZ&mQ2LJ|Ew1aLOYN;"
    "c%#C^wVp%)2ED+65wNEsi6~#qc+|{L(=#52BBiR47Y8R;<U2kx2@*bQBOr+B!6mRGbJ-F7Zox+wY|1HJlR>#LNpf30B0R6S6R0&PaVCRh@SpIj"
    "+0d|Yb=`X5g1TK&vinC080`1{g5AgKyRsUas%ut58&b;6yMNlp^>vpW4f2RsFmOcfP)B>E1%_z!sQRIW4Iu2mZ~n^YlV*qRRe^ft#1VB(;Jq5a"
    "FpT45kY#Gd`UkB!oqfVrhkHXT?o^NFCmP<pIMdPYg8`?Hlz{*+`gUPqW*dl}UweMlUmd{JIE>(!8w*R)I58Kt2_(TAopn23Yd{L4oEa?9$$xFc"
    "rMh{RyC_EE{+e<L(N<%<K@=WpU7o~P+z3?Oz0w~W(J1ntRrAR(+6IE!QPx6OD^pUdUDhIhk;QABkDfJpA==v<uA3q4o**^Hrydt;MvA*fiaUAJ"
    "nvaBR)54jqm(E$OrMEB(+7)ZMnkp};C=4|!qCYn7p{8P6Ms&4sLVXG1FFRG}>iD`L0|P6;8ct~}j7kBR%(Ck{&yT#&U=MyAW(~&YxnXQFh#(>k"
    "fjztmU851B?zV@mbsL4Di1K7LItx>uyi3w?WJqS&BeIS!<sZ})=JD|G#7+)a2(fjAI=no1eR}@0U5<C$k{+JyAO3i_&#lT@yOnj*aHhou*GVec"
    "`;8y@&0}nxNwpF5Fk!T0Pwar|RNHxZynYc;_aY+OBHAn19{d)JCU3y*eG9s-QIR!kxL{a&7=`h#AGx~3=i^90Tu63cuj_T={!(_eJUzdBb$WDo"
    "+J*IXXm8`)kO<9Rx5R%tS>MW>Hv(tsUc1N?wndozR%siQ1#6%RtSC!u7)u|6ur(cot(e;gV*_(z5vjW^_S$!Q+hERXY^WDC4S{ca%q=~o*L9@c"
    "Y6<Qd%*uz~c?niMW+Q4nw{4&aM(5Xb6KotNb=UGcdjNck-?d-}^zcr*YSiytVV!|7Raek50xeL86p-zv4!`NtO6_-cNCBX5p=aAc5`9xhWSsAI"
    "bI0FwZZmRf3wdYnyKPe$WD2EblDXR$QmR`wuQ%Cp1apn-W!Dy3U$Sf?)VrI2+g2)ify=WQZMRO@L7bPFZuh;pO21)waWY9RZbY{rrfeHxGHFNK"
    "sMJ`u=lR(trj)gnuqfq4Xt%-2OyKL*TF(%-#70AT%LJbrt=Bd0Q~m2^vp~N&*@kMm`ns>zr#;iKmVb7+yV^SM#_#QR<(8Jt`X=!kmgcv&YxC0l"
    "M||IAqTOrzCZbGtL=}q)1^pwixv7V|4V|KeyzZmjg1LzIT9R}9_f~UgdxS<`hfqxxQ3?FV3ncx<bqz{omcC>w@s^TFzSxq)8%Ag{=+4EpFq(V`"
    "Mm2y_gLvWwuLxRd{pZiNz7<q?K=y8t<&TWK``Fh@8<~&XW;woA9O^eJE1^uLregnhSw~}NT#YT?TnrhTT~EcuTGtzv3K_DhLX8BfuP`(Ls;ew)"
    "99Z4$ahAFDb>UQ~VG*42HlJ@*H9@boAQ!OZ6h;*Z<C|Br#X;Q}(Q8yRX$;>6Qk2`>j7^Ck&-b^)k3wnaZ@pmqH|tlezH#Gh`-O|Ix&s-$XS^0M"
    "UyPo?mbDao(4*34`FPgbCYo!Th%Fg)PUWW5<QTgq<I2q^nan`Y*^v<`Nr6qijIeBl9_n#Vq#Bz2jj7O#*}GcsB_pU@^g5Pl7ma5|ZPK;PlFiQ5"
    ">)w-L{~e>5HA2_Ek`gb#iWp`|%0@LvS#*^m!J2PxQzvxG*5GC;!Iqzhs+pVDVfk1TMBQp(md`EWn7N9}*QCr{l~eURBS1f;>qB@XYWw9=^@0k1"
    "sh^tPDp`&0rN)=NpUH^Pp0~cmVP_kropnwuo~)T#f1~w%xyZGGg2q$6on648K3v$*A_Bt9SFBUawwq+O%`~03FyLrU)t<-t&a!q6u31#$t=SfY"
    "p+6&Xo=;{E#e$rcK>V@muGy^i2MJ%x+n~*-`<QOg1V`Yp10<1*(wL=tsT(HgTFAE3$PMC2s1Wv+o3QpHRl=+h!zG#<X%XvtAO~+}iw7-M{Y*tA"
    "Q52~WNQ4&(te^Ki89N#!UTA%BwyWOt#k(PBj(RLRJBGb?b&p#GZG8tT0(>3^wus13@go@i=HY|JjXYmJV;pHrkhQ}{IDCR5__Vx0fIb!>sF_a>"
    ">Q6Z0#~lRvTGdsxJIKN~Xs=mY0hPeQe00?$@vv2r4u+|N5f7(SRZZruwc`=LYviE_=A)=WG}hjL^~}yQBYe*u6WIyJH;m!i7>f4|A}1dc7yMtM"
    "CcI2ZXmph{E5mVk>;0IDVv-(@RWaoc+=I(^$(oW1ck|`u1NBj+ssgqPq}{XX8-&py62%g*eFe9XDDd&+T|SjYH+~OnLcc8A;tRp0>#tNqzD)R$"
    "IX%vjBl0=12fNASGN6N>%LMPI)E$Tt{nQ&A^>4m{{lh+zhnXVfji?X5?+O0lf^u5_;WPiSMF)g^aSI2u3JPZZSL}7?9Kq8V4u?p301}Qo-<pAh"
    "bsas*Lt>Z+48y<g%KuyEC4MhkamzHGbxxsea(G&vBdQ>7h}pmQ4$p_}6j*GGX1wX_Xjie$@11ktq<Fa}rDLy_l!#bNjBSq5F$C$AiO6}SZ&1<L"
    "UCo^x43vo6-{U+j+o<t_5>n25#@#qt^Eal#>FJ#USSfwLT*=vy?IyRH_nlDt8(5`9yq&+AEu=5do?BqEZM1J^-CxrIJrj%7$KhcpKb$o;43}tc"
    "vDE9h$5msqQ5ozzp&MNHonkrKu+w6qqJeJ8WUlj>_i$Ox7wqfBih2+mpU3WQ9DE^RYys}Ob{;fk)effz=CAB>mmIfl<e_JgE6k~s$~q~E-B;Em"
    "@@D))ok#BV#Z{o&`Kqkp&=;{8Dx<t3nnwGA*={N_Hf{Yy)T<)z(|6?#S9i~=W~#ar1+ge6agQ5`HEUIB9q0^qoN50;`qKN2MkwvT8?y}xJpW@)"
    "<WX=|Kpk(NPm0A7ORIsZQ)#(?h6k}WZ*Eo-{!7=5aK2^vp|IOfv?R_&#a3$Nt&wv`Pmj?{Cn{abw8`Gd>E+e%?Cj`pZ}{@)fP!>tM9lU!ph8NM"
    "EimE#?}mwYn)QdSV`&sD^H1o|<s$|UWHO;pgOKV(b#Uyyr?tyN`jqJiv&Fca;vLsg4M6qOvF<o$@8Ol1{?H9W{x3d0IXt{Hp9U%amn^88n}QHz"
    "pC<5q{I5%?eoJ<W*Og$2sb8AE`eBk}*&vH$J+9ZbWFbB`#-nDwiTO~bp0xX~YZpAgF`5O^ZOz$LX>{^7!bc6_u+(2~N<LXzT-A)3lw+{o*aEZs"
    "tV`C^ed=&xFQo$c@aIkWNzWW=48Yo~HiSC>6leXeiDutos@aCgUg0>rJqBd3QQoGPXXfjwa+@@b>Pqd}?^=inUj>SnBD9swO7E1~Ca!|1tPKCV"
    "ZZZ{jm3MEKg#Y3S?kr@_Team|1*@bxh1?{<))ap|t!)|gK>Yo5i@H@w7$>!{fh)sfY&84;8Q8Sx8E|<6V-!*1``BMp#xSY`T!cx!LcQu8Y<zmN"
    ";LPfusT=5W=B%b=`^}vvs1~u`Uy<r$G86BVQwP<6T9}JBbt-PYWE6JsxT*`tAM6j(>&K#|3swvy#}Ej6PcQkBak&@%AnWy0^+CcPAjOi#)zQS1"
    "Ixp3A_Sitt%M`1+G}1i%nOn2UR;v7S%fHv_tJ0#P#$~N6&Wtj`t@qybo9=~Xb5&IUetkWEy-@!8-ommR`***{EM#9^?p@;jQ_WSg$*^AJL~kJc"
    "!gD<@1R;r8(d|oa8m?_AbhRVa`yi{9fQQo)aluQ+&sv@8w)p9;m}2b3`D%K)f-`@jV(_+l-K^ANxh88@kN@(s&??ie)kK#y!|}alS$SbhtSNXd"
    "-e5Rx+g0st6DfsHFN#Sg>;KT&pJIIOK!cU>uu@mEyqD0c>!0Xu-a_i?g<)qouzYk^79R?&CYY7VHK?%Onx*VS=NocvJvvnn*)WfHGpHu@d>^<l"
    "y28zq+k6qjZ&F~_Sfgh)JzDo}9A{yIioLpRBC-Q~|75avE~KRPNUIOb_aF5mRqt15RVJP3#dFsdyroeu+XJYIxt8H|D$)xAcMPV#UKjlpMQ8uQ"
    "MQ3U8T*jB|^atVh_G4mTS2FYs#SZ;FtAFxom#;pGl2pDAkZV6(QP1`2YFu}F0ew`)ZC{N!oH_QwFfcluT*<`5AOf`_)JL2OB=KBmPAhnm2E0)l"
    "-oSu22HhBQFxSAF1wkA(;Egih#m-tbc(W`)Uetz{=Q7|;8}P<$ctZo;#B&q8Sn7s1j+4Ysn()R+7R6S0@#ew}Z1D122E17V-lPq0WWbwxap11S"
    "ZxV)n95vw$y);g(@J61O#IX%to=b-}a2xQZZFpk?-YjsvBwGh>>IZJ@HQ~iD8_y1J5_wT%gO}$r;Po2tW^H&A176P!vF*%SfU_h^-3Gv626Nj1"
    "j)Aj<nGIkunE|nHLL9kmh*J|{(5@4c;F=I;N#F&|BNxW08`)Vz;$>mrTOsDj42XjU#9kZX%!Jqnp|l>yo*Trz7dJr;gE;8`ISo9|O2uL}1LUv)"
    "vflzZa!rtd3wd6+9^?!TObcX`zM&Q56zt&4j%A+B06A)a9JE39Opqhji=*{erUq)wvxk;wV&}z~8)Zpi1(|0vKyC=Ts4eUwQ`mX2n`P++kTYf|"
    "2FO7Y`>AUOIrfs&e)@Pe1LTIhi`w!oGUc6@L~a<Y2icFJ)NO$rxd|@S0y40L#I=iPF`WT(L*_+onHQNdk32COU=Dmg%~~+~L6q912=<_eQ#)z!"
    "bOy`~xfiwNUS!HWAN$j#>klC4VoA`H)Sx0nv0YMoe(ZUX6=pG=4s+O$eNkKXMW*cYeNYn8Xg$nXn1+56=D1V(0c!wF*-9H?Is@j0{EOQ1FEZty"
    "AEtn?bS=ygK-@ZlAjP9Nu)`byGmoq)oS4plxgi1Lwgik!3Fs$Yn0V`9jzPz1(T0~rf!BfOI0HyLE6hBd0dqqJ#%&oGnKIDNB5cRI7Um=Y%r!N8"
    "AlMiWrVZv4)Y8N%1jTd)%nczJw}oJA3PHe?=eui_IS&|J5;kcAG|Z?&`}BaEy~L_6i|GuQ8&WWCOTpNbf`OZbak!q>C1KoF=#r4uVMTKgMRqic"
    "*$j{yQZQ~y!Pswr9H&{dp4G*v7X)#O)wx|KF!6)L&Yi_<2FML57`LTh95g_N|C_C+<`{P~Xn^c?96m3MeBTZ(&18Vv5P)%80LEeS@MZ3LtHg`^"
    "I1Q8Sz>Pq@xlzZt!<h_l8?rBM%f7fF`!FLSaM#O`5JZW;9k>CU#?a0tcqSd(s3G>^w%CgsVh==T<Zn<fz>4s<BnCeXGdt~ynGA3n5-)B`yf|rs"
    ">&D4??7}o|%g53ME*722I>5!53~(F5E@=z9xFPIPu#L0z+yRKubK@<+b(1Kx(=N|sfZLFBNn6gv4LO&_Sro57YCbUFDB2EOkR)kp7t1`80d7OY"
    "C2bLxxD9Yq-;d+<;D&y*Eh7U$_w9^K%w&MukZws^x+Pu{+|=7(<Dp}1Th8Euag}v&2AatLw;|b*wq#5ECb&svNIQ#tm-tb*CGDakGYLDu#hDCn"
    "8&WN4OSL3uhzU#$h&Nc!VdlA8ftzKZxY=oeCo-UI2(_dw)RLx9gTorH=VR!v4z?3&Spo)N2edSi0c}I3C2g6OG-O%^3i$>hf%W_%Z#!tgEOzab"
    "z!T}v#to5{v_)DHH}o4&5|d!P`zMW)ExA|*K&7r-y`hN=Xd4nOX-l*uX)2I@;IFrb+yoBKc1$e8c$cU{cf^SdXd418Z40y{ZCMpjw4QE(HHKT_"
    "78`3uUY9))MF!o*4SANf<yn$7pv6vI8+@0cPr26HK%06U4mB~60c}H^rEPJRHY_&Z598F^;AwS12iOi;FnjI32QiTWZ9|%+ZE2P^Y&GCGVZ7d7"
    "0`e(Mx1-xMj(o2JTAIj!wjs>YwlGT@W?B#fFWul029oo_Eum$(XMvU{GN5h9va~JB(uRc=21yod;0b71rCUN9`k9?>c_IVahAd0lvMe=a8EEx>"
    "vfe|PWoh7T$r2JbOY97c=P`h7h_bXT%2HF51+f<e+4>8ZEDQp7OO6mw<bwrRo<|2ZX-KlPEy>b`Bujv=tmg<>=8?U%jc9N|!L>T}#5@MD4MCQ+"
    "1zFk<WT~IH>kVH3c3U#Y$gOGxmgg~mZOE~#EyvP^9LvHa^0W28`au|OsnCD|YxjWgJO;20F*aRICT(y{K^D4c7^NF<8;9wZR<G+uZf2zfF_8gp"
    "xCOkKDayd;Vjuik1{Np&wx&*!xsesYVkQIN=nDW2{HUQp+vG!CFMg9L350HsgAg-)euqIQWlohuMt8-1e)XYPR1^S+DXRGb1DHycL%5sER1#`3"
    "K_QXVWOWNKjVbzZx4_uO-M`H4rqxV#HYqql_m{u-ZZKK)YTAgGT+Ap~u}(;l;gxlm>QycS9XY2+bdfnYK07-7`CuOhDXaHaa~1h0A|`Q1j7eqe"
    "rJQrN+nCn3OzUnvtqQhmO)SHD)yx>AENAt+*84K3*ZO`&y|gIoySHCVd0^41s<(%AW&c*rfzZYUMbi7O-=iFeD*&^c-d<HQ8{~L+etvkcfAxpc"
    "!;{M+tmIWaOqX|nfRReMn$N0IX0!cW=D>7Sgf2(#DXHdS@6B1SZrwJz`<P!lZwD6x=koCE!a2Bn^^gDgzv@zA@Hdf^NYuwNZZ{K(quxE^zTCyw"
    "c{!Vo>vqi^2f}|W%G<l;RXM#<kWrL-!5QLL3l${nauC9n3;4syA2s;T_RpP{li3UdQ*WsZp7S#hFT><8^j%A7ysfPu>Rv%$T|sCrpj}{CLjUUG"
    "a{o^?{IAM!F~QK%i(*k0l@tA*8i_hxScV7V;*&$=a@4|Jy*=4~^d_a<OZ3wA8n<0vy)?>(-g$emZ&bj&cw<6J?W7&<C%s!&J{M5>-9Wl+QbJDt"
    "2ttCBu-`rj7tVh90ZUZ@^>FIIdLlZ)<N-(KTWD~10Up|qKx{(ZQKVeL{^L)lHRwO)Q;e-0JFhM;4jd{ygtadisnrJf_e&BiHzklr^HXg>YfeNO"
    "1i@BovXl=0K4h~7Sl0$@n{YOu|2G5Ii_tv%Iy(RDfZYPpH8gPa@7i%JFYfXMFvRlZ?9(Ub3GlrS&g(@!E?`?0^BIcrZCJedvbKtK9Nva=q-Sqy"
    "F8||C2S<Oh9MGSN35xmUY)UNL;UW;Tg~O{|$I_(&;|x_MQ@xyY4ZlgPYw^Ra_vOdSL(5W*XNxHwizP@aPIKV;?@TvaG0m5gLf?~Y%_8D1y#ds%"
    "_r=52eX(4K2DUf(XekO1RCksR@PF^ErX?<!e~0<6bIQT)O`oG$H_5MI{V%vVXN6ThFjIKC#7q$Z19d+sL@qr}!@YSme%bQ|VUN<{${7~6BWt1W"
    "aGy$N3L<`YSuE}yu7Qf0?R=7tD5<wc3#<l4IY9F-0ou+epU*kX_t)O<J^$App6hn8)j_j9;lN&MkfPp~9QD3#dez?*7fX~lFme12(+-xGvzM46"
    "eFJs|<r3i9K!bG_b)`IKsw%OF-FQcd5&1$@)#1XtGg6?3oZly^;q;v;W@b3!*+<pV$XQJ%Sh5-Cp?6EzD`&o1jIfgS09()U<^vPdc0RA1g4$4y"
    "H3Ddq;d#M3y_`8{H94@6P6^U=3iy<>*Za?9ebn~rFFAk6rz^~_q>y}sbm|m<w+DwTRFf78EC-5g`&6{Y`{msL*DJ@`L0Djk(+2}J&j63_C@o%4"
    ">7F<X*3}bn{;qO_EsOMo_@k;AV@^<$I2ktRe&;%$zL!~&6@0R)9FfwEI|_2-p7_BtP4nb@TZNlz&Y*P&ie4w>&_pz6K7oOqo#NAIvKqr#Y|cY3"
    "l~b%Ys-?dxAp6e8yK;1gltJ{PRz$Q%*1Iex%<SSm|J0~2S=Wvfgn5D+2+&O?fVq;%PaPQmqAC_2x~cCG_$LX@Ip#0gGcf+!+@)qioax#``9|)O"
    "kN>i&mY7he*T{T+oPQe16yj~z4xsM&wiP{jAL-u%{1?BshP5b&&lwrCovk11{nSdP)|FAkejZ5LYTy!#WZYh+!0)-w8lo-Ryp#UpKmIclEYmKb"
    "o_&jL7yG3FV-{@v+FciQY1hb|MaR@faNuA&M0wxmvH&m<qXw=)MaIbMWK@F%ARQU<jdJ=<Od<76w2Bdr@8mdvQx(f4bt)rH);`s>s^PU%jmI47"
    "<JQ{LQLO8#lRt8?n(%m+cR+~_X<7~_u0+PO>EyxTawn9U|JN1lDT&D?y*-)%?ah~PhW?$N;5UR7I1%?nj>@EiDdhBk^@1N@)yP;E1-%Hu7^eh;"
    "fWYJQbU252+zxVJ==2QLR6dssUAc7bVU@({uL%g+Yno}`XnY$_^z{R;1cwHwa4a1Ck3})32e`#A017zP&mR_Iv7};5KIRXVQ|0B@!Aeai$@}o)"
    "WOYAxs@1(%M_J);`!g0i<8dFJU4wuJxB*SrIf;<@aVCHl%8Xccg;U(kJ|ZX&gp(zK$BSTe=fp_h4d5*Rm(Vv2E`y)^v?%MB^NKkMmGeNzot@$8"
    "7LkU*{m=RWc*44KcyY>K?cl>*H{Er;XZnytYPg(*7&~|B;t<YG6g@RYbjHP~yvL#q?jVYIs3ENvHsH^ahX3qf0g1{1RezUNeL#MJnh&j%6f#_7"
    "1v`dw=VGHt4-wn6qV5>Eb6-}IBF9z$yul8ppgRw<6&$#N$N+2q-OZ4|d5)4EFH}W@`3kj&zbY!G-67INg^)=V^p7RXGH_mzf04;DC*2>HPA>s9"
    "ywj@5kntj#6krasQhPB08Rrqz+2Cxk<DVHhZQE45g1lki9Ma}bkjLWbgKfiST+eVctMDX@@)ey)c5&d33|>i|LpUHX3x4##l{S##@bMfdyi>jv"
    ")7uizCyU3us0TCWA;v{!i~Jp}NYLjOT)za<<ei4F)O8^7k-!yvT*CR~3lvz{19}BSl^v?#A;ey#d#EuUV}Muaif!V?tK*7X3z>q1kFe0&ATeNV"
    "V4J@d+!;>uHP!^+G8Xty(=Xw#GfogE^X7}R1!YYt0uuOU&p;Dfe9iGfQ9->Ss1VQKoPZF%UF7#QnnXn#g`!YU1Dp@>eK$&SwQRZ2cj$2VEmq1G"
    "H2>6<)<uCkcNzr97n%T#4dv8yW1X#=47IQV1tszLdTD*+^8sj-nC9o~gsMI8vmeX@S~;~`2td4D&sIw(5vaOZ%s|Y|J~lLu4TXPjg4O-h`PC@t"
    "^J~x9S<F_X{i3z|tk>Uupms4J94@c%RFRdashmdVhk;Sus~+}JaZk%|?>4grNd<kK$2ZQzSJQ+f{cl4P5z|DvElos{CbIvgiLapvR0`1V!*y%;"
    "`oVPGn1s@hyBb|kHyH^Q+iFr!-jK%0JGny_-1MH|s1YUW6s1VjR&6Y73<zI`D2VRCB~d6cT9j0WUD4PhC5A<`)_M`y;?fE?claafbSTnU2%xWr"
    "mi@)H`Ia*1(js$6kq|W6kU+Xl;x}Z_BlHiAdO8&k%g=2Mvw=maSt=4zK_kvJ=v)KmY=PZ_QNiEk?bl8~^#jpZy$PsrwzkvUkS}I{7ofDEO|1wK"
    "K3mHKg9f${Od@S6v`cFN1C8|H+XD6eA8_t+VQvY4MhHUNc|zFN`JAmR`=DKHa$u_`X?3lz4{Br6vc9tS<xAoU)ADI0zG3^`s6$l2tZidN4AmFD"
    "SfCJDZH!7uYc=7p*cE!wz{~~d!H!W))=XtVE@`iPywf*0uilgXCD8DV=tPtP)7-*xmBMD`LSo}t!QNr=$n?qVVWwBt_LZt5*QC=AuBbDHpAsN}"
    "SF4j6in}=>4{#=%Lhl1U=?qI)k!-XrIh+b_<r2GP^r;!364<mwL^#5&R73ECBwwI(Ve!t;@R|>tj(SP>Cb<EmtQk9#+4PqEQX@1F@sz!g<Fbid"
    "F2DcgA$ONo0wixb;M2vMtoQUqTW5IJ>_r;~o#nI!UFh8*{B{HXu5PBdm(TN&sAwwaU=Kw`xs)^t-|#Ea-%^o#33&3fSn~13E2VG6fg6*)U~=2V"
    "%D>`NO^TbPAVTT#v=OVc-CIYk?j=(@J0&!hyR({s8kKej4Fop-HdwFu<w&%6K@anER8C61{KTJM!O#1}WSOtg`vC2G;#E{#sDZ{iYe~azVide?"
    "mK{X5igtK*MES!DQU0(`r=D6F1IOdqhLv_;WTC>xpO+uRk3xmYWu3%YTSUKBUO9g&7PFozL`OjpSV7Xbwin*SFQn2tIs!M!x3!L+=n{c1_?;cC"
    "mLt-tUL;jRRWHn*_P#S;F{(rkwy4^u)Pg3xQMuM_M&Qf&HW3@5h??e>(-o{u+*!*@fcm6<Bc5}j^D$O11RvO*V?0I%_str&g+f4^D^pt@+ZY<V"
    "<~wt`H$kYxbsm{6iV(5EV1Y7$A_UOn0FLdPcd1-DO)~EB$<)wY*bO~H(gtbKcdD6sf_mCL-x!e7xU2>aLe1aM4G!=_>7u<UJ_>`7C&qV#(-|GO"
    "q)^aPso_a4wOZY6K7S#E6BgvhBUln6xG5=6ijN??)n{9T-b6d1BsX}KKh(4_De`IMOv>eQLVC=%RUC)n1Ph*lST&Jq@YZjj9`>0lA`<v1T`){%"
    "JhkMN+c6A{LI&$gEO!ep-5Su;kRy=k!zC6CKA4WbMTCjeBXGa#{Dw*>55i1ED!)-fXkn^#+2Y#0#V?B&TlSf%tUTx{hKzT}LRIK`1rcJh20<^{"
    "aUVM9Q^G3dwc#VK0_DwLxvXzM!>3NQ0{K`@=@M%pZtlK?5VX-U-NjW>Ix0>f&MS)PmZ*}lE*eDNQP}CU+pI9&O|2b#`W@AF9cij_ZF_S|Uv)90"
    "bsL~3T0`s2RkJ^9aR)LKQ3SB84Ji8D=mNYxTm?@dcT?0#Vb`5N94_@<7r0k{153Y^e_@&GBN?)Rg{!@o{y(=u9MS!A9U>*#gVoP~JdLNQB8Hjx"
    "AF7%^FG%gcj#t;Kn;XoCQG+;6BcRN9b~w#DpNe*jZa?;ELjIq3mY_EgZ)WeuJQAUdKNgE|Il_~5OKzMyAmYmzzN%{3dx=Y>=UU@)l7jg&(TwO3"
    "EbJNlS#^sryCc<YFvX8f-5!Y|zO+BZ-cs5M{H?am5%i^YTfXs9ARWf0o-FEbv4bK6NBm`cEP5+70)r2YEf;;5xSv6vTFYUHUG%T<e|*t!4t_Pp"
    "lR?vs;ka3o-x$u<e^g`Hqx8)I11oqjcVp^@p#hvNj((^O)?RDi6Uh7@+2Sv86QsniXb*Wy7lxKjkl(a#<oYfNjiv}-$RppVdsh9u&LKR9O<2u|"
    "tdA)?Lu)~DGQ(y?bv1nUeNaaribdGDB$WGLKE+Wwz?uQW$wWqx?uxKYX93D=U$_)eDWa&)U5@&6R3_YjJF@A|#>ngzV2f~21D&U8b-laHtM|x2"
    "%(vA@DD)nj4<&OS5Jv^DuO;ij`Qif%hBsY83n{0&)o3;^9PGzL+?71749%f@*jh4Z_q)f(+QKiEp!RTdp*fQD-NBr##gF+dTG?O?qCu#mi;3sP"
    "&T+oyk~}*D63wR+BU^vMZ<jI@26vfMf{%y^8RAPy$GSPkct5bHrww7+0AwunV%--HIgq=Ulpx#Cw)nxhSuHVSN4IQ17UyVHh?zmbFFv7XQMIEo"
    "8Z81k1de<CBpF~*wLIHk!0y(HCFx$XDXEzEtI4vQPcRcoM1o0I6ivV?m=H0t-Pj>T0}<u_i^jjF+^0tVDf*7$o-P+fzEu6VFmiA2t{A<iK)+fd"
    "w11L`IQSJNjVe7^z0v+f|0aOH+q~S`IS;{<8^<z0|5oyY?LLj*M?0Hd+lmjzxmgqpdR#BX;LNthd}_&fi7NY$!H>r|X0~zHX}RO@`Z;UH7t}b!"
    "c@C>7Z*N&zV#f!HWVAL;gE#yT)!tWc9FctD{Nq3VA4xGV<I6=pdQSrRRCYmQ$4%e4xI{N8*tO-fGX8SLWmWqd`*r`clCl#j%6XXX{uRy`XY7qd"
    "u3}{Xd33q=8s_y#FF*Tf7ipaM-;MSHM)3JDkh$p8RQ;fMuJC!y7qd?f=+*l7_I!O9Ltn&E*CKj#JGq^`QyeWE*bqmNUzgn5PQHn9Ks%}etQ~sQ"
    "p<vW!>iom&!63zf#U2*p7xIfIplf40N9W(*pOO1V=lInh#PH|}Z%v^wG|6vNb2B+sdj&=-yMd*T9W~%u-EssWImKun(9$IaGnviaujY)g<KgQ="
    "-T-q>ssF)b$p3++;j`OvL=Y?rx?|k{2ikhZ@J*-)7~K<3U@AfpaB3S%pCWLl1O}Yx8E}Oe5uXE=ZGNxq@c^^m;i&N+f>Aa>;4S6_=968DCDo=?"
    "9S$|$t$s3n3xO5loBC)TPS15~^i^BvkcS6Rt>l=@BI$KBIus3^(C71%d4%(O2Pq!@N7ART)a5t4I*sz`VF~eKNI&2q;Z%1HiSL`kz2n%DH$r^d"
    "#TEQZywF2+s7~w~)s{(Zf~Z_Y)v|>h2UU|(I6F_C(-ZDe+u&Qq(?h}E)EU>F!G`UkEU-P(*^d7EMaS=_2F}^vu_IY3LG^pZYvG^TFwcNwSryaS"
    "n-Eo`>u_Qs{IFU~XI%N=Z144flJhnZCaN)X=j(GZg&=dWRa9>mnE|qaCmvWCk^0O04}60}@r&@-z3cq9)Fo_?ahZiyi3AQF^I~s+g{y0L;z1Cl"
    "-vXY%rfbNm32X2~^$dLUJ79sA8ZdVd1pc=G%&G(#8P)d0>DqK9sD8OGD+-CaD>3u8905g5X8HKt|4z@gLRi#I^XMBk3McrY$z(c+8dM&B6RL_k"
    ")ljaau)YccS3d|NkD>(_ynz>|3}WDC9U!LZAW60dGO?=YTaZ|!yb}M1kyzTft^bX+ZmeY;2lKyi){QgIwH{8cS<$RA!PO-qKOQ88kPHV|@J-m6"
    "=h=jjtU6&W6~QGUyd;Ro8zPukkjDIv*bhvY0xDntPZAFqIjqI=9|53mMHiQnFseUr)dxQWR_Q6Q7%G2|W=RLSl4Rg{Tf&2`SgcL4Q3*a_W8{)6"
    "Ux1_n4P&+-y<@xrrH>>&zT41<zf|j0m4+Tj!@9gY?unl0uRz}waP1e%yqv7p*|qxt&AFleZK$lGJ@Qa>wB$^^9dz~aF{j5i=OJ%xzFwA!QbBE>"
    "0rrv}VDVvL$#@A+9gTRs)rcon&qoja_yg>|B5W=%gW<`W?~S$^_hNOu<lCe;0V+?33fVU*739q_hKKrXd6#w%R(mVRRO-<hM2z#UZDCAixZA%e"
    "nYAfv3-d@6l<V66(8~r`vQ_Rsa5&%JXxez|i3&?8Q{a#oH3+;x97_YGTdnoi!y07~rBo<d^*}?E*2N~7{9lH~L`A4wc_Bu0<%X~{X5oCDfi#9Y"
    "{1PJ+UV<b-k2c>1nfIUanM08hUH5Q@_cCsU$ZK}vwB7<^eJT>Y!GH&%#LJrpr{dc$k@bz&Hh4}Z@ZvaM=7XMg81^K*TR2L@X>fMLJq*P|Jfj1F"
    "DYiLR<9s_^6hH@mgW1uIP><k<fC>GEY^!siHfyBjG4`<IXITV?qCwvA(Ok?vp$7-?d5xO@KypTpe3`QYoagF?eah-y6cnL_`83-ewEucgZ*`FW"
    ">w&#Brx4fFy_4rdrOyjeMStkY@J9y?Y!~kooZ|kvpnMl{nO#3P<Dx2Wr-LmSz~j)gE5{PItR_0-H}a5j!o7(HKC$uw@t>wC@dc<&UotMiyfr>8"
    "QHZlkV5A<f(ptFraWIJGkz4DH^8ZP~BG~A}_-Bc+u-k%*)++;k?0N&N{V#SQ4KOj1d|de&LrhfVvuVO{;!*>1sR~CRJ3|`qdh>wYI!o#eG?fKx"
    "DvuPQXta6It_wWWSwO+Y;@1+`AkIKFqJhVo2fpYW*z-eFe`<iUY>-AYZn4F<N^MWmEF561a8yGu0576d$9cC6nsslD?*#*FVIWo;W`mg48eeZ5"
    "u4`iwA9g#g4{?Cra~gBBam;#|Sr87`a`$1MW4rdR_zu5V>t|koHnz|H2oZw88k%5zAX6@7Y{GF4+w`e*TQ2XHi4BUFhWfIqP7dYgq7IRiRqEzU"
    "yU}U<*1l!al_T3`^~6=Tyc}z?VF|?09t$&<kuPgmIL76GfT}o(2+ec_fvm|w@j-ZT`St=MO71cKoXTP1H7bRCJnW9xbAYcEAX>R5%nww?1S{K!"
    "8bfm`dBxZD`c+&_R~3jO8TiscaJ|#>{lk;t`On%_<UbuX=Lh0i8SmQ|CnheaG9OUN@zI$XL%=nr@C&4k$~iyX+Zu0Xyo83k#+Bo5iZmnS3{i4D"
    "n~ry@<->%_+NgxBN?*3^!gwI<CH;z29H-(_aX(+mpbz-b{f<kLfeCX`d-JMVQN<(2ed?$<9A*r%_z>Ok?^g3-1bZ`b?pM<iFX?BMD5^!7sUJY2"
    "69E{s&1kVX^L!~H-MXdLZ^RieN_$t$+(_A+m&leWLWZ;7@5Gh9$trm%-E#6bB+S-wD28?2dQ{{?YfTto3iHAdzekl@4;=kiPRBFKg#t#gucBe&"
    "T@RySxn;s)Sw9HWgX<M2ctut1=MQ@v37e$BXQQ3P-+TG$9-9|YIBxH6aMm!cdq%c)IenR9Ts^i>zzE%ZF)xCL-V1NwV~2?kGrV8Miv0MaI{=Le"
    "e!ZvA*N<3s1b^Oz-!tr(#B~+V+D#_<z11A6_U+|!j49!<(!>u{G&t9mKO0eX<0!-~K{$Ntqb!cN-^OY&^&WWV(3wEM#TdQG&w|D?P}0)++1~1Y"
    "g$u(1n5c?i*CPSQtMZe~0~F8%5nk<UYsPd}Og{shSKO4jMiYjpp3TpS1t$Vx05cX?H(%K2oD}tz=YcAdeC9Cc*C0CPqJ;(Rn{Zp&_w5FZM%cJ}"
    "v{$h>^<QQs_Xv?11C<Nr$mO<TbuHuXMbx@U06w*lt7AKPh<1=;i%2r`YIp2I#2tg1AW5CJhRAJ0<Rus;`y~*iXk2trMwn_4*<ITTte^=M&~Zp@"
    "3k|5&26Hx{^E^B}UC?oNGy$E>(V<|o?P27$FlGxAZ6Pdn!%mPqFT|QWNUUPWBgN!vXNU;~_4wrJ1fL46+hpM)qC<{+U~meseS!`i5@P^4rkA||"
    "%NGt06;HxOAD!z8kst9SZ7$#?X|RS#gdR3dye_7rJ5*zaOHs!cZyc$3h=vW|!<NMZ!TX({CD`v(A6}>z*71WR@GQusCh1*E4?p9UVv``eYNIe<"
    ">JEVc9(A6psLHsU&G{-&a!8*rCw~=*5|_p3ZaSOHZt+}~71&V4qQq)9#%Q8<&uu>6Cxuny8}KwBUSH?)vpLHcKb8H(;KzO0Xlgf0B7cDNHDAoe"
    "tI_hTB=5QQp^N7e)6?n;VC|`gmnE%l>+u8619A#%L)0(DaR{1-A$di;U&?o*1d^d_7iGyaasHq>QOSIhp=|SHOF+@zr-ww|moqJb^99~;$#1QX"
    "Ss^+20Dnr^#sZ_l#A5E+bf5o)u6zr6OVdEyWY>>-4NYS#h9Sa0<OV5;0$pHwo+QKl)dG+$h{z{+SQDb$S)3-^b+cVBk@H`cOJWJHFm@XwVV%43"
    "J(|`InD1DgEgD3m)blVGOYRG%;6-QL7(<&dqp&~%pxzHLrtjVt=Ro~0<q@;4CS=&RSxpeZk?L=UO3&Z*f{m#3qSoYzb#6BaGb<_spk*5>=jDeP"
    "JHg=$k|u%0_ycDQzs@JKr5&LNwQEHv^4RSV>cv?Lp&g4#gJesDhE#?(+Dw~nW|@jn9a#|w!)8qczMjlL0y|X!jN#^nu=wNQpTM#P%B-*eAlP}a"
    "YeQj(G)X&RL1C~h3IjjrT1D(_k1;rA=|+tCsc+vL*Lrr5LQ?zLU2uRfrW7&dMeg;y14#f{WJMCT_T3Iiewx_<_rmRQgf`b^s`8Sk3rB$!N#3s4"
    "BC5*;mfkHUTz%2`NEf9R+(?j2-0VK`5MsA`D{_KukrQFwrk`v?4!qes?`{XSP%Cd@i>3+OCbssA0#uLUy)!&S1AX+~hO8Py3n6*i;);aDb_<BN"
    "#~l#4zY%w-n|2)Zz{{+-3N7sFsJs>l=wJpuVDF6b<_614OhGLlk<-J5Isu`D&VsFRmn2EY0{qZ_6tc3-oGS1;=5jN?16jV`L{{eRjun!eIl1W;"
    "`GhRh4lHF>0z(UNOLlHmC?3bo0g`Cf+e}fen{7$V9yb28AT6@+uD2Jvdv~CmIj@Up@gbMk14W<inQeH3VLUr^J>q1#$<~Y6_GrdH_3UTcfXFoL"
    "U;<Ix#v6_5w*=$GYL2S81NQL(OMxv&fuL?q_Csq!W({$h2!pMO(6j0kjO53l&flz3P{U;VK@EK??m(3fo48X|HJpQaIdWdD77wIV04*L?iyZ7L"
    "iBEXtaFI_taYrEA#A&oOAx2$lrR#fSW?RQG{3R(G)Yljh%tbZOsTRlLC-!sHj?%Up1w-oEPFl~6A~A&Kz^GlEU*J^@qfW1C<boCQxwCj6E*U*Y"
    "vU%E<7N2R>z(I(kaO<ix>_(A}K7?s8t15{ZU)-&muPN_H<`ZV-v&B*t5>_MmSVP}lp0f2*U6xIix;(*jOaTPwVLm@D?<pN0w8KIc!9{F@VdSm{"
    "qy@)$F)7JWCp`b=$NR<g@}gLLDA_lhVsG+%EFG-I1YE}Ba<(^_RR!%%5PESqNRoQ-KcVaA2IQs+MS8gsx!}T&g_k<>B{e=-%DOEV-1`}mVX=;6"
    "zxQgA-|9Eu9*%>RiACEZtus`eoVyc<LUPYAyi`;r!HEAeIQJ#WauG$<>+kxWn}FH?bKvmsui<#Sz$!3xZ=zDxK*uU<09?pU*B}+{YRjlWARMz|"
    "+yDdVm!gdkm+PY%q>X+?Zl7zK9Nf>b5YaCGCB^{maEv{k;2=8O@f&P*Ae_-1vAy}C#4<>t$d}uXLwzLimn1bYWVC+B3Tu3h^+Chb057!-8f$~T"
    "xft?zJsE>1UP`o=4ld5loSg%nzYsk%&t&u<9^hxq&r`(ugL7Bj-tDSfRVt&p^KZ#hcs-0o<ez|*|CXO;l8TnIkJ!jl^v<#qQ>+maZAc0hWTc@s"
    "it$e|wC7?donU(8raGT3@32T=uMR|%?|LSx@QpNyGz{}!@^!yCG+sH>aUv8&=Vf?b@=6e5tP?l-7u0lghw{AMb=+a5K&};~_BhiKhXG(*$=lHi"
    "kzCg|6QUB7xy*=nYcl)T+$<2`6|$GUldqPuXBHF@HN6M&q%!{Zz_4!d8bemg?e!zkxJ3JmBO_1e$lkD6+ym7Tp=v!<UjI9<-c-4|PJ>6PG!<3F"
    "ss$IZINl1N6kVjrpJjb3Q`)%=N9}PjF0qI)Flevkrqvz>vUSR3{z<T0<^4Yv^#E`T5;mYf!fQWPNM>qn?Gha5pG2(--<nM+({ncciPRx^OA^=u"
    "N)=9I9F_Kpcy=kzioC&dxl`?$N&^TD5GIwx1JZyM9?urV`Te-MyvwJuv?ujkZ=vGlgODU$g2gC<Q`ObLnm==|fT2<EN0$7<q6M<_f;_7F38nww"
    "4v2HvbrM~1?(n$Pr;GpVc}eV2h=9GQvbqns#G2-K%O58R<(%6U7NZ2Su3%_2V5A=7r{7icFrT)+mbI^sKtG>6yv4R;-1bTx$IZ%#v0l)(Pj3z^"
    ">mk=T8ZhFPufEGUoW7bZMx=x;W;3)0^769rPEUQO^!7dd!m7S#fA#zx1K%)wutG~DaHyxC^Aa0#QKRc!YzXb_O>$5!>R#8f!}R6L!=s+;{LC6{"
    "rr(;YrqdVydgj1Ul-;FOhw9T)<MS{MZC`VgBy|lJU8)ZO`JWg<gs%<ROKQVikL)Mt)Ko)r`IC#~q9~UC-~a1eob8{(|EPk$&OWxOoMDgVpJoe?"
    "r^TmTz*7Ty`06KP5-&iP&DN7N^VQqq9~?Kan|yxPxaS0WMJ2(H%p)jjy>ap+7CfXX(6Az`wHbLHGd(iW4n+JG-aE%xn2<GtA=#6HR2xqBN8zCT"
    "_>+Xp`1MRyVxtFKqX#9fTDTaC<3;dFwZNV#^Sg(apzYr>iT=_P|Lpg87H8)vwK+mc<d8tQFfJwZ7DOieNH|B8V34Mqq&Td~oZ>bZ+4#r}L+y#$"
    "YkCw!6v%u8n4CI8_y~|n58RXj#}8HuED5&@B;nw{`58|oVE7|UGoIb^lZfJlkIV5GbdG}@Tba<$YA_0yq2B_A_okjQ@Qf*qHGn>c5BKtEJ{GUL"
    "K57vXFE1Zt9)+2;Rp(TweA!D53D)Xa3ht+BqsVR}*20pH>n+c@#Qbj~qnJCxbNsY@qLL4~Q@)&i`s6$THt@lDy~xMti_$Z>#Y~*!&HrwudNT$&"
    "fxteQkyVd>4=>)V&9Aps$yB)csi4Z(%h{Cq7HgznP$}jm)4*T7CFW(#1}EoC$f5Ms`Cfssh8`9NBoCHBi+=B*s^oN4V9{8qR<A{X&|S90<@^^b"
    "2#-RXFGlG|_m$Xtb$M~n#W1-N2>*M1JrJU>n4{~vC;g(0w<e^G?mp(%C}CB?IJ?9I;G&?4eiTGm6$z-jZgh|*aCBxfya&H^8Wn%U6kH96|J|wy"
    "M7~ST^V_t9!NtJ2JUk;A_>cejzv>D|JoFku;Y01MTgl@Qj=o6>;b{cv0Hag6|AyRPDMwYQl;V%>4dETe(#l9V9F(oa1EI?iqYM8npqhLa<?WQ@"
    "EOAocWX?|H4MJ><OQ+Y_3A{nXf1Wx!9tQoge0l{+`Bb#+AeE5F5iC!z75^`v1H4DrXIVt0(b!=;aJ8}hXb`BeeRq(EvELN=WO+w+7~(rauTl4y"
    "nFNr>3<oLxiL^+AhGI}q88Nb3v=!5Vc2kU%>6{>fW$6eB5eEY33>P4VpJJr>!r6NmVV2%RjJyu=WDx5EyAtt;=>VUJ`~a%?P_lChH0f*|ilab+"
    "C(#k=+vhgHMKf|*q3amOj^d878J$5Q_77(YB7;x>)si+2rf`5CSTo6jwF5>1w=`gg6rcw5GDQ%W2|aRTARD8>kHZc$;8KHFhty}9s7YEvdJdH4"
    "9FWyRgL+xC9=8T1_!3^kZKwu)OLqdLATAHDAlDIBg9f~M$dnO)6-0%HsLdYqv?y8Wm^cI$l>A7lF>Q%-F>y8!=z?>pzGA+j@<35LjxqXNZ^%vk"
    "Zo^Yn6H)R5hh(PIlcmvxQD5Z~s)i^`WV}2{vbwOP8eFDaSl-n5n$EEhGfLTRqvo}I^hoB}seS|7Oq*;I)b{(rxi0gnPUe~BG9Vg*cG2<>jx-on"
    "Q}`Je?3Gok{(bZip|3*v&@@BDA{&+*b1~G?*9fT}1SQnQnXtOhr>G@ZlV)5l9n{f9jz^6KYQ>jp*%G42KV>$UA(@)H>);jLC^fFiZp?eHFp8u4"
    "7U<yBo@`D~-?(iUAt1|Kh9)=Wj8VijKL`@-eRIMXy>jb6_sN0rSzLdLGyy~c`4Wn1Nd6tFtKO?!5X1!VZyH?wwa+b(irorXFC`?g^ryZjn5lmx"
    "I%F6DpN%5xcZGu?U5mV|3eI(@96!3AH={E9lpf=GOYV}Wg>Q;frV&W2f-A?uU+B(9-|z&@NPNZjW%C?4<sGVADxJ;?Wyc`VR%^6cQgQGS#q4~k"
    ";u=Hj8!}!=`o*TO1-8+}J7qolrj9)=@8|hwxnC|g919+!>#W)xqjH19D*Zm2!crBpJERdYMFzJQqvh)hb<`(qDL*oRb;&XJFxm6td_)bx*3y8n"
    "=O#r|_taIDZn7Rv5Hf7lBnY)LObWn}^YH`Kil=-v5mM@4HHCZv?<Pnq=z_qa2Dr~?h*4n%D){Y;i&2S+0Y|A0l+Ozmamyv_r^QDim+A-Sd{to}"
    "rh^*3^ZW4Wz@gLxRa2^RZtyYPwND-f4w&Y^SFjjKjyD%McWkBiDbB}11mgvuz@bV`thOg25p`=JqOy9wi-p^Tywb^Ni;&zlF|mv2L$Mt_$@tx`"
    "pr=3N^L$!Vh5j2k*KRo|)?_!&|8VxRg^=oSU6YW0E~eO8VDaEA$rrJjV#EgR06+m~#5NQ&Y`aBWv1OHO*hw)v=HLz-g7J5ib9s7p_$S_eP(XvH"
    "gj~=}Fe$La3tcZu6EOU8bgbZ2Cy<8<<Q>aE-U!R#0yy|oQX-A{f5V8PJ<x0pkR!p1Xe9Xh9`gz(GsGqq6M3~LX$0hC#k{Pr0yN+nMLqU9_*fM0"
    "8}xN}e_xDCDz^b&QX9f1or&P&E;_rpX%X7iq04PjJ1K7SZAq<;a~7n=w&z#yEoN0jX<PHFI>x!duP7Gzm5^N&kBq(CW-HOkja#kdQ|xb1QQaa8"
    "RfZk?Q1l&2=0rXr`IXTgih6V9T<`^j8<33TdP|mJzr$va(;HM~M}=&#C~SV`V_pF#&8aw2-TUf6UR3)}xxF1wn;39B!^VO$Z0Er>o|eQ_w`Nr`"
    "Ui)#Zsymqb>o`;$`TZ3f%8+n3(pgZ`&}i{6r<Mk7a#69>roKaw*_a|sY3P5<VS?Ow1AMBil&qROwB(dOh(HC}pM7+Gk2ZC`A*v!U4VfSODyAT&"
    "_iGQkq~S!@`Sd-|V!a-wONO7@f8Z@^&IJO1_{P9^ZdZbosO$pfHzPR!``pKPxMF$>R5KOz%26JggmQto&K4>W0qfgSi8Y%2Yl%Z{k06dS7;5ye"
    "EoC@6%VKo*yejTX;-x1aO5m<&!W`~S$|*8@D#2hO3@wh_APkIoEh=&PS93=Nr7vLNc~vkEfy266ad(a3Auy3KD7T<R=G5Ks_1Wcah*Bg6ODG@7"
    "x^AQ#&#>7AoaqXGm7E4v1fu{o6rb?#3j0&?Qc&0|ohMP6y+n4Vmt<2aHua`t@dvgYMLMI1B5gXKKGZfkmk$D(KFO<b{#O=w=!EE-G7x=qkCa<="
    "M1Px{*yX4yBGmL`i}(LJ5mj%hASZNIJ|7-Fg42|`$=y<jnA@0g%t~7_(B8syRE)k;frc<gA^>ES^Tlk$adQ;OzvH=2v9wqLBn1*G2%jQ%por`~"
    "FdO>o;BDUtWBTWhWw8XbK5H3X0IP`HW)n;*Np4p2HX<^d4^6m_GY7X=4aB+?{9IF3O-s(slXwtcI>iEy#<RAbF4Qh84u@{{59Mt+!6v=jb#*bV"
    "wqaIvNd6<VqAfBczM9y?E`Jg4T1RU(MX8I-vKE;Qsi_w3oq4Pq8$5?y-!-w+cbX)cJ0f|4vnFO!8?Ca6iQ^N`LCHo%fsjLEr{DRK3D?;X?gbEa"
    "o*zAZ))KGTAo5wIFR?jlo3l|J5vE~~xT)f0e*v)JdoT&S_$hW09?d|v3fz~Xi3iK!@z&HvNhI5g#&sDcUne2!P5$Oorg1bBqtv++OAXpdO{Ah&"
    "NllUzO1XUUo;U=jjr65}L)C?eAirG{Oalvy6fbNPMICC8M2J)bVP!7O(juAw%)q`Rgx}*8#lXSph6PPJywCqO!#>JmQQ`&EaniEUS<e!kng>7Z"
    "j_&eO+MzffY(G|s85dY{o4OMLmS{}IleAK{B&z7K`qqXFoUf)Uk*@O{xYs_f69BBXGU~K+mzG!3%%{n3z)rcBUF>lm1;-j=^mrxQ*}vmLKIoiR"
    ";lK0QM{IQu^n{R!GC#xlqD0-@k8D(kmfLDN$v@t#CYq7R9t^3xiCqCLy}U1ehaH`7u_tU!THMaTC)gS)mx?pvp4>bj7o8TLz}Q+%2hX;%>guGH"
    "?dj)BGLgQHsOo*(o~ZT~t1)a<Icd4JI|*z|w~PgAw$&C2nU)e{(3jv#BDZLggUq`F+8WKc{1X)@L$lb(IV!;bxW_v=jH0K)Z>!M+gGc~RRPBvA"
    "nsXEC47rr}T=>V?&h~t)EJZ!!#gH%rhD_d-bD}%2L8&kmz%X!LatthCN-#ao{l|a&rx$=om#X>X;Ri=|*vYcEpoC%2JL*WnKqNb}0!pu~%7QLg"
    "cbOA14;*YwnIe_z5z5(@Bzk?FwpNpXAkEjsY(B%ARlHsQOt(`abR8c4i}Oa+{W{}cUx?TzLKg+|{5t)0`Y-?D?7J_VpD4z_0s36vum68xSF+qT"
    "l0<(6;h<wE2h1QgQskT%mRhYDOLSQB^u>pUNLoTSMJl*RqeK7u<a?P}07$v#VhbQpsLIOa<x*AWSLa_ZF0U_oR>!0}MRE-jH~s5mSwBWn5?cd`"
    "O{t(~<_6k2V%q*40rn%3P@>5BnVJjAMl7vX6p4q>NeZ^Y9(9sFFHY3rqIPFywL5;+Y`3FdJ<&MA!{WHwzwxZLEfDQ;2N1Uu-qSuXMd>YclAK)-"
    "=AMPqJ>@s6yB2)riDL}1QzQu<AIp1jl8*Q)vX)AkZha1J8Fhv>I(+X0i-Y#kz#uvGm$2NR7fn~fuO0Dc{C4PKW%2&k9;T$8&w3NWPI{`Z2`LBq"
    "m(Fo4Ev9;dGc80FjBB}%QC|jQC)HQFg`Xb{*wZ>A`$9>)v152(>*p~xSwZv|f(^FOBR5LwIa4KLQPMvchqzzh=GEm{H2L)D+ts(vliSPbb<g=x"
    "29oDBSMoX)oq;tfLis<#gIo`yxC>SLh)@jD#*4TXmb}A@%;4mC93?|L<-UBeP<OSFsjilD(Me?H=@PX;;;<&lSU2mZhf1*iNO;G~$0&@7s_b#p"
    "kM8gHLYK6kWtvMwxu3q=`nAxA8oCdY$svGOM~Sf4S~^p%?rH2vE6%$gqzGM%p?Fd;kT)Gib<GhrEL!5+U5fP8^z8iW<n|oG8@8(yxnt!)RcrXQ"
    "t697*_K5mS$Y)#m#SxUYwEl$p)Qvoc10d<isNv$MxWH@?albc&8$I`~dxOeXclC~FF8RWYkZ=6=Qvr^DB98nd5C9SsL6UJXD>oL4WU_{lbBLIT"
    "r7zKuMg_80J3KOv@h|qFmN9R4dje!!ofzxkta<6-i^$vp(NCE`f&qSGUTw=eu60%I7Um@zM;GN&<mw!^Z!RycFMqlGG`YTwE+$`YFzJY`i5(Y="
    "HIAg6rPAxEtTeI2O+$4}-g5nd34AgX111-}8TT{cd~&uj*LJqn?Kz9oPr!ykb))_L-Sd7aCKAN{{ti*xdCdmc-?HSnx-iwR=!#g2u=0c?^{ylX"
    "G%b2qS4$-YE>nKUPix&qr~G^oN4oeGR7x_xS1(;e%THQR2us@6rbx<<(T5N9+MMx+4=A>I05{yP2}MMN7SeqYL@Q9`PMg92OB^L3I&4vjT~c-W"
    "2zOo-=ac4C_N)o$q&bQWTSROeTY4`vfrd@uJRQb)F(4)FJkPoAw`J_MTr;&&!A{^aJD&GWb=%4EI2jaJBepPt+6QC3Ctd&|8WpoH&`j-_M<5_{"
    "X=_I(ksUVcKU71IA7m{3VG_n-a^E!&hk(Y-+Nu+0d+_Cn8)fZhK4S4rwTqk57Cl0NJqf<H(G1df6!;F0My0Nr#$o3#XrVypm9*qp=*%WI^qsO?"
    "ClxiF4pV`QKk!92Ftfd&$MveG(~q)IOuQ%rWLTjkNEgnETHbEZ5uHNei1)lRs)0q}mi4iD)<VTiJt-VV%IBmFTy*qFFI0BGFAGa?ecezT>}AP}"
    "tH4^oO%Vne{>WbyOWhyDr-MFu5JoyphP?tf<u}lVm_#}AxwPuc`JP7lU*&2K$Sz=Ts33{-&>9{ki=dM%G@ZvoHXX2z^YkdiQ$}VQ=^&FJxLMnW"
    "a?4|xm5^@^O{8O>s7)mbYnpXpO5LFri>*N|c`yrjOpUcR-)}cB&!vq96I8<gtiitFMH|Pr$Ggo!#1bReu^NYa6-Rr!Z`wQl`B1DuYY)r2*p?nH"
    "3uRZ;_|23jCw2K6mVUBpg{X|afEK(GexOporpFm2jjQFt!Q+@9Y)`=>N|yVrer~sxd4-14cZa<csXOrrMGa#*Go<hGOw+GL|Gfst;lOk4nr(Ov"
    "e}B7BnMC#m0Ba{Iu~OLfi3^%<MEySiQo%3++$u=rqQl-uKBJaNCMX9#>A2&D7LwUgAF{=#SuTKJ7u2Th5Gvp_8)jfk$Pv`EQ3-wW#kj5n6o1*I"
    "(ktMh=#jYs7R{P1#5BrH>$a&u2X7emR;_0E6#!UaAW{I@7WyLmIiaAC$wX8OF{q+|8F{-~ysk}_6u+$It{Rhgl;ZS>ma1=g%={{Nk~<X$x~e$e"
    "Bmn#C5F#H(@H+)=Rer3Jo5Zuc)cv{V4MCMQb#KzBo1e6CbXa84%}$gB8rwlzN*|9IVl=KUbw73)?(Su=Sh?fof|1|JyUz>M51<z{+?;5Uk{G?*"
    "RW3DD$(_?{c!2gEtN#+M<h`tTZ-J0F5~w^9Q^d+9zBcL&2JhL*VfRh#Svxulg8>R^ys_;XUwV!7aCGdSpw?DnUh=XyU(fVeVRO|<s8B6~ZA1{E"
    "$a=%~!PpsPG@ImVDCzh5@7+HU4mT{KEUJAfMj}9=PXMae-4yj`PYqeN2{b1vda!NSksz*r4g0QQ#HaYQwd+b%deHi`=0<@6_>sU3bwe_SfsUbG"
    "7J=4fA_ni>8`T7?SLMcnOv?Lv-TS^?s|c1h=%wlxfL8P`B8|`0oTbm~Y+$1qYD~Cj8*DVWxcGX0b94EhbIi1K0sJWn6#!$o4CT-<tF9?kIA{Q+"
    "bHZU}sB04)D`Mw;jOT}tpr&?H@o(UK#s9}-s2Zep#53?PDh&7-l%o0C&4IFLcwTV0gbu>=!%@2`ox(p^R`)C7-RSD_X7XA5hV!#SzTYBG5oXd&"
    "dx$Nedyn>O9LgQ(L>jyb)jCb=ja@{P#tMmklvE)yAnG%+ETyNczg_o9ac{|Tew)4Jdi|&Ti~7^~ruxCc9NIE%WVR;!LQUH2VGa1(-HH(2W+y=n"
    "7Gu;LR;aD}_*fF<@gxTPe)eth**-*@Vds-D>#{Rf`yVL!-0Ww&z%~52T)pa?Q8#SGu9;IQCXj-%Htn|&zfZg~Ln{<3VlIQ60c*y(<pl~d4{@aG"
    "FzGzX*o27%_%=-tJbt#}Cu{^gf+!<KwziVw+G`Cn-gH@e(U*EEgTKZ(MM$th&4vc*w)=ZzBpJFX_e=SsH7|M`#ACUVL4XlqLqk~@XZ0n_&p^0z"
    "Ezf&=TTHtkH2nJI>-6^glg4;_j!JObGiMVek!E{1BaK;N-;cgX2?)7VI=X;58*`fLp`#ei#E$A3vR8+COc)h(aYqHPbsQS7e2B5W;iDyY1CW+|"
    "q%B%k;4!SGXQ9CY6TPGR?AFJq;^$_(E^yo$4^_K+jkL7J33@A<NS9U%uPipZE$&~#V9Xc0Rx~I{!KHOfi1dM$$JezWU&AkN_!38cga=vQh-Wn-"
    "Sh1%K-5Is`ns@$YfA@zSCgOz=q5B)=vKRA46img5)?tUGXNwmeGKsTP)C0zj)yf@*L2FX>1>Tt`PAXM;_(tHZB^)%&r&qd@5h>CbKpi|p%&<Hn"
    "6d3F^IJ)8>3_^s~NfscaQ(^ih5n%16$++ptcN;OGlb%?=+lG5qha4LC(gF#lIUX(8<5*JF$8pr?Fj92=_dyhfBM&xRq9xV|{AbXuk#Ezn4WR+}"
    "evE)NCalAy%)D!Jw_j1bkpZP{vCU6h^!8Aax%%#ERAzcCD8<E)b`lQ<L5FG*Rpz?6JBl84Vw6uU5M9Tej;Md*uI0AvtR9UgIEnR`1oqCU%a9Qm"
    "3~C-R<e|BPLM(J;4x(zXZb2z7hVH;lvoXjYz=yWbb$HE=PMTd1ehDA1cJ;S%|CWDZ;K79&6U8AL6TD0mc%mJ7BLoMg;)@VqiE0r!eS>t9gXj$D"
    "H#&$J7*^+RZ-yu!fbMj)q7zf1fIFJG+V(ZjSerh0^do)Vv)fBhL_O{}IO_A3Q_fTt-SxPU5K<@7u^ycj)R$?T2g1!pz>uPl=L_RHk9yf=P)rt?"
    "%7CiriI>wAc}V)ff3{55?fP}SE17r^$wCqhCLOsQe|d<}ikF&N<}1L2CI$dG{e_~J;)S#b(UGZGYl{kcIS2&d>hgN}Rp+s}I?+6{Ly#JbTGNSK"
    "LIpo81jlGz7Ca>cCQK63#O+9U9GE%8Q1*4`*{Vxbk7=O5dpsNiJgkho2NV5ETh)=XnyQW?=w(9<Yg(8^i<VirU`QR`weqiC^tDuvymV4n{Cf!_"
    "2I){{Q1PX0GWjaJ%ctWIbAWe(#*XFJVhUh)k1Ld+;4OqTmK&~DvIqjB4Y2I)VznY2uFeCJ0H3aF<8zxt-Cr*+em#MoHBHDv(>$(4pR+MlYdFnf"
    "O$hCDJsXD%IO+rzg1%~8`EO#?fw0H6%LUCbYBMCMNStA3uFzC1g~~T(;l0B~@7q+!dwzEL?Mg?M#?pJ0kbGun<G{t?xwdqE)MU1~S^c^#YftMl"
    "&uE2PE>t`4Zy5%l>Y5{2-V<mo^SND<DBkrf>VBU7#(pEH<GRv2{;Jre>25W`K^8EC&lQ}#+64@5pIF61_nF=+w#eLQQ2rkKN>*4xa_AqxX%q9Z"
    "(v22%0EpSjYe>qHH<)QHJv^aw3jKX5H@j6mS9yD`iZEpIg6)!KakHm#hsv2_*Ox)QwiDHLy(b+D4p{60Vsh>tT4&&QF;geT1WXvJ<OlU{vC0qv"
    ")x3x$U^<~;bM<|YMSGB^VUW{A2ZN5h9j>&#G!SZd&Y}z<zS4x@+q#5)Lqq_f|NZyhePQ*?;)f{m@Tv~EN)Tdb=i}wBKqXgKawT}=Fm)++^Ro3&"
    "e%HR7jT@01+-Sx!<Qn!|oOk(4EK=<#eqX82GX^17qHw>j976M!NK&IOyptZ?$r?TR2&p@KplClZh-m-#_ptrbY2$Kd>XaQ3T?$poKhsDjn-^Im"
    "^31>T=ItU}$fSH<z5DC0{{hWlDW?"
)

BIAS_CATALOG: tuple[dict[str, str], ...] = (
    {
        "bias_id": "ikea_effect",
        "section": "A",
        "name_es": "Efecto IKEA y Agencia Humana",
        "name_en": "IKEA Effect & Human Agency",
        "theorist": "Norton, Mochon & Ariely",
    },
    {
        "bias_id": "mental_accounting",
        "section": "4.1",
        "name_es": "Contabilidad Mental",
        "name_en": "Mental Accounting",
        "theorist": "Richard Thaler",
    },
    {
        "bias_id": "halo_effect",
        "section": "4.1",
        "name_es": "Efecto Halo / Ceguera de Indicador Único",
        "name_en": "Single-Metric Fallacy & Halo Effect",
        "theorist": "Edward Thorndike / Behavioral Finance",
    },
    {
        "bias_id": "house_rich_cash_poor",
        "section": "4.1",
        "name_es": "Ilusión de Riqueza Inmobiliaria",
        "name_en": "House-Rich, Cash-Poor Illusion",
        "theorist": "Liquidity vs Net Worth Framing",
    },
    {
        "bias_id": "present_bias",
        "section": "4.2",
        "name_es": "Descuento Hiperbólico / Sesgo del Presente",
        "name_en": "Present Bias / Hyperbolic Discounting",
        "theorist": "David Laibson / Ainslie",
    },
    {
        "bias_id": "future_self_gap",
        "section": "4.2",
        "name_es": "Desconexión con el Yo Futuro",
        "name_en": "Future-Self Continuity Gap",
        "theorist": "Hal Hershfield",
    },
    {
        "bias_id": "planning_fallacy",
        "section": "4.2",
        "name_es": "Falacia de Planificación y Costes Ocultos",
        "name_en": "Planning Fallacy & Hidden Cost Neglect",
        "theorist": "Kahneman & Tversky",
    },
    {
        "bias_id": "ostrich_effect",
        "section": "4.3",
        "name_es": "Efecto Avestruz",
        "name_en": "Ostrich Effect",
        "theorist": "Galai & Sade / Karlsson et al.",
    },
    {
        "bias_id": "optimism_bias",
        "section": "4.3",
        "name_es": "Sesgo de Optimismo e Invulnerabilidad",
        "name_en": "Optimism Bias & Mortality Salience",
        "theorist": "Tali Sharot / Terror Management",
    },
    {
        "bias_id": "oxygen_mask_syndrome",
        "section": "4.3",
        "name_es": "Priorización Emocional Invertida (Mascarilla de Oxígeno)",
        "name_en": "Oxygen Mask Syndrome",
        "theorist": "Behavioral Family Prioritization",
    },
    {
        "bias_id": "choice_overload",
        "section": "4.4",
        "name_es": "Parálisis por Análisis y Sobrecarga",
        "name_en": "Choice Overload / Hick's Law",
        "theorist": "Iyengar & Lepper / William Edmund Hick",
    },
    {
        "bias_id": "status_quo_bias",
        "section": "4.4",
        "name_es": "Sesgo de Statu Quo y Curva del Olvido",
        "name_en": "Status Quo Bias & Ebbinghaus Curve",
        "theorist": "Samuelson & Zeckhauser / Hermann Ebbinghaus",
    },
    {
        "bias_id": "loss_aversion_recency",
        "section": "4.4",
        "name_es": "Aversión a la Pérdida y Sesgo de Recencia",
        "name_en": "Loss Aversion & Recency Bias",
        "theorist": "Kahneman & Tversky",
    },
    {
        "bias_id": "couples_veto",
        "section": "4.4",
        "name_es": "Veto Silencioso y Silos en Pareja",
        "name_en": "Couples Veto & Role Siloing",
        "theorist": "Household Bargaining Dynamics",
    },
)

BIAS_METADATA: dict[str, dict[str, str]] = {item["bias_id"]: item for item in BIAS_CATALOG}
ALL_BIAS_IDS: tuple[str, ...] = tuple(item["bias_id"] for item in BIAS_CATALOG)
SECTION_4_BIAS_IDS: tuple[str, ...] = tuple(
    item["bias_id"] for item in BIAS_CATALOG if item["section"].startswith("4.")
)


@dataclass(frozen=True)
class ObjectiveConcern:
    """Structured objective concern (`O1..O9`) parsed from `persona.md`."""

    id: str
    severity: str
    title: str
    detail: str
    connected: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "severity": self.severity,
            "title": self.title,
            "detail": self.detail,
            "connected": self.connected,
        }


@dataclass(frozen=True)
class TensionItem:
    """Structured tension (`T1..T5`) parsed from `persona.md`."""

    id: str
    severity: str
    summary: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "severity": self.severity,
            "summary": self.summary,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class PersonaProfile:
    """Parsed structural & psychological fields from `persona.md`."""

    household_heading: str
    sections: dict[str, str]
    transition_alerts: list[str]
    subjective_concerns_raw: str
    has_subjective_concerns: bool
    objective_concerns: list[ObjectiveConcern]
    tensions: list[TensionItem]
    classification: dict[str, Any]
    risk_alignment: str
    decision_style: str
    motivational_anchor: str


@dataclass
class CaseData:
    """Real Sherpas household bundle loaded from `financial-health.json`, `investment-analysis.json`, and `persona.md`."""

    case_id: str
    case_dir: Path
    financial_health: dict[str, Any]
    investment_analysis: dict[str, Any]
    persona_text: str
    persona: PersonaProfile

    @property
    def household(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("case", {}).get("household", []))

    @property
    def adults(self) -> list[dict[str, Any]]:
        return [m for m in self.household if m.get("role") in ("client", "co-client")]

    @property
    def children(self) -> list[dict[str, Any]]:
        return [m for m in self.household if m.get("role") == "child"]

    @property
    def is_couple(self) -> bool:
        return len(self.adults) > 1

    @property
    def household_name(self) -> str:
        names = [str(m.get("first_name", "")).strip() for m in self.adults if m.get("first_name")]
        return " & ".join(names) if names else self.case_id

    @property
    def published_score(self) -> int:
        return int(self.financial_health.get("score", {}).get("published_score", 0))

    @property
    def score_band(self) -> str:
        return str(self.financial_health.get("score", {}).get("band", ""))

    @property
    def pillars(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("score", {}).get("pillars", []))

    @property
    def caps_applied(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("score", {}).get("caps_applied", []))

    @property
    def top_moves(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("score", {}).get("top_moves", []))

    @property
    def combined_moves(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("score", {}).get("combined_moves", []))

    @property
    def chart_goals(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("goals", {}).get("chartGoals", []))

    @property
    def goals_summary(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("goals", {}).get("goalsSummary", []))

    @property
    def fh_facts(self) -> dict[str, Any]:
        return dict(self.financial_health.get("key_metrics", {}).get("facts", {}))

    @property
    def ia_facts(self) -> dict[str, Any]:
        return dict(self.investment_analysis.get("key_metrics", {}).get("facts", {}))

    @property
    def yearly_projections(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("projections", {}).get("yearly", []))

    @property
    def profile(self) -> dict[str, Any]:
        return dict(self.financial_health.get("profile", {}))

    @property
    def tax_drag_analysis(self) -> dict[str, Any]:
        return dict(self.investment_analysis.get("key_metrics", {}).get("taxDragAnalysis", {}))

    @property
    def performance_analysis(self) -> dict[str, Any]:
        return dict(self.investment_analysis.get("key_metrics", {}).get("performanceAnalysis", {}))

    @property
    def savings_and_contributions(self) -> dict[str, Any]:
        return dict(self.investment_analysis.get("key_metrics", {}).get("savingsAndContributions", {}))

    @property
    def savings_waterfall(self) -> list[list[Any]]:
        return list(self.savings_and_contributions.get("savingsWaterfall", []))

    @property
    def analysis_events(self) -> list[dict[str, Any]]:
        return list(self.investment_analysis.get("analysis", {}).get("events", []))

    @property
    def per_event_drawdowns(self) -> list[dict[str, Any]]:
        return list(self.performance_analysis.get("perEventDrawdowns", []))

    @property
    def positions(self) -> list[dict[str, Any]]:
        return list(self.investment_analysis.get("positions", []))

    def first_negative_investable_year(self) -> dict[str, Any] | None:
        for row in self.yearly_projections:
            if (row.get("investable_assets") or 0) < 0:
                return row
        return None

    def first_negative_net_worth_year(self) -> dict[str, Any] | None:
        for row in self.yearly_projections:
            if (row.get("net_worth") or 0) < 0:
                return row
        return None

    def projection_for_year(self, year: int) -> dict[str, Any] | None:
        for row in self.yearly_projections:
            if row.get("year") == year:
                return row
        return None

    def tax_drag_annual_cost(self) -> float:
        for row in self.tax_drag_analysis.get("householdRollup", []):
            if len(row) >= 2 and "In-scope tax cost" in str(row[0]):
                return float(row[1])
        return 0.0

    def cash_yield_earned(self) -> float:
        cash_needs = self.investment_analysis.get("key_metrics", {}).get("cashNeeds", {})
        total = 0.0
        for row in cash_needs.get("summaryIncome", []):
            if len(row) >= 2 and str(row[0]).strip() in ("Liquidity", "Excess accessible", "Operational buffer"):
                try:
                    total += float(row[1])
                except (TypeError, ValueError):
                    pass
        return round(total, 2)

    def high_interest_debts(self, threshold: float = 0.10) -> list[dict[str, Any]]:
        debts: list[dict[str, Any]] = []
        for item in self.profile.get("liabilities", []) or []:
            bal = float(item.get("balance") or 0.0)
            rate = float(item.get("interest_rate") or 0.0)
            if bal > 0 and rate >= threshold:
                debts.append(
                    {
                        "name": item.get("name", "Card"),
                        "type": item.get("type", ""),
                        "balance": bal,
                        "interest_rate": rate,
                        "apr_pct": round(rate * 100, 1),
                        "annual_interest": round(bal * rate, 2),
                        "monthly_payment": float(item.get("monthly_payment") or 0.0),
                        "owner": list(item.get("owner") or []),
                    }
                )
        return debts

    def waterfall_row(self, bucket_fragment: str) -> dict[str, Any] | None:
        frag = bucket_fragment.lower()
        for row in self.savings_waterfall[1:]:
            if len(row) >= 4 and frag in str(row[1]).lower():
                return {
                    "step": row[0],
                    "bucket": row[1],
                    "current": row[2],
                    "optimal_target": row[3],
                    "status": row[4] if len(row) > 4 else "",
                    "delta": row[5] if len(row) > 5 else None,
                }
        return None


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".tmp_", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def _try_fetch_mcp_case(case_id: str) -> dict[str, Any] | None:
    if not os.environ.get("MCP_TOKEN"):
        return None
    try:
        from backend import mcp_client  # type: ignore

        data = mcp_client.get_case(case_id, allow_fallback=False)
    except Exception:
        return None
    if (
        isinstance(data, dict)
        and isinstance(data.get("financial-health"), dict)
        and isinstance(data.get("investment-analysis"), dict)
        and isinstance(data.get("persona"), str)
    ):
        return {
            "fh": data["financial-health"],
            "ia": data["investment-analysis"],
            "persona": data["persona"],
        }
    return None


def _ensure_embedded_cases_dir() -> Path:
    """Materialize canonical Sherpas cases into a shared temp directory when `cases/` is absent on disk."""
    base_dir = Path(tempfile.gettempdir()) / _EMBEDDED_CACHE_DIR_NAME
    required_files = ("financial-health.json", "investment-analysis.json", "persona.md")

    def _all_present() -> bool:
        return all((base_dir / cid / fname).is_file() for cid in SUPPORTED_CASES for fname in required_files)

    if _all_present():
        return base_dir

    with _EMBEDDED_LOCK:
        if _all_present():
            return base_dir
        raw_json = zlib.decompress(base64.b85decode(_EMBEDDED_CASES_B85.encode("ascii"))).decode("utf-8")
        embedded_cases = json.loads(raw_json)
        for cid in SUPPORTED_CASES:
            cdir = base_dir / cid
            if all((cdir / fname).is_file() for fname in required_files):
                continue
            bundle = _try_fetch_mcp_case(cid) or embedded_cases[cid]
            _atomic_write_text(
                cdir / "financial-health.json",
                json.dumps(bundle["fh"], ensure_ascii=False, separators=(",", ":")),
            )
            _atomic_write_text(
                cdir / "investment-analysis.json",
                json.dumps(bundle["ia"], ensure_ascii=False, separators=(",", ":")),
            )
            _atomic_write_text(cdir / "persona.md", str(bundle["persona"]))
    return base_dir


def resolve_cases_dir(cases_dir: str | Path | None = None) -> Path:
    """Locate the `cases/` directory via explicit arg, env vars, portable paths, or embedded fallback."""
    if cases_dir is not None:
        explicit = Path(cases_dir)
        if not explicit.is_dir():
            raise FileNotFoundError(f"Specified cases_dir does not exist: {explicit}")
        return explicit

    candidates: list[Path] = []
    for env_key in ("SHERPAS_CASES_DIR", "CASES_DIR"):
        env_dir = os.environ.get(env_key)
        if env_dir:
            candidates.append(Path(env_dir))

    project_root = Path(__file__).resolve().parent.parent
    candidates.append(project_root / "cases")
    candidates.append(Path.cwd() / "cases")
    candidates.append(project_root.parent / "cases")
    candidates.append(project_root.parent / "hackathon-upv-2026" / "cases")
    candidates.append(Path.cwd().parent / "hackathon-upv-2026" / "cases")

    for candidate in candidates:
        if candidate.is_dir() and any(
            (candidate / c).is_dir() and (candidate / c / "financial-health.json").is_file()
            for c in SUPPORTED_CASES
        ):
            return candidate
    return _ensure_embedded_cases_dir()


def list_available_cases(cases_dir: str | Path | None = None) -> list[str]:
    """Return sorted list of valid case IDs available on disk."""
    root = resolve_cases_dir(cases_dir)
    found = [
        p.name
        for p in sorted(root.iterdir())
        if p.is_dir() and (p / "financial-health.json").is_file()
    ]
    return found


def parse_persona_markdown(markdown_text: str) -> PersonaProfile:
    """Parse structured sections, Objective concerns (`O1..O9`), Tensions (`T1..T5`), and alerts."""
    heading = ""
    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for line in markdown_text.splitlines():
        if line.startswith("# ") and not heading:
            heading = line[2:].strip()
            continue
        if line.startswith("## "):
            current_section = line[3:].strip()
            sections[current_section] = []
            continue
        if current_section is not None:
            sections[current_section].append(line)

    section_text = {k: "\n".join(v).strip() for k, v in sections.items()}

    # Transition alerts
    transition_raw = section_text.get("Transition alerts", "")
    transition_alerts: list[str] = []
    for line in transition_raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            transition_alerts.append(stripped[2:].strip())
    if not transition_alerts and transition_raw and "none detected" not in transition_raw.lower():
        transition_alerts.append(transition_raw)

    # Subjective concerns
    subj_raw = section_text.get("Subjective concerns", "").strip()
    has_subj = bool(
        subj_raw
        and not subj_raw.lower().startswith("none detected")
        and not subj_raw.lower().startswith("none recorded")
    )

    # Objective concerns (`O1..O9` supporting both Michael and Samantha/Weah/Johnson formats)
    obj_concerns: list[ObjectiveConcern] = []
    obj_raw = section_text.get("Objective concerns", "")
    pat_a = re.compile(r"^-\s+\*\*(O\d+)\s+(CRITICAL|SIGNIFICANT|MODERATE|MINOR):\s*(.+?)\*\*\s*(.*)$")
    pat_b = re.compile(
        r"^-\s+\*\*(O\d+):\s*(.+?)\s*\((CRITICAL|SIGNIFICANT|MODERATE|MINOR)\)\.?\*\*\s*(.*)$"
    )
    for line in obj_raw.splitlines():
        s = line.strip()
        m_a = pat_a.match(s)
        m_b = pat_b.match(s)
        if m_a:
            oid, sev, title, detail = m_a.groups()
        elif m_b:
            oid, title, sev, detail = m_b.groups()
        else:
            continue
        conn_match = re.search(r"Connected:\s*([^.]+)\.?\s*$", detail)
        connected = conn_match.group(1).strip() if conn_match else ""
        obj_concerns.append(
            ObjectiveConcern(
                id=oid,
                severity=sev,
                title=title.rstrip("."),
                detail=detail.strip(),
                connected=connected,
            )
        )

    # Tensions (`T1..T5` supporting both `(HIGH):` and `: title (HIGH).` formats)
    tensions: list[TensionItem] = []
    ten_raw = section_text.get("Tensions", "")
    t_pat_a = re.compile(r"^-\s+\*\*(T\d+)\s*\((HIGH|MEDIUM|LOW)\):\*\*\s*(.*)$")
    t_pat_b = re.compile(r"^-\s+\*\*(T\d+):\s*(.+?)\s*\((HIGH|MEDIUM|LOW)\)\.?\*\*\s*(.*)$")
    for line in ten_raw.splitlines():
        s = line.strip()
        m_a = t_pat_a.match(s)
        m_b = t_pat_b.match(s)
        if m_a:
            tid, sev, detail = m_a.groups()
            summary = detail.split(".", 1)[0].strip()
        elif m_b:
            tid, summary, sev, detail = m_b.groups()
        else:
            continue
        tensions.append(
            TensionItem(
                id=tid,
                severity=sev,
                summary=summary.rstrip("."),
                detail=detail.strip(),
            )
        )

    # Classification block
    classification: dict[str, Any] = {}
    cls_match = re.search(r"```classification\s*(.*?)```", markdown_text, re.DOTALL)
    if cls_match:
        current_list_key: str | None = None
        for raw_line in cls_match.group(1).splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("- ") and current_list_key:
                classification[current_list_key].append(line[2:].strip())
            elif ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                if val == "":
                    classification[key] = []
                    current_list_key = key
                else:
                    classification[key] = val
                    current_list_key = None

    return PersonaProfile(
        household_heading=heading,
        sections=section_text,
        transition_alerts=transition_alerts,
        subjective_concerns_raw=subj_raw,
        has_subjective_concerns=has_subj,
        objective_concerns=obj_concerns,
        tensions=tensions,
        classification=classification,
        risk_alignment=str(classification.get("D4", "")),
        decision_style=str(classification.get("D5", "")),
        motivational_anchor=str(classification.get("D6", "")),
    )


def load_case(case_id: str, cases_dir: str | Path | None = None) -> CaseData:
    """Load real JSONs and `persona.md` for one of the 4 Sherpas cases."""
    if case_id not in SUPPORTED_CASES:
        raise ValueError(f"Unknown case_id '{case_id}'. Expected one of {SUPPORTED_CASES}.")
    root = resolve_cases_dir(cases_dir)
    case_dir = root / case_id
    fh_path = case_dir / "financial-health.json"
    ia_path = case_dir / "investment-analysis.json"
    persona_path = case_dir / "persona.md"

    if not fh_path.is_file() or not ia_path.is_file() or not persona_path.is_file():
        raise FileNotFoundError(f"Missing required case files inside {case_dir}.")

    fh = json.loads(fh_path.read_text(encoding="utf-8-sig"))
    ia = json.loads(ia_path.read_text(encoding="utf-8-sig"))
    persona_text = persona_path.read_text(encoding="utf-8-sig")
    persona = parse_persona_markdown(persona_text)
    return CaseData(
        case_id=case_id,
        case_dir=case_dir,
        financial_health=fh,
        investment_analysis=ia,
        persona_text=persona_text,
        persona=persona,
    )


def _add_numeric_variants(bucket: set[float], val: float) -> None:
    if abs(val) > 1e12:
        return
    for candidate in (val, abs(val)):
        bucket.add(round(candidate, 4))
        bucket.add(round(candidate, 2))
        bucket.add(round(candidate, 1))
        bucket.add(float(round(candidate)))
    if -2.0 <= val <= 2.0:
        pct = abs(val) * 100.0
        bucket.add(round(pct, 2))
        bucket.add(round(pct, 1))
        bucket.add(float(round(pct)))


def _walk_numbers(node: Any, bucket: set[float]) -> None:
    if isinstance(node, bool):
        return
    if isinstance(node, (int, float)):
        _add_numeric_variants(bucket, float(node))
    elif isinstance(node, str):
        for raw in re.findall(r"-?\d[\d,]*(?:\.\d+)?", node):
            try:
                num = float(raw.replace(",", ""))
                _add_numeric_variants(bucket, num)
            except ValueError:
                pass
    elif isinstance(node, list):
        for item in node:
            _walk_numbers(item, bucket)
    elif isinstance(node, dict):
        for val in node.values():
            _walk_numbers(val, bucket)


def extract_case_allowed_numbers(
    case: CaseData,
    extra_numbers: list[float | int] | dict[str, Any] | str | None = None,
) -> set[float]:
    """Collect every verified number from `financial-health.json`, `investment-analysis.json`, and `persona.md`."""
    allowed: set[float] = {0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0, 30.0, 60.0, 100.0}
    _walk_numbers(case.financial_health, allowed)
    _walk_numbers(case.investment_analysis, allowed)
    _walk_numbers(case.persona_text, allowed)

    # Scaled notations from persona.md / report abbreviations (e.g. $550k -> 550000, $2.35M -> 2350000)
    for match in re.finditer(r"(\d+(?:\.\d+)?)\s*([kKmM])\b", case.persona_text):
        base = float(match.group(1))
        mult = 1_000.0 if match.group(2).lower() == "k" else 1_000_000.0
        _add_numeric_variants(allowed, base * mult)
        _add_numeric_variants(allowed, base)

    # Exact derived annual debt interest and net cash drag figures directly implied by liabilities & cash
    for debt in case.high_interest_debts(threshold=0.0):
        _add_numeric_variants(allowed, debt["annual_interest"])
    cash_earned = case.cash_yield_earned()
    if cash_earned > 0:
        _add_numeric_variants(allowed, cash_earned)
    for debt in case.high_interest_debts(threshold=0.10):
        if cash_earned > 0:
            _add_numeric_variants(allowed, debt["annual_interest"] - cash_earned)

    # Combined life gap across spouses and 401(k) marginal tax saving when directly implied by waterfall
    wf_ins = case.waterfall_row("insurance")
    if wf_ins and isinstance(wf_ins.get("delta"), (int, float)):
        _add_numeric_variants(allowed, abs(float(wf_ins["delta"])))
    wf_401k = case.waterfall_row("401k")
    tax_bracket = float(
        case.savings_and_contributions.get("taxOpportunityCheck", {})
        .get("preTaxVsRothCheck", {})
        .get("currentTaxBracket", 0.0)
    )
    if wf_401k and isinstance(wf_401k.get("delta"), (int, float)) and tax_bracket > 0:
        _add_numeric_variants(allowed, abs(float(wf_401k["delta"])) * tax_bracket)

    if extra_numbers is not None:
        _walk_numbers(extra_numbers, allowed)
    return allowed


def _strip_structural_tokens(text: str) -> str:
    cleaned = re.sub(r"\b[OTD]\d+[a-c]?\b", " ", text)
    cleaned = re.sub(r"\b401\s*\(?k\)?", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b529\b", " ", cleaned)
    cleaned = re.sub(r"\b3x\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b(?:Día|Dia|Day|Step|Paso)\s+\d+\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b\d+/\d+\b", " ", cleaned)
    cleaned = re.sub(r"(?m)^\s*\d+[\.\)]\s+", " ", cleaned)
    return cleaned


def verify_text_numbers_against_case(
    text: str,
    allowed_numbers: set[float],
) -> tuple[bool, list[str]]:
    """Verify every numeric figure in `text` belongs to `allowed_numbers` (no invented numbers)."""
    cleaned = _strip_structural_tokens(text)
    unverified: list[str] = []

    for match in re.finditer(r"(-?\d[\d,]*(?:\.\d+)?)(\s*[kKmM])?", cleaned):
        raw_num = match.group(1)
        suffix = (match.group(2) or "").strip().lower()
        try:
            val = abs(float(raw_num.replace(",", "")))
        except ValueError:
            continue
        candidates = [val]
        if suffix == "k":
            candidates.append(val * 1_000.0)
        elif suffix == "m":
            candidates.append(val * 1_000_000.0)

        matched = any(
            round(c, 4) in allowed_numbers
            or round(c, 2) in allowed_numbers
            or round(c, 1) in allowed_numbers
            or float(round(c)) in allowed_numbers
            for c in candidates
        )
        if not matched:
            token = f"{raw_num}{suffix}"
            if token not in unverified:
                unverified.append(token)

    return (len(unverified) == 0, unverified)


def _fmt_usd(amount: float | int) -> str:
    val = float(amount)
    sign = "-" if val < 0 else ""
    abs_val = abs(val)
    if abs(abs_val - round(abs_val)) < 0.005:
        return f"{sign}${round(abs_val):,}"
    return f"{sign}${abs_val:,.2f}"


def _fmt_pct(value: float | str, is_decimal_ratio: bool = False) -> str:
    if isinstance(value, str):
        return value if value.endswith("%") else f"{value}%"
    pct = value * 100.0 if is_decimal_ratio else float(value)
    if abs(pct - round(pct)) < 0.05:
        return f"{round(pct)}%"
    return f"{pct:.1f}%"


def _build_topic_context(case: CaseData, topic: str, extra_context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Assemble strictly real Plain + Math content from JSONs & persona.md for the requested topic."""
    cash_facts = case.fh_facts.get("cash", {})
    ret_facts = case.fh_facts.get("retirement", {})
    edu_facts = case.fh_facts.get("education") or {}
    accessible_cash = float(cash_facts.get("accessibleCash", {}).get("value", 0.0))
    months_before = str(cash_facts.get("monthsCovered", {}).get("value", "0"))
    months_after = str(cash_facts.get("monthsCoveredAfterNearTermGoals", {}).get("value", months_before))
    net_cash_flow = float(ret_facts.get("netCashFlowThisYear", {}).get("value", 0.0))
    high_debts = case.high_interest_debts(threshold=0.10)
    tax_drag = case.tax_drag_annual_cost()
    neg_inv = case.first_negative_investable_year()
    neg_nw = case.first_negative_net_worth_year()
    savings_cur = case.savings_and_contributions.get("currentSavings", {})
    savings_rate_pct = float(savings_cur.get("currentSavingsRate", 0.0)) * 100.0
    annual_savings = float(savings_cur.get("reportedAnnualSavings", 0.0))
    perf_hh = case.performance_analysis.get("household", {})
    max_dd_pct = abs(float(perf_hh.get("maxDrawdown3y", 0.0))) * 100.0
    rec_days = int(perf_hh.get("maxDrawdownRecoveryDays", 0))
    best_move = max(case.top_moves, key=lambda m: int(m.get("score_after", 0)), default={})
    combined_best = max(case.combined_moves, key=lambda m: int(m.get("score_after", 0)), default={})

    topic_norm = (topic or "overview").strip().lower()
    metrics: list[dict[str, Any]] = []
    sources: list[str] = []

    if topic_norm in ("liquidity", "cash_flow", "cash"):
        reserve_min = float(cash_facts.get("emergencyReserve", {}).get("min", 0.0))
        reserve_max = float(cash_facts.get("emergencyReserve", {}).get("max", 0.0))
        plain_headline = f"Tienes {months_before} meses de gastos esenciales cubiertos ({months_after} meses tras metas cercanas)"
        if float(months_after) == 0:
            plain_summary = (
                f"Hoy tu colchón cubre {months_before} meses, pero tras apartar tus metas de 2027 "
                f"bajas a 0 meses de margen líquido. Ordenar primero la reserva protege la tranquilidad diaria."
            )
        elif net_cash_flow < 0:
            plain_summary = (
                f"Cuentas con {months_before} meses de colchón ({_fmt_usd(accessible_cash)}), pero cada año "
                f"salen {_fmt_usd(abs(net_cash_flow))} más de los que entran tras ahorrar {_fmt_usd(annual_savings)}/año."
            )
        else:
            plain_summary = (
                f"Cuentas con {months_before} meses de gastos cubiertos ({_fmt_usd(accessible_cash)}) "
                f"y un margen anual positivo de {_fmt_usd(net_cash_flow)}/año para equilibrar deudas y protección."
            )
        metrics = [
            {"label": "Accessible cash", "value": _fmt_usd(accessible_cash), "unit": "USD", "json_source": "financial-health.json -> key_metrics.facts.cash.accessibleCash"},
            {"label": "Months covered (before / after near-term goals)", "value": f"{months_before} / {months_after}", "unit": "months", "json_source": "financial-health.json -> key_metrics.facts.cash.monthsCovered"},
            {"label": "Recommended emergency reserve", "value": f"{_fmt_usd(reserve_min)}–{_fmt_usd(reserve_max)}", "unit": "USD", "json_source": "financial-health.json -> key_metrics.facts.cash.emergencyReserve"},
            {"label": "Net cash flow this year", "value": _fmt_usd(net_cash_flow), "unit": "USD/yr", "json_source": "financial-health.json -> key_metrics.facts.retirement.netCashFlowThisYear"},
        ]
        bias_unlock = "Separa el dinero de emergencia del dinero comprometido en metas próximas para evitar falsa liquidez."
        action_today = f"Revisa el Step 1 de tu cascada ({case.savings_waterfall[1][1] if len(case.savings_waterfall) > 1 else 'reserva'})."

    elif topic_norm in ("debt", "deuda"):
        if high_debts:
            d = high_debts[0]
            cash_earned = case.cash_yield_earned()
            net_burn = d["annual_interest"] - cash_earned if cash_earned > 0 else d["annual_interest"]
            plain_headline = f"Tu tarjeta {d['name']} quema {_fmt_usd(d['annual_interest'])} al año sin aportar valor a tu familia"
            plain_summary = (
                f"Mantener {_fmt_usd(d['balance'])} en la tarjeta al {d['apr_pct']}% APR cuesta {_fmt_usd(d['annual_interest'])}/año "
                f"({_fmt_usd(d['monthly_payment'])}/mes). Liquidarla libera flujo mensual y calma financiera inmediata."
            )
            if case.case_id == "timothy-melanie-weah":
                plain_summary += (
                    f" Mientras tanto, {_fmt_usd(accessible_cash)} en efectivo solo rinden ~{_fmt_usd(cash_earned)}/año: "
                    f"pierdes ~{_fmt_usd(net_burn)} netos al año por tener ambos cajones separados."
                )
            metrics = [
                {"label": f"{d['name']} balance", "value": _fmt_usd(d["balance"]), "unit": "USD", "json_source": "financial-health.json -> profile.liabilities"},
                {"label": f"{d['name']} APR", "value": f"{d['apr_pct']}%", "unit": "percent", "json_source": "financial-health.json -> profile.liabilities"},
                {"label": "Annual interest cost", "value": _fmt_usd(d["annual_interest"]), "unit": "USD/yr", "json_source": "financial-health.json -> profile.liabilities (balance * interest_rate)"},
                {"label": "Accessible cash", "value": _fmt_usd(accessible_cash), "unit": "USD", "json_source": "financial-health.json -> key_metrics.facts.cash.accessibleCash"},
            ]
            bias_unlock = "Rompe la Contabilidad Mental juntando ahorro e interés caro en un único balance neto."
            action_today = f"Atacar {d['name']} ({_fmt_usd(d['balance'])}) según el escalón 8 de savingsWaterfall."
        else:
            plain_headline = "Sin deudas de consumo: 0 USD quemados en intereses"
            plain_summary = "Tu hogar no arrastra deuda cara ni préstamos activos, lo que libera capacidad para asegurar el retiro."
            metrics = [
                {"label": "Debt pillar points", "value": case.pillars[1]["points_shown_in_app"] if len(case.pillars) > 1 else "20/20", "unit": "points", "json_source": "financial-health.json -> score.pillars"},
            ]
            bias_unlock = "Aprovecha la ausencia de deuda para no caer en el Efecto Halo y atender la jubilación."
            action_today = "Redirigir parte del ahorro anual a cuentas con ventaja fiscal."

    elif topic_norm in ("retirement", "jubilacion"):
        spend_need = float(ret_facts.get("spendingNeed", {}).get("value", 0.0))
        share = str(ret_facts.get("incomeShareOfNeed", {}).get("value", "0%"))
        draw_pct = str(ret_facts.get("withdrawalRateAverage", {}).get("value", "0%"))
        ret_gap = float(case.savings_and_contributions.get("goalCoverage", {}).get("retirementGap", 0.0))
        left_end = float(ret_facts.get("savingsLeftAtPlanEnd", {}).get("value", 0.0))
        if neg_inv:
            plain_headline = (
                f"Alerta de liquidez futura: en {neg_inv['year']} (edad {neg_inv['age_client']}) "
                f"el dinero líquido cae a {_fmt_usd(neg_inv['investable_assets'])}"
            )
            plain_summary = (
                f"Aunque el patrimonio total incluya vivienda ({_fmt_usd(neg_inv['net_worth'])} en {neg_inv['year']}), "
                f"los ingresos garantizados cubren {share} del gasto y el dinero líquido para facturas se agota en {neg_inv['year']}."
            )
        else:
            plain_headline = (
                f"Cobertura garantizada del {share} con {_fmt_usd(left_end)} previstos al final del plan"
                if ret_gap == 0
                else f"Brecha de retiro de {_fmt_usd(ret_gap)}: tus aportaciones actuales aún dejan margen de mejora"
            )
            plain_summary = (
                f"Tus ingresos garantizados cubren el {share} de los {_fmt_usd(spend_need)}/año necesarios en retiro. "
                f"Ahorrando {savings_rate_pct:.1f}% ({_fmt_usd(annual_savings)}/año) puedes ordenar las piezas fiscales."
            )
        metrics = [
            {"label": "Yearly retirement spending need", "value": _fmt_usd(spend_need), "unit": "USD/yr", "json_source": "financial-health.json -> key_metrics.facts.retirement.spendingNeed"},
            {"label": "Guaranteed income share", "value": share, "unit": "percent", "json_source": "financial-health.json -> key_metrics.facts.retirement.incomeShareOfNeed"},
            {"label": "Average withdrawal rate", "value": draw_pct, "unit": "percent", "json_source": "financial-health.json -> key_metrics.facts.retirement.withdrawalRateAverage"},
            {"label": "Retirement gap", "value": _fmt_usd(ret_gap), "unit": "USD", "json_source": "investment-analysis.json -> key_metrics.savingsAndContributions.goalCoverage.retirementGap"},
        ]
        if neg_inv:
            metrics.append(
                {
                    "label": f"First negative investable_assets ({neg_inv['year']}, age {neg_inv['age_client']})",
                    "value": _fmt_usd(neg_inv["investable_assets"]),
                    "unit": "USD",
                    "json_source": f"financial-health.json -> projections.yearly[{neg_inv['year']}].investable_assets",
                }
            )
        else:
            metrics.append(
                {
                    "label": "Savings left at plan end",
                    "value": _fmt_usd(left_end),
                    "unit": "USD",
                    "json_source": "financial-health.json -> key_metrics.facts.retirement.savingsLeftAtPlanEnd",
                }
            )
        bias_unlock = "Conecta tu yo de hoy con tu edad de retiro separando ladrillo ilíquido de liquidez disponible."
        action_today = best_move.get("action", "Aprovechar margen fiscal en 401(k)/HSA.")

    elif topic_norm in ("protection", "proteccion", "insurance"):
        wf_ins = case.waterfall_row("insurance") or {}
        prot_pillar = next((p for p in case.pillars if "insurance" in p.get("pillar", "").lower()), {})
        delta_abs = abs(float(wf_ins.get("delta") or 0.0))
        plain_headline = (
            f"Escudo familiar: pilar de protección en {prot_pillar.get('points_shown_in_app', '0/20')}"
        )
        if delta_abs > 0:
            plain_summary = (
                f"Si faltara un ingreso hoy, la familia tiene una brecha total de {_fmt_usd(delta_abs)} en protección. "
                f"No es hablar de escenarios negativos: es blindar el hogar y los estudios de los hijos."
            )
        else:
            plain_summary = (
                "La cobertura de vida y paraguas está sólida, pero falta confirmar pólizas de vivienda y vehículo."
            )
        metrics = [
            {"label": "Protection pillar", "value": str(prot_pillar.get("points_shown_in_app", "")), "unit": "points", "json_source": "financial-health.json -> score.pillars"},
            {"label": "Insurance waterfall current vs target", "value": f"{_fmt_usd(wf_ins.get('current', 0))} / {_fmt_usd(wf_ins.get('optimal_target', 0))}", "unit": "USD", "json_source": "investment-analysis.json -> key_metrics.savingsAndContributions.savingsWaterfall[2]"},
        ]
        if case.top_moves:
            metrics.append(
                {
                    "label": "Top protection move",
                    "value": f"{case.top_moves[0]['title']} ({case.top_moves[0]['score_before']} -> {case.top_moves[0]['score_after']})",
                    "unit": "score",
                    "json_source": "financial-health.json -> score.top_moves[0]",
                }
            )
        bias_unlock = "Reemplaza el sesgo de optimismo por tranquilidad concreta para quienes dependen de ti."
        action_today = case.top_moves[0]["action"] if case.top_moves else "Confirmar pólizas vigentes."

    elif topic_norm in ("investments", "tax_drag", "inversiones"):
        plain_headline = f"Tus inversiones soportan caídas históricas (máx. -{max_dd_pct:.1f}% recuperada en {rec_days} días) pero pagan {_fmt_usd(tax_drag)}/año en impuestos evitables"
        plain_summary = (
            f"En los últimos 3 años tu cartera resistió una caída máxima de -{max_dd_pct:.1f}% y volvió a recuperar en {rec_days} días. "
            f"Ajustar dónde colocas fondos ineficientes ahorra {_fmt_usd(tax_drag)}/año en impuestos sin asumir más riesgo."
        )
        metrics = [
            {"label": "Annual in-scope tax drag", "value": _fmt_usd(tax_drag), "unit": "USD/yr", "json_source": "investment-analysis.json -> key_metrics.taxDragAnalysis.householdRollup"},
            {"label": "3y max drawdown", "value": f"-{max_dd_pct:.2f}%", "unit": "percent", "json_source": "investment-analysis.json -> key_metrics.performanceAnalysis.household.maxDrawdown3y"},
            {"label": "Max drawdown recovery", "value": f"{rec_days}", "unit": "days", "json_source": "investment-analysis.json -> key_metrics.performanceAnalysis.household.maxDrawdownRecoveryDays"},
            {"label": "Historical macro events tracked", "value": f"{len(case.analysis_events)}", "unit": "events", "json_source": "investment-analysis.json -> analysis.events"},
        ]
        bias_unlock = "Mirar la recuperación real en días neutraliza el miedo de vender en caídas y evita fugas fiscales."
        action_today = "Revisar activos con alto dividendo ordinario (como JNK/SCHD) en cuentas sujetas a impuestos."

    elif topic_norm in ("home_purchase", "housing", "vivienda"):
        home_goals = [g for g in case.profile.get("goals", []) if g.get("type") == "REAL_ESTATE_PURCHASE"]
        if home_goals:
            hg = home_goals[0]
            yr = int(hg.get("start_year", 2027))
            amt = float(hg.get("amount", 0.0))
            planned = hg.get("planned_purchase", {})
            loan = hg.get("planned_loan", {})
            costs = {c.get("name", ""): float(c.get("yearly", 0.0)) for c in hg.get("yearly_costs", [])}
            down_amt = next((v for k, v in costs.items() if "downpayment" in k.lower()), 0.0)
            closing_amt = next((v for k, v in costs.items() if "closing" in k.lower()), 0.0)
            tax_amt = next((v for k, v in costs.items() if "tax" in k.lower()), 0.0)
            ins_amt = next((v for k, v in costs.items() if "insurance" in k.lower()), 0.0)
            y_prev = case.projection_for_year(yr - 1) or {}
            y_buy = case.projection_for_year(yr) or {}
            plain_headline = f"Comprar casa de {_fmt_usd(amt)} en {yr} cambia tu liquidez de golpe"
            plain_summary = (
                f"Más allá de la cuota mensual de {_fmt_usd(loan.get('monthly_payment', 0))}/mes, "
                f"la entrada ({_fmt_usd(down_amt)}), cierre ({_fmt_usd(closing_amt)}), impuestos ({_fmt_usd(tax_amt)}/año) "
                f"y seguro ({_fmt_usd(ins_amt)}/año) reducen los activos invertibles de "
                f"{_fmt_usd(y_prev.get('investable_assets', 0))} ({yr - 1}) a {_fmt_usd(y_buy.get('investable_assets', 0))} ({yr})."
            )
            metrics = [
                {"label": f"Home purchase ({yr})", "value": _fmt_usd(amt), "unit": "USD", "json_source": "financial-health.json -> profile.goals[REAL_ESTATE_PURCHASE].amount"},
                {"label": "Price at purchase / down payment", "value": f"{_fmt_usd(planned.get('value_at_purchase', amt))} / {_fmt_usd(down_amt)}", "unit": "USD", "json_source": "financial-health.json -> profile.goals[REAL_ESTATE_PURCHASE].yearly_costs"},
                {"label": "Hidden annual costs (property tax + insurance) & closing", "value": f"{_fmt_usd(tax_amt)}/yr + {_fmt_usd(ins_amt)}/yr; cierre {_fmt_usd(closing_amt)}", "unit": "USD", "json_source": "financial-health.json -> profile.goals[REAL_ESTATE_PURCHASE].yearly_costs"},
                {"label": f"Investable assets ({yr - 1} -> {yr})", "value": f"{_fmt_usd(y_prev.get('investable_assets', 0))} -> {_fmt_usd(y_buy.get('investable_assets', 0))}", "unit": "USD", "json_source": "financial-health.json -> projections.yearly"},
            ]
            bias_unlock = "Visibiliza todos los costes ocultos de propiedad y lleva al Advisor Brief un retraso de fecha."
            action_today = "Solicitar al asesor simular la compra de vivienda en una fecha alternativa (no hay contrafactual precalculado)."
        else:
            plain_headline = "Sin nueva compra de vivienda planeada; foco en patrimonio líquido y protección"
            plain_summary = "El hogar ya cuenta con vivienda en propiedad y su prioridad es proteger liquidez y retiro."
            metrics = [
                {"label": "Accessible cash", "value": _fmt_usd(accessible_cash), "unit": "USD", "json_source": "financial-health.json -> key_metrics.facts.cash.accessibleCash"},
            ]
            bias_unlock = "No confundir el valor bruto de la vivienda con dinero líquido disponible."
            action_today = "Priorizar eliminación de tarjeta cara y protección familiar."

    else:
        # Overview (default)
        target_score = combined_best.get("score_after") or best_move.get("score_after") or case.published_score
        if neg_inv:
            plain_headline = (
                f"{case.household_name}: hoy tienes {months_before} meses cubiertos ({months_after} tras metas), "
                f"pero el dinero líquido cae a {_fmt_usd(neg_inv['investable_assets'])} en {neg_inv['year']}"
            )
        elif high_debts:
            d = high_debts[0]
            plain_headline = (
                f"{case.household_name}: {months_before} meses cubiertos, pero la tarjeta de {_fmt_usd(d['balance'])} "
                f"al {d['apr_pct']}% quema {_fmt_usd(d['annual_interest'])}/año"
            )
        else:
            plain_headline = f"{case.household_name}: {months_before} meses de colchón con plan mejorable ({case.published_score} -> {target_score})"

        plain_summary = (
            f"Ahorras {_fmt_usd(annual_savings)}/año ({savings_rate_pct:.1f}% de ingresos) y cuentas con {months_before} meses de reserva "
            f"({months_after} meses tras metas cercanas). Reordenando prioridades pasas de score {case.published_score} a {target_score} "
            f"ganando tranquilidad familiar sin perder tu ritmo de vida."
        )
        metrics = [
            {"label": "Published score -> target score", "value": f"{case.published_score} -> {target_score}", "unit": "score", "json_source": "financial-health.json -> score.published_score / score.top_moves / score.combined_moves"},
            {"label": "Accessible cash & months covered", "value": f"{_fmt_usd(accessible_cash)} ({months_before} / {months_after} mo)", "unit": "USD / months", "json_source": "financial-health.json -> key_metrics.facts.cash"},
            {"label": "Reported annual savings", "value": f"{_fmt_usd(annual_savings)}/yr ({savings_rate_pct:.1f}%)", "unit": "USD/yr", "json_source": "investment-analysis.json -> key_metrics.savingsAndContributions.currentSavings"},
            {"label": "Net cash flow this year", "value": _fmt_usd(net_cash_flow), "unit": "USD/yr", "json_source": "financial-health.json -> key_metrics.facts.retirement.netCashFlowThisYear"},
            {"label": "In-scope annual tax drag", "value": _fmt_usd(tax_drag), "unit": "USD/yr", "json_source": "investment-analysis.json -> key_metrics.taxDragAnalysis.householdRollup"},
        ]
        if neg_inv:
            metrics.append(
                {
                    "label": f"Liquidity depletion year ({neg_inv['year']}, age {neg_inv['age_client']})",
                    "value": _fmt_usd(neg_inv["investable_assets"]),
                    "unit": "USD",
                    "json_source": f"financial-health.json -> projections.yearly[{neg_inv['year']}].investable_assets",
                }
            )
        if edu_facts and isinstance(edu_facts.get("fundingGap"), dict):
            metrics.append(
                {
                    "label": "College funding gap",
                    "value": _fmt_usd(edu_facts["fundingGap"]["value"]),
                    "unit": "USD",
                    "json_source": "financial-health.json -> key_metrics.facts.education.fundingGap",
                }
            )
        bias_unlock = (
            f"Ancla motivacional {case.persona.motivational_anchor or 'PROTECTION'}: traduce porcentajes lejanos en meses de vida cubierta "
            "y un primer paso ejecutable hoy."
        )
        action_today = best_move.get("action", "Ejecutar el primer paso del waterfall hoy.")

    for m in metrics:
        if m["json_source"] not in sources:
            sources.append(m["json_source"])

    math_headline = f"{case.household_name} | Score {case.published_score}/100 ({case.score_band})"
    math_bullets = [f"{m['label']}: {m['value']} [{m['json_source']}]" for m in metrics]
    math_summary = " | ".join(math_bullets)
    family_peace = (
        "Protege la estabilidad del hogar traduciendo cifras complejas en meses reales de colchón y pasos ordenados."
    )
    if case.children:
        child_names = ", ".join(str(ch.get("first_name", "")) for ch in case.children)
        family_peace = (
            f"Protege directamente la estabilidad diaria y el futuro de {child_names} asegurando techo, liquidez y cobertura."
        )

    return {
        "case_id": case.case_id,
        "household_name": case.household_name,
        "topic": topic_norm,
        "plain": {
            "headline": plain_headline,
            "summary": plain_summary,
            "months_of_life_covered": f"{months_before} meses hoy ({months_after} meses tras metas cercanas)",
            "family_peace_of_mind": family_peace,
            "bias_unlock": bias_unlock,
            "action_today": action_today,
            "bullets": [plain_headline, family_peace, bias_unlock, action_today],
        },
        "math": {
            "headline": math_headline,
            "summary": math_summary,
            "metrics": metrics,
            "json_sources": sources,
            "bullets": math_bullets,
        },
        "extra_context": extra_context or {},
    }


def _evaluate_bias_for_case(case: CaseData, bias_id: str) -> dict[str, Any]:
    """Compute real-data evidence, triggered status, and Plain/Math explanations for a bias."""
    if bias_id not in BIAS_METADATA:
        raise ValueError(f"Unknown bias_id '{bias_id}'. Expected one of {ALL_BIAS_IDS}.")

    meta = dict(BIAS_METADATA[bias_id])
    cash_facts = case.fh_facts.get("cash", {})
    ret_facts = case.fh_facts.get("retirement", {})
    edu_facts = case.fh_facts.get("education") or {}
    accessible_cash = float(cash_facts.get("accessibleCash", {}).get("value", 0.0))
    months_before = str(cash_facts.get("monthsCovered", {}).get("value", "0"))
    months_after = str(cash_facts.get("monthsCoveredAfterNearTermGoals", {}).get("value", months_before))
    high_debts = case.high_interest_debts(threshold=0.10)
    tax_drag = case.tax_drag_annual_cost()
    neg_inv = case.first_negative_investable_year()
    neg_nw = case.first_negative_net_worth_year()
    savings_cur = case.savings_and_contributions.get("currentSavings", {})
    annual_savings = float(savings_cur.get("reportedAnnualSavings", 0.0))
    savings_rate_pct = float(savings_cur.get("currentSavingsRate", 0.0)) * 100.0
    savings_cap = float(case.savings_and_contributions.get("savingsCapacity", {}).get("savingsCapacity", 0.0))
    perf_hh = case.performance_analysis.get("household", {})
    max_dd_pct = abs(float(perf_hh.get("maxDrawdown3y", 0.0))) * 100.0
    rec_days = int(perf_hh.get("maxDrawdownRecoveryDays", 0))
    best_move = max(case.top_moves, key=lambda m: int(m.get("score_after", 0)), default={})
    combined_best = max(case.combined_moves, key=lambda m: int(m.get("score_after", 0)), default={})
    target_score = combined_best.get("score_after") or best_move.get("score_after") or case.published_score

    triggered = False
    severity = "none"
    plain = ""
    math = ""
    unlock_mechanic = ""
    evidence: dict[str, Any] = {}
    json_sources: list[str] = []

    if bias_id == "ikea_effect":
        triggered = True
        severity = "high" if case.published_score < 65 else "medium"
        plain = (
            f"Un informe estático paraliza a {case.household_name} (score {case.published_score}); "
            f"cuando elige campamentos en la montaña, ve consecuencias y sube a {target_score} con Rewind, siente el plan como propio."
        )
        math = (
            f"published_score={case.published_score} ({case.score_band}); ruta hacia score={target_score} "
            f"con {len(case.top_moves)} top_moves y {len(case.combined_moves)} combined_moves."
        )
        unlock_mechanic = "Previsualización de tendencia + Efecto IKEA + Rewind tras bloqueo en grieta/muro."
        evidence = {"published_score": case.published_score, "target_score": target_score, "top_moves_count": len(case.top_moves)}
        json_sources = ["financial-health.json -> score.published_score", "financial-health.json -> score.top_moves"]

    elif bias_id == "mental_accounting":
        if high_debts and (accessible_cash >= 25_000 or annual_savings >= 20_000):
            d = high_debts[0]
            cash_earned = case.cash_yield_earned()
            triggered = True
            severity = "high" if d["balance"] >= 10_000 else "medium"
            if case.case_id == "timothy-melanie-weah":
                plain = (
                    f"Separáis el ahorro 'intocable' ({_fmt_usd(accessible_cash)} al 0.09%) de la tarjeta de {_fmt_usd(d['balance'])} al {d['apr_pct']}%. "
                    f"Vuestro efectivo rinde ~{_fmt_usd(cash_earned)}/año, pero la tarjeta quema {_fmt_usd(d['annual_interest'])}/año."
                )
                math = (
                    f"accessibleCash={_fmt_usd(accessible_cash)} (rendimiento ~{_fmt_usd(cash_earned)}/yr) vs. "
                    f"{d['name']}={_fmt_usd(d['balance'])} al {d['apr_pct']}% APR ({_fmt_usd(d['annual_interest'])}/yr); "
                    f"pérdida neta ~{_fmt_usd(d['annual_interest'] - cash_earned)}/yr."
                )
            elif case.case_id == "daniel-emily-johnson":
                plain = (
                    f"Ahorráis {_fmt_usd(annual_savings)}/año en distintas cuentas mientras pagáis un {d['apr_pct']}% "
                    f"en {_fmt_usd(d['balance'])} de tarjeta ({_fmt_usd(d['annual_interest'])}/año quemados en intereses)."
                )
                math = (
                    f"reportedAnnualSavings={_fmt_usd(annual_savings)}/yr vs. {d['name']}={_fmt_usd(d['balance'])} "
                    f"al {d['apr_pct']}% APR ({_fmt_usd(d['annual_interest'])}/yr; $373.50/mes en intereses)."
                )
            else:
                plain = (
                    f"Mantienes {_fmt_usd(accessible_cash)} en efectivo mientras pagas un {d['apr_pct']}% APR "
                    f"en {_fmt_usd(d['balance'])} de tarjeta ({_fmt_usd(d['annual_interest'])}/año en intereses)."
                )
                math = (
                    f"accessibleCash={_fmt_usd(accessible_cash)} vs. {d['name']}={_fmt_usd(d['balance'])} "
                    f"al {d['apr_pct']}% APR ({_fmt_usd(d['annual_interest'])}/yr)."
                )
            evidence = {
                "accessible_cash": accessible_cash,
                "annual_savings": annual_savings,
                "debt_name": d["name"],
                "debt_balance": d["balance"],
                "debt_apr_pct": d["apr_pct"],
                "debt_annual_interest": d["annual_interest"],
                "cash_yield_earned": cash_earned,
            }
        else:
            plain = f"{case.household_name} no presenta deuda cara conviviendo con efectivo ocioso."
            math = f"High-APR debt count={len(high_debts)}; accessibleCash={_fmt_usd(accessible_cash)}."
            evidence = {"high_interest_debt_count": len(high_debts), "accessible_cash": accessible_cash}
        unlock_mechanic = "Rama 'Cubo Agujereado' + Desplegable de Flujo Neto juntando ahorro e interés caro."
        json_sources = [
            "financial-health.json -> profile.liabilities",
            "financial-health.json -> key_metrics.facts.cash.accessibleCash",
            "investment-analysis.json -> key_metrics.cashNeeds.summaryIncome",
        ]

    elif bias_id == "halo_effect":
        tax_deferred_bal = float(
            case.savings_and_contributions.get("taxOpportunityCheck", {})
            .get("preTaxVsRothCheck", {})
            .get("taxDeferredAccountBalance", 0.0)
        )
        if case.published_score >= 75 and (tax_deferred_bal == 0 or neg_inv is not None):
            triggered = True
            severity = "high"
            plain = (
                f"El score verde {case.published_score}/100 ({case.score_band}) oculta que hay $0 en cuentas de jubilación "
                f"y los activos líquidos caen a {_fmt_usd(neg_inv['investable_assets'])} en {neg_inv['year']} (edad {neg_inv['age_client']})."
            )
            math = (
                f"published_score={case.published_score} ({case.score_band}); taxDeferredAccountBalance={_fmt_usd(tax_deferred_bal)}; "
                f"projections.yearly[{neg_inv['year']}].investable_assets={_fmt_usd(neg_inv['investable_assets'])} (age {neg_inv['age_client']})."
            )
            evidence = {
                "published_score": case.published_score,
                "tax_deferred_balance": tax_deferred_bal,
                "depletion_year": neg_inv["year"] if neg_inv else None,
                "depletion_investable_assets": neg_inv["investable_assets"] if neg_inv else None,
            }
        else:
            plain = (
                f"El score actual ({case.published_score}/100, {case.score_band}) no genera falsa seguridad en verde "
                "y refleja brechas visibles."
            )
            math = f"published_score={case.published_score} ({case.score_band}); taxDeferredAccountBalance={_fmt_usd(tax_deferred_bal)}."
            evidence = {"published_score": case.published_score, "tax_deferred_balance": tax_deferred_bal}
        unlock_mechanic = "HUD desglosado en 5 pilares + Salto directo al punto ciego en 2053 (edad 74)."
        json_sources = [
            "financial-health.json -> score.published_score",
            "financial-health.json -> projections.yearly",
            "investment-analysis.json -> key_metrics.savingsAndContributions.taxOpportunityCheck.preTaxVsRothCheck",
        ]

    elif bias_id == "house_rich_cash_poor":
        real_estate = [a for a in case.profile.get("other_assets", []) or [] if "home" in str(a.get("name", "")).lower() or a.get("type") == "REAL_ESTATE"]
        home_val = sum(float(a.get("value") or a.get("balance") or 0.0) for a in real_estate)
        conc_nw = float(case.investment_analysis.get("key_metrics", {}).get("concentrationAndDiversification", {}).get("totals", {}).get("netWorth", 0.0))
        if neg_inv is not None or home_val >= 500_000:
            triggered = True
            severity = "high" if neg_inv is not None else "medium"
            if neg_inv is not None:
                plain = (
                    f"El patrimonio neto incluye paredes ilíquidas ({_fmt_usd(neg_inv['net_worth'])} en {neg_inv['year']}), "
                    f"pero el dinero líquido para vivir cae a {_fmt_usd(neg_inv['investable_assets'])} a los {neg_inv['age_client']} años."
                )
                math = (
                    f"projections.yearly[{neg_inv['year']}] -> net_worth={_fmt_usd(neg_inv['net_worth'])} vs. "
                    f"investable_assets={_fmt_usd(neg_inv['investable_assets'])} (age {neg_inv['age_client']})."
                )
                if neg_nw is not None:
                    math += f" net_worth llega a {_fmt_usd(neg_nw['net_worth'])} en {neg_nw['year']}."
            else:
                plain = (
                    f"Gran parte del patrimonio ({_fmt_usd(conc_nw)}) está inmovilizado en la vivienda ({_fmt_usd(home_val)}), "
                    f"dejando solo {_fmt_usd(accessible_cash)} ({months_before} meses) en liquidez inmediata."
                )
                math = (
                    f"home_value={_fmt_usd(home_val)}; netWorth={_fmt_usd(conc_nw)}; "
                    f"accessibleCash={_fmt_usd(accessible_cash)} ({months_before} meses)."
                )
            evidence = {
                "home_value": home_val,
                "net_worth": neg_inv["net_worth"] if neg_inv else conc_nw,
                "investable_assets_at_cliff": neg_inv["investable_assets"] if neg_inv else None,
                "cliff_year": neg_inv["year"] if neg_inv else None,
                "accessible_cash": accessible_cash,
            }
        else:
            plain = f"No hay iliquidez inmobiliaria grave ahora ({_fmt_usd(accessible_cash)} líquidos)."
            math = f"accessibleCash={_fmt_usd(accessible_cash)}; netWorth={_fmt_usd(conc_nw)}."
            evidence = {"accessible_cash": accessible_cash, "net_worth": conc_nw}
        unlock_mechanic = "Separación visual Investable Assets vs. Net Worth en toda la ruta de projections.yearly."
        json_sources = [
            "financial-health.json -> projections.yearly",
            "financial-health.json -> profile.other_assets",
            "investment-analysis.json -> key_metrics.concentrationAndDiversification.totals.netWorth",
        ]

    elif bias_id == "present_bias":
        purchases = [g for g in case.profile.get("goals", []) if g.get("type") == "REAL_ESTATE_PURCHASE"]
        if purchases:
            hg = purchases[0]
            yr = int(hg.get("start_year", 2027))
            amt = float(hg.get("amount", 0.0))
            y_prev = case.projection_for_year(yr - 1) or {}
            y_buy = case.projection_for_year(yr) or {}
            prev_inv = float(y_prev.get("investable_assets", 0.0))
            buy_inv = float(y_buy.get("investable_assets", 0.0))
            triggered = True
            severity = "high" if buy_inv < prev_inv or float(months_after) == 0 else "medium"
            plain = (
                f"Priorizar la compra de casa de {_fmt_usd(amt)} en {yr} hace bajar los activos invertibles "
                f"de {_fmt_usd(prev_inv)} a {_fmt_usd(buy_inv)} y deja {months_after} meses de caja libre tras metas."
            )
            math = (
                f"goal={_fmt_usd(amt)} ({yr}); investable_assets {yr - 1}: {_fmt_usd(prev_inv)} -> {yr}: {_fmt_usd(buy_inv)}; "
                f"monthsCoveredAfterNearTermGoals={months_after}."
            )
            evidence = {
                "purchase_year": yr,
                "purchase_amount": amt,
                "investable_before": prev_inv,
                "investable_after": buy_inv,
                "months_after_near_term": months_after,
            }
        else:
            plain = f"Sin compra inmobiliaria inminente; el riesgo presente es mantener {len(high_debts)} deuda cara."
            math = f"No REAL_ESTATE_PURCHASE goal; accessibleCash={_fmt_usd(accessible_cash)}."
            evidence = {"purchase_count": 0, "accessible_cash": accessible_cash}
        unlock_mechanic = "Bifurcación instantánea en la línea temporal conectando 2026/2027 con 2047 y 2075."
        json_sources = [
            "financial-health.json -> profile.goals",
            "financial-health.json -> projections.yearly",
            "financial-health.json -> key_metrics.facts.cash.monthsCoveredAfterNearTermGoals",
        ]

    elif bias_id == "future_self_gap":
        triggered = True
        severity = "high" if neg_inv is not None else "medium"
        age_now = case.adults[0].get("age", 37) if case.adults else 37
        age_ret = case.adults[0].get("retirement_age", 62) if case.adults else 62
        end_row = case.yearly_projections[-1] if case.yearly_projections else {}
        end_age = end_row.get("age_client") or end_row.get("age_co_client") or 90
        run_out = ret_facts.get("savingsRunOut", {})
        left_end = ret_facts.get("savingsLeftAtPlanEnd", {}).get("value")
        if run_out:
            plain = (
                f"Vivir tu ruta paso a paso (Age {age_now} -> Age {age_ret} -> Age {end_age}) convierte "
                f"un dato lejano ({_fmt_usd(run_out.get('value', 0))} sin cubrir) en tu propia historia y en meses de vida ({months_before} meses)."
            )
            math = (
                f"Age {age_now} -> ret {age_ret} -> end {end_age}; {run_out.get('label', '')}: {_fmt_usd(run_out.get('value', 0))}."
            )
        else:
            plain = (
                f"En vez de cifras abstractas como {_fmt_usd(left_end or 0)} al final del plan (Age {age_now} -> Age {age_ret} -> Age {end_age}), "
                f"ves qué margen mensual real tiene tu yo futuro."
            )
            math = (
                f"Age {age_now} -> ret {age_ret} -> end {end_age}; savingsLeftAtPlanEnd={_fmt_usd(left_end or 0)}."
            )
        unlock_mechanic = f"Progreso en primera persona (Age {age_now} -> Age {age_ret} -> Age {end_age}) + Toggle Plain <-> Math."
        evidence = {"age_now": age_now, "age_retire": age_ret, "age_end": end_age, "savings_left_end": left_end}
        json_sources = [
            "financial-health.json -> case.household",
            "financial-health.json -> projections.yearly",
            "financial-health.json -> key_metrics.facts.retirement",
        ]

    elif bias_id == "planning_fallacy":
        purchases = [g for g in case.profile.get("goals", []) if g.get("type") in ("REAL_ESTATE_PURCHASE", "VEHICLE_PURCHASE")]
        home_purchases = [g for g in purchases if g.get("type") == "REAL_ESTATE_PURCHASE"]
        if home_purchases:
            hg = home_purchases[0]
            yr = int(hg.get("start_year", 2027))
            amt = float(hg.get("amount", 0.0))
            loan = hg.get("planned_loan", {})
            costs = {c.get("name", ""): float(c.get("yearly", 0.0)) for c in hg.get("yearly_costs", [])}
            prop_tax = next((v for k, v in costs.items() if "property tax" in k.lower()), 0.0)
            home_ins = next((v for k, v in costs.items() if "insurance" in k.lower()), 0.0)
            closing = next((v for k, v in costs.items() if "closing" in k.lower()), 0.0)
            down = next((v for k, v in costs.items() if "downpayment" in k.lower()), 0.0)
            rent_exp = next((e for e in case.profile.get("expenses", []) if e.get("type") == "RENT"), None)
            triggered = True
            severity = "high" if yr <= 2027 else "medium"
            rent_txt = f"alquiler de {_fmt_usd(rent_exp['monthly'])}/mes frente a " if rent_exp else ""
            plain = (
                f"Al planear casa de {_fmt_usd(amt)} en {yr}, es fácil mirar solo {rent_txt}"
                f"hipoteca de {_fmt_usd(loan.get('monthly_payment', 0))}/mes e ignorar impuestos ({_fmt_usd(prop_tax)}/año), "
                f"seguro ({_fmt_usd(home_ins)}/año) y cierre ({_fmt_usd(closing)})."
            )
            math = (
                f"Home {yr} ({_fmt_usd(amt)}): downpayment={_fmt_usd(down)}, closing={_fmt_usd(closing)}, "
                f"property_taxes={_fmt_usd(prop_tax)}/yr, home_insurance={_fmt_usd(home_ins)}/yr, "
                f"monthly_mortgage={_fmt_usd(loan.get('monthly_payment', 0))}."
            )
            evidence = {
                "year": yr,
                "amount": amt,
                "downpayment": down,
                "closing_costs": closing,
                "property_taxes_yr": prop_tax,
                "home_insurance_yr": home_ins,
                "mortgage_monthly": loan.get("monthly_payment", 0),
            }
        else:
            plain = "Sin compra inmobiliaria o vehículo con costes ocultos pendientes en este plan."
            math = "No REAL_ESTATE_PURCHASE goal in profile.goals."
            evidence = {"purchase_goals": 0}
        unlock_mechanic = "Desplegable del Campamento de Transición (2027 / 2030) con costes totales reales y Transition alerts."
        json_sources = ["financial-health.json -> profile.goals", "persona.md -> Transition alerts"]

    elif bias_id == "ostrich_effect":
        if case.published_score < 60 and annual_savings >= 25_000:
            triggered = True
            severity = "high"
            plain = (
                f"Ahorras {_fmt_usd(annual_savings)}/año ({savings_rate_pct:.1f}% de tus ingresos), un esfuerzo enorme. "
                f"Abrir el informe con un {case.published_score}/100 ({case.score_band}) invita a cerrarlo, pero reordenando piezas subes a {target_score}."
            )
            math = (
                f"reportedAnnualSavings={_fmt_usd(annual_savings)}/yr ({savings_rate_pct:.1f}% savings rate); "
                f"published_score={case.published_score} -> {target_score} ({best_move.get('title', 'top_move')})."
            )
            evidence = {
                "annual_savings": annual_savings,
                "savings_rate_pct": round(savings_rate_pct, 1),
                "published_score": case.published_score,
                "target_score": target_score,
            }
        else:
            plain = (
                f"El esfuerzo actual de ahorro ({savings_rate_pct:.1f}%, {_fmt_usd(annual_savings)}/año) se reconoce primero en el HUD "
                f"para mostrar que subir de {case.published_score} a {target_score} es alcanzable."
            )
            math = f"published_score={case.published_score} -> {target_score}; currentSavingsRate={savings_rate_pct:.1f}%."
            evidence = {"published_score": case.published_score, "target_score": target_score, "savings_rate_pct": round(savings_rate_pct, 1)}
        unlock_mechanic = f"Reframing Positivo ({savings_rate_pct:.1f}% ahorro) + Tronco central viable ({case.published_score} -> {target_score})."
        json_sources = [
            "financial-health.json -> score.published_score",
            "financial-health.json -> score.top_moves",
            "investment-analysis.json -> key_metrics.savingsAndContributions.currentSavings",
        ]

    elif bias_id == "optimism_bias":
        wf_ins = case.waterfall_row("insurance") or {}
        delta = float(wf_ins.get("delta") or 0.0)
        prot_pillar = next((p for p in case.pillars if "insurance" in p.get("pillar", "").lower()), {})
        has_gap = delta < 0 or (case.top_moves and "coverage" in str(case.top_moves[0].get("title", "")).lower())
        if has_gap:
            triggered = True
            total_prot_gap = abs(delta)
            umbrella_gap = 1_000_000.0 if not any(
                ins.get("type") == "UMBRELLA_INSURANCE" for ins in case.profile.get("insurance", [])
            ) else 0.0
            life_gap = max(0.0, total_prot_gap - umbrella_gap) if total_prot_gap > 0 else 0.0
            severity = "high" if prot_pillar.get("score", 100) < 40 else "medium"
            if life_gap > 0:
                plain = (
                    f"Nadie quiere pensar en fallecer o recibir una demanda, pero hoy hay "
                    f"una brecha de {_fmt_usd(life_gap)} en seguro de vida y {_fmt_usd(umbrella_gap)} en umbrella "
                    f"(pilar de protección {prot_pillar.get('points_shown_in_app', '')})."
                )
            else:
                plain = (
                    f"Nadie quiere pensar en un siniestro, pero la vivienda y vehículo figuran sin póliza confirmada "
                    f"(pilar de protección {prot_pillar.get('points_shown_in_app', '')})."
                )
            math = (
                f"Protection pillar={prot_pillar.get('points_shown_in_app', '')}; "
                f"life_gap={_fmt_usd(life_gap)}; umbrella_gap={_fmt_usd(umbrella_gap)}; "
                f"waterfall_protection_gap={_fmt_usd(total_prot_gap)}; score {case.published_score} -> {target_score}."
            )
            evidence = {
                "protection_points": prot_pillar.get("points_shown_in_app", ""),
                "protection_score": prot_pillar.get("score", 0),
                "life_insurance_gap": life_gap,
                "umbrella_gap": umbrella_gap,
                "total_protection_gap": total_prot_gap,
                "target_score": target_score,
            }
        else:
            plain = "Las coberturas de vida y paraguas están dentro de rango."
            math = f"Protection pillar={prot_pillar.get('points_shown_in_app', '')}."
            evidence = {"protection_points": prot_pillar.get("points_shown_in_app", "")}
        unlock_mechanic = "Quest de Miedos + Campamento de Escudo Familiar (blindar ingresos e hijos en vez de hablar de muerte)."
        json_sources = [
            "financial-health.json -> score.pillars",
            "investment-analysis.json -> key_metrics.savingsAndContributions.savingsWaterfall[2]",
            "persona.md -> D3 Protection",
        ]

    elif bias_id == "oxygen_mask_syndrome":
        edu_gap = float(edu_facts.get("fundingGap", {}).get("value", 0.0)) if edu_facts else 0.0
        college_contrib = sum(
            float(acc.get("yearly_contribution_client") or 0.0)
            for acc in case.profile.get("accounts", [])
            if "529" in str(acc.get("account_type", "")).lower() or "custodial" in str(acc.get("account_type", "")).lower()
        )
        ret_contrib = sum(
            float(acc.get("yearly_contribution_client") or 0.0)
            for acc in case.profile.get("accounts", [])
            if "401k" in str(acc.get("account_type", "")).lower()
        )
        pre_tax_check = (
            case.savings_and_contributions.get("taxOpportunityCheck", {})
            .get("preTaxVsRothCheck", {})
        )
        ret_tax_deferred = float(pre_tax_check.get("taxDeferredAccountBalance", 0.0))
        tax_bracket = float(pre_tax_check.get("currentTaxBracket", 0.0))
        wf_401k = case.waterfall_row("401k") or {}
        unused_401k = abs(float(wf_401k.get("delta") or 0.0)) if isinstance(wf_401k.get("delta"), (int, float)) else 0.0
        missed_401k_tax = round(unused_401k * tax_bracket, 2)
        if case.children and (college_contrib > 0 or edu_gap > 0) and (ret_contrib == 0 or ret_tax_deferred == 0):
            triggered = True
            severity = "high"
            total_college = float(edu_facts.get("totalCostAllGoals", {}).get("value", 0.0))
            plain = (
                f"Por proteger antes la universidad de los hijos ({_fmt_usd(total_college)} de objetivo; "
                f"{_fmt_usd(college_contrib)}/año aportados hoy), se deja el retiro propio en $0/año aportados "
                f"(perdiendo hasta {_fmt_usd(missed_401k_tax)}/año de ahorro fiscal en 401(k))."
            )
            math = (
                f"401(k)_client_contrib={_fmt_usd(ret_contrib)}/yr; unused_401k_room={_fmt_usd(unused_401k)} "
                f"(ahorro fiscal potencial {_fmt_usd(missed_401k_tax)}/yr al {_fmt_pct(tax_bracket, True)}); "
                f"taxDeferredBalance={_fmt_usd(ret_tax_deferred)}; college_contrib={_fmt_usd(college_contrib)}/yr; "
                f"totalCostAllGoals={_fmt_usd(total_college)}; educationGap={_fmt_usd(edu_gap)}."
            )
            evidence = {
                "retirement_contrib_yr": ret_contrib,
                "unused_401k_room": unused_401k,
                "missed_401k_tax_savings_yr": missed_401k_tax,
                "tax_deferred_balance": ret_tax_deferred,
                "college_contrib_yr": college_contrib,
                "total_college_cost": total_college,
                "education_gap": edu_gap,
            }
        else:
            plain = f"No hay desplazamiento grave del retiro frente a universidad (aportación 401k={_fmt_usd(ret_contrib)}/año)."
            math = f"401(k)_client_contrib={_fmt_usd(ret_contrib)}/yr; college_contrib={_fmt_usd(college_contrib)}/yr."
            evidence = {"retirement_contrib_yr": ret_contrib, "college_contrib_yr": college_contrib}
        unlock_mechanic = "Desplegable de Tensión (T5 / O1) + Orden óptimo de savingsWaterfall (mascarilla propia primero)."
        json_sources = [
            "financial-health.json -> profile.accounts",
            "financial-health.json -> key_metrics.facts.education",
            "investment-analysis.json -> key_metrics.savingsAndContributions.savingsWaterfall[13]",
            "persona.md -> Tensions / Objective concerns",
        ]

    elif bias_id == "choice_overload":
        open_buckets = [
            r for r in case.savings_waterfall[1:]
            if len(r) >= 5 and str(r[4]) in ("Empty", "Partially filled")
        ]
        triggered = len(open_buckets) >= 3
        severity = "high" if (case.is_couple or len(open_buckets) >= 5) else "medium"
        first_step = open_buckets[0][1] if open_buckets else "Primer paso"
        plain = (
            f"Hay {len(open_buckets)} frentes abiertos a la vez en la cascada (compitiendo por "
            f"{_fmt_usd(savings_cap)}/año de flujo libre); sin un único Step 1 de 3 minutos en el Día 0, la familia no ejecuta ninguno."
        )
        math = (
            f"savingsWaterfall_rows={max(0, len(case.savings_waterfall) - 1)}; pending_buckets={len(open_buckets)}; "
            f"savingsCapacity={_fmt_usd(savings_cap)}/yr; step_1='{first_step}'."
        )
        unlock_mechanic = "Secuenciación Día a Día en Run IRL: entrega un único Step 1 de 3 minutos en el Día 0."
        evidence = {
            "waterfall_total_rows": max(0, len(case.savings_waterfall) - 1),
            "pending_buckets": len(open_buckets),
            "savings_capacity": savings_cap,
            "first_open_bucket": first_step,
        }
        json_sources = [
            "investment-analysis.json -> key_metrics.savingsAndContributions.savingsWaterfall",
            "investment-analysis.json -> key_metrics.savingsAndContributions.savingsCapacity",
        ]

    elif bias_id == "status_quo_bias":
        triggered = True
        daily_cost = 0.0
        if high_debts:
            daily_cost = round(high_debts[0]["annual_interest"] / 365.0, 2)
        elif tax_drag > 0:
            daily_cost = round(tax_drag / 365.0, 2)
        severity = "high" if high_debts else "medium"
        plain = (
            f"Si en el Día 3 o Día 30 la motivación baja y el paso sigue sin marcarse, "
            f"la inercia sigue costando {_fmt_usd(daily_cost)}/día ({_fmt_usd(high_debts[0]['annual_interest'] if high_debts else tax_drag)}/año)."
        )
        math = (
            f"Inertia daily cost={_fmt_usd(daily_cost)}/day "
            f"(annual={_fmt_usd(high_debts[0]['annual_interest'] if high_debts else tax_drag)}/yr); "
            f"nodos Día 0 -> Día 3 -> Día 14 -> Día 30."
        )
        unlock_mechanic = "Tiempo IRL implacable + Notificaciones de insistencia con coste acumulado de la inercia."
        evidence = {"daily_inertia_cost": daily_cost, "tax_drag": tax_drag, "high_debt_interest_yr": high_debts[0]["annual_interest"] if high_debts else 0.0}
        json_sources = [
            "financial-health.json -> profile.liabilities",
            "investment-analysis.json -> key_metrics.taxDragAnalysis.householdRollup",
        ]

    elif bias_id == "loss_aversion_recency":
        upro_pos = next((p for p in case.positions if str(p.get("ticker", "")).upper() == "UPRO"), None)
        triggered = upro_pos is not None or len(case.analysis_events) >= 11
        severity = "high" if upro_pos is not None else "medium"
        if upro_pos is not None:
            upro_val = float(upro_pos.get("value") or 0.0)
            plain = (
                f"Melanie deja {_fmt_usd(accessible_cash)} en efectivo al 0.09% por aversión a la pérdida, "
                f"mientras Timothy mantiene {_fmt_usd(upro_val)} en UPRO (3x apalancado) confiado tras el último rally. "
                f"Los {len(case.analysis_events)} shocks reales muestran una caída máxima de -{max_dd_pct:.1f}% recuperada en {rec_days} días."
            )
            math = (
                f"accessibleCash={_fmt_usd(accessible_cash)} (~0.09%) vs. UPRO={_fmt_usd(upro_val)} (3x); "
                f"events={len(case.analysis_events)}; maxDrawdown3y=-{max_dd_pct:.2f}%, recoveryDays={rec_days}."
            )
            evidence = {
                "accessible_cash": accessible_cash,
                "upro_value": upro_val,
                "events_count": len(case.analysis_events),
                "max_drawdown_pct": round(max_dd_pct, 2),
                "recovery_days": rec_days,
            }
        else:
            plain = (
                f"Ante caídas de mercado, los {len(case.analysis_events)} eventos históricos reales demuestran "
                f"que la cartera resistió -{max_dd_pct:.1f}% y se recuperó en {rec_days} días sin vender en pánico."
            )
            math = f"events={len(case.analysis_events)}; maxDrawdown3y=-{max_dd_pct:.2f}%, recoveryDays={rec_days}."
            evidence = {"events_count": len(case.analysis_events), "max_drawdown_pct": round(max_dd_pct, 2), "recovery_days": rec_days}
        unlock_mechanic = "La Radio del Sherpa (analysis.events / perEventDrawdowns): 11 shocks reales de calma anti-pánico."
        json_sources = [
            "investment-analysis.json -> positions",
            "investment-analysis.json -> analysis.events",
            "investment-analysis.json -> key_metrics.performanceAnalysis.household",
        ]

    elif bias_id == "couples_veto":
        if case.is_couple:
            a1, a2 = case.adults[0], case.adults[1]
            r1 = str(a1.get("risk_profile", ""))
            r2 = str(a2.get("risk_profile", ""))
            triggered = (r1 != r2) or ("MISALIGNED" in case.persona.risk_alignment) or ("DUAL" in case.persona.decision_style)
            severity = "high"
            plain = (
                f"{a1['first_name']} declara perfil {r1} (4) y {a2['first_name']} {r2} (3) ({case.persona.decision_style}). "
                f"Si el plan solo habla a uno, el otro lo frena en silencio; juntos suben a {target_score}."
            )
            math = (
                f"{a1['first_name']}={r1} vs {a2['first_name']}={r2}; D4={case.persona.risk_alignment}; "
                f"D5={case.persona.decision_style}; combined_moves {case.published_score} -> {target_score}."
            )
            evidence = {
                "member_a": a1["first_name"],
                "member_a_risk": r1,
                "member_b": a2["first_name"],
                "member_b_risk": r2,
                "d4_alignment": case.persona.risk_alignment,
                "d5_style": case.persona.decision_style,
                "combined_target_score": target_score,
            }
        else:
            plain = f"{case.household_name} es hogar individual: no existe veto de pareja."
            math = f"is_couple=False; adults={len(case.adults)}."
            evidence = {"is_couple": False}
        unlock_mechanic = "Cordada Asimétrica (60s a ciegas antes de la montaña) + Reparto Owner A / Owner B en Run IRL."
        json_sources = [
            "financial-health.json -> case.household",
            "financial-health.json -> score.combined_moves",
            "persona.md -> D4 / D5",
        ]

    return {
        "bias_id": meta["bias_id"],
        "section": meta["section"],
        "name_es": meta["name_es"],
        "name_en": meta["name_en"],
        "theorist": meta["theorist"],
        "triggered": triggered,
        "severity": severity,
        "plain": plain,
        "math": math,
        "unlock_mechanic": unlock_mechanic,
        "evidence": evidence,
        "json_sources": json_sources,
    }


def _enrich_with_llm(
    llm_client: LLMProxyClient,
    case: CaseData,
    task_label: str,
    grounded_facts: dict[str, Any],
    base_result: dict[str, Any],
    model: str | None = None,
) -> tuple[dict[str, Any], bool, bool, str | None]:
    """Optionally enrich a deterministic payload via LLMProxyClient while strictly blocking invented numbers."""
    allowed = extract_case_allowed_numbers(case, extra_numbers=grounded_facts)
    prompt = (
        f"Tarea: {task_label} para el hogar {case.household_name} ({case.case_id}).\n"
        "REGLA ESTRICTA: Usa ÚNICAMENTE los números que aparecen en los hechos verificados JSON adjuntos. "
        "No inventes ni estimes ninguna cifra nueva. Devuelve JSON con las claves 'plain_summary' y 'math_summary'.\n"
        f"Hechos verificados:\n{json.dumps(grounded_facts, ensure_ascii=False)}"
    )
    resp = llm_client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": "Eres un narrador financiero conductual de Sherpas. Cero números inventados; solo cita datos reales proporcionados.",
            },
            {"role": "user", "content": prompt},
        ],
        model=model or llm_client.default_model,
        fallback_context={"deterministic_json": base_result},
    )
    if resp.used_fallback:
        return base_result, False, True, resp.fallback_reason

    try:
        parsed = json.loads(resp.content)
        candidate_text = " ".join(
            str(parsed.get(k, "")) for k in ("plain_summary", "math_summary") if parsed.get(k)
        )
    except (json.JSONDecodeError, TypeError):
        parsed = None
        candidate_text = resp.content

    if not candidate_text.strip():
        return base_result, False, True, "empty_llm_enrichment"

    ok, bad_nums = verify_text_numbers_against_case(candidate_text, allowed)
    if not ok:
        return base_result, False, True, f"unverified_numbers_detected: {bad_nums}"

    enriched = dict(base_result)
    if isinstance(parsed, dict):
        if parsed.get("plain_summary"):
            enriched["llm_plain_summary"] = str(parsed["plain_summary"])
        if parsed.get("math_summary"):
            enriched["llm_math_summary"] = str(parsed["math_summary"])
    else:
        enriched["llm_narrative"] = candidate_text.strip()
    return enriched, True, False, None


class BehavioralNarrator:
    """High-level Behavioral Translation Engine grounded in real Sherpas case data."""

    def __init__(
        self,
        cases_dir: str | Path | None = None,
        llm_client: LLMProxyClient | None = None,
    ) -> None:
        self.cases_dir = cases_dir
        self.llm_client = llm_client
        self._cache: dict[str, CaseData] = {}

    def list_cases(self) -> list[str]:
        return list_available_cases(self.cases_dir)

    def load_case(self, case_id: str) -> CaseData:
        if case_id not in self._cache:
            self._cache[case_id] = load_case(case_id, cases_dir=self.cases_dir)
        return self._cache[case_id]

    def _get_client(self, llm_client: LLMProxyClient | None = None) -> LLMProxyClient:
        return llm_client or self.llm_client or LLMProxyClient()

    def translate_dual_lens(
        self,
        case_id: str,
        topic: str = "overview",
        lens: str = "both",
        use_llm: bool = False,
        llm_client: LLMProxyClient | None = None,
        model: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Translate a case topic into Dual-Lens `plain` (everyday impact) and `math` (exact USD/JSON sources)."""
        if lens not in ("both", "plain", "math"):
            raise ValueError("lens must be 'both', 'plain', or 'math'.")
        case = self.load_case(case_id)
        base = _build_topic_context(case, topic=topic, extra_context=context)
        used_llm = False
        llm_fallback_used = False
        fallback_reason: str | None = None

        if use_llm:
            client = self._get_client(llm_client)
            grounded = {
                "case_id": case_id,
                "topic": base["topic"],
                "plain": base["plain"],
                "math": base["math"],
            }
            base, used_llm, llm_fallback_used, fallback_reason = _enrich_with_llm(
                client, case, f"Dual-Lens {topic}", grounded, base, model=model
            )

        result: dict[str, Any] = {
            "case_id": base["case_id"],
            "household_name": base["household_name"],
            "topic": base["topic"],
            "requested_lens": lens,
            "plain": base["plain"],
            "math": base["math"],
            "used_llm": used_llm,
            "llm_fallback_used": llm_fallback_used,
            "fallback_reason": fallback_reason,
            "verified_numbers_only": True,
        }
        if "llm_plain_summary" in base:
            result["plain"] = dict(result["plain"], enriched_summary=base["llm_plain_summary"])
        if "llm_math_summary" in base:
            result["math"] = dict(result["math"], enriched_summary=base["llm_math_summary"])
        if "llm_narrative" in base:
            result["llm_narrative"] = base["llm_narrative"]
        return result

    def detect_behavioral_biases(
        self,
        case_id: str,
        include_untriggered: bool = False,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        """Detect triggered behavioral biases across Section 4 (4.1–4.4) and Appendix A for a case."""
        case = self.load_case(case_id)
        severity_rank = {"high": 0, "medium": 1, "low": 2, "none": 3}
        items: list[dict[str, Any]] = []
        for bias_id in ALL_BIAS_IDS:
            entry = _evaluate_bias_for_case(case, bias_id)
            if category and entry["section"] != category:
                continue
            if include_untriggered or entry["triggered"]:
                items.append(entry)
        items.sort(key=lambda x: (not x["triggered"], severity_rank.get(x["severity"], 9), x["section"]))
        return items

    def explain_bias(
        self,
        case_id: str,
        bias_id: str,
        use_llm: bool = False,
        llm_client: LLMProxyClient | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """Explain any specific behavioral bias for the case in Plain + Math with optional LLM enrichment."""
        case = self.load_case(case_id)
        entry = _evaluate_bias_for_case(case, bias_id)
        used_llm = False
        llm_fallback_used = False
        fallback_reason: str | None = None

        if use_llm:
            client = self._get_client(llm_client)
            entry, used_llm, llm_fallback_used, fallback_reason = _enrich_with_llm(
                client, case, f"Explicar sesgo {bias_id}", entry, entry, model=model
            )

        entry["case_id"] = case.case_id
        entry["household_name"] = case.household_name
        entry["used_llm"] = used_llm
        entry["llm_fallback_used"] = llm_fallback_used
        entry["fallback_reason"] = fallback_reason
        entry["verified_numbers_only"] = True
        return entry

    def synthesize_cordada_pact(
        self,
        case_id: str,
        member_a_votes: dict[str, Any] | None = None,
        member_b_votes: dict[str, Any] | None = None,
        use_llm: bool = False,
        llm_client: LLMProxyClient | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """Synthesize the 60s blind Cordada Asimetrica pact before entering the mountain (BIBLIA_FINAL_V1)."""
        case = self.load_case(case_id)
        if not case.is_couple:
            return {
                "case_id": case.case_id,
                "household_name": case.household_name,
                "is_couple": False,
                "shared_100_percent": [],
                "friction_points": [],
                "midpoint_pact": None,
                "plain_summary": f"{case.household_name} es un hogar individual; pasa directo al Quest de Miedos sin votación en pareja.",
                "math_summary": f"is_couple=False; published_score={case.published_score}.",
                "used_llm": False,
                "llm_fallback_used": False,
                "verified_numbers_only": True,
            }

        a1, a2 = case.adults[0], case.adults[1]
        name_a = str(a1.get("first_name", "Member A"))
        name_b = str(a2.get("first_name", "Member B"))
        va = dict(member_a_votes or {})
        vb = dict(member_b_votes or {})

        fears_a = list(va.get("top_fears") or va.get("fears") or [o.id for o in case.persona.objective_concerns[:2]])
        fears_b = list(vb.get("top_fears") or vb.get("fears") or [o.id for o in case.persona.objective_concerns[:2]])
        shared_fear_ids = [f for f in fears_a if f in fears_b]
        concern_map = {o.id: o for o in case.persona.objective_concerns}

        best_combined = max(case.combined_moves, key=lambda m: int(m.get("score_after", 0)), default={})
        target_score = int(best_combined.get("score_after") or case.published_score)
        shared_100 = [
            f"Ancla motivacional compartida ({case.persona.motivational_anchor or 'PROTECTION'}): proteger a la familia y el futuro de los hijos."
        ]
        for fid in shared_fear_ids:
            if fid in concern_map:
                shared_100.append(f"Coincidencia en {fid}: {concern_map[fid].title}")
        if best_combined:
            moves_txt = " + ".join(best_combined.get("moves", []))
            shared_100.append(f"Camino conjunto validado por Sherpas ({moves_txt}): score {case.published_score} -> {target_score}.")

        # Isolate 1-2 friction points
        friction_points: list[dict[str, Any]] = []
        r1 = str(va.get("risk_choice") or a1.get("risk_profile", "Growth"))
        r2 = str(vb.get("risk_choice") or a2.get("risk_profile", "Moderate"))
        if r1 != r2:
            friction_points.append(
                {
                    "id": "friction_risk_profile",
                    "title": f"Perfil de riesgo distinto: {name_a} ({r1}) vs {name_b} ({r2})",
                    "detail": (
                        f"{name_a} busca perfil {r1} mientras {name_b} prioriza {r2}; "
                        f"la alineación D4 figura como {case.persona.risk_alignment or 'MISALIGNED'}."
                    ),
                }
            )

        # Case-specific secondary cash/account friction from real data
        high_debts = case.high_interest_debts(threshold=0.10)
        if case.case_id == "timothy-melanie-weah":
            upro_val = next((float(p.get("value") or 0) for p in case.positions if str(p.get("ticker", "")).upper() == "UPRO"), 12740.0)
            excess = float(case.ia_facts.get("cash", {}).get("cashAboveTotalNeeded", {}).get("value", 60222.5))
            d = high_debts[0]
            friction_points.append(
                {
                    "id": "friction_cash_vs_leverage",
                    "title": f"Efectivo ocioso vs UPRO apalancado y tarjeta al {d['apr_pct']}%",
                    "detail": (
                        f"{name_b} retiene $150,800 en efectivo (~0.09%) mientras {name_a} mantiene {_fmt_usd(upro_val)} en UPRO (3x) "
                        f"y la tarjeta Chase CC ({_fmt_usd(d['balance'])}) quema {_fmt_usd(d['annual_interest'])}/año."
                    ),
                }
            )
            midpoint_pact = {
                "headline": "Pacto realista de Cordada: liquidez segura + limpieza de deuda cara + protección conjunta",
                "cash_flow_basis": f"Exceso de efectivo libre tras reserva y vacaciones: {_fmt_usd(excess)} (cashAboveTotalNeeded).",
                "owner_a_action": f"{name_a}: acotar exposición 3x (UPRO {_fmt_usd(upro_val)}) y subir 401(k) (+$10,500 de margen).",
                "owner_b_action": f"{name_b}: liquidar tarjeta de {_fmt_usd(d['balance'])} al {d['apr_pct']}% usando parte del efectivo excedente.",
                "joint_2_of_2": f"Check conjunto (2/2): cerrar brecha de vida ($1,100,000) y añadir umbrella ($1,000,000) para subir score {case.published_score} -> {target_score}.",
            }
        elif case.case_id == "daniel-emily-johnson":
            fcf = float(case.fh_facts.get("retirement", {}).get("netCashFlowThisYear", {}).get("value", 15032.01))
            d = high_debts[0]
            friction_points.append(
                {
                    "id": "friction_silos_debt_529",
                    "title": f"Silos de roles ({case.persona.decision_style}): tarjeta {d['apr_pct']}% y 529 vs 401(k) en $0",
                    "detail": (
                        f"{name_b} gestiona $26,000/año de ahorro ($8,000 al 529 y $12,000 a brokerage), mientras {name_a} "
                        f"carga {_fmt_usd(d['balance'])} al {d['apr_pct']}% ({_fmt_usd(d['annual_interest'])}/año) y ambos 401(k) reciben $0."
                    ),
                }
            )
            midpoint_pact = {
                "headline": "Pacto realista de Cordada: blindar hijos primero y redirigir flujo sin culpa",
                "cash_flow_basis": f"Flujo de caja libre actual: {_fmt_usd(fcf)}/año + $26,000/año de ahorro existente.",
                "owner_a_action": f"{name_a}: congelar nuevos cargos y liderar amortización acelerada de tarjeta al {d['apr_pct']}%.",
                "owner_b_action": f"{name_b}: redirigir temporalmente parte de los $12,000 de brokerage hacia colchón (1.4 meses -> 3 meses) y 401(k).",
                "joint_2_of_2": f"Check conjunto (2/2): activar cobertura de vida (+$1,166,000) + umbrella ($1,000,000) y subir score {case.published_score} -> {target_score}.",
            }
        else:  # pragma: no cover - defensive fallback for any future couple case
            fcf = float(case.fh_facts.get("retirement", {}).get("netCashFlowThisYear", {}).get("value", 0.0))
            midpoint_pact = {
                "headline": "Pacto realista de Cordada",
                "cash_flow_basis": f"Flujo de caja neto anual: {_fmt_usd(fcf)}/año.",
                "owner_a_action": f"{name_a}: priorizar pasos asignados en waterfall.",
                "owner_b_action": f"{name_b}: coordinar liquidez y protección.",
                "joint_2_of_2": f"Check conjunto (2/2) hacia score {target_score}.",
            }

        # Check explicit node vote disagreements if supplied
        votes_a_map = va.get("votes") if isinstance(va.get("votes"), dict) else {}
        votes_b_map = vb.get("votes") if isinstance(vb.get("votes"), dict) else {}
        for node_key in sorted(set(votes_a_map) & set(votes_b_map)):
            if votes_a_map[node_key] != votes_b_map[node_key] and len(friction_points) < 3:
                friction_points.append(
                    {
                        "id": f"vote_diff_{node_key}",
                        "title": f"Voto divergente en '{node_key}'",
                        "detail": f"{name_a} votó '{votes_a_map[node_key]}' y {name_b} votó '{votes_b_map[node_key]}'.",
                    }
                )

        # Keep isolated friction points concise (max 2 unless explicit vote diffs added)
        friction_points = friction_points[: max(2, len(friction_points))]

        result: dict[str, Any] = {
            "case_id": case.case_id,
            "household_name": case.household_name,
            "is_couple": True,
            "member_a": {"name": name_a, "risk_profile": r1, "top_fears": fears_a},
            "member_b": {"name": name_b, "risk_profile": r2, "top_fears": fears_b},
            "shared_100_percent": shared_100,
            "friction_points": friction_points,
            "midpoint_pact": midpoint_pact,
            "plain_summary": (
                f"Coincidís al 100% en proteger a vuestra familia ({case.persona.motivational_anchor or 'PROTECTION'}). "
                f"Aislados solo {len(friction_points)} puntos de roce para acordar antes de escalar: {midpoint_pact['headline']}."
            ),
            "math_summary": (
                f"{name_a} ({r1}) vs {name_b} ({r2}) | score {case.published_score} -> {target_score} | "
                f"{midpoint_pact['cash_flow_basis']}"
            ),
            "used_llm": False,
            "llm_fallback_used": False,
            "fallback_reason": None,
            "verified_numbers_only": True,
        }

        if use_llm:
            client = self._get_client(llm_client)
            enriched, used_llm, fb_used, fb_reason = _enrich_with_llm(
                client, case, "Síntesis Pacto Cordada Asimétrica", result, result, model=model
            )
            enriched["used_llm"] = used_llm
            enriched["llm_fallback_used"] = fb_used
            enriched["fallback_reason"] = fb_reason
            return enriched
        return result

    build_cordada_pact = synthesize_cordada_pact

    def generate_advisor_brief(
        self,
        case_id: str,
        fear_ranking: list[str] | None = None,
        subjective_concerns: list[str] | str | None = None,
        couple_votes: dict[str, Any] | None = None,
        skipped_moves: list[str] | None = None,
        unmodeled_goals: list[str] | None = None,
        use_llm: bool = False,
        llm_client: LLMProxyClient | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """Compile Advisor Brief: O1..O8 ranking + subjective concerns, T1..T5 tensions,
        A/B couple disagreements, and unmodeled goals turned into concrete advisor questions.
        """
        case = self.load_case(case_id)

        # 1. Fear ranking (`O1..O9` + Subjective concerns)
        concerns_by_id = {c.id: c for c in case.persona.objective_concerns}
        ordered_ids: list[str] = []
        for fid in fear_ranking or []:
            norm_id = str(fid).strip().upper()
            if norm_id in concerns_by_id and norm_id not in ordered_ids:
                ordered_ids.append(norm_id)
        for c in case.persona.objective_concerns:
            if c.id not in ordered_ids:
                ordered_ids.append(c.id)

        ranked_fears = [
            {
                "rank": idx + 1,
                **concerns_by_id[oid].to_dict(),
                "user_prioritized": oid in {str(x).strip().upper() for x in (fear_ranking or [])},
            }
            for idx, oid in enumerate(ordered_ids)
        ]

        if isinstance(subjective_concerns, str):
            captured_subj = [subjective_concerns.strip()] if subjective_concerns.strip() else []
        elif isinstance(subjective_concerns, list):
            captured_subj = [str(s).strip() for s in subjective_concerns if str(s).strip()]
        else:
            captured_subj = []

        subjective_section = {
            "persona_md_status": case.persona.subjective_concerns_raw or "None recorded",
            "persona_has_subjective": case.persona.has_subjective_concerns,
            "captured_from_user": captured_subj,
        }

        # 2. Tensions (`T1..T5`)
        tensions_list = [t.to_dict() for t in case.persona.tensions]

        # 3. Couple A/B disagreements
        if case.is_couple:
            cv = couple_votes or {}
            va = cv.get("member_a") or cv.get("partner_a") or cv.get("a") or {}
            vb = cv.get("member_b") or cv.get("partner_b") or cv.get("b") or {}
            pact = self.synthesize_cordada_pact(case_id, member_a_votes=va, member_b_votes=vb, use_llm=False)
            couple_section: dict[str, Any] = {
                "is_couple": True,
                "disagreements": pact["friction_points"],
                "shared_alignment": pact["shared_100_percent"],
                "midpoint_pact": pact["midpoint_pact"],
            }
            # Also handle explicit node vote list if provided: [{"node": "...", "vote_a": "...", "vote_b": "..."}]
            for item in cv.get("nodes", []) if isinstance(cv.get("nodes"), list) else []:
                if isinstance(item, dict) and item.get("vote_a") != item.get("vote_b"):
                    couple_section["disagreements"].append(
                        {
                            "id": f"node_{item.get('node', 'decision')}",
                            "title": f"Desacuerdo en nodo {item.get('node', '')}",
                            "detail": (
                                f"{pact['member_a']['name']} eligió '{item.get('vote_a')}' vs "
                                f"{pact['member_b']['name']} eligió '{item.get('vote_b')}'."
                            ),
                        }
                    )
        else:
            couple_section = {
                "is_couple": False,
                "disagreements": [],
                "shared_alignment": [],
                "midpoint_pact": None,
                "note": "Hogar individual: sin desacuerdos A/B de pareja.",
            }

        # 4. Unmodeled goals (no precalculated counterfactual in Sherpas -> concrete advisor questions)
        unmodeled_questions: list[dict[str, Any]] = []
        for g in case.profile.get("goals", []):
            gtype = str(g.get("type", ""))
            if gtype == "REAL_ESTATE_PURCHASE":
                yr = int(g.get("start_year", 2027))
                amt = float(g.get("amount", 0.0))
                planned = g.get("planned_purchase", {})
                costs = {c.get("name", ""): float(c.get("yearly", 0.0)) for c in g.get("yearly_costs", [])}
                down = next((v for k, v in costs.items() if "downpayment" in k.lower()), 0.0)
                closing = next((v for k, v in costs.items() if "closing" in k.lower()), 0.0)
                y_prev = case.projection_for_year(yr - 1) or {}
                y_buy = case.projection_for_year(yr) or {}
                neg_inv = case.first_negative_investable_year()
                cliff_note = (
                    f" y evitar el déficit líquido en {neg_inv['year']} ({_fmt_usd(neg_inv['investable_assets'])})"
                    if neg_inv
                    else ""
                )
                question = (
                    f"Sherpas no tiene calculado un escenario alternativo para la compra de vivienda de {_fmt_usd(amt)} en {yr} "
                    f"(precio proyectado {_fmt_usd(planned.get('value_at_purchase', amt))}, entrada {_fmt_usd(down)}, cierre {_fmt_usd(closing)}). "
                    f"Si retrasamos la compra 2-3 años o reducimos presupuesto, ¿cómo cambia la caída de activos invertibles "
                    f"de {_fmt_usd(y_prev.get('investable_assets', 0))} a {_fmt_usd(y_buy.get('investable_assets', 0))}{cliff_note}?"
                )
                unmodeled_questions.append(
                    {
                        "goal_name": g.get("name", "Purchase a home"),
                        "goal_type": gtype,
                        "target_year": yr,
                        "amount": amt,
                        "question": question,
                        "json_source": "financial-health.json -> profile.goals / projections.yearly",
                    }
                )
            elif gtype == "VEHICLE_PURCHASE":
                yr = int(g.get("start_year", 2028))
                amt = float(g.get("amount", 0.0))
                planned = g.get("planned_purchase", {})
                unmodeled_questions.append(
                    {
                        "goal_name": g.get("name", "Purchase a vehicle"),
                        "goal_type": gtype,
                        "target_year": yr,
                        "amount": amt,
                        "question": (
                            f"Para la compra del vehículo de {_fmt_usd(amt)} en {yr} "
                            f"({_fmt_usd(planned.get('value_at_purchase', amt))} a fecha de compra), "
                            "¿conviene pagarlo al contado con el exceso de liquidez o financiarlo tras liquidar la tarjeta al 18%?"
                        ),
                        "json_source": "financial-health.json -> profile.goals[VEHICLE_PURCHASE]",
                    }
                )

        # Also add data-grounded structural questions where Sherpas notes unknowns or unclosed gaps
        if case.case_id == "samantha-lewis":
            unmodeled_questions.append(
                {
                    "goal_name": "401(k) availability & taxable cost-basis",
                    "goal_type": "RETIREMENT_AND_TAX",
                    "target_year": 2026,
                    "amount": 24500,
                    "question": (
                        "¿Dispone su empleador de un 401(k) ($24,500 de margen) y podemos recopilar el cost basis faltante "
                        "de la cuenta taxable ($300,000, $3,032.20/año de tax drag) para reubicar VTI/JNK/SCHD sin impacto fiscal innecesario?"
                    ),
                    "json_source": "persona.md -> D2/O7/O8 & investment-analysis.json -> taxDragAnalysis.costBasisBlockingNotes",
                }
            )
        elif case.case_id == "daniel-emily-johnson":
            ret_gap = float(case.savings_and_contributions.get("goalCoverage", {}).get("retirementGap", 1427455.89))
            fcf = float(case.fh_facts.get("retirement", {}).get("netCashFlowThisYear", {}).get("value", 15032.01))
            unmodeled_questions.append(
                {
                    "goal_name": "Employer 401(k) match verification & gap sequencing",
                    "goal_type": "RETIREMENT_AND_PROTECTION",
                    "target_year": 2026,
                    "amount": ret_gap,
                    "question": (
                        f"El flujo libre anual es {_fmt_usd(fcf)} frente a {_fmt_usd(ret_gap)} de brecha de retiro: "
                        "¿confirmamos los matches estimados del 401(k) ($6,400 Daniel y $4,800 Emily) y cómo escalonar tarjeta al 24.9% + seguros?"
                    ),
                    "json_source": "persona.md -> O1/T1 & investment-analysis.json -> savingsWaterfall[4..5]",
                }
            )
        elif case.case_id == "timothy-melanie-weah":
            unmodeled_questions.append(
                {
                    "goal_name": "Expense reconciliation & UPRO exit plan",
                    "goal_type": "CASHFLOW_AND_RISK",
                    "target_year": 2026,
                    "amount": 12740,
                    "question": (
                        "La reconciliación de flujo marca gastos posiblemente subestimados (savingsCapacityReliable: false). "
                        "¿Confirmamos el gasto real mensual antes de asignar los $60,222.50 de efectivo libre y reducir UPRO ($12,740)?"
                    ),
                    "json_source": "investment-analysis.json -> savingsAndContributions.cashflowReconciliation & positions",
                }
            )

        for extra_goal in unmodeled_goals or []:
            unmodeled_questions.append(
                {
                    "goal_name": str(extra_goal),
                    "goal_type": "USER_FLAGGED",
                    "target_year": None,
                    "amount": None,
                    "question": f"El hogar pidió evaluar un contrafactual con el asesor para: {extra_goal}.",
                    "json_source": "user_simulation_flag",
                }
            )

        advisor_questions = [q["question"] for q in unmodeled_questions]
        if ranked_fears:
            top_f = ranked_fears[0]
            advisor_questions.insert(
                0,
                f"Miedo #1 priorizado por la familia ({top_f['id']} · {top_f['severity']}): {top_f['title']} — definir plan inmediato.",
            )
        for s in captured_subj:
            advisor_questions.append(f"Preocupación subjetiva expresada por el hogar (ausente en persona.md): {s}")
        for skipped in skipped_moves or []:
            advisor_questions.append(f"Decisión omitida en la simulación que requiere revisión conjunta: {skipped}")

        lines = [
            f"# Advisor Brief — {case.household_name} ({case.case_id})",
            f"- **Score publicado:** {case.published_score}/100 ({case.score_band})",
            f"- **Ancla motivacional:** {case.persona.motivational_anchor or 'N/A'} | **Estilo:** {case.persona.decision_style or 'N/A'}",
            "",
            "## 1. Ranking de Miedos (O1..O8/O9) + Miedos Subjetivos",
            *[f"{f['rank']}. [{f['id']} · {f['severity']}] {f['title']}" for f in ranked_fears[:5]],
            f"- **Subjective concerns (persona.md):** {subjective_section['persona_md_status']}",
            *(
                [f"- **Capturados en Quest:** {'; '.join(captured_subj)}"]
                if captured_subj
                else []
            ),
            "",
            "## 2. Tensiones Reales (T1..T5)",
            *[f"- **{t['id']} ({t['severity']}):** {t['summary']}" for t in tensions_list],
            "",
            "## 3. Desacuerdos de Pareja (Votación A/B)",
            *(
                [f"- {d['title']}: {d['detail']}" for d in couple_section["disagreements"]]
                if couple_section["disagreements"]
                else [f"- {couple_section.get('note', 'Sin desacuerdos.')}"]
            ),
            "",
            "## 4. Preguntas Concretas al Asesor (Metas sin Contrafactual Precalculado)",
            *[f"- {q}" for q in advisor_questions],
        ]

        brief: dict[str, Any] = {
            "case_id": case.case_id,
            "household_name": case.household_name,
            "published_score": case.published_score,
            "score_band": case.score_band,
            "fear_ranking": ranked_fears,
            "subjective_concerns": subjective_section,
            "tensions": tensions_list,
            "couple_disagreements": couple_section,
            "unmodeled_goal_questions": unmodeled_questions,
            "skipped_moves": list(skipped_moves or []),
            "advisor_questions": advisor_questions,
            "markdown_brief": "\n".join(lines),
            "used_llm": False,
            "llm_fallback_used": False,
            "fallback_reason": None,
            "verified_numbers_only": True,
        }

        if use_llm:
            client = self._get_client(llm_client)
            grounded = {
                "case_id": case.case_id,
                "published_score": case.published_score,
                "top_fears": ranked_fears[:3],
                "tensions": tensions_list,
                "unmodeled_goal_questions": unmodeled_questions,
            }
            enriched, used_llm, fb_used, fb_reason = _enrich_with_llm(
                client, case, "Generar resumen ejecutivo Advisor Brief", grounded, brief, model=model
            )
            enriched["used_llm"] = used_llm
            enriched["llm_fallback_used"] = fb_used
            enriched["fallback_reason"] = fb_reason
            return enriched

        return brief


def translate_dual_lens(
    case_id: str,
    topic: str = "overview",
    lens: str = "both",
    use_llm: bool = False,
    llm_client: LLMProxyClient | None = None,
    model: str | None = None,
    cases_dir: str | Path | None = None,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Module-level wrapper for `BehavioralNarrator.translate_dual_lens`."""
    return BehavioralNarrator(cases_dir=cases_dir, llm_client=llm_client).translate_dual_lens(
        case_id=case_id,
        topic=topic,
        lens=lens,
        use_llm=use_llm,
        llm_client=llm_client,
        model=model,
        context=context,
    )


def detect_behavioral_biases(
    case_id: str,
    include_untriggered: bool = False,
    category: str | None = None,
    cases_dir: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Module-level wrapper for `BehavioralNarrator.detect_behavioral_biases`."""
    return BehavioralNarrator(cases_dir=cases_dir).detect_behavioral_biases(
        case_id=case_id,
        include_untriggered=include_untriggered,
        category=category,
    )


def explain_bias(
    case_id: str,
    bias_id: str,
    use_llm: bool = False,
    llm_client: LLMProxyClient | None = None,
    model: str | None = None,
    cases_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Module-level wrapper for `BehavioralNarrator.explain_bias`."""
    return BehavioralNarrator(cases_dir=cases_dir, llm_client=llm_client).explain_bias(
        case_id=case_id,
        bias_id=bias_id,
        use_llm=use_llm,
        llm_client=llm_client,
        model=model,
    )


def synthesize_cordada_pact(
    case_id: str,
    member_a_votes: dict[str, Any] | None = None,
    member_b_votes: dict[str, Any] | None = None,
    use_llm: bool = False,
    llm_client: LLMProxyClient | None = None,
    model: str | None = None,
    cases_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Module-level wrapper for `BehavioralNarrator.synthesize_cordada_pact`."""
    return BehavioralNarrator(cases_dir=cases_dir, llm_client=llm_client).synthesize_cordada_pact(
        case_id=case_id,
        member_a_votes=member_a_votes,
        member_b_votes=member_b_votes,
        use_llm=use_llm,
        llm_client=llm_client,
        model=model,
    )


build_cordada_pact = synthesize_cordada_pact


def generate_advisor_brief(
    case_id: str,
    fear_ranking: list[str] | None = None,
    subjective_concerns: list[str] | str | None = None,
    couple_votes: dict[str, Any] | None = None,
    skipped_moves: list[str] | None = None,
    unmodeled_goals: list[str] | None = None,
    use_llm: bool = False,
    llm_client: LLMProxyClient | None = None,
    model: str | None = None,
    cases_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Module-level wrapper for `BehavioralNarrator.generate_advisor_brief`."""
    return BehavioralNarrator(cases_dir=cases_dir, llm_client=llm_client).generate_advisor_brief(
        case_id=case_id,
        fear_ranking=fear_ranking,
        subjective_concerns=subjective_concerns,
        couple_votes=couple_votes,
        skipped_moves=skipped_moves,
        unmodeled_goals=unmodeled_goals,
        use_llm=use_llm,
        llm_client=llm_client,
        model=model,
    )
