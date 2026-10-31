# W03 — Qwen → Qwen2 모임 Q&A

[W03 주차 페이지](README.md) · 모임: 2026-10-31(토) · 기록: 모임 채팅

이 문서의 항목은 W03 모임 채팅에 나온 질문과 의견을 파트별로 묶은 것이며, 질문한 사람의 이름은 적지 않았습니다. 항목마다 "모임에서"는 그 자리에서 나온 질문과 답·의견만 옮긴 것이고, "보충"은 모임 뒤에 논문·공식 문서 같은 원문을 열어 확인한 내용입니다(원문에 없는 추론은 해석, 직접 계산은 계산, 원문에 적히지 않은 것은 원문 미기술로 표시). 슬라이드 링크의 'Architecture 덱'은 [slides/qwen-architecture-deck.html](slides/qwen-architecture-deck.html), '배경 덱'은 [slides/alignment-background-study.html](slides/alignment-background-study.html)입니다.

## 목차

- [Tokenizer](#tokenizer)
- [Data & Synthesis](#data--synthesis)
- [Architecture (MoE)](#architecture-moe)
- [Alignment & RL](#alignment--rl)
- [후속으로 볼 것](#후속으로-볼-것)

## Tokenizer

### Q. 다국어 쪽 설명의 "낮을수록 좋다"는 말은 토크나이저를 거친 뒤 토큰이 적게 나온다는 것과 같은 뜻인가?

**모임에서:** 발표의 다국어 쪽 설명에 나온 "낮을수록 좋다"는 말이, 같은 글을 토크나이저로 잘랐을 때 토큰이 적게 나온다는 것과 같은 뜻(동치)인지 묻는 질문이 나왔습니다. 모임에서 답이 기록되지 않았습니다.

**보충:** 이 설명은 Qwen Figure 3(인코딩 압축률)을 가리키는 것으로 보입니다(해석). 같은 언어의 같은 문서로 모델끼리 비교할 때는 "막대가 낮다 = 토큰이 적다"로 읽어야 원문과 맞습니다. 다만 원문에 식이 없으므로 아래 3번은 해석입니다.

1. Qwen §2.2와 Figure 3(p.6) 원문: 언어마다 문서 100만 개를 무작위로 골라 여러 모델의 encoding compression rate(인코딩 압축률)를 비교했습니다. 100개 언어를 지원하는 XLM-R(Conneau et al. 2019의 다국어 모델)의 토크나이저를 기준값 1로 두었고, XLM-R 막대는 그림에 그리지 않았습니다.
2. 그림의 y축 이름은 "Compression Ratio"입니다. 분홍색 Qwen 막대는 거의 모든 언어에서 가장 낮습니다. 예를 들어 ko(한국어)에서 LLaMA-7B는 약 2.8이고 Qwen은 약 1.25입니다(그림에서 눈으로 읽은 값). 본문은 Qwen이 대부분 언어에서 경쟁 모델보다 압축 효율이 높고, 더 적은 토큰으로 더 많은 정보를 담기 때문에 서빙 비용이 줄어든다고 씁니다. 막대가 가장 낮은 Qwen을 "압축 효율이 높다"고 했으므로, 이 그림에서는 낮을수록 좋습니다.
3. 해석: y = (그 모델의 토큰 수) ÷ (같은 문서를 XLM-R로 자른 토큰 수)로 읽어야 1·2번과 앞뒤가 맞습니다. 이렇게 읽으면 같은 문서에서 "막대가 낮다"와 "토큰이 적게 나온다"는 같은 말입니다.
4. 계산 예시(한 문장으로 직접 실행): "토크나이저는 자주 나오는 바이트열을 합친다"(23글자, UTF-8로 61바이트)를 네 토크나이저로 잘랐습니다.

   | 토크나이저 | 토큰 수 | XLM-R 대비 |
   |---|---|---|
   | XLM-R (어휘 250,002개) | 16 | 16 ÷ 16 = 1.00 |
   | Qwen (Qwen-7B 어휘 파일. Qwen2 토크나이저도 21개로 같음) | 21 | 21 ÷ 16 ≈ 1.31 |
   | cl100k_base (GPT-3.5 · GPT-4의 어휘, 이하 cl100k) | 25 | 25 ÷ 16 ≈ 1.56 |
   | Llama 2 (Llama 2 §2.2: LLaMA 1과 같은 토크나이저) | 34 | 34 ÷ 16 ≈ 2.13 |

   문장이 하나뿐이라 값의 크기는 그림(문서 100만 개)과 다릅니다. 그래도 한국어에서 Llama 2 > Qwen > XLM-R 순서는 그림과 같습니다.

5. 해석상 주의할 점이 두 가지 있습니다. (a) 값은 언어마다 그 언어를 XLM-R로 잘랐을 때의 토큰 수로 나눈 상대값입니다. 그래서 언어끼리 막대 높이를 비교해 "th가 en보다 몇 배 비싸다"고 읽을 수는 없습니다. 언어별 절대 토큰 수는 원문에 나오지 않습니다(원문 미기술). (b) 토큰이 적다는 것은 원문이 말하는 학습·서빙 효율이고, 그것만으로 모델 품질이 좋다는 뜻은 아닙니다. 원문은 어휘를 키워도 downstream(사전학습을 마친 모델에 실제로 시키는 하류 과제) 성능이 유지됐다는 예비 실험을 언급하지만, 수치는 적지 않았습니다(원문 미기술).

- 원문: [Qwen §2.2 · Figure 3 · p.6](https://arxiv.org/pdf/2309.16609v1#page=6) · [Llama 2 §2.2 Tokenizer · p.6](https://arxiv.org/pdf/2307.09288v2#page=6)
- 슬라이드: [배경 덱 p.19 · Fig. 3 읽는 법](slides/alignment-background-study.html#s19) · [배경 덱 p.7 · 18토큰 vs 9토큰](slides/alignment-background-study.html#s7)

### Q. 한글은 자음·모음의 조합이라 개수가 적고 한자는 조합이 무궁무진할 텐데, 언어별 토큰 개수 차이가 왜 10배도 안 되나? 어떻게 처리한 것인가?

**모임에서:** 발표에서 언어(문자)별 개수를 설명한 뒤 나온 질문입니다. 한국어는 자음·모음만 놓고 보면 개수가 얼마 안 되고, 한자는 뜻글자라 조합이 무궁무진하다고 생각했습니다. 그래서 차이가 훨씬 클 줄 알았는데 10배도 안 되는 이유와, 어떻게 처리했는지를 물었습니다. 기록된 문장이 중간에 끊겨 있어서 "10배"가 정확히 어떤 기대였는지는 분명하지 않습니다. 질문에 이어 "토크나이저 단어장도 웹에서 가져온 데이터로 만드니 결과가 이렇게 된 것 아닐까"라는 추측이 나왔습니다. 질문자 본인의 가설인지 다른 참가자의 답인지는 기록상 분명하지 않습니다.

**보충:**

**(1) 질문의 '개수'는 원문에 나오는 수치가 아닙니다.** 어휘 구성에 대해 Qwen §2.2가 쓴 내용은 네 가지입니다. cl100k_base에서 출발했다는 것, 자주 쓰는 중국어 글자·단어와 다른 언어의 글자·단어를 어휘에 더했다는 것, LLaMA를 따라 숫자를 한 자리씩 나눴다는 것, 최종 어휘가 약 152K라는 것입니다. 언어별 개수는 적지 않았습니다(원문 미기술). Qwen2 §2.1에 따르면 Qwen2도 같은 토크나이저를 쓰고, 일반 토큰 151,643개와 control 토큰 3개로 이루어집니다. 모임에서 말한 언어별 개수는 배경 덱 p.12의 값으로 보입니다(해석). 덱은 Qwen-7B 어휘 파일과 cl100k를 직접 비교해 "새 토큰 52,487개 중 한자 24,625개, 한글 3,286개"를 셌습니다. 24,625 ÷ 3,286 ≈ 7.5배이므로 "10배가 안 된다"는 말과 맞습니다.

같은 파일로 다시 세어 보았습니다(계산, 직접 실행).

- cl100k 일반 토큰 100,256개에서, Qwen에 없는 cl100k 토큰 1,100개(2자리 숫자 100개 + 3자리 숫자 1,000개)를 빼면 99,156개입니다. 이 토큰들이 Qwen의 0–99,155번입니다.
- Qwen 일반 토큰 151,643개 − 99,156개 = 새 토큰 52,487개(99,156–151,642번)입니다.
- 세는 기준은 다음과 같습니다. 새 토큰 52,487개 가운데 UTF-8 글자로 온전히 풀리는 51,812개만 셌습니다. 나머지 675개(52,487 − 51,812)는 글자 중간에서 끊긴 바이트 조각이라 글자로 풀리지 않습니다. '한글'은 Unicode 이름이 HANGUL로 시작하는 글자, 즉 완성형 음절(U+AC00–D7A3)과 자모(ㅋ·ㅎ·ᄀ 등)입니다. '한자'는 CJK 통합 한자(U+4E00–9FFF, 확장 A U+3400–4DBF, 확장 B 이후 U+20000–323AF)와 호환 한자(U+F900–FAFF, U+2F800–2FA1F)입니다.
- 이 기준으로 한글이 한 글자라도 들어 있는 새 토큰은 3,286개로 덱과 같습니다. 이 가운데 완성형 음절이 든 것은 3,192개이고, 음절 없이 자모만 든 것이 94개입니다(3,192 + 94 = 3,286).
- 한자가 한 글자라도 들어 있는 새 토큰은 25,174개로, 덱의 24,625개와 다릅니다. 덱의 24,625개는 재현하지 못했습니다. 덱은 토큰마다 문자 체계를 하나씩만 정해 나눈 표라서 세는 방식이 다른 것으로 보입니다(해석).
- 배율은 25,174 ÷ 3,286 ≈ 7.7배이고, 한글을 완성형 음절로만 세면 25,174 ÷ 3,192 ≈ 7.9배입니다. 세는 기준을 바꾸면 값이 조금 달라집니다. 예를 들어 같은 51,812개를 Unicode 문자 체계 속성(\p{Hangul}, \p{Han})으로 세면 한글 3,313개, 한자 25,239개입니다.

**(2) '자모 조합 수'가 토큰 수를 정하지 않는 이유를 단계별로 봅니다.**

1. 한글은 완성형 음절마다 Unicode 번호가 이미 있습니다. 초성 19 × 중성 21 × 종성 28(받침 없음 포함) = 19 × 588 = 11,172자입니다(Unicode §3.12의 LCount · VCount · TCount · SCount). 시작 번호가 U+AC00이므로 끝 번호는 0xAC00 + 11,172 − 1 = 0xD7A3, 즉 U+D7A3입니다(계산).
2. UTF-8은 U+0800–U+FFFF 범위의 글자를 3바이트로 저장합니다(RFC 3629 §3). 한글 음절은 모두 이 범위에 있어서 3바이트입니다(예: '한' U+D55C → ED 95 9C). '漢' U+6F22처럼 U+FFFF 이하에 있는 한자도 3바이트입니다(→ E6 BC A2). U+10000 이상에 있는 확장 한자는 4바이트입니다(예: U+20000 → F0 A0 80 80). (계산, 직접 실행)
3. Qwen 토크나이저는 입력을 먼저 NFC(Normalization Form C: 풀어 쓴 자모를 완성형 글자로 합치는 Unicode 정규화)로 바꿉니다(tokenization_qwen.py). 그래서 자모를 풀어 쓴 글도 완성형 음절로 합쳐진 뒤에 바이트로 바뀝니다. 결국 토크나이저는 한글을 자모 단위로 보지 않습니다. 한자와 똑같이 "글자 하나 = 3바이트"로 봅니다(해석).
4. BPE(Byte Pair Encoding)는 가장 자주 나오는 기호 쌍을 새 기호 하나로 바꾸는 과정을 반복해서 어휘를 만듭니다(Sennrich et al. 2016 §3.2). byte-level BPE는 이 과정을 바이트에서 시작합니다. 그래서 어휘에 몇 개가 들어가는지는 그 문자 체계로 이론상 만들 수 있는 조합 수가 정하지 않습니다. 어휘를 만들 때 쓴 데이터에서 얼마나 자주 나왔는지, 그리고 몇 개를 추가하기로 했는지가 정합니다(해석). Qwen 원문도 "자주 쓰는(commonly used)" 중국어 글자와 단어를 더했다고 씁니다.
5. 실제 Qwen 새 토큰을 종류별로 나누면 다음과 같습니다(계산, 직접 실행). 세는 기준은 (1)과 같고, 이 표의 한글 열은 세 줄 모두 완성형 음절만 셉니다.

   | 새 토큰의 종류 | 한자 | 한글 음절 | 배율 |
   |---|---|---|---|
   | ① 한 글자짜리(앞에 공백이 붙은 것도 셈) | 8,455 | 2,499 | 8,455 ÷ 2,499 ≈ 3.4배 |
   | ② 두 글자 이상이고 전부 한자 / 전부 한글 음절(앞에 공백이 붙은 것도 셈) | 16,169 | 693 | 16,169 ÷ 693 ≈ 23배 |
   | ③ 그 문자가 한 글자라도 든 것 | 25,174 | 3,192 | 25,174 ÷ 3,192 ≈ 7.9배 |

   ①과 ②를 더한 값과 ③의 차이는 다음과 같습니다(계산).

   - 한자: 25,174 − (8,455 + 16,169) = 550개입니다. 한자에 문장부호 등 다른 글자가 섞인 토큰입니다.
   - 한글 음절: 3,192 − (2,499 + 693) = 0개입니다. 음절이 든 토큰에는 다른 글자가 섞인 것이 없습니다. 한글 음절 토큰 가운데 앞에 공백이 붙은 것은 ①에 116개, ②에 414개입니다(공백 없는 것만 세면 ① 2,383개, ② 279개).
   - (1)의 한글 3,286개와 이 표의 3,192개가 다른 것은, (1)이 자모만 든 토큰 94개(ㅋ·ㅎ·ㅠ 등)도 셌기 때문입니다.

   표에서 읽을 수 있는 것은 다음과 같습니다.

   - 한 글자 토큰끼리 비교하면 차이는 3.4배뿐입니다. 큰 차이는 여러 글자짜리 "단어" 토큰에서 나옵니다(23배). 한자 쪽 새 토큰의 약 64%(16,169 ÷ 25,174)가 단어 토큰입니다. 전체 7.5–7.9배(세는 기준에 따라 다름)는 이 두 경우가 섞인 결과입니다(해석).
   - Qwen 어휘 전체에서 한 글자 토큰으로 들어 있는 한글 음절은 서로 다른 것만 세어 2,512자입니다. 11,172자의 약 22.5%(2,512 ÷ 11,172)입니다. 같은 기준으로 한자는 9,004자입니다. 어휘에 없는 나머지 음절은 바이트 조각 여러 개로 표현됩니다. 예를 들어 '토크'(바이트 ED 86 A0 · ED 81 AC)는 [ED 86] [A0 ED] [81] [AC]의 4토큰으로 잘립니다. 둘째 토큰은 '토'의 마지막 바이트와 '크'의 첫 바이트를 합친 것입니다. 이처럼 byte-level BPE는 글자 경계와 상관없이 자주 붙어 나오는 바이트를 합칩니다.
6. 모임의 추측("웹 데이터로 단어장을 만들어서")을 원문과 대조해 보았습니다. Qwen §2.1은 사전학습 데이터에 공개 웹 문서·백과사전·책·코드 등이 들어가고 영어와 중국어의 비중이 크다고 씁니다. 하지만 어휘를 추가할 때 어떤 데이터를 썼는지, 언어별로 몇 개씩 배분했는지는 적지 않았습니다(원문 미기술). 추측은 4번의 원리와 어긋나지 않습니다(해석). 다만 원문으로 확인할 수는 없습니다.
7. 한국어를 자모 단위로 자르면 어떻게 되는지는 다음 항목에서 공유된 논문의 자모(CV) 결과로 볼 수 있습니다.

- 원문: [Qwen §2.2 · p.6](https://arxiv.org/pdf/2309.16609v1#page=6) · [Qwen §2.1 · p.5](https://arxiv.org/pdf/2309.16609v1#page=5) · [Qwen2 §2.1 · p.3](https://arxiv.org/pdf/2407.10671v4#page=3) · [Unicode 16.0 §3.12](https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-3/) · [RFC 3629 §3](https://www.rfc-editor.org/rfc/rfc3629) · [Sennrich et al. 2016 §3.2 · p.3](https://aclanthology.org/P16-1162.pdf#page=3) · [Qwen-7B tokenization_qwen.py](https://huggingface.co/Qwen/Qwen-7B/raw/main/tokenization_qwen.py)
- 슬라이드: [배경 덱 p.12 · 새 토큰 중 한자 · 한글](slides/alignment-background-study.html#s12) · [배경 덱 p.4 · 유니코드와 UTF-8](slides/alignment-background-study.html#s4) · [배경 덱 p.14 · byte-level BPE](slides/alignment-background-study.html#s14) · [배경 덱 p.18 · BPE 학습은 빈도로](slides/alignment-background-study.html#s18)

### 의견: 한국어 토큰화 방법을 비교한 논문 공유

**모임에서:** 앞 질문에 이어, 한국어 토큰화 방법을 비교한 논문(ACL Anthology, AACL-IJCNLP 2020) 링크가 공유되었습니다. 자모·음절·BPE 등을 비교했는데, 대체로 형태소 분석 + BPE가 좋다고 보고한다는 소개였습니다. 후속으로 "앞으로 한국어 모델 논문을 읽을 때 형태소 분석을 했는지, 자모를 고려했는지 확인하자"는 메모가 남았습니다.

**보충:** 공유된 논문은 Park, Lee, Jang, Jung, *An Empirical Study of Tokenization Strategies for Various Korean NLP Tasks*, AACL-IJCNLP 2020, pp.133–142입니다.

- 비교한 방법(§4)은 여섯 가지입니다. 자모(CV, Consonant and Vowel), 음절, 형태소(MeCab-ko), 서브워드(SentencePiece BPE), 형태소 인식 서브워드(MeCab-ko로 형태소를 먼저 나눈 뒤 BPE 적용), 어절(공백 단위)입니다.
- 번역(한→영, 영→한)에서는 형태소 인식 서브워드 32K의 BLEU(기계 번역 품질 점수)가 가장 높았습니다(test 기준 Ko-En 40.34, En-Ko 40.41. Table 3).
- NLU(Natural Language Understanding) 5개 과제에 대해, 결론(§7)은 하나의 최선 전략이 없다고 씁니다. KorQuAD에서는 BPE만 쓴 서브워드 64K가 가장 좋았고(Table 6: EM/F1 74.04/86.66. EM은 서브워드 32K도 74.04로 같음), 나머지 KorNLI · KorSTS · NSMC · PAWS-X 네 과제에서는 형태소 인식 서브워드 64K가 최적이었다고 씁니다(§5.2.6, §7).
  - 다만 Table 6 값을 보면 예외가 있습니다. KorSTS test는 형태소 인식 서브워드 32K가 78.11로 64K의 76.78보다 높습니다. KorSTS에서 64K가 가장 높은 것은 dev(84.29)입니다. NSMC test는 64K 89.66, 32K 89.65로 거의 같습니다.
  - 따라서 모임의 소개("대체로 형태소 + BPE가 좋다")는 대체로 맞습니다. 예외는 KorQuAD이고, 표의 값으로는 KorSTS test도 예외입니다.
- 자모(CV) 방식은 어휘가 166개로 가장 작고, OOV(Out-Of-Vocabulary, 어휘에 없는 토큰) 비율도 0.02%로 가장 낮습니다. 하지만 Table 3의 평균 길이(Avg. Length)가 142.75로 음절 방식(69.20)의 약 2.1배(142.75 ÷ 69.20 ≈ 2.06)이고, 번역 성능은 음절·서브워드 방식보다 낮았습니다. 저자들은 자모 하나가 너무 많은 문맥 정보를 떠맡아야 하기 때문이라고 추측합니다. "자모로 보면 개수가 적다"는 것이 곧 효율적이라는 뜻은 아님을 보여 주는 근거입니다(해석).
  - Avg. Length의 단위(문장당 토큰 수인지)는 원문 정의를 확인하지 못했습니다. Table 3 일부 행의 어휘 크기 표기도 PDF 텍스트 추출에서 빠져 확인하지 못했습니다.
- 적용 범위에 주의해야 합니다(해석). 이 논문은 한국어 전용 SentencePiece BPE로 BERT-Base와 번역 모델을 실험했습니다. 다국어 byte-level BPE를 쓰는 Qwen에 결과를 그대로 옮길 수는 없습니다.

- 원문: [Park et al. 2020 (ACL Anthology)](https://aclanthology.org/2020.aacl-main.17/) · [같은 논문 Table 3 · p.4](https://aclanthology.org/2020.aacl-main.17.pdf#page=4) · [Table 6 · p.6](https://aclanthology.org/2020.aacl-main.17.pdf#page=6) · [§5.2.6 · p.7](https://aclanthology.org/2020.aacl-main.17.pdf#page=7) · [§7 Conclusion · p.8](https://aclanthology.org/2020.aacl-main.17.pdf#page=8)

### Q. 글자와 숫자를 다르게 처리한다면, 글자와 숫자가 섞인 단어(예: llama2)는 어떻게 잘리나?

**모임에서:** "llama (token id) / 2 (token id) …"처럼 글자 부분과 숫자 부분이 따로 토큰이 된다는 답이 나왔고, 질문자도 이해했다고 답했습니다.

**보충:** 글자와 숫자가 따로 잘린다는 답은 맞습니다. 다만 직접 돌려 보면 'llama'도 토큰 하나가 아니라 두 개로 잘립니다.

1. 원문: Qwen §2.2는 LLaMA를 따라 숫자를 한 자리씩 나눴다고 씁니다. Llama 2 §2.2도 모든 숫자를 한 자리씩 나눈다고 씁니다. 실제로 어떻게 나누는지(정규식)는 두 원문 모두 적지 않았습니다(원문 미기술).
2. 공개 코드(Qwen-7B tokenization_qwen.py)를 보면, BPE를 적용하기 전에 정규식으로 글을 미리 나눕니다(pre-tokenization). 정규식에서 `[^\r\n\p{L}\p{N}]?\p{L}+`는 글자(\p{L})가 이어진 덩어리를, `\p{N}`은 숫자(\p{N}) 한 개를 잡습니다. 두 패턴이 서로 다른 갈래라서, 글자와 숫자는 이 단계에서 이미 다른 덩어리가 됩니다. Qwen2-7B tokenizer.json의 pre_tokenizer도 같은 정규식입니다(로컬 사본에서 확인).
3. 합치기(BPE)는 덩어리마다 따로 실행됩니다. tiktoken(Qwen §2.2가 출발점으로 쓴 공개 BPE 토크나이저 라이브러리) 구현에서도 정규식으로 나눈 '단어'마다 bpe_encode를 따로 호출합니다. 그래서 'a2'처럼 글자와 숫자에 걸친 토큰은 생기지 않습니다(해석: 구현 방식에서 따라 나오는 결과).
4. 직접 실행한 결과입니다. Qwen-7B qwen.tiktoken과 Qwen2-7B tokenizer.json에서 id가 같게 나왔습니다.

   | 입력 | 미리 나누기 | 토큰(조각) | token_id |
   |---|---|---|---|
   | llama2 | llama · 2 | ll · ama · 2 | 654 · 3029 · 17 |
   | Llama2-7B | Llama · 2 · - · 7 · B | L · lama · 2 · - · 7 · B | 43 · 80001 · 17 · 12 · 22 · 33 |
   | 123456 | 1 · 2 · 3 · 4 · 5 · 6 | 1 · 2 · 3 · 4 · 5 · 6 | 16 · 17 · 18 · 19 · 20 · 21 |

5. 다른 토크나이저와 비교해 보았습니다. cl100k(GPT-3.5 · GPT-4) 정규식도 글자와 숫자를 다른 갈래로 둡니다(설치된 tiktoken 0.14.0 소스에서 확인). 다만 숫자는 `\p{N}{1,3}`, 즉 1–3자리를 한 덩어리로 묶습니다. 그래서 'llama2'는 cl100k에서도 ll · ama · 2(id 657 · 3105 · 17)로 Qwen과 모양이 같습니다. 차이는 숫자가 길 때 나타납니다. '123456'을 cl100k는 123 · 456의 2토큰으로, Qwen은 6토큰으로 자릅니다. 즉 Qwen이 바꾼 것은 글자와 숫자를 나누는 부분이 아니라, 숫자를 한 자리씩 끊는 부분입니다. Llama 2 토크나이저(SentencePiece)도 'llama2'를 ▁ll · ama · 2로 자릅니다(직접 실행).

- 원문: [Qwen §2.2 · p.6](https://arxiv.org/pdf/2309.16609v1#page=6) · [Llama 2 §2.2 Tokenizer · p.6](https://arxiv.org/pdf/2307.09288v2#page=6) · [Qwen-7B tokenization_qwen.py](https://huggingface.co/Qwen/Qwen-7B/raw/main/tokenization_qwen.py)
- 슬라이드: [배경 덱 p.10 · 숫자를 한 자리씩](slides/alignment-background-study.html#s10) · [배경 덱 p.5 · 정규화 → 미리 나누기 → 합치기](slides/alignment-background-study.html#s5) · [배경 덱 p.23 · 합치기는 미리 나누기 경계를 넘지 못한다](slides/alignment-background-study.html#s23)

## Data & Synthesis

### Q. 복잡도·다양성을 높이거나 지시문을 어렵게 만든 데이터의 효과를 2턴짜리 MT-Bench로 확인했는데, 여러 턴·긴 context에서도 통할까?

**모임에서:** 복잡도·다양성을 바꾸거나 지시문을 어렵게 만드는 식으로 데이터를 바꿔 성능이 좋아지는지 확인한 연구들을 보았습니다. 그런데 그 결과는 두 턴까지만 있는 MT-Bench로 잰 것이니, 여러 턴이 이어지는 환경이나 긴 context-length에서도 통할지 묻는 질문이 나왔습니다. 채팅에는 "Nemotron의 SDG나 'Instruction Following with Composable Constraints' 같은 자료를 보면 될 것 같다"는 안내가 남았습니다. 구체적인 결론은 기록되지 않았습니다.

**보충:**

1. MT-Bench(멀티턴 질문 세트)는 2턴이 맞습니다. 문항은 80개로, 8개 범주마다 10개씩입니다. 모든 문항이 두 턴으로 되어 있습니다(§2.2, §3.5). 한 답에 점수를 매기는 방식에서는 80 × 2 = 160턴의 평균을 냅니다. 두 번째 턴을 채점할 때는 대화 전체를 프롬프트 하나에 넣고, GPT-4 심판에게 두 번째 질문에 집중하라고 지시합니다.
2. 발표에서 본 연구들이 근거로 삼은 평가의 범위는 다음과 같습니다.
   - InsTag: 태그로 고른 6K 데이터로 학습한 TagLM-13b-v1.0(LLaMA-13B 기반)의 MT-Bench 점수는 6.44±0.04입니다. 같은 LLaMA 기반으로 125K 데이터로 학습한 Vicuna-13B v1.3은 6.39입니다(Table 3). Llama 2 기반인 TagLM-13b-v2.0은 6.55±0.02입니다. 저자들도 Limitations에서 결론이 주로 MT-Bench에 기대고 있다고 밝힙니다.
   - Tree-Instruct: 노드를 3 · 6 · 10개 더하자 MT-Bench가 4.74 → 6.10 · 6.27 · 6.43으로, AlpacaEval(강한 LLM 심판, 예: GPT-4가 기준 모델의 답보다 평가 대상 모델의 답을 고른 비율을 재는 평가) 승률이 46.02 → 59.53 · 66.38 · 72.66으로 올랐습니다(Table 1).
   - 해석: 복잡도·다양성의 효과는 최대 2턴(MT-Bench)과 AlpacaEval에서 확인된 것입니다. 3턴 이상이나 긴 대화에서도 효과가 같은지는 이 논문들만으로는 알 수 없습니다. 질문의 지적이 맞습니다.
3. Qwen2 자체의 경우를 원문에서 확인했습니다. instruction-tuned 모델은 single-turn과 multi-turn instruction-following 데이터로 학습했습니다(§1). SFT(Supervised Fine-Tuning)는 50만 개가 넘는 예제로, sequence length 32,768로 2 epoch 학습했습니다(§4.2). 길이 제한 같은 제약이 붙은 지시에서는 LLM(Large Language Model)이 Python 검증 함수를 만들어 응답이 제약을 지키는지 확인합니다(§4.1.2 Execution Feedback). 평가에는 MT-Bench · Arena-Hard · AlignBench · MixEval · IFEval(Instruction-Following Evaluation)을 썼습니다(§5.2.1). 긴 context는 NIAH(Needle in a Haystack) · NeedleBench · LV-Eval로 평가했습니다(§5.2.3). 원문 설명으로는 셋 다 긴 글에서 사실을 찾거나 여러 근거를 종합해 답하는 과제입니다. NIAH는 긴 글(8K–128K 토큰)의 여러 깊이에 넣어 둔 사실을 찾게 합니다(p.15). NeedleBench는 사실 2–5개를 넣어 동시에 찾고 multi-hop 추론을 하게 하고, LV-Eval은 여러 근거를 한꺼번에 이해해야 하는 QA 데이터셋 11개로 이루어집니다(p.18). 여러 턴 대화를 길게 이어 가는 평가와 멀티턴 학습 데이터의 비율·턴 수는 원문에 나오지 않습니다(원문 미기술).
4. Nemotron: 채팅의 SDG는 Synthetic Data Generation(합성 데이터 생성)의 약자로 보입니다(해석). 채팅에 어느 보고서인지 적혀 있지 않아, 채팅의 'Nemotron의 SDG'가 가리키는 자료는 확인하지 못했습니다. 여기서는 Nemotron-4 340B Technical Report를 확인했습니다.
   - 정렬 데이터의 98% 이상이 합성 데이터입니다.
   - §3.2.1 Prompt Preparation: 선호 데이터에는 2턴 프롬프트를 썼습니다. ShareGPT의 사용자 질문에, 중간 단계 instruct 모델이 만든 답과 다음 사용자 질문을 붙인 형태입니다. 지시 따르기 프롬프트는 IFEval(Zhou et al. 2023)의 검증 가능한(verifiable) 지시 템플릿으로 만들었습니다. 지시가 이후 대화 전체에 적용되는 멀티턴 지시 따르기 프롬프트와, 이전 답을 고치라고 요구하는 두 번째 턴 프롬프트도 따로 만들었습니다.
   - §3.2.2 Synthetic Dialogue Generation: 대화 하나는 3턴입니다. 모델이 assistant와 user 역할을 번갈아 맡고(role-playing), user에게는 성격(persona)을 명시하는 프롬프트를 줍니다. 사용자 턴에서는 공손한 문구를 지워 실제 질문처럼 다듬습니다. Nemotron-4-340B-Reward가 대화 품질에 점수를 매기고, 기준값 미만인 대화는 버립니다.
   - 길이: base 모델의 sequence length는 4,096입니다(Table 1). 정렬 단계의 길이는 확인하지 못했습니다. 해석하면, 이 파이프라인은 '여러 턴'은 다루지만 '긴 context'를 겨냥한 설계로 보기는 어렵습니다.
5. 'Instruction Following with Composable Constraints'라는 제목과 정확히 같은 NeurIPS 2026 워크숍(Workshop on the Linguistic Principles for Foundation Models) 포스터를 찾았습니다. 학회 페이지의 초록에 따르면 다음과 같습니다.
   - 제약을 깊이·너비를 조절한 트리(composable constraint tree)로 표현하고, 트리의 노드마다 결정적 코드로 지켜졌는지 검증합니다.
   - 벤치마크 ComposeIF는 사람이 검증한 깊이 3·4짜리 400개로 구성되고, 가장 강한 모델의 점수는 55.25%입니다.
   - 검증기로 거른 학습 예제 105,161개로 Qwen3-8B를 LoRA(Low-Rank Adaptation)로 한 번 학습하자 ComposeIF +12.75, COLLIE +25.16, IFBench +11.09가 올랐습니다.

   초록에는 멀티턴이나 긴 context에 대한 언급이 없습니다. 본문(OpenReview)은 열지 못해서, 멀티턴을 다루는지는 확인하지 못했습니다. 해석하면, 이 연구는 '한 턴 안에서 제약을 얼마나 깊게 겹치는가'를 다루는 자료로 보입니다.
6. 여러 턴에서 성능이 떨어진다는 것을 보인 연구 중 이번에 확인한 것들입니다.

   | 연구 | 설정 | 결과 |
   |---|---|---|
   | MT-Bench-101 | 대화 1,388개 · 4,208턴, 과제 13개(3단계 분류) | LLM 21개를 평가. 흔한 정렬 기법이나 채팅 전용 설계가 멀티턴 능력을 뚜렷이 높이지 못함 |
   | Multi-IF | IFEval을 3턴 · 8개 언어로 확장, 대화 4,501개 | o1-preview의 전체 언어 평균 정확도가 1턴 0.877 → 3턴 0.707. 턴이 늘수록 모든 모델의 실패가 늘어난다고 보고 |
   | LLMs Get Lost In Multi-Turn Conversation | 시뮬레이션 대화 20만 개 이상, 생성 과제 6개 | 지시를 한 턴에 다 줄 때보다 여러 턴에 나눠 줄 때 평균 39% 하락. 능력(aptitude) 손실은 작고 불안정성(unreliability) 증가가 큼. 대화 중 한 번 잘못 들어서면 회복하지 못함 |

   해석: 2턴 MT-Bench 점수가 좋아도 3턴 이상에서 그대로 유지된다는 보장은 없습니다. "복잡한 제약 + 여러 턴"이라는 질문의 조건을 가장 직접 재는 평가는 Multi-IF입니다.

- 원문: [Qwen2 §1 · p.3](https://arxiv.org/pdf/2407.10671v4#page=3) · [Qwen2 §4.1.1–4.1.2 · p.7](https://arxiv.org/pdf/2407.10671v4#page=7) · [Qwen2 §4.2 · p.8](https://arxiv.org/pdf/2407.10671v4#page=8) · [Qwen2 §5.2.1 · p.12](https://arxiv.org/pdf/2407.10671v4#page=12) · [Qwen2 §5.2.3 · p.15](https://arxiv.org/pdf/2407.10671v4#page=15) · [Qwen2 §5.2.3 NeedleBench · LV-Eval · p.18](https://arxiv.org/pdf/2407.10671v4#page=18) · [MT-Bench (Zheng et al. 2023) §2.2 · §3.5](https://arxiv.org/abs/2306.05685) · [InsTag Table 3](https://arxiv.org/html/2308.07074) · [Tree-Instruct Table 1](https://arxiv.org/abs/2308.05696) · [AlpacaEval 공식 저장소](https://github.com/tatsu-lab/alpaca_eval) · [Nemotron-4 340B §3.2.1–3.2.2](https://arxiv.org/abs/2406.11704) · [Instruction Following with Composable Constraints (NeurIPS 2026 워크숍 페이지)](https://neurips.cc/virtual/2026/164739) · [MT-Bench-101](https://arxiv.org/abs/2402.14762) · [Multi-IF](https://arxiv.org/abs/2410.15553) · [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- 슬라이드: [배경 덱 p.41 · 다양성 · 복잡도의 정의](slides/alignment-background-study.html#s41) · [배경 덱 p.42 · InsTag 실험과 MT-Bench](slides/alignment-background-study.html#s42) · [배경 덱 p.45 · Tree-Instruct 결과](slides/alignment-background-study.html#s45)

## Architecture (MoE)

### Q. MoE를 안정적으로 잘 학습하려면 어떤 방법이 있나? (모임 후속 메모)

**모임에서:** MoE(Mixture-of-Experts) 학습을 안정적으로 잘 하는 방법은 논문들에서 확인해 보자는 후속 메모만 남았습니다. 모임에서 답이 기록되지 않았습니다.

**보충:** 두 가지를 확인했습니다. 첫째는 Qwen2 보고서가 MoE에 대해 밝힌 내용이고, 둘째는 MoE 학습 안정화·부하 균형 기법으로 널리 인용되는 원 논문입니다.

**① Qwen2 보고서가 밝힌 것 (§2.2.2, Table 1)**

- **구조:** Qwen1.5-MoE-A2.7B와 거의 같은 구조입니다. 원래 FFN(Feed-Forward Network) 자리에 expert FFN n개를 둡니다. gate 네트워크 G가 토큰마다 p = softmax(G(x))를 구하고, p가 가장 큰 k개 expert의 출력만 p로 가중합합니다. 식으로는 y = Σ_{i∈topk(p)} p_i·E_i(x)입니다(Eq. 1–2).
- **fine-grained expert:** Mistral-7B에서 Mixtral 8x7B로 갈 때는 expert 하나를 원래 FFN 크기 그대로 두고, 8개 중 2개를 켭니다. Qwen2는 expert를 더 작게 만들고 더 많이 켭니다. 원문은 총 파라미터와 활성 파라미터가 같다면 이쪽이 expert 조합을 더 풍부하게 만든다고 설명합니다.
  - 계산: Qwen2-7B의 FFN 중간 차원 18,944 ÷ expert 중간 차원 2,560 = 7.4입니다. 따라서 expert 하나는 원래 FFN의 약 1/7.4 크기입니다.
  - 계산: 고를 수 있는 조합 수는 Mixtral이 C(8, 2) = 28가지이고, Qwen2의 routed expert는 C(64, 8) = 4,426,165,368 ≈ 4.4×10⁹가지입니다.
- **shared + routed expert:** 모든 토큰이 지나가는 shared expert와 gate가 골라 쓰는 routed expert를 함께 둡니다. 원문은 이 구성의 근거로 DeepSpeed-MoE와 DeepSeekMoE를 인용합니다. Table 1에 따르면 routed expert 64개 중 8개를 켜고, shared expert는 8개입니다. "# Activated Experts 8"에는 shared expert가 포함되지 않습니다.
  - 공개 구현(보고서 밖): Hugging Face의 Qwen2-57B-A14B `config.json`에는 shared expert가 `shared_expert_intermediate_size: 20480`(= 2,560 × 8)짜리 FFN 하나로 들어 있습니다. transformers v4.40.1 코드는 이 출력에 토큰마다 sigmoid(shared_expert_gate(x))를 곱한 뒤 routed 출력에 더합니다. 이 gate는 보고서에 나오지 않습니다(원문 미기술).
- **expert 초기화(upcycling 변형):** 학습을 마친 dense 모델(expert를 골라 쓰지 않고 모든 파라미터를 매번 쓰는 보통 모델)의 가중치에서 시작합니다.
  1. FFN을 ⌈n × h_E / h_FFN⌉벌 복제합니다. 계산: ⌈64 × 2,560 / 18,944⌉ = ⌈163,840 / 18,944⌉ = ⌈8.65⌉ = 9벌
  2. 복제본마다 중간 차원의 순서를 섞습니다(shuffle). 같은 FFN에서 복제한 expert끼리도 서로 달라지게 하려는 것입니다.
  3. expert 크기(2,560칸)로 잘라 64개를 만들고, 남는 칸은 버립니다. 계산: 9 × 18,944 − 163,840 = 170,496 − 163,840 = 6,656칸
  4. expert마다 파라미터의 50%를 무작위로 다시 초기화합니다. 원문은 이 무작위성이 학습 중 탐색 능력을 높일 "가능성(potentially)"이 있다고만 적었습니다.
- **원문 미기술:** load-balancing loss, router z-loss, router 초기화, capacity factor나 token dropping 같은 MoE 전용 학습 설정은 보고서에 없습니다. 50%라는 비율을 고른 근거도 없습니다. 보고서에서 "training stability"라는 말은 dense 모델의 RMSNorm·pre-normalization을 설명하는 §2.2.1에 한 번 나올 뿐입니다.
  - capacity factor: expert 하나가 받을 수 있는 토큰 수의 상한을 (배치의 토큰 수 ÷ expert 수) × capacity factor로 정하는 배수입니다. token dropping: 이 상한을 넘겨 expert로 보내진 토큰은 그 expert의 계산을 건너뛰고 residual 연결로 다음 층에 그대로 넘어갑니다(둘 다 Switch Transformer §2.2).
  - RMSNorm은 기존 layer normalization을 대신하는 정규화이고, pre-normalization은 정규화를 각 층의 앞쪽에 두는 방식입니다. Qwen §2.3은 pre-normalization이 post-normalization보다 학습 안정성이 좋다고 알려져 있고, RMSNorm으로 바꿔도 성능은 같으면서 효율이 좋아졌다고 씁니다.
- **공개 구현 참고:** 같은 `config.json`에는 `router_aux_loss_coef: 0.001`과 `output_router_logits: false`가 들어 있습니다. transformers v4.40.1의 Qwen2-MoE 코드(`Qwen2MoeForCausalLM.forward`)는 `output_router_logits`가 켜지면 load-balancing loss(aux_loss)를 계산하고, label이 주어졌을 때만 `loss += router_aux_loss_coef × aux_loss`로 전체 loss에 더합니다. label이 없으면 aux_loss는 계산해서 돌려주기만 합니다. 코드 주석에 따르면 이 loss는 Switch Transformer의 식 (4)–(6)입니다. 이 값을 실제 사전학습에서도 썼는지는 확인하지 못했습니다.
- **앞선 사례:** Qwen1.5-MoE 공식 블로그에는 초기화에 무작위성을 넣었더니 수렴이 크게 빨라졌다는 내용이 있습니다.

**② 널리 인용되는 기법 (원 논문 확인)**

| 기법 | 원 논문 | 하는 일 | 논문이 쓴 값·결론 |
|---|---|---|---|
| load-balancing 보조 loss | Switch Transformer (Fedus et al., 2021) §2.2 | loss = α · N · Σᵢ fᵢ · Pᵢ. N은 expert 수, fᵢ는 expert i로 보낸 토큰의 비율, Pᵢ는 expert i에 배정된 router 확률의 비율입니다. 토큰이 한 expert로 몰릴수록 값이 커져 벌점이 됩니다 | α = 10⁻² |
| 선택적 정밀도·작은 초기화 | Switch Transformer §2.4 | bfloat16 같은 낮은 정밀도는 router의 softmax 계산 문제를 키울 수 있습니다. 그래서 router 입력만 float32로 바꾸고, float32는 router 함수 안에서만 씁니다. 초기화 scale은 기본값 s = 1.0을 10분의 1로 줄입니다 | Table 2: bfloat16만 쓴 모델은 발산했습니다. 선택적 정밀도는 float32와 같은 품질(−1.716 vs −1.718)을 bfloat16 수준의 속도로 냈습니다 |
| router z-loss | ST-MoE (Zoph et al., 2022) §3.3 | L_z = (1/B) · Σᵢ (log Σⱼ e^{xⱼ⁽ⁱ⁾})². B는 토큰 수, j는 expert N개에 걸친 합, x는 router로 들어가는 logit입니다. logit이 커지지 못하게 벌점을 줍니다 | c_z = 0.001(hyperparameter sweep으로 고름). 같은 논문에서 곱셈 상호작용 제거, 노이즈 주입(input jitter·dropout), update clipping 강화는 안정성은 올렸지만 품질을 떨어뜨렸습니다(Table 2–4). z-loss는 품질 손해 없이 안정성을 높였다고 보고합니다(Table 4: −1.741 vs 기준 −1.755). 시험한 기법 가운데 품질을 지킨 것은 z-loss뿐입니다(해석: Table 2–4 비교) |
| auxiliary-loss-free balancing | Wang et al., 2024 (arXiv 2408.15664) | top-K를 고르기 전에 routing 점수에 expert별 bias를 더하고, 각 expert의 최근 부하를 보고 bias를 조정합니다. 보조 loss를 크게 줄 때 생기는 간섭 gradient(interference gradients)를 피하려는 방법입니다 | 최대 3B 파라미터·200B 토큰 실험에서 보조 loss 방식보다 성능과 부하 균형이 모두 좋았다고 보고합니다 |
| global-batch LBL(Load-Balancing Loss) | Qiu et al., 2025 (arXiv 2501.11873) | 기존 프레임워크는 LBL을 micro-batch마다 계산합니다. micro-batch에는 시퀀스가 몇 개 없어서 사실상 시퀀스 단위로 균형을 강요하게 되고, 이것이 expert의 전문화를 막습니다. 이 논문은 LBL을 global batch 단위로 계산합니다 | 최대 42.8B 파라미터·400B 토큰 실험에서 사전학습 perplexity와 하류 과제 성능이 함께 좋아지고, expert 전문화도 뚜렷해졌다고 보고합니다. 저자 일부가 Qwen2 보고서 저자 목록에도 있지만, Qwen2(arXiv 2407)보다 나중에 나온 논문이라 Qwen2가 이 방식을 썼다는 근거는 되지 않습니다 |

Switch Transformer와 ST-MoE는 ar5iv HTML 본문을, 나머지 두 편은 arXiv 초록 페이지를 요약 도구로 읽었습니다. PDF와 한 줄씩 대조하지는 못했습니다.

해석: 표의 기법은 겨냥하는 문제가 둘로 나뉩니다.

- 수치 불안정(loss 발산): 선택적 정밀도, 작은 초기화, z-loss
- 부하 불균형(토큰이 일부 expert로 몰림): load-balancing loss, auxiliary-loss-free, global-batch LBL

Qwen2 보고서만으로는 이 가운데 무엇을 어떻게 조합했는지 알 수 없습니다. 공개 config에서 확인되는 것은 load-balancing loss 계수뿐입니다.

- 원문: [Qwen2 §2.2.1–2.2.2 · p.4](https://arxiv.org/pdf/2407.10671v4#page=4) · [Qwen2 Table 1 · Expert Initialization · p.5](https://arxiv.org/pdf/2407.10671v4#page=5) · [Qwen §2.3 · p.7](https://arxiv.org/pdf/2309.16609v1#page=7) · [Switch Transformer §2.2 · §2.4 (arXiv 2101.03961)](https://arxiv.org/abs/2101.03961) · [ST-MoE §3.3 (arXiv 2202.08906)](https://arxiv.org/abs/2202.08906) · [Auxiliary-Loss-Free Load Balancing (arXiv 2408.15664)](https://arxiv.org/abs/2408.15664) · [Demons in the Detail: global-batch LBL (arXiv 2501.11873)](https://arxiv.org/abs/2501.11873) · [Qwen1.5-MoE 공식 블로그](https://qwenlm.github.io/blog/qwen-moe/) · [Qwen2-57B-A14B config.json (Hugging Face)](https://huggingface.co/Qwen/Qwen2-57B-A14B/blob/main/config.json) · [transformers v4.40.1 modeling_qwen2_moe.py](https://github.com/huggingface/transformers/blob/v4.40.1/src/transformers/models/qwen2_moe/modeling_qwen2_moe.py)
- 슬라이드: [Architecture 덱 p.18 · MoE Eq. (1)–(2)](slides/qwen-architecture-deck.html#s18) · [Architecture 덱 p.19 · fine-grained expert](slides/qwen-architecture-deck.html#s19) · [Architecture 덱 p.20 · shared · routed expert](slides/qwen-architecture-deck.html#s20) · [Architecture 덱 p.21 · upcycling](slides/qwen-architecture-deck.html#s21) · [배경 덱 p.33 · MoE upcycling 원전과 Qwen2](slides/alignment-background-study.html#s33)

### Q. MoE를 왜 7B에서 확장했을까?

**모임에서:** Qwen2의 MoE 모델을 왜 7B 모델에서 확장했는지 묻는 질문이 나왔습니다. 모임에서 답이 기록되지 않았습니다.

**보충:**

- **원문이 밝힌 것:**
  - §2.2.3: "Qwen2-57B-A14B is upscaled from Qwen2-7B."
  - Expert Initialization: dense 모델의 가중치로 expert를 초기화합니다.
  - §3.1: MoE 모델은 upcycling 원칙에 따라 4.5T 토큰을 추가로 사전학습했습니다.
  - Table 1: Qwen2-7B는 7T 토큰으로 학습했습니다.
  - 따라서 MoE는 4.5T로 처음부터 학습한 모델이 아닙니다. 7T로 학습한 7B에서 출발해 4.5T를 더 학습한 모델입니다.
- **Table 1에서 같은 것과 다른 것:** MoE의 hidden size 3,584, 층 수 28, query head 28, KV(Key-Value) head 4, head size 128은 모두 7B와 같습니다. 다른 것은 FFN입니다. 7B는 중간 차원 18,944인 FFN 하나를 쓰고, MoE는 2,560짜리 routed expert 64개와 shared expert 8개를 씁니다.
- **목표:** Table 3 캡션에 따르면 57B-A14B는 30B급 dense 모델의 성능에 맞추도록 설계되었습니다.
  - §5.2.2 본문(p.14)은 사내 중국어 평가에서 MoE가 대부분 영역에서 Qwen1.5-32B-Chat보다 좋았지만 지식 이해(knowledge understanding)는 예외였다고 씁니다. 저자는 이 차이가 사전학습 토큰이 부족했기 때문일 수 있다고 보고, 사전학습을 이어갈 계획이라고 적었습니다.
  - Table 10(p.16)의 값을 보면 지식(Knowledge 64.15 vs 68.63) 외에 추론(Reasoning 59.89 vs 62.87)도 Qwen1.5-32B-Chat보다 낮습니다. 나머지는 높습니다: 시험(Exam) 73.67 vs 67.59, 이해(Comprehension) 67.52 vs 64.67, 코딩(Coding) 40.66 vs 35.28, 수학(Math) 63.90 vs 60.62, 평균 61.63 vs 59.94.
- **왜 하필 7B를 골랐는지는 원문 미기술입니다.**
- **질문을 '왜 처음부터 학습하지 않고 dense 모델에서 확장했나'로 읽는 경우:** Qwen2 보고서는 "upcycling 원칙에 따라"라고만 적었습니다. 같은 팀의 Qwen1.5-MoE 공식 블로그에는 이유가 나옵니다. 이 블로그는 Qwen-1.8B를 Qwen1.5-MoE-A2.7B로 바꿔 만든 과정을 다룹니다.
  - MoE를 처음부터 학습해 최고 성능에 이르는 것은 비효율적이고 어려울 수 있다.
  - upcycling을 하면 원래 모델만큼의 토큰을 다시 학습할 필요가 없다.
  - Qwen1.5-7B보다 학습 비용이 75% 줄었다.

계산: '총 57B · 활성 14B'가 어떻게 나오는지 확인했습니다. 가정은 다음과 같습니다. SwiGLU(Swish와 Gated Linear Unit을 합친 활성화 함수, Qwen §2.3)를 쓰는 FFN은 행렬 3개(gate·up·down)로 셉니다. 어휘 수는 Table 1의 151,646을 씁니다. config의 `vocab_size` 151,936을 써도 반올림하면 같습니다. bias·norm·router(3,584 × 64 × 28 ≈ 6.4M)는 작아서 뺐습니다.

| 부분 | 계산 | 값 |
|---|---|---|
| embedding (입력·출력을 따로 둠, tying 없음) | 2 × 151,646 × 3,584 | 약 1.09B |
| attention (Q·O는 3,584×3,584, K·V는 3,584×(4×128 = 512)) | 층마다 3,584×3,584×2 + 3,584×512×2 = 29.36M, × 28층 | 약 0.82B |
| expert 하나 | 3 × 3,584 × 2,560 | 약 27.5M |
| shared expert (중간 차원 20,480) | 3 × 3,584 × 20,480 = 220.2M, × 28층 | 약 6.17B |
| routed 64개 전체 | 64 × 27.5M × 28층 | 약 49.33B |
| routed 활성 8개 | 8 × 27.5M × 28층 | 약 6.17B |
| **총** | 1.09 + 0.82 + 6.17 + 49.33 | **약 57.4B** |
| **활성** | 1.09 + 0.82 + 6.17 + 6.17 | **약 14.2B** |

계산 결과가 이름의 57B-A14B와 맞습니다.

해석(저자 설명이 아님):

- upcycling은 FFN 밖의 가중치(embedding, attention, norm)를 출발 dense 모델에서 그대로 가져옵니다. 그래서 출발 모델이 MoE의 폭과 층 수를 정합니다.
- 7B에서 출발하면 FFN 밖 부분은 약 1.91B(1.09 + 0.82)입니다. 층마다 켜지는 FFN은 shared 220.2M + 활성 routed 220.2M = 440.4M이고, 이는 7B의 층당 FFN(3 × 3,584 × 18,944 = 203.7M)의 약 2.16배입니다.
- 같은 방식으로 72B에서 출발한다고 가정해 보겠습니다. Table 1의 hidden 8,192, 80층, query head 64, KV head 8을 쓰면 다음과 같습니다.
  - attention: 층마다 8,192×8,192×2 + 8,192×1,024×2 = 151.0M, × 80층 ≈ 12.08B
  - embedding: 2 × 151,646 × 8,192 ≈ 2.48B
  - 합: FFN을 하나도 켜지 않아도 약 14.6B
  - 그러면 '활성 14B로 30B급 dense 성능'이라는 목표와 맞지 않습니다.
- 정리하면 '작은 dense 모델에서 출발해 더 큰 dense 모델 수준의 MoE를 만든다'는 방향입니다. Qwen1.5-MoE가 1.8B에서 출발한 것과 같은 흐름으로 볼 수 있습니다.

- 원문: [Qwen2 Table 1 · §2.2.3 · p.5](https://arxiv.org/pdf/2407.10671v4#page=5) · [Qwen §2.3 · p.7](https://arxiv.org/pdf/2309.16609v1#page=7) · [Qwen2 §3.1 · p.6](https://arxiv.org/pdf/2407.10671v4#page=6) · [Qwen2 Table 3 · p.10](https://arxiv.org/pdf/2407.10671v4#page=10) · [Qwen2 §5.2.2 · p.14](https://arxiv.org/pdf/2407.10671v4#page=14) · [Qwen2 Table 10 · p.16](https://arxiv.org/pdf/2407.10671v4#page=16) · [Qwen2-57B-A14B config.json (Hugging Face)](https://huggingface.co/Qwen/Qwen2-57B-A14B/blob/main/config.json) · [Qwen1.5-MoE 공식 블로그](https://qwenlm.github.io/blog/qwen-moe/)
- 슬라이드: [Architecture 덱 p.21 · upcycling](slides/qwen-architecture-deck.html#s21) · [Architecture 덱 p.22 · Qwen2 Table 1](slides/qwen-architecture-deck.html#s22) · [Architecture 덱 p.25 · Qwen2 Table 3 (MoE)](slides/qwen-architecture-deck.html#s25) · [배경 덱 p.34 · MoE는 +4.5T](slides/alignment-background-study.html#s34)

## Alignment & RL

### Q. 일반성을 높이려고 StackExchange · Reddit을 썼다는데, '일반성이 높아졌다'는 것은 어떻게 측정했나?

**모임에서:** 발표에서 일반성을 높이려고 StackExchange·Reddit 데이터를 썼다는 설명이 있었습니다. 이를 두고 '일반성을 높인다'는 것을 어떻게 측정했는지 묻는 질문이 나왔습니다. 모임에서 답이 기록되지 않았습니다.

**보충:**

1. **전제 확인:** StackExchange·Reddit 데이터는 Qwen 보고서가 아니라 PMP(Preference Model Pretraining)의 원전인 Askell et al. 2021에 나옵니다. 배경 덱 p.52도 출처를 Askell 2021로 적었습니다.
   - Qwen §3.2.1의 설명: RM(Reward Model)도 LLM처럼 사전학습(PMP)을 먼저 하고 finetune을 합니다. PMP에는 대량의 비교 데이터(질문 하나에 서로 다른 응답 두 개와 선호 표시)가 필요하다고만 적었습니다.
   - Qwen이 PMP 데이터로 무엇을 얼마나 썼는지는 원문 미기술입니다. Qwen 본문에서 StackExchange나 Reddit이라는 말은 PMP 설명에 나오지 않습니다. 그래서 Qwen이 실제로 StackExchange·Reddit을 썼는지는 확인할 수 없습니다.
   - Qwen이 PMP에 붙인 인용은 Askell 2021이 아니라 Bai et al. 2022b(arXiv 2204.05862)입니다. 이 논문의 제목은 *Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback*이고, 여기서 RLHF는 Reinforcement Learning from Human Feedback(사람 피드백 기반 강화학습)의 약자입니다.
2. **원전(Askell 2021, App. C.1)의 PMP 데이터:**
   - StackExchange: 학습 쌍 5.8M, 테스트 쌍 59k. 답마다 log₂(1 + 추천 수)를 반올림한 값을 점수로 주고, 질문자가 채택한 답이면 1을 더합니다. 점수가 다른 두 답을 뽑아 한 쌍을 만듭니다.
   - Reddit: 학습 쌍 1.1M, 테스트 쌍 11k. 마지막 댓글만 다른 두 댓글 줄기를 뽑고, 마지막 댓글의 추천이 많은 쪽을 좋은 쪽으로 봅니다.
   - Wikipedia: 학습 쌍 1.4M, 테스트 쌍 14k. "vandalism 의심"으로 되돌린 편집에서 되돌린 쪽을 좋은 쪽으로 봅니다. 배경 덱 p.52는 Wikipedia 규모를 "—"로 비워 두었는데, 이 값으로 채울 수 있습니다.
   - 위 수치와 규칙은 Askell 2021 PDF(arXiv v3) App. C.1(p.34–36)에서 확인했습니다.
3. **원전이 잰 것(§4.2):** PMP를 한 모델과 하지 않은 모델을 같은 데이터로 finetune한 뒤 정확도를 비교했고, finetune 데이터의 양을 바꿔 가며 쟀습니다. finetune 데이터는 Learn to Summarize, HellaSwag, 그리고 Ethics 5종(Commonsense Morality · Deontology · Justice · Utilitarianism · Virtue)으로, 모두 7개입니다.
   - 52B 모델에서 PMP를 했을 때와 안 했을 때의 정확도 차이를 finetune 쌍 수에 따라 보인 그림은 Figure 4(p.7)입니다. 배경 덱 p.52가 든 그림도 이 Figure 4입니다.
   - 모델 크기별 결과는 Figure 16(p.21)입니다. finetune 시퀀스 1k개(500쌍)일 때, Mix 데이터로 PMP를 하면 약 1B보다 큰 모델에서 성능이 크게 좋아졌고, 작은 모델에는 도움이 되지 않는 것으로 보였습니다.
   - 원전은 PMP 데이터와 finetune 데이터의 분포가 비슷하지 않은 경우가 많은데도 sample efficiency가 좋아졌다고 적었습니다.
   - 해석: 원전이 잰 것은 막연한 '일반성'이라기보다, 사람 선호 데이터가 적을 때 PMP가 얼마나 도움이 되는가(sample efficiency, 전이)입니다.
4. **Qwen이 잰 것(Table 4):** test pairwise accuracy, 즉 사람이 좋다고 표시한 답에 모델이 더 높은 점수를 준 쌍의 비율입니다. 7개 세트에서 쟀습니다.
   - Qwen 사내 세트 2개: Helpful-base(RLHF 전 Qwen의 응답), Helpful-online(RLHF 후 Qwen의 응답)
   - 외부 공개 세트 5개: Anthropic Helpful-base·Helpful-online, OpenAI Summ., Stanford SHP(Stanford Human Preferences Dataset), OpenAI PRM800K
   - 저자의 결론: "PMP 모델이 분포 밖(out-of-distribution) 데이터에서 높은 일반화 능력을 보인다." 따라서 Qwen이 말하는 '일반성'은 외부 세트 5개의 정확도로 판단한 것입니다.
   - 저자는 test 정확도가 "중요하지만 유일하지는 않은" 지표라고 적었습니다. 다른 지표가 무엇인지는 원문 미기술입니다.
5. **SHP와 Reddit:** 외부 세트 중 Stanford SHP는 Reddit 글과 댓글로 만든 데이터입니다. 18개 주제에 걸친 선호 385K개이고, 나중에 쓰였는데도 점수가 더 높은 댓글을 더 선호된 쪽으로 봅니다(Hugging Face 데이터셋 카드).
   - 해석: Qwen의 PMP 데이터에 Reddit이 들어 있었다면 SHP는 완전한 '분포 밖'이 아닐 수 있습니다. 하지만 PMP 데이터 출처가 원문 미기술이라 판단할 수 없습니다.
6. **해석:** Qwen Table 4에는 PMP를 거치지 않은 RM이 없습니다. 그래서 'PMP가 일반성을 높였다'는 비교 근거는 이 표에 없습니다. 표가 보여 주는 것은 두 가지입니다.
   - PMP 모델 자체가 외부 세트에서 내는 정확도
   - finetune한 뒤에도 그 수준이 거의 유지된다는 점(다음 항목)
   - PMP를 한 경우와 하지 않은 경우를 직접 비교한 실험은 Askell 2021에 있습니다.

- 원문: [Qwen §3.2.1 · p.10](https://arxiv.org/pdf/2309.16609v1#page=10) · [Qwen Table 4 · p.11](https://arxiv.org/pdf/2309.16609v1#page=11) · [Qwen 참고문헌 (Bai et al. 2022b) · p.23](https://arxiv.org/pdf/2309.16609v1#page=23) · [Askell et al. 2021 (arXiv 2112.00861)](https://arxiv.org/abs/2112.00861) · [같은 논문 Figure 4 · p.7](https://arxiv.org/pdf/2112.00861v3#page=7) · [§4.2 · Figure 16 · p.21](https://arxiv.org/pdf/2112.00861v3#page=21) · [App. C.1 · p.34](https://arxiv.org/pdf/2112.00861v3#page=34) · [Stanford SHP 데이터셋 카드 (Hugging Face)](https://huggingface.co/datasets/stanfordnlp/SHP)
- 슬라이드: [배경 덱 p.51 · RM 전에 PMP](slides/alignment-background-study.html#s51) · [배경 덱 p.52 · PMP 데이터 (Askell 2021)](slides/alignment-background-study.html#s52) · [배경 덱 p.56 · Table 4 읽는 법](slides/alignment-background-study.html#s56)

### Q. 학습(Training) 뒤 자기 데이터에서는 크게 오르고 남의 데이터에서는 적게 변한 결과를 어떻게 봐야 하나?

**모임에서:** Training(학습)으로 좀 더 나아진 부분도 있겠지만, 자기 데이터에서는 크게 오르고 남의 데이터에서는 변동이 적은 결과를 어떻게 보느냐는 질문이 나왔습니다. 모임에서 답이 기록되지 않았습니다.

**보충:** 앞 질문과 같은 흐름이라, 이 질문은 Qwen Table 4(PMP 모델 대 finetune한 RM)를 가리키는 것으로 보입니다(해석). Table 4의 값을 원문 그대로 옮기고 차이를 계산했습니다. 단위는 %입니다.

| 테스트 세트 | 구분 | PMP | RM | RM − PMP (계산) |
|---|---|---|---|---|
| Qwen Helpful-base | 자기 | 62.68 | 74.78 | +12.10 |
| Qwen Helpful-online | 자기 | 61.62 | 69.71 | +8.09 |
| Anthropic Helpful-base | 외부 | 76.52 | 73.98 | −2.54 |
| Anthropic Helpful-online | 외부 | 65.43 | 64.57 | −0.86 |
| OpenAI Summ. | 외부 | 69.60 | 69.99 | +0.39 |
| Stanford SHP | 외부 | 60.05 | 60.10 | +0.05 |
| OpenAI PRM800K | 외부 | 70.59 | 70.52 | −0.07 |

계산(평균):

- 자기 세트 2개: PMP (62.68 + 61.62) / 2 = 124.30 / 2 = 62.15, RM (74.78 + 69.71) / 2 = 144.49 / 2 = 72.245 → 약 +10.1
- 외부 세트 5개: PMP 342.19 / 5 = 68.438, RM 339.16 / 5 = 67.832 → 약 −0.6

원문의 결론은 "PMP 모델은 분포 밖 데이터에서 일반화가 높고, RM은 Qwen 보상 데이터에서 크게 좋아진다"입니다.

해석:

- RM finetune 데이터는 크기와 sampling 전략을 달리한 여러 Qwen 모델의 응답입니다. 이 응답을 Qwen의 주석 가이드라인에 따라 사람이 평가했습니다(§3.2.1). Qwen Helpful-base 테스트도 'RLHF 전 Qwen의 응답'이라 finetune 데이터와 분포가 가깝습니다. 그러니 이 세트에서 크게 오른 것은 분포 안으로 적응한 결과로, 예상할 수 있는 일입니다.
- 외부 세트의 변동은 −2.54 ~ +0.39입니다. finetune이 외부 세트 실력을 올리지도 크게 깎지도 않았다고 읽을 수 있습니다. 다만 Anthropic Helpful-base에서 2.54 떨어진 것이 가장 큰 하락입니다.
- PPO(Proximal Policy Optimization) 단계에서 RM이 채점하는 대상은 Qwen 정책 모델 자신의 응답입니다. 그래서 실제로 쓰일 때는 자기 분포에서의 정확도가 더 직접적으로 중요합니다.
- 테스트 세트 크기, 신뢰구간, 반복 실행 여부는 원문 미기술입니다. 그래서 ±0.4 수준의 차이가 의미 있는 변화인지는 판단할 수 없습니다. Helpful-online의 상승 폭(+8.09)이 Helpful-base(+12.10)보다 작은 이유도 원문 미기술입니다.

- 원문: [Qwen §3.2.1 · p.10](https://arxiv.org/pdf/2309.16609v1#page=10) · [Qwen Table 4 · p.11](https://arxiv.org/pdf/2309.16609v1#page=11)
- 슬라이드: [배경 덱 p.56 · Table 4 읽는 법](slides/alignment-background-study.html#s56) · [배경 덱 p.57 · Table 4 결과](slides/alignment-background-study.html#s57)

### Q. Online 기법과 Offline 기법은 무엇이 다른가?

**모임에서:** "Online 기법 vs Offline 기법"이라는 질문만 기록되어 있고, 무엇을 가리키는지는 채팅만으로 분명하지 않습니다. 모임에서 답이 기록되지 않았습니다.

**보충:** 해석: 이 질문은 Qwen2 §4.3의 offline·online DPO(Direct Preference Optimization)를 가리키거나, 같은 절에 나오는 Online Merging Optimizer를 가리키는 것으로 보입니다. 아래에서 둘 다 확인합니다. Qwen2 §4.3은 RLHF를 offline 학습과 online 학습의 두 단계로 차례로 진행합니다.

| | offline 단계 | online 단계 |
|---|---|---|
| 학습 쌍의 출처 | 미리 만들어 둔 선호 데이터 P = {(x, y⁺, y⁻)} | 현재 정책 모델에서 응답을 여러 개 샘플 |
| 좋은 쪽·나쁜 쪽을 정하는 주체 | 데이터를 만들 때 정해짐: 사람 주석(순위 매기기)과 자동 합성(rejection sampling의 맞은·틀린 풀이, 코드 실행 피드백, constitutional feedback 등, §4.1) | RM이 가장 선호하는 응답과 가장 덜 선호하는 응답을 고름 |
| 학습 방법 | DPO로 y⁺와 y⁻의 likelihood 차이를 키움 | 고른 쌍으로 episode마다 DPO |

- **Online Merging Optimizer:** §4.3의 마지막 문장에 나옵니다. alignment tax, 즉 생성을 사람 선호에 맞추는 과정에서 원래 성능이 떨어지는 현상을 줄이려고 썼다고 합니다. 원 논문(Lu et al. 2024)의 저자 6명은 모두 Qwen2 보고서 저자 목록에도 있습니다. 원 논문의 내용은 다음 순서입니다.
  1. RLHF 모델과 SFT 모델의 파라미터를 보간하면 선호와 기본 능력 사이의 균형을 조절할 수 있다는 것을 먼저 확인했습니다. 이렇게 하면 alignment tax는 줄지만 alignment reward도 함께 떨어집니다.
  2. 그래서 학습이 끝난 뒤 한 번 섞지 않고, RLHF의 optimization step마다 섞습니다. 매 step의 gradient를 'SFT 모델 − 사전학습 모델'의 파라미터 차이와 합칩니다.
  3. Qwen·LLaMA 계열 1.8B–8B 모델과 DPO·KTO(Kahneman-Tversky Optimization: 응답 쌍 대신 '바람직한가'라는 이진 신호로 학습하는 방법) 등에서 실험했습니다. 14개 벤치마크에서 alignment reward는 오르고 alignment tax는 줄었다고 보고합니다.
- 해석: §4.3의 'online'은 두 가지 뜻으로 쓰입니다. online DPO의 'online'은 학습 데이터를 현재 정책에서 새로 만든다는 뜻입니다. Online Merging의 'online'은 optimizer step마다 섞는다는 뜻입니다.
- **online이 필요한 이유(외부 근거):** OAIF(Online AI Feedback) 논문 §2의 설명은 다음과 같습니다. offline 방식에서는 정책이 학습 중에 자기 생성물에 대한 피드백을 받지 못합니다. 데이터의 분포는 고정되어 있는데 정책은 계속 바뀌므로 학습이 off-policy가 됩니다. off-policy는 지금 학습 중인 정책이 아닌 다른 정책이 만든 데이터로 학습하는 것이고, 지금 학습 중인 정책이 만든 데이터로 학습하는 것은 on-policy입니다(OAIF App. A.2).
- **원문 미기술:** Qwen2가 online 단계를 둔 이유, RM 학습 방법, β(DPO에서 기준 정책, 보통 SFT 모델에서 얼마나 멀어질지 조절하는 계수. DPO 논문 §3)·샘플 수·episode 수, Online Merging을 두 단계 중 어디에 적용했는지는 모두 원문에 없습니다.

- 원문: [Qwen2 §4.1 · p.6](https://arxiv.org/pdf/2407.10671v4#page=6) · [Qwen2 §4.1.2 · p.7](https://arxiv.org/pdf/2407.10671v4#page=7) · [Qwen2 §4.3 · p.8](https://arxiv.org/pdf/2407.10671v4#page=8) · [Online Merging Optimizers (arXiv 2405.17931)](https://arxiv.org/abs/2405.17931) · [OAIF §2 · App. A.2 (arXiv 2402.04792)](https://arxiv.org/html/2402.04792v2) · [DPO §3 (arXiv 2305.18290)](https://arxiv.org/html/2305.18290v3) · [KTO (arXiv 2402.01306)](https://arxiv.org/abs/2402.01306)
- 슬라이드: [배경 덱 p.64 · offline → online DPO](slides/alignment-background-study.html#s64) · [배경 덱 p.68 · Online Merging](slides/alignment-background-study.html#s68) · [배경 덱 p.75 · 두 가지 'Online'](slides/alignment-background-study.html#s75)

### Q. Online DPO에서 Reward 모델은 고정인가, 정책과 같이 업데이트하나?

**모임에서:** Online DPO에서 reward 모델을 고정하는지, 정책과 함께 업데이트하는지 묻는 질문이 나왔습니다. 모임 중에는 답이 기록되지 않았습니다. 모임 뒤에 조사 결과가 추가로 공유되었습니다. 업데이트하지 않는 것이 일반적이지만, 정책 모델이 계속 업데이트되면서 RM을 해킹할 수 있어서 RM도 주기적으로 함께 업데이트하는 방식이 있다는 내용입니다. 함께 공유된 표의 행은 다음과 같습니다.

| 연구 | 정책 학습 | RM 업데이트 | 새 정답 신호 |
|---|---|---|---|
| OAIF (2024) | Online DPO | 없음 | 고정된 LLM Judge |
| D2PO (COLM 2024) | Online DPO | 주기적 | 새로운 Human/Gold Preference |
| Mutual-Taught (ACL 2025) | Iterative DPO | 주기적 | Policy 전후 비교 기반 Pseudo-label |

채팅 기록에는 표의 제목과 열 이름이 없어, 열 이름은 정리하면서 붙였습니다.

**보충:** 세 논문을 원문으로 열어 다시 확인했습니다. 공유된 표는 큰 줄기에서 원문과 맞고, 두 칸은 아래 '표를 읽을 때 주의할 점'처럼 읽는 것이 더 정확합니다. 칸마다 원문에서 확인한 내용으로 다시 쓰면 다음과 같습니다.

| 연구 (확인한 서지) | 정책 학습 | RM·judge 업데이트 | 새 선호 신호의 출처 |
|---|---|---|---|
| OAIF: Guo et al., *Direct Language Model Alignment from Online AI Feedback*, arXiv 2402.04792 (2024년 2월). arXiv 페이지에 학회 표기가 없어 정식 출판 학회는 확인하지 못했습니다 | 현재 모델에서 응답 두 개를 샘플해 online으로 학습. DPO·IPO(identity policy optimisation)·SLiC(sequence likelihood calibration) 세 방법에 모두 적용 | RM 없음. LLM annotator(주 실험은 PaLM 2-L)를 prompting으로만 씀. annotator를 학습시킨다는 설명은 없음 | 매 iteration마다 LLM annotator가 두 응답 중 선호하는 쪽을 고름 |
| D2PO: Singhal et al., *D2PO: Discriminator-Guided DPO with Response Evaluation Models*, arXiv 2405.01511. arXiv comments에 "Accepted to COLM 2024" | DPO. gold label 쌍과, discriminator가 붙인 silver label 쌍으로 학습 | 주기적. 정해진 step 간격마다 gold 주석을 새로 모아 discriminator(기본은 Bradley-Terry RM. Bradley-Terry 모델은 두 응답의 보상 r₁, r₂로 응답 1이 선호될 확률을 exp(r₁) ÷ (exp(r₁) + exp(r₂))로 둡니다. DPO 논문 Eq. 1)를 업데이트(간격의 구체적 값은 확인하지 못했습니다). gold를 받을 쌍은 discriminator 점수 차가 가장 작은 쌍으로 고르고, 무작위로 골라도 대부분 비슷했다고 보고 | 논문의 정의로 gold는 "보통 사람 또는 LLM-as-a-judge". 실험에서는 GPT-4 기반 UltraFeedback 점수(1–5), 명시적으로 정의한 gold reward 함수(합성 과제), EurusRM을 gold로 씀 |
| Mutual-Taught: Shi et al., *Mutual-Taught for Co-adapting Policy and Reward Models*, ACL 2025 Long, pp. 16285–16298 | EM(Expectation-Maximization) 방식의 E-step. 이전 정책으로 on-policy 샘플한 응답을 현재 RM이 순위 매기고, 그 쌍으로 iterative DPO | M-step에서 RM을 다시 학습. 본 실험은 한 round에 정책 2회, RM 1회 업데이트. RM은 이어서 학습하지 않고 매번 base RM에서 다시 시작 | 업데이트된 정책의 응답 y_t를 이전 정책의 응답 y_{t−1}보다 선호한다고 두는 pseudo-label. 이전 RM의 점수 차 Δr = r_{t−1}(y_t) − r_{t−1}(y_{t−1})가 −ε_t 이하인 쌍은 버림(ε_t = 학습 프롬프트 전체에 걸친 r_{t−1}(y_{t−1}) 점수의 표준편차. iteration마다 값 하나, §4.3). 추가 사람 주석은 없지만, 사전학습된 RM(FsfairX)과 UltraFeedback 프롬프트는 씀 |

- **'업데이트하지 않는 것이 일반적'에 대해:** OAIF §4.4에 "RLAIF(RL from AI Feedback)·RLHF에서 쓰는 RM은 정책 학습 중에 업데이트되지 않는 경우가 많다"는 문장이 있습니다. 같은 곳에서 정책의 출력 분포가 바뀌면 RM의 평가 능력이 일반화되지 않을 수 있다고 덧붙입니다. 모임 뒤 조사 내용과 맞습니다.
- **'RM 해킹'에 대해:** Mutual-Taught §1은 정책의 출력이 RM의 학습 데이터 분포에서 멀어지는 것을 reward hacking으로 이어지는 현상으로 설명합니다. D2PO가 밝힌 동기는 학습 중 정책 분포가 바뀌는 문제(예: 응답이 길어짐)입니다. D2PO의 서론과 §3에는 reward hacking이라는 말이 나오지 않습니다.
- **표를 읽을 때 주의할 점:**
  - OAIF의 "고정된 LLM Judge"는 'annotator를 학습시키지 않고 prompting으로만 쓴다'로 읽는 것이 정확합니다. 원문에서 가중치를 고정(freeze)한다는 직접 표현은 확인하지 못했습니다.
  - D2PO의 "Human/Gold"는 논문 정의로는 사람 또는 LLM judge입니다. 실제 실험의 gold는 GPT-4 점수와 정의된 reward 함수였습니다.
- **Qwen2의 경우:** §4.3은 online 단계에서 "reward models"로 즉각 피드백을 받고, RM이 가장 선호하는 응답과 가장 덜 선호하는 응답을 고른다고만 적었습니다. 보고서에서 reward model이 나오는 곳은 이 절뿐입니다. RM을 어떻게 학습했는지, online 단계에서 RM을 고정했는지 업데이트했는지는 원문 미기술입니다.

- 원문: [Qwen2 §4.3 · p.8](https://arxiv.org/pdf/2407.10671v4#page=8) · [OAIF §2 · §4.4 (arXiv 2402.04792)](https://arxiv.org/html/2402.04792v2) · [D2PO §3 · §4.1 (arXiv 2405.01511)](https://arxiv.org/html/2405.01511v2) · [Mutual-Taught (ACL Anthology)](https://aclanthology.org/2025.acl-long.794/) · [Mutual-Taught §1 · §4 · App. B (arXiv 2506.06292)](https://arxiv.org/html/2506.06292v2) · [DPO Eq. 1 (arXiv 2305.18290)](https://arxiv.org/html/2305.18290v3)
- 슬라이드: [배경 덱 p.64 · offline → online DPO](slides/alignment-background-study.html#s64) · [배경 덱 p.75 · 두 가지 'Online'](slides/alignment-background-study.html#s75)

## 후속으로 볼 것

- [ ] 한국어 모델 논문을 읽을 때 형태소 분석을 썼는지, 자모 단위를 고려했는지 확인하기
- [ ] 멀티턴·긴 context 환경에서 복잡도·제약 기반 합성 데이터가 효과가 있는지 Nemotron의 SDG와 'Instruction Following with Composable Constraints' 자료로 살펴보기
- [ ] MoE를 안정적으로 학습하는 방법(load-balancing 보조 loss, router z-loss, auxiliary-loss-free balancing 등)을 논문들에서 확인하기: 이 문서의 보충에 1차 정리를 넣었으니, 앞으로 다른 MoE 보고서를 읽을 때 어떤 기법을 썼는지 함께 확인
- [ ] Online DPO에서 RM을 고정하는지, 주기적으로 업데이트하는지 조사하기: 모임 뒤 1차 조사(OAIF · D2PO · Mutual-Taught)가 공유되었고, 세 논문의 원문 대조 결과를 이 문서에 반영함
