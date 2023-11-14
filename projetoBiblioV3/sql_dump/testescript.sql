PGDMP         (            
    {            biblioteca_db    13.12    13.12 A               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            	           1262    16385    biblioteca_db    DATABASE     b   CREATE DATABASE biblioteca_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';
    DROP DATABASE biblioteca_db;
                biblio    false            �           1247    16515    role    TYPE     @   CREATE TYPE public.role AS ENUM (
    'ADMIN',
    'CLIENTE'
);
    DROP TYPE public.role;
       public          biblio    false            �            1259    16437    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    biblio    false            �            1259    16480 	   devolucao    TABLE     �   CREATE TABLE public.devolucao (
    emprestimo_id integer,
    id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    "notaDePagamento_id" integer
);
    DROP TABLE public.devolucao;
       public         heap    biblio    false            �            1259    16478    devolucao_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devolucao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.devolucao_id_seq;
       public          biblio    false    212            
           0    0    devolucao_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.devolucao_id_seq OWNED BY public.devolucao.id;
          public          biblio    false    211            �            1259    16444 
   emprestimo    TABLE     �   CREATE TABLE public.emprestimo (
    exemplar_id integer,
    usuario_id integer,
    id integer NOT NULL,
    created_at timestamp without time zone NOT NULL
);
    DROP TABLE public.emprestimo;
       public         heap    biblio    false            �            1259    16442    emprestimo_id_seq    SEQUENCE     �   CREATE SEQUENCE public.emprestimo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.emprestimo_id_seq;
       public          biblio    false    208                       0    0    emprestimo_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.emprestimo_id_seq OWNED BY public.emprestimo.id;
          public          biblio    false    207            �            1259    16421    exemplar    TABLE     P   CREATE TABLE public.exemplar (
    livro_id integer,
    id integer NOT NULL
);
    DROP TABLE public.exemplar;
       public         heap    biblio    false            �            1259    16419    exemplar_id_seq    SEQUENCE     �   CREATE SEQUENCE public.exemplar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.exemplar_id_seq;
       public          biblio    false    205                       0    0    exemplar_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.exemplar_id_seq OWNED BY public.exemplar.id;
          public          biblio    false    204            �            1259    16410    livro    TABLE     �   CREATE TABLE public.livro (
    "Autor" character varying NOT NULL,
    "EP" boolean NOT NULL,
    id integer NOT NULL,
    nome character varying NOT NULL
);
    DROP TABLE public.livro;
       public         heap    biblio    false            �            1259    16408    livro_id_seq    SEQUENCE     �   CREATE SEQUENCE public.livro_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.livro_id_seq;
       public          biblio    false    203                       0    0    livro_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.livro_id_seq OWNED BY public.livro.id;
          public          biblio    false    202            �            1259    16493    notadepagamento    TABLE     z   CREATE TABLE public.notadepagamento (
    preco numeric(5,2) NOT NULL,
    usuario_id integer,
    id integer NOT NULL
);
 #   DROP TABLE public.notadepagamento;
       public         heap    biblio    false            �            1259    16491    notadepagamento_id_seq    SEQUENCE     �   CREATE SEQUENCE public.notadepagamento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.notadepagamento_id_seq;
       public          biblio    false    214                       0    0    notadepagamento_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.notadepagamento_id_seq OWNED BY public.notadepagamento.id;
          public          biblio    false    213            �            1259    16462    reserva    TABLE     �   CREATE TABLE public.reserva (
    exemplar_id integer,
    usuario_id integer,
    id integer NOT NULL,
    created_at timestamp without time zone NOT NULL
);
    DROP TABLE public.reserva;
       public         heap    biblio    false            �            1259    16460    reserva_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reserva_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.reserva_id_seq;
       public          biblio    false    210                       0    0    reserva_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.reserva_id_seq OWNED BY public.reserva.id;
          public          biblio    false    209            �            1259    16388    usuario    TABLE       CREATE TABLE public.usuario (
    nome character varying NOT NULL,
    email character varying NOT NULL,
    endereco character varying NOT NULL,
    telefone character varying NOT NULL,
    id integer NOT NULL,
    hashed_password character varying NOT NULL,
    tipo public.role
);
    DROP TABLE public.usuario;
       public         heap    biblio    false    670            �            1259    16386    usuario_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.usuario_id_seq;
       public          biblio    false    201                       0    0    usuario_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;
          public          biblio    false    200            Y           2604    16483    devolucao id    DEFAULT     l   ALTER TABLE ONLY public.devolucao ALTER COLUMN id SET DEFAULT nextval('public.devolucao_id_seq'::regclass);
 ;   ALTER TABLE public.devolucao ALTER COLUMN id DROP DEFAULT;
       public          biblio    false    212    211    212            W           2604    16447    emprestimo id    DEFAULT     n   ALTER TABLE ONLY public.emprestimo ALTER COLUMN id SET DEFAULT nextval('public.emprestimo_id_seq'::regclass);
 <   ALTER TABLE public.emprestimo ALTER COLUMN id DROP DEFAULT;
       public          biblio    false    208    207    208            V           2604    16424    exemplar id    DEFAULT     j   ALTER TABLE ONLY public.exemplar ALTER COLUMN id SET DEFAULT nextval('public.exemplar_id_seq'::regclass);
 :   ALTER TABLE public.exemplar ALTER COLUMN id DROP DEFAULT;
       public          biblio    false    205    204    205            U           2604    16413    livro id    DEFAULT     d   ALTER TABLE ONLY public.livro ALTER COLUMN id SET DEFAULT nextval('public.livro_id_seq'::regclass);
 7   ALTER TABLE public.livro ALTER COLUMN id DROP DEFAULT;
       public          biblio    false    203    202    203            Z           2604    16496    notadepagamento id    DEFAULT     x   ALTER TABLE ONLY public.notadepagamento ALTER COLUMN id SET DEFAULT nextval('public.notadepagamento_id_seq'::regclass);
 A   ALTER TABLE public.notadepagamento ALTER COLUMN id DROP DEFAULT;
       public          biblio    false    213    214    214            X           2604    16465 
   reserva id    DEFAULT     h   ALTER TABLE ONLY public.reserva ALTER COLUMN id SET DEFAULT nextval('public.reserva_id_seq'::regclass);
 9   ALTER TABLE public.reserva ALTER COLUMN id DROP DEFAULT;
       public          biblio    false    209    210    210            T           2604    16391 
   usuario id    DEFAULT     h   ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);
 9   ALTER TABLE public.usuario ALTER COLUMN id DROP DEFAULT;
       public          biblio    false    200    201    201            �          0    16437    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          biblio    false    206   >H                 0    16480 	   devolucao 
   TABLE DATA           X   COPY public.devolucao (emprestimo_id, id, created_at, "notaDePagamento_id") FROM stdin;
    public          biblio    false    212   hH       �          0    16444 
   emprestimo 
   TABLE DATA           M   COPY public.emprestimo (exemplar_id, usuario_id, id, created_at) FROM stdin;
    public          biblio    false    208   �H       �          0    16421    exemplar 
   TABLE DATA           0   COPY public.exemplar (livro_id, id) FROM stdin;
    public          biblio    false    205   I       �          0    16410    livro 
   TABLE DATA           8   COPY public.livro ("Autor", "EP", id, nome) FROM stdin;
    public          biblio    false    203   MI                 0    16493    notadepagamento 
   TABLE DATA           @   COPY public.notadepagamento (preco, usuario_id, id) FROM stdin;
    public          biblio    false    214   �I       �          0    16462    reserva 
   TABLE DATA           J   COPY public.reserva (exemplar_id, usuario_id, id, created_at) FROM stdin;
    public          biblio    false    210   �I       �          0    16388    usuario 
   TABLE DATA           ]   COPY public.usuario (nome, email, endereco, telefone, id, hashed_password, tipo) FROM stdin;
    public          biblio    false    201   "J                  0    0    devolucao_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.devolucao_id_seq', 4, true);
          public          biblio    false    211                       0    0    emprestimo_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.emprestimo_id_seq', 5, true);
          public          biblio    false    207                       0    0    exemplar_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.exemplar_id_seq', 7, true);
          public          biblio    false    204                       0    0    livro_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.livro_id_seq', 5, true);
          public          biblio    false    202                       0    0    notadepagamento_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.notadepagamento_id_seq', 2, true);
          public          biblio    false    213                       0    0    reserva_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.reserva_id_seq', 2, true);
          public          biblio    false    209                       0    0    usuario_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.usuario_id_seq', 6, true);
          public          biblio    false    200            b           2606    16441 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            biblio    false    206            h           2606    16485    devolucao devolucao_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.devolucao
    ADD CONSTRAINT devolucao_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.devolucao DROP CONSTRAINT devolucao_pkey;
       public            biblio    false    212            d           2606    16449    emprestimo emprestimo_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.emprestimo
    ADD CONSTRAINT emprestimo_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.emprestimo DROP CONSTRAINT emprestimo_pkey;
       public            biblio    false    208            `           2606    16426    exemplar exemplar_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.exemplar
    ADD CONSTRAINT exemplar_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.exemplar DROP CONSTRAINT exemplar_pkey;
       public            biblio    false    205            ^           2606    16418    livro livro_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.livro
    ADD CONSTRAINT livro_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.livro DROP CONSTRAINT livro_pkey;
       public            biblio    false    203            j           2606    16498 $   notadepagamento notadepagamento_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.notadepagamento
    ADD CONSTRAINT notadepagamento_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.notadepagamento DROP CONSTRAINT notadepagamento_pkey;
       public            biblio    false    214            f           2606    16467    reserva reserva_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.reserva DROP CONSTRAINT reserva_pkey;
       public            biblio    false    210            \           2606    16396    usuario usuario_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_pkey;
       public            biblio    false    201            p           2606    16486 &   devolucao devolucao_emprestimo_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devolucao
    ADD CONSTRAINT devolucao_emprestimo_id_fkey FOREIGN KEY (emprestimo_id) REFERENCES public.emprestimo(id);
 P   ALTER TABLE ONLY public.devolucao DROP CONSTRAINT devolucao_emprestimo_id_fkey;
       public          biblio    false    212    2916    208            q           2606    16504 +   devolucao devolucao_notaDePagamento_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devolucao
    ADD CONSTRAINT "devolucao_notaDePagamento_id_fkey" FOREIGN KEY ("notaDePagamento_id") REFERENCES public.notadepagamento(id);
 W   ALTER TABLE ONLY public.devolucao DROP CONSTRAINT "devolucao_notaDePagamento_id_fkey";
       public          biblio    false    212    2922    214            l           2606    16450 &   emprestimo emprestimo_exemplar_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.emprestimo
    ADD CONSTRAINT emprestimo_exemplar_id_fkey FOREIGN KEY (exemplar_id) REFERENCES public.exemplar(id);
 P   ALTER TABLE ONLY public.emprestimo DROP CONSTRAINT emprestimo_exemplar_id_fkey;
       public          biblio    false    208    2912    205            m           2606    16455 %   emprestimo emprestimo_usuario_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.emprestimo
    ADD CONSTRAINT emprestimo_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);
 O   ALTER TABLE ONLY public.emprestimo DROP CONSTRAINT emprestimo_usuario_id_fkey;
       public          biblio    false    208    2908    201            k           2606    16427    exemplar exemplar_livro_id_fkey    FK CONSTRAINT        ALTER TABLE ONLY public.exemplar
    ADD CONSTRAINT exemplar_livro_id_fkey FOREIGN KEY (livro_id) REFERENCES public.livro(id);
 I   ALTER TABLE ONLY public.exemplar DROP CONSTRAINT exemplar_livro_id_fkey;
       public          biblio    false    203    2910    205            r           2606    16499 /   notadepagamento notadepagamento_usuario_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.notadepagamento
    ADD CONSTRAINT notadepagamento_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);
 Y   ALTER TABLE ONLY public.notadepagamento DROP CONSTRAINT notadepagamento_usuario_id_fkey;
       public          biblio    false    2908    214    201            n           2606    16468     reserva reserva_exemplar_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_exemplar_id_fkey FOREIGN KEY (exemplar_id) REFERENCES public.exemplar(id);
 J   ALTER TABLE ONLY public.reserva DROP CONSTRAINT reserva_exemplar_id_fkey;
       public          biblio    false    210    2912    205            o           2606    16473    reserva reserva_usuario_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);
 I   ALTER TABLE ONLY public.reserva DROP CONSTRAINT reserva_usuario_id_fkey;
       public          biblio    false    210    201    2908            �      x�3�L174H62�0I����� (	�         J   x�]ʱ�0���F��a��?G�H)R߅P�r,�Eb����)�%���5�CX�-Ԕ�;��v�nS��y�      �   M   x�Eʱ�0��L��I"p�d�9�*��58b�E,p��h�C,�_�$Z�Y�s׽�N�/(&��&�B�������      �      x�3�4�2�4�2�4b3 6����� (�      �   X   x����0 �3L��l�Z�U�������;�71�A��΅����k�HYj�VFP[>�i=����l�4�Z~^.��2�"����         !   x�34�35�4�4�24�30�4�4����� 1��      �   ,   x�3�4�4�4202�54�54T04�2"s=33cCC�=... ~v�      �   p  x�U�Ɏ�@�s�<�����ED1siB�MЧ��q*��?՗��(I�N]�D���3	�|/������Ba���XO$��_���5��7F�fVǌ�^y��Y��"@�{����Sj��� %0|�C)V�R��._�˨�Z�_�R�x8��
.}�Ogh�'5���OB����#��H/2Mc��{��䮵-P��6�j�4�����T��<�%U8V��/870�ަCy^��cK������J";:�a͟N��p%����5�Z��?]x�4Ϸ6X��;�ކ]9���j�u���d �H�a1J��w��B��؆���kޔ$�D�l?��u1�V����q?J�     