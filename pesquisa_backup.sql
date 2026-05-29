--
-- PostgreSQL database dump
--

\restrict lF9LL2ocqLvE4d19IHvgnaiEImerp84vHO4LuW2bLop2q93NhzwHYWar31qujpy

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: pesquisa_foto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pesquisa_foto (foto_id, pesquisa_id, foto_data, nome_arquivo, descricao, data_upload, foto_path, legenda, ativo) FROM stdin;
1	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818514_0_WhatsApp Image 2026-04-18 at 16.59.13.jpeg	\N	1
2	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818523_1_WhatsApp Image 2026-04-18 at 16.59.12(4).jpeg	\N	1
3	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818524_2_WhatsApp Image 2026-04-18 at 16.59.12(3).jpeg	\N	1
4	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818525_3_WhatsApp Image 2026-04-18 at 16.59.12(2).jpeg	\N	1
5	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818525_4_WhatsApp Image 2026-04-18 at 16.59.12(1).jpeg	\N	1
6	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818526_5_WhatsApp Image 2026-04-18 at 16.59.12.jpeg	\N	1
7	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818527_6_WhatsApp Image 2026-04-18 at 16.59.11.jpeg	\N	1
8	29	\N	\N	\N	2026-04-25 19:16	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq29_1777155386943_0_WhatsApp Image 2026-04-23 at 18.40.57.jpeg	\N	1
9	30	\N	\N	\N	2026-04-25 19:42	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq30_1777156958140_0_WhatsApp Image 2026-04-23 at 18.40.58(1).jpeg	\N	1
10	30	\N	\N	\N	2026-04-25 19:42	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq30_1777156958144_1_WhatsApp Image 2026-04-23 at 18.40.58.jpeg	\N	1
11	28	\N	\N	\N	2026-04-25 19:54	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1777157641494_0_WhatsApp Image 2026-04-23 at 18.40.57(2).jpeg	\N	1
13	37	\N	\N	\N	2026-05-10 20:25	/app/fotos_pesquisa/pq37_1778444711424_0_IMG_20260428_160023709_AE.jpg	\N	0
14	37	\N	\N	\N	2026-05-10 20:43	/app/fotos_pesquisa/pq37_1778445809820_0_IMG_20260428_160023709_AE.jpg	\N	0
16	37	\N	\N	\N	2026-05-10 22:38	/app/fotos_pesquisa/pq37_1778452685278_0_IMG_20260428_160023709_AE.jpg	\N	1
\.


--
-- Data for Name: pesquisa_preco; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pesquisa_preco (pesquisa_id, data_pesquisa, pdv_id, cliente_id, fornecedor_id, observacao, status, foto_path) FROM stdin;
35	2026-05-04	160	93	3	\N	finalizado	\N
36	2026-05-04	160	93	2	\N	finalizado	\N
37	2026-04-28	8	14	3	\N	finalizado	\N
44	2026-05-08	2	3	3	\N	finalizado	\N
5	2026-03-31	2	3	1	\N	finalizado	\N
6	2025-11-25	1	2	1	\N	finalizado	\N
7	2025-11-27	2	3	1	\N	finalizado	\N
8	2025-11-25	4	10	1	\N	finalizado	\N
9	2025-11-28	5	11	1	\N	finalizado	\N
10	2025-11-28	6	12	1	\N	finalizado	\N
11	2025-11-28	7	13	1	\N	finalizado	\N
12	2025-11-27	8	14	1	\N	finalizado	\N
14	2025-11-25	9	15	1	\N	finalizado	\N
15	2025-11-25	\N	16	1	\N	finalizado	\N
16	2025-11-28	11	17	1	\N	finalizado	\N
17	2025-11-27	12	18	1	\N	finalizado	\N
19	2025-11-27	14	20	1	\N	finalizado	\N
20	2025-11-27	13	19	1	\N	finalizado	\N
21	2026-04-03	9	15	1	\N	finalizado	\N
25	2026-04-05	15	21	1	\N	finalizado	\N
26	2026-04-07	4	10	2	\N	finalizado	\N
27	2026-04-07	4	10	1	\N	finalizado	\N
28	2026-04-15	154	94	1	\N	finalizado	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq_28_WhatsApp Image 2026-04-18 at 16.59.12.jpeg
29	2026-04-15	154	94	3	\N	finalizado	\N
31	2026-04-28	8	14	4	Gerente: Diego	finalizado	\N
46	2026-05-25	192	120	3	\N	finalizado	\N
45	2026-05-20	160	93	3	\N	finalizado	\N
47	2026-05-25	192	120	4	\N	finalizado	\N
48	2026-05-25	192	120	2	\N	finalizado	\N
50	2026-05-28	193	121	3	\N	finalizado	\N
49	2026-05-28	193	121	2	\N	finalizado	\N
34	2026-05-03	156	96	3	\N	finalizado	\N
32	2026-04-28	8	14	1	Gerente: Diego	finalizado	\N
30	2026-04-15	154	94	2	\N	finalizado	\N
\.


--
-- Data for Name: pesquisa_preco_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pesquisa_preco_item (pesquisa_item_id, pesquisa_id, produto_id, produto_concorrente_id, preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra, observacao, preco_proprio, facing, preco_concorrente, marca_concorrente_livre, obs_concorrente, foto_path, unidade_coleta, peso_coleta, preco_kg) FROM stdin;
7	5	30	27	4.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
8	5	31	28	4.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
11	5	2	9	2.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
12	5	2	5	4.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
13	5	2	7	2.99	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
14	5	3	10	4.99	0	15	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
15	5	3	13	2.99	0	10	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
16	5	6	1	14.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
17	5	7	17	15.49	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
19	6	6	1	14.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
20	6	2	9	2.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
21	7	3	10	4.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
22	7	3	4	2.99	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
23	7	8	15	14.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
24	7	6	3	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
26	8	13	26	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
27	8	12	32	24.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
28	8	12	33	34.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
29	8	12	34	28.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
30	9	2	5	3.15	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
31	9	2	6	2.15	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
32	9	3	10	2.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
33	9	3	11	2.15	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
34	9	3	4	1.75	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
35	9	6	1	11.19	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
36	9	9	21	8.25	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
37	10	10	18	8.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
38	10	2	5	3.99	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
39	10	2	6	2.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
40	10	2	7	2.59	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
41	10	3	10	4.49	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
42	10	3	11	2.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
43	10	3	13	2.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
44	10	6	1	12.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
45	10	12	25	5.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
46	11	10	18	8.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
47	11	9	21	10.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
48	11	9	22	7.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
49	11	2	6	2.79	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
50	11	10	19	7.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
51	11	8	15	11.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
52	11	12	25	6.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
53	11	12	35	13.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
54	12	10	18	7.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
55	12	2	5	3.69	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
56	12	2	9	2.49	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
57	12	3	10	3.69	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
58	12	3	13	2.49	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
59	12	8	15	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
60	12	7	17	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
61	12	6	36	7.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
62	14	2	8	2.39	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
63	15	12	25	9.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
64	15	12	37	14.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
65	15	2	38	7.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
66	16	2	5	4.19	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
68	16	2	9	2.69	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
69	16	2	6	2.69	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
70	16	10	18	7.39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
71	16	10	20	3.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
72	16	3	10	3.39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
73	16	3	12	2.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
74	16	3	13	2.69	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
75	16	9	21	8.29	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
76	16	9	23	6.45	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
77	16	6	1	12.79	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
78	16	6	14	8.29	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
79	16	12	25	5.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
80	16	12	39	5.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
81	16	12	24	6.19	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
82	16	8	15	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
83	16	8	16	7.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
84	17	6	1	12.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
85	17	12	35	12.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
87	19	2	9	2.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
88	19	3	10	4.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
89	19	3	13	2.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
90	19	6	1	14.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
91	20	12	37	13.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
92	21	3	54	2.39	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
93	21	3	4	1.79	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
94	21	2	7	1.79	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
95	10	2	40	12.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
96	10	10	41	8.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
97	10	9	44	4.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
98	10	9	45	5.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
99	10	12	46	32.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
100	10	12	47	14.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
101	15	12	50	46.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
102	12	10	41	7.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
103	12	9	43	8.19	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
104	9	9	42	8.15	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
105	20	12	53	36.5	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
106	20	12	55	44.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
107	20	9	56	6.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
108	16	9	42	7.39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
109	16	9	45	5.19	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
110	16	9	44	4.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
111	16	12	46	44.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
112	16	12	48	24.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
113	16	12	49	17.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
114	16	12	52	16.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
115	11	10	41	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
116	11	9	44	6.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
117	11	9	42	10.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
118	11	9	45	6.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
119	11	12	46	34.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
120	11	12	47	16.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
121	11	12	50	29.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
122	8	12	49	27.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
123	25	12	25	19.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
124	25	2	5	3.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
125	25	31	28	3.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
126	25	31	57	5.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
127	26	47	58	22.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
128	26	47	59	36.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
129	26	47	60	39.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
130	26	47	61	36.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
131	26	47	62	36.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
132	26	47	63	36.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
133	26	75	64	34.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
134	26	47	65	39.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
135	26	75	66	35.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
136	27	11	67	11.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
137	27	11	68	14.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
138	27	13	26	14.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
139	27	9	43	19.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
140	27	12	49	22.99	0	10	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
141	27	12	25	7.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
142	27	12	33	34.99	0	11	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
143	27	12	34	28.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
145	28	7	17	13.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
146	28	6	1	14.49	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
147	28	3	10	4.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
148	28	2	5	4.99	0	10	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
149	28	7	69	10.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
150	28	8	16	10.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
151	28	2	8	2.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
152	28	2	9	2.99	0	16	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
153	28	3	13	2.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
154	28	2	40	14.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
155	28	2	70	14.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
156	28	2	71	17.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
157	28	12	47	38.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
158	28	11	72	33.19	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
159	28	14	73	21.29	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
160	28	9	21	9.99	0	9	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
163	28	11	75	30.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
165	28	11	77	40.49	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
166	28	11	78	34.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
167	28	11	79	68.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
168	28	14	80	43.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
169	28	11	81	18.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
170	29	248	85	20.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
171	29	269	238	22.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
172	29	264	239	20.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
173	29	254	97	8.49	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
174	29	257	92	17.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
175	30	47	62	32.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
176	30	47	63	32.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
177	30	47	240	26.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
178	30	52	241	30.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
179	28	31	28	3.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
180	28	31	242	3.79	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
181	28	31	243	9.19	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
182	28	31	244	6.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
183	28	31	245	5.89	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
184	31	373	214	8.49	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
185	31	373	\N	9.29	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
186	31	373	248	9.29	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
187	31	373	204	8.69	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
188	31	373	249	8.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
189	31	370	250	4.79	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
190	31	367	251	11.99	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
191	31	370	252	4.99	0	12	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
192	31	370	254	4.99	0	24	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
193	31	371	212	8.79	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
194	31	370	213	5.69	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
195	31	367	255	5.89	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
197	32	2	256	1.99	0	19	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
198	32	2	5	4.19	0	7	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
199	32	3	10	4.19	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
200	32	8	15	11.59	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
201	32	9	21	8.39	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
202	32	9	42	8.39	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
203	32	10	41	8.39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
204	32	9	43	13.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
217	36	33	\N	30.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
223	37	312	260	37.99	0	10	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
218	36	45	\N	30.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
219	36	34	\N	30.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
210	34	311	153	24.49	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
211	35	309	146	24.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
212	35	311	257	26.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
220	36	47	240	27.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
213	35	311	258	26.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
215	35	309	151	20.9	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
216	35	311	259	17.38	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
221	36	47	61	37.64	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
222	36	47	63	37.64	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
247	44	308	\N	26.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
249	44	308	156	27.96	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
250	44	312	\N	39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
251	44	312	260	39.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
252	44	309	\N	29.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
253	44	309	151	26.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
254	44	308	147	32.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
255	45	309	146	24.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
256	46	309	151	20.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
257	47	370	202	5.7	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
258	48	\N	240	28.3	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
259	48	71	261	48.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
260	49	47	262	39.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
261	49	47	263	44.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
262	49	47	264	39.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
263	49	48	265	32.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
264	50	311	153	64.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	Kg	1	64.9
265	50	246	266	134.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	Kg	1	134.9
266	50	307	267	119.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	Kg	1	119.9
\.


--
-- Name: pesquisa_foto_foto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pesquisa_foto_foto_id_seq', 16, true);


--
-- Name: pesquisa_preco_item_pesquisa_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pesquisa_preco_item_pesquisa_item_id_seq', 266, true);


--
-- Name: pesquisa_preco_pesquisa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pesquisa_preco_pesquisa_id_seq', 50, true);


--
-- PostgreSQL database dump complete
--

\unrestrict lF9LL2ocqLvE4d19IHvgnaiEImerp84vHO4LuW2bLop2q93NhzwHYWar31qujpy

