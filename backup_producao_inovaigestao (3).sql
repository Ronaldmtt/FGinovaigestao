--
-- PostgreSQL database dump
--

-- Dumped from database version 16.11 (f45eb12)
-- Dumped by pg_dump version 17.5

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
-- Name: _system; Type: SCHEMA; Schema: -; Owner: neondb_owner
--

CREATE SCHEMA _system;


ALTER SCHEMA _system OWNER TO neondb_owner;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: replit_database_migrations_v1; Type: TABLE; Schema: _system; Owner: neondb_owner
--

CREATE TABLE _system.replit_database_migrations_v1 (
    id bigint NOT NULL,
    build_id text NOT NULL,
    deployment_id text NOT NULL,
    statement_count bigint NOT NULL,
    applied_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE _system.replit_database_migrations_v1 OWNER TO neondb_owner;

--
-- Name: replit_database_migrations_v1_id_seq; Type: SEQUENCE; Schema: _system; Owner: neondb_owner
--

CREATE SEQUENCE _system.replit_database_migrations_v1_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE _system.replit_database_migrations_v1_id_seq OWNER TO neondb_owner;

--
-- Name: replit_database_migrations_v1_id_seq; Type: SEQUENCE OWNED BY; Schema: _system; Owner: neondb_owner
--

ALTER SEQUENCE _system.replit_database_migrations_v1_id_seq OWNED BY _system.replit_database_migrations_v1.id;


--
-- Name: client; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.client (
    id integer NOT NULL,
    nome character varying(200) NOT NULL,
    email character varying(120),
    telefone character varying(20),
    endereco text,
    created_at timestamp without time zone,
    creator_id integer NOT NULL,
    public_code character varying(32),
    observacoes text,
    empresa character varying(200)
);


ALTER TABLE public.client OWNER TO neondb_owner;

--
-- Name: client_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.client_id_seq OWNER TO neondb_owner;

--
-- Name: client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.client_id_seq OWNED BY public.client.id;


--
-- Name: comentarios; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.comentarios (
    id integer NOT NULL,
    contato_id integer NOT NULL,
    texto text NOT NULL,
    data_criacao timestamp without time zone
);


ALTER TABLE public.comentarios OWNER TO neondb_owner;

--
-- Name: comentarios_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.comentarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comentarios_id_seq OWNER TO neondb_owner;

--
-- Name: comentarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.comentarios_id_seq OWNED BY public.comentarios.id;


--
-- Name: contato_files; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.contato_files (
    id integer NOT NULL,
    filename character varying(255) NOT NULL,
    original_name character varying(255) NOT NULL,
    mime_type character varying(100),
    file_size integer,
    descricao text,
    storage_path character varying(500) NOT NULL,
    created_at timestamp without time zone,
    contato_id integer NOT NULL,
    uploaded_by_id integer NOT NULL
);


ALTER TABLE public.contato_files OWNER TO neondb_owner;

--
-- Name: contato_files_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.contato_files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contato_files_id_seq OWNER TO neondb_owner;

--
-- Name: contato_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.contato_files_id_seq OWNED BY public.contato_files.id;


--
-- Name: contatos; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.contatos (
    id integer NOT NULL,
    nome_empresa character varying(200) NOT NULL,
    nome_contato character varying(200) NOT NULL,
    email character varying(200) NOT NULL,
    telefone character varying(50) NOT NULL,
    observacoes text,
    estagio character varying(100) NOT NULL,
    data_criacao timestamp without time zone,
    data_atualizacao timestamp without time zone
);


ALTER TABLE public.contatos OWNER TO neondb_owner;

--
-- Name: contatos_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.contatos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contatos_id_seq OWNER TO neondb_owner;

--
-- Name: contatos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.contatos_id_seq OWNED BY public.contatos.id;


--
-- Name: crm_stages; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.crm_stages (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    ordem integer NOT NULL,
    is_fixed boolean NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.crm_stages OWNER TO neondb_owner;

--
-- Name: crm_stages_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.crm_stages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.crm_stages_id_seq OWNER TO neondb_owner;

--
-- Name: crm_stages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.crm_stages_id_seq OWNED BY public.crm_stages.id;


--
-- Name: file_categories; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.file_categories (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    icone character varying(50),
    cor character varying(20),
    ordem integer,
    created_at timestamp without time zone
);


ALTER TABLE public.file_categories OWNER TO neondb_owner;

--
-- Name: file_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.file_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.file_categories_id_seq OWNER TO neondb_owner;

--
-- Name: file_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.file_categories_id_seq OWNED BY public.file_categories.id;


--
-- Name: lead; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.lead (
    id integer NOT NULL,
    nome character varying(200) NOT NULL,
    empresa character varying(200),
    email character varying(120),
    telefone character varying(20),
    cargo character varying(100),
    origem character varying(50),
    valor_estimado double precision,
    etapa character varying(50) NOT NULL,
    convertido boolean NOT NULL,
    perdido boolean NOT NULL,
    motivo_perda text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    observacoes text,
    responsavel_id integer,
    converted_to_client_id integer
);


ALTER TABLE public.lead OWNER TO neondb_owner;

--
-- Name: lead_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.lead_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.lead_id_seq OWNER TO neondb_owner;

--
-- Name: lead_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.lead_id_seq OWNED BY public.lead.id;


--
-- Name: lead_interaction; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.lead_interaction (
    id integer NOT NULL,
    tipo character varying(50) NOT NULL,
    descricao text NOT NULL,
    created_at timestamp without time zone,
    lead_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.lead_interaction OWNER TO neondb_owner;

--
-- Name: lead_interaction_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.lead_interaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.lead_interaction_id_seq OWNER TO neondb_owner;

--
-- Name: lead_interaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.lead_interaction_id_seq OWNED BY public.lead_interaction.id;


--
-- Name: project; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.project (
    id integer NOT NULL,
    nome character varying(200) NOT NULL,
    transcricao text,
    created_at timestamp without time zone,
    client_id integer NOT NULL,
    responsible_id integer NOT NULL,
    contexto_justificativa text,
    descricao_resumida text,
    problema_oportunidade text,
    objetivos text,
    alinhamento_estrategico text,
    escopo_projeto text,
    fora_escopo text,
    premissas text,
    restricoes text,
    status character varying(20) DEFAULT 'em_andamento'::character varying NOT NULL,
    progress_percent integer DEFAULT 0,
    prazo date
);


ALTER TABLE public.project OWNER TO neondb_owner;

--
-- Name: project_api_credentials; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.project_api_credentials (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    provedor character varying(100) NOT NULL,
    descricao text,
    api_key_masked character varying(50),
    api_key_encrypted text,
    ambiente character varying(20),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    project_id integer NOT NULL,
    created_by_id integer NOT NULL
);


ALTER TABLE public.project_api_credentials OWNER TO neondb_owner;

--
-- Name: project_api_credentials_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.project_api_credentials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_api_credentials_id_seq OWNER TO neondb_owner;

--
-- Name: project_api_credentials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.project_api_credentials_id_seq OWNED BY public.project_api_credentials.id;


--
-- Name: project_api_endpoints; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.project_api_endpoints (
    id integer NOT NULL,
    nome character varying(200) NOT NULL,
    url character varying(500) NOT NULL,
    metodo character varying(10),
    descricao text,
    headers text,
    body_exemplo text,
    documentacao_link character varying(500),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    project_id integer NOT NULL,
    credential_id integer,
    created_by_id integer NOT NULL
);


ALTER TABLE public.project_api_endpoints OWNER TO neondb_owner;

--
-- Name: project_api_endpoints_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.project_api_endpoints_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_api_endpoints_id_seq OWNER TO neondb_owner;

--
-- Name: project_api_endpoints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.project_api_endpoints_id_seq OWNED BY public.project_api_endpoints.id;


--
-- Name: project_api_keys; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.project_api_keys (
    id integer NOT NULL,
    project_id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying(100) NOT NULL,
    prefix character varying(12) NOT NULL,
    key_hash character varying(256) NOT NULL,
    scopes_json text,
    created_at timestamp without time zone,
    last_used_at timestamp without time zone,
    expires_at timestamp without time zone,
    revoked_at timestamp without time zone
);


ALTER TABLE public.project_api_keys OWNER TO neondb_owner;

--
-- Name: project_api_keys_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.project_api_keys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_api_keys_id_seq OWNER TO neondb_owner;

--
-- Name: project_api_keys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.project_api_keys_id_seq OWNED BY public.project_api_keys.id;


--
-- Name: project_files; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.project_files (
    id integer NOT NULL,
    filename character varying(255) NOT NULL,
    original_name character varying(255) NOT NULL,
    mime_type character varying(100),
    file_size integer,
    descricao text,
    storage_path character varying(500) NOT NULL,
    created_at timestamp without time zone,
    project_id integer NOT NULL,
    category_id integer,
    uploaded_by_id integer NOT NULL
);


ALTER TABLE public.project_files OWNER TO neondb_owner;

--
-- Name: project_files_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.project_files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_files_id_seq OWNER TO neondb_owner;

--
-- Name: project_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.project_files_id_seq OWNED BY public.project_files.id;


--
-- Name: project_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_id_seq OWNER TO neondb_owner;

--
-- Name: project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.project_id_seq OWNED BY public.project.id;


--
-- Name: project_users; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.project_users (
    project_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.project_users OWNER TO neondb_owner;

--
-- Name: system_api_keys; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.system_api_keys (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying(100) NOT NULL,
    prefix character varying(12) NOT NULL,
    key_hash character varying(256) NOT NULL,
    scopes_json text,
    created_at timestamp without time zone,
    last_used_at timestamp without time zone,
    expires_at timestamp without time zone,
    revoked_at timestamp without time zone
);


ALTER TABLE public.system_api_keys OWNER TO neondb_owner;

--
-- Name: system_api_keys_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.system_api_keys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_api_keys_id_seq OWNER TO neondb_owner;

--
-- Name: system_api_keys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.system_api_keys_id_seq OWNED BY public.system_api_keys.id;


--
-- Name: task; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.task (
    id integer NOT NULL,
    titulo character varying(200) NOT NULL,
    descricao text,
    status character varying(20) NOT NULL,
    data_conclusao date,
    created_at timestamp without time zone,
    completed_at timestamp without time zone,
    project_id integer NOT NULL,
    assigned_user_id integer,
    disparada boolean DEFAULT false NOT NULL,
    disparada_at timestamp without time zone,
    ordem integer DEFAULT 0
);


ALTER TABLE public.task OWNER TO neondb_owner;

--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_id_seq OWNER TO neondb_owner;

--
-- Name: task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id;


--
-- Name: todo_item; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.todo_item (
    id integer NOT NULL,
    texto character varying(300) NOT NULL,
    completed boolean NOT NULL,
    created_at timestamp without time zone,
    completed_at timestamp without time zone,
    task_id integer NOT NULL,
    due_date date,
    comentario text
);


ALTER TABLE public.todo_item OWNER TO neondb_owner;

--
-- Name: todo_item_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.todo_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.todo_item_id_seq OWNER TO neondb_owner;

--
-- Name: todo_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.todo_item_id_seq OWNED BY public.todo_item.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    sobrenome character varying(100) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256) NOT NULL,
    is_admin boolean NOT NULL,
    created_at timestamp without time zone,
    reset_token character varying(100),
    reset_token_expires timestamp without time zone,
    acesso_clientes boolean DEFAULT true NOT NULL,
    acesso_projetos boolean DEFAULT true NOT NULL,
    acesso_tarefas boolean DEFAULT true NOT NULL,
    acesso_kanban boolean DEFAULT true NOT NULL,
    acesso_crm boolean DEFAULT true NOT NULL,
    receber_notificacoes boolean DEFAULT true NOT NULL
);


ALTER TABLE public."user" OWNER TO neondb_owner;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO neondb_owner;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: replit_database_migrations_v1 id; Type: DEFAULT; Schema: _system; Owner: neondb_owner
--

ALTER TABLE ONLY _system.replit_database_migrations_v1 ALTER COLUMN id SET DEFAULT nextval('_system.replit_database_migrations_v1_id_seq'::regclass);


--
-- Name: client id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.client ALTER COLUMN id SET DEFAULT nextval('public.client_id_seq'::regclass);


--
-- Name: comentarios id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.comentarios ALTER COLUMN id SET DEFAULT nextval('public.comentarios_id_seq'::regclass);


--
-- Name: contato_files id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.contato_files ALTER COLUMN id SET DEFAULT nextval('public.contato_files_id_seq'::regclass);


--
-- Name: contatos id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.contatos ALTER COLUMN id SET DEFAULT nextval('public.contatos_id_seq'::regclass);


--
-- Name: crm_stages id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.crm_stages ALTER COLUMN id SET DEFAULT nextval('public.crm_stages_id_seq'::regclass);


--
-- Name: file_categories id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.file_categories ALTER COLUMN id SET DEFAULT nextval('public.file_categories_id_seq'::regclass);


--
-- Name: lead id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.lead ALTER COLUMN id SET DEFAULT nextval('public.lead_id_seq'::regclass);


--
-- Name: lead_interaction id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.lead_interaction ALTER COLUMN id SET DEFAULT nextval('public.lead_interaction_id_seq'::regclass);


--
-- Name: project id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project ALTER COLUMN id SET DEFAULT nextval('public.project_id_seq'::regclass);


--
-- Name: project_api_credentials id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_credentials ALTER COLUMN id SET DEFAULT nextval('public.project_api_credentials_id_seq'::regclass);


--
-- Name: project_api_endpoints id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_endpoints ALTER COLUMN id SET DEFAULT nextval('public.project_api_endpoints_id_seq'::regclass);


--
-- Name: project_api_keys id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_keys ALTER COLUMN id SET DEFAULT nextval('public.project_api_keys_id_seq'::regclass);


--
-- Name: project_files id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_files ALTER COLUMN id SET DEFAULT nextval('public.project_files_id_seq'::regclass);


--
-- Name: system_api_keys id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.system_api_keys ALTER COLUMN id SET DEFAULT nextval('public.system_api_keys_id_seq'::regclass);


--
-- Name: task id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);


--
-- Name: todo_item id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.todo_item ALTER COLUMN id SET DEFAULT nextval('public.todo_item_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: replit_database_migrations_v1; Type: TABLE DATA; Schema: _system; Owner: neondb_owner
--

COPY _system.replit_database_migrations_v1 (id, build_id, deployment_id, statement_count, applied_at) FROM stdin;
1	db1f7eb9-ba5a-4065-a946-38e2f1abe327	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	2	2025-08-26 22:48:51.246455+00
2	30a50322-0e39-4507-8b30-608ef15d513c	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	6	2025-10-31 12:26:36.884499+00
3	27e744a1-a8b1-42ec-823b-ee414a6a2f53	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	1	2025-10-31 18:20:14.283742+00
4	cb594ab5-2d99-4649-9212-234eeb1421f0	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	1	2025-11-03 15:45:57.179862+00
5	218e5dd5-e62f-450d-8582-4ec896b42f8c	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	3	2025-11-07 00:39:54.360974+00
6	5d0f6d16-ca75-4af9-a1f6-9c4ef0491c2f	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	1	2025-11-11 20:06:04.0174+00
7	63517a6c-9b16-47b3-a7aa-3d8bb54b25af	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	3	2025-11-14 18:33:03.115541+00
8	55505ccd-a90e-4f54-9519-01fddb8e84f5	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	1	2025-11-17 19:07:41.349617+00
9	065f5e6f-478d-46c0-9de1-18d014b26c74	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	2	2025-12-04 16:44:52.452218+00
10	620cfc52-6cd3-4e00-9c50-22d80e0a9439	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	12	2025-12-09 20:20:27.405314+00
11	3ad780ef-b9e4-45a7-8a61-2a89d00ac63c	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	3	2025-12-15 15:06:37.973062+00
12	483ce0e1-3f04-4e4d-a0ee-eae35e55d721	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	4	2025-12-17 15:58:44.110806+00
13	2fa35ed4-d859-48dc-8d61-a9a23a208d75	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	3	2025-12-18 18:11:11.6443+00
14	cbf7c076-0386-49f3-9c03-d894d9222c55	16fe4e1e-b969-4929-b999-9ce0d58ffdbb	1	2025-12-18 21:20:46.51595+00
\.


--
-- Data for Name: client; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.client (id, nome, email, telefone, endereco, created_at, creator_id, public_code, observacoes, empresa) FROM stdin;
1	Sá Cavalcante	sa@sacavalcante.com.br			2025-08-25 14:20:47.41767	2	76GMPAFU	\N	\N
2	inovai.lab	inovai@inovailab.com	21971497710	Rua Major Rubens Vaz, 536, Gávea. 	2025-08-25 15:50:13.268065	1	1WNK9F97	\N	\N
3	AvSales-Aeropool	humberto@avsales.com	21999996565	Rua Major Rubens Vaz, 536	2025-08-26 19:26:14.654693	1	\N	\N	\N
4	BoraBaila	borabailar@borabailar.com.br	2199999-8888		2025-08-26 19:17:33.70383	1	II5Y8XAO	\N	\N
5	OÁZ	bento@oaz.co	+55 11 99364-5364	Al Minstro Rocha Azevedo 912	2025-09-02 16:54:15.690966	1	ZQJL3A0O	\N	\N
7	Taurus Capacetes	Renato.cavalcanti@taurus.com.br	+55 21 99620-1203		2025-10-13 16:41:56.960419	1	\N	\N	\N
8	Inovai.Lab - Produtos	vitor@inovailab.com	21997855082	Rua Major Rubens Vaz	2025-10-27 21:18:57.750331	1	\N	\N	\N
10	Rede Brasil	jaqueline@rbr.com.br	27 99983-8759		2026-01-09 16:22:22.793932	1	\N		\N
11	FAPERJ				2026-01-22 15:32:12.238532	1	\N		\N
6	AC Burlamaqui	fernanda.correa@acburlamaqui.com.br	+55 21 98326-1741		2025-10-13 16:41:46.691432	1	3VE73D18	\N	\N
\.


--
-- Data for Name: comentarios; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.comentarios (id, contato_id, texto, data_criacao) FROM stdin;
3	16	Enviado a seguinte proposta pra ele:\r\n\r\n\r\nProposta Comercial — Automações com IA para a nova marca do Silvio\r\nProponente: inovAI.lab\r\n Cliente: Silvio Procopio\r\n Data: 24/11/2025\r\n\r\n1. Visão geral e objetivo\r\nA inovAI.lab propõe implementar automações com Inteligência Artificial que nascem junto com a marca para:\r\nEliminar fricção na compra — oferecendo autonomia ao cliente, sem depender de vendedor humano invasivo.\r\n\r\n\r\nAumentar conversão no início — no online e em bazares/pop-ups, com diferenciais visíveis.\r\n\r\n\r\nEscalar com operação enxuta — reduzindo necessidade de time grande e treinamento constante.\r\n\r\n\r\nO projeto é modular, permitindo ativação por etapas conforme o momento e budget da marca.\r\n\r\n2. Dois modelos de entrega\r\nOpção 1 — No-Code / Low-Code (n8n-like)\r\nAutomações em fluxos visuais conectando e-commerce + IA + integrações padrão.\r\n Vantagens: menor investimento inicial, implantação mais rápida.\r\n Limites: menor personalização e barreira de cópia no futuro.\r\nOpção 2 — Code / Custom (padrão inovAI.lab)\r\nSolução sob medida com arquitetura própria (RAG + validações + APIs + UX custom).\r\n Vantagens: mais confiável, experiência mais “marca nativa”, escalável e difícil de copiar.\r\n Limites: setup maior e prazo um pouco mais longo.\r\n\r\n3. Escopo modular de soluções\r\nMódulo A — Vendedor IA (prioridade 1)\r\nDescrição\r\n Agente vendedor treinado no catálogo, tamanhos, materiais, políticas e tom de voz da marca. Atendimento não invasivo, com recomendações e CTA de compra.\r\nEntregáveis\r\nVendedor virtual com personalidade da marca\r\n\r\n\r\nBase de conhecimento (RAG) com catálogo + informações de produto\r\n\r\n\r\nFluxos de venda completos\r\n\r\n\r\nPainel simples de métricas\r\n\r\n\r\nIntegrações previstas\r\nShopify (ou e-commerce equivalente)\r\n\r\n\r\nPrazo estimado\r\n3 a 5 semanas\r\n\r\n\r\nInvestimento\r\nNO-CODE:\r\n\r\n\r\nSetup: R$ 4.500\r\n\r\n\r\nMensalidade/infra: R$ 450/mês\r\n\r\n\r\nCODE / CUSTOM:\r\n\r\n\r\nSetup: R$ 9.000\r\n\r\n\r\nMensalidade/infra + evolução: R$ 750/mês\r\n\r\n\r\n\r\nMódulo B — Provador Virtual / Try-On por Foto (prioridade 2)\r\nDescrição\r\n Cliente envia foto e recebe preview usando a peça. Diferencial para conversão no online e em bazares.\r\nEntregáveis\r\nPOC com coleção cápsula\r\n\r\n\r\nExperiência integrada ao e-commerce e/ou QR code para bazar\r\n\r\n\r\nPolítica de privacidade de imagens\r\n\r\n\r\nMonitoramento de uso e impacto\r\n\r\n\r\nPrazo estimado\r\n4 a 7 semanas\r\n\r\n\r\nInvestimento\r\nNO-CODE:\r\n\r\n\r\nSetup POC cápsula: R$ 7.500\r\n\r\n\r\nExpansão p/ coleção completa: R$ 3.000\r\n\r\n\r\nMensalidade de processamento: R$ 600/mês\r\n\r\n\r\nCODE / CUSTOM:\r\n\r\n\r\nSetup POC cápsula: R$ 12.500\r\n\r\n\r\nExpansão p/ coleção completa: R$ 5.000\r\n\r\n\r\nMensalidade de processamento + ajustes: R$ 1.000/mês\r\n\r\n\r\n\r\nMódulo C — Comunicação Hiperpersonalizada (CRM / WhatsApp / E-mail)\r\nDescrição\r\n Segmentação automática por histórico de compras e geração de campanhas 1:1 no tom da marca.\r\nEntregáveis\r\nSegmentação comportamental automática\r\n\r\n\r\nMensagens personalizadas geradas por IA\r\n\r\n\r\nRotina de disparo com fila de aprovação\r\n\r\n\r\nMétricas de performance\r\n\r\n\r\nPrazo estimado\r\n3 a 4 semanas após base mínima de clientes\r\n\r\n\r\nInvestimento\r\nNO-CODE:\r\n\r\n\r\nSetup: R$ 3.000\r\n\r\n\r\nMensalidade: R$ 300/mês\r\n\r\n\r\nCODE / CUSTOM:\r\n\r\n\r\nSetup: R$ 6.000\r\n\r\n\r\nMensalidade: R$ 500/mês\r\n\r\n\r\n\r\nMódulo D — Smart Cameras / Heatmap (fase futura)\r\nDescrição\r\n Visão computacional para mapa de calor, fluxo de pessoas e interesse por áreas/produtos em loja/pop-up.\r\nEntregáveis\r\nPipeline de captura/contagem\r\n\r\n\r\nHeatmap por período\r\n\r\n\r\nInsights automáticos\r\n\r\n\r\nDashboard\r\n\r\n\r\nPrazo estimado\r\n4 a 6 semanas quando houver espaço físico recorrente\r\n\r\n\r\nInvestimento\r\nNO-CODE:\r\n\r\n\r\nSetup: R$ 6.000\r\n\r\n\r\nMensalidade: R$ 500/mês\r\n\r\n\r\nCODE / CUSTOM:\r\n\r\n\r\nSetup: R$ 10.000\r\n\r\n\r\nMensalidade: R$ 1.000/mês\r\n\r\n\r\n\r\n4. Pacotes recomendados\r\nPacote 1 — Começo Disruptivo Enxuto\r\nInclui: Módulo A\r\nNO-CODE: Setup R$ 4.500 | Mensal R$ 450\r\n\r\n\r\nCUSTOM: Setup R$ 9.000 | Mensal R$ 750\r\n\r\n\r\n\r\nPacote 2 — Tração e Conversão\r\nInclui: Módulo A + Módulo B (POC cápsula)\r\nNO-CODE: Setup R$ 12.000 | Mensal R$ 1.050\r\n\r\n\r\nCUSTOM: Setup R$ 21.500 | Mensal R$ 1.750\r\n\r\n\r\n\r\nPacote 3 — Marca IA Nativa\r\nInclui: Módulo A + Módulo B (expandido) + Módulo C\r\nNO-CODE: Setup R$ 18.000 | Mensal R$ 1.350\r\n\r\n\r\nCUSTOM: Setup R$ 32.500 | Mensal R$ 2.250\r\n\r\n\r\n\r\n5. Condições comerciais\r\nEscopo final confirmado em reunião de scoping (60–90 min):\r\n coleção cápsula, nº de SKUs, stack do e-commerce, nível de realismo do try-on e canais de comunicação.\r\n\r\n\r\nPagamento por módulo: 50% kickoff + 50% entrega (ou por marcos).\r\n\r\n\r\nMensalidade cobre: infraestrutura cloud/modelos, monitoramento contínuo e ajustes leves.\r\n\r\n\r\n\r\n6. Cronograma macro\r\nScoping & definição de módulos/pacote\r\n\r\n\r\nKickoff técnico\r\n\r\n\r\nEntrega do Módulo A\r\n\r\n\r\nEntrega do Módulo B\r\n\r\n\r\nEvolução para C e D conforme maturidade da marca\r\n\r\n\r\n\r\n7. Próximos passos\r\nAgendar scoping.\r\n\r\n\r\nEm até 48h após scoping, enviamos cronograma fechado.\r\n\r\n\r\nAssinatura e início do pacote escolhido.\r\n\r\n\r\n\r\n	2025-11-24 23:02:01.19779
4	18	Fiz 2o contato dia 25/11	2025-11-25 13:28:27.411636
5	6	Fiz 3o contato 24/11  Com Luiz mas não obtive retorno. Para iniciar um projeto de recadastramento de sócios.	2025-11-25 13:29:54.830179
6	7	Fizemos a reunião  dia 20/11 foi um sucesso. Agora Rapha vai enviar os designs e planilha de produtos e pedido para validar a operação. 	2025-11-25 13:32:39.694259
7	14	Contato dia 24/11 me retornou pedindo para entrar em contato na seman de 8/12	2025-11-25 13:33:50.683468
8	13	Dia 24/11 produto bem adiantado faltando finalizar em outra plataforma. Apresentar para Ronald. CRM integrado a Zenfisio.	2025-11-25 13:36:03.524981
9	5	Contato feito em 25/11 - para marcar 2a reunião.	2025-11-25 13:36:37.756581
10	19	Enviado mensagem para a Fernanda Branco pedindo uma reunião	2025-12-01 17:26:17.822012
11	20	Reuniao Realizada com a Luiza na segunda, dia 1 de dezembro. Ficou alinhado de marcarmos uma reuniao pra entender melhor o sistema que eles precisam criar com mais dois gerentes. 	2025-12-01 17:27:15.310944
12	10	Enviado mensagem para o Gustavo na segunda dia 1 de dezembro de 2025 pedindo a segunda reunião de aprofundamento. 	2025-12-01 17:30:03.947005
13	18	Feito outro contato pelo Paulo dia 01 dezembro de 2025. Caso nao retorne vamos entrar em contato direto com o Mario Chady	2025-12-01 17:30:47.642928
14	6	1/12 ligar para Roberto Dir. Fin.  e dia 2/12 Ligar novamente Luiz	2025-12-01 17:33:33.398564
15	8	Reuniao marcada para dia 2 de dezembro de 2025 com o Theo e a Rachel. 	2025-12-01 17:34:10.684256
16	15	Enviado mensagem no dia 1 de dezembro pedindo a segunda reunião. 	2025-12-01 17:36:23.459377
17	16	Reuniao marcada para terça feira (2 de dezembro de 2025) para discutir a proposta comercial enviada. 	2025-12-01 17:37:55.716114
18	10	Segunda reunião agendada para quinta feira (4 de dezembro de 2025) as 11:30 com o Gustavo. 	2025-12-01 17:57:48.165624
19	15	Agendado viagem para Vitoria para conhecer o negocio do cliente entre os dias 09 a 10 de dezembro 2025. 	2025-12-01 19:05:35.350375
20	21	Aguardando retorno do Saulo. 	2025-12-01 19:08:28.539526
21	16	Reunião de follow-up para discutir a proposta comercial enviada pela inovAI.lab. Silvio confirmou que está na fase embrionária da marca de moda, com início de operação enxuto em bazares/pop-ups e e-commerce, e que a principal necessidade agora é definir escopo mínimo viável e custos para caber no orçamento inicial.\r\n\r\nReforçamos a lógica modular do projeto e a priorização por impacto rápido em conversão e redução de fricção no atendimento. O Silvio mostrou maior aderência ao Módulo A (Vendedor IA) como primeira entrega, por ser o diferencial mais imediato tanto no online quanto nos bazares e por reduzir dependência de vendedores humanos. O Provador Virtual (Módulo B) segue como segunda prioridade, para ser avaliado após validação inicial do e-commerce e da coleção cápsula. Também conversamos sobre possibilidades futuras de comunicação hiperpersonalizada pós-compra e visão computacional em loja, mas ficando para uma fase posterior, quando houver base de clientes e operação mais estável.\r\n\r\nFicou alinhado que o próximo passo é um scoping mais objetivo para fechar:\r\n\r\nstack final do e-commerce (Shopify permanece como caminho provável),\r\n\r\ndefinição da coleção/quantidade de SKUs para treino do vendedor,\r\n\r\ntom de voz/persona da marca,\r\n\r\njornada de compra e canais (online + bazares).\r\n\r\nApós esse scoping, inovAI.lab envia cronograma fechado e Silvio decide pacote/módulos para kickoff.	2025-12-02 17:54:28.844853
22	8	Ligação 4/12. Rachel retornou solicitando para colocar o projeto para Janeiro. Eles estão implementando um novo ERP e precisam definir antes alguns fluxos, para dar sequencia a nossa implantação. 	2025-12-04 16:02:20.600304
23	21	Segunda reuniao realizada. Agora é necessário pegar a transcrição e montar a proposta, o cronograma e a documentação 3 etapas sugeridas pelo cliente. 	2025-12-05 19:53:54.767448
24	10	Enviado mensagem para o Gustavo pedindo a reunião tecnica com o time dele. 	2025-12-11 16:46:33.363425
25	20	Proposta abaixo enviada para a Luiza. \r\n\r\nPROPOSTA TÉCNICA E COMERCIAL\r\nPlataforma de Distribuição de Conteúdo Educacional + IA Tutora\r\nProposta apresentada por: inovAI.lab\r\nCliente: Grupo Salta / Ensino Elite\r\nData: (preencher quando for enviar)\r\n1. Introdução\r\n\r\nO Grupo Salta, por meio do Ensino Elite, manifestou a necessidade de uma plataforma própria e profissional para organizar, distribuir e monitorar conteúdos educacionais voltados para os segmentos:\r\n\r\nPré-vestibular (ENEM, UERJ, Unicamp, outros)\r\n\r\nSegmento Militar\r\n\r\nTrilhas especializadas com conteúdos extras pagos ou exclusivos\r\n\r\nAtualmente, a distribuição ocorre via Google Sites + links de Drive, formato considerado internamente como amador, limitado e sem escalabilidade, conforme mencionado pela liderança educacional na reunião.\r\n\r\nA inovAI.lab apresenta, abaixo, a proposta de desenvolvimento de uma plataforma robusta, moderna e escalável, com opção de IA Tutora personalizada, construída com arquitetura preparada para integração futura com o sistema Atlas.\r\n\r\n2. Objetivos do Projeto\r\n2.1 Objetivos Principais\r\n\r\nProfissionalizar a distribuição de conteúdo do Elite.\r\n\r\nGarantir segurança e proteção de vídeos e materiais.\r\n\r\nCriar trilhas segmentadas conforme tipo de prova e produto contratado.\r\n\r\nDisponibilizar uma área do aluno e uma área administrativa completa.\r\n\r\nObter analytics reais de aprendizado e engajamento.\r\n\r\nEstabelecer base tecnológica para futuras integrações com o Atlas.\r\n\r\n2.2 Objetivos Opcionais (Pacote 2)\r\n\r\nImplementar IA Tutora alinhada aos materiais exclusivos do Elite.\r\n\r\nOferecer explicações personalizadas, suporte ao aluno, correção de questões e recomendações de estudo.\r\n\r\nDisponibilizar dashboards de inteligência de aprendizagem para coordenação.\r\n\r\n3. Escopo da Solução\r\n\r\nA inovAI.lab desenvolverá a plataforma em duas modalidades de entrega, conforme detalhamento abaixo.\r\n\r\n4. PACOTE 1 – Plataforma Essencial (MVP Profissional)\r\nValor Total: R$ 35.000,00\r\nPrazo estimado: 8 a 10 semanas\r\n4.1 Módulo do Aluno\r\n\r\nLogin individual com autenticação segura\r\n\r\nPainel personalizado por segmento (ENEM / Militar / Trilhas específicas)\r\n\r\nAcesso a aulas, materiais e simulados\r\n\r\nPlayer interno protegido contra download\r\n\r\nHistórico de progresso e conteúdos marcados como concluídos\r\n\r\n4.2 Módulo Administrativo\r\n\r\nUpload de vídeos e materiais complementares\r\n\r\nCriação e organização de trilhas por turma, tema e tipo de prova\r\n\r\nGestão de usuários e permissões\r\n\r\nPainel simples de engajamento\r\n\r\n4.3 Analytics Essenciais\r\n\r\nVisualizações por conteúdo\r\n\r\nAcesso por aluno\r\n\r\nProgresso individual e por trilha\r\n\r\nExportação de relatórios (CSV/Excel)\r\n\r\n4.4 Arquitetura e Tecnologia\r\n\r\nInfraestrutura escalável (AWS, GCP ou equivalente)\r\n\r\nBackend em Python/Node\r\n\r\nFrontend responsivo\r\n\r\nBanco de dados seguro e estruturado\r\n\r\nAPI preparada para futura integração com o Atlas (SSO, sincronização e deep links)\r\n\r\n4.5 Design e UX\r\n\r\nLayout moderno e responsivo\r\n\r\nConstrução colaborativa entre inovAI.lab e equipe pedagógica\r\n\r\nManual de uso da plataforma\r\n\r\n5. PACOTE 2 – Plataforma + IA Tutora Integrada\r\nValor Total: R$ 50.000,00\r\nPrazo estimado: 12 a 14 semanas\r\n\r\n(Inclui todo o conteúdo do Pacote 1)\r\n\r\n5.1 IA Tutora Educacional\r\n\r\nExplicações guiadas sobre conteúdos do curso\r\n\r\nResolução passo a passo de dúvidas enviadas pelo aluno\r\n\r\nRecomendações personalizadas com base no perfil, trilha e histórico\r\n\r\nFerramentas de adaptação de linguagem por nível de dificuldade\r\n\r\nTreinamento da IA sobre PDFs e conteúdos específicos do Elite\r\n\r\n5.2 Anamnese de Aprendizagem\r\n\r\nDiagnóstico inicial do aluno\r\n\r\nPerfil cognitivo e estilo de estudo\r\n\r\nIdentificação de lacunas\r\n\r\n5.3 Analytics Avançados\r\n\r\nHeatmap de abandono por vídeo (minuto a minuto)\r\n\r\nRelatórios de engajamento por turma, trilha e segmento\r\n\r\nMapas de dificuldade pelos temas mais perguntados à IA\r\n\r\nDashboard estratégico para coordenação pedagógica\r\n\r\n6. Entregáveis Finais\r\nPara o Pacote 1\r\n\r\nPlataforma completa hospedada e funcionando\r\n\r\nÁreas do aluno e administrador\r\n\r\nTrilhas configuradas\r\n\r\nAnalytics essenciais\r\n\r\nDocumentação técnica e de uso\r\n\r\nPara o Pacote 2\r\n\r\nTodos os itens do Pacote 1\r\n\r\nMódulo completo de IA Tutora\r\n\r\nDashboards avançados\r\n\r\nRelatórios automáticos\r\n\r\nTreinamento da IA nos conteúdos do Elite\r\n\r\n7. Itens Não Inclusos\r\n\r\nIntegração final com o Atlas (dependente do time interno deles)\r\n\r\nProdução de conteúdo audiovisual\r\n\r\nHospedagem mensal (pode ser provisionada conforme uso)\r\n\r\nSuporte contínuo pós-entrega (pode ser contratado à parte)\r\n\r\n8. Condições Comerciais\r\nModelos de Pagamento\r\n\r\n40% na assinatura do contrato\r\n\r\n30% na entrega da primeira versão navegável\r\n\r\n30% na entrega final\r\n\r\nValidade da Proposta\r\n\r\n30 dias a partir da data de emissão\r\n\r\nGarantia\r\n\r\n90 dias de garantia técnica após entrega\r\n\r\nCorreções de bugs incluídas\r\n\r\nSolicitações de novas funcionalidades não estão incluídas\r\n\r\n9. Diferenciais da inovAI.lab\r\n\r\nMetodologia comprovada de entrega em 30 a 45 dias para automações\r\n\r\nExperiência com plataformas de ensino e implementações de IA\r\n\r\nEspecialistas em produtos educacionais orientados por dados\r\n\r\nArquitetura pensada para escalar para todo o Grupo Salta\r\n\r\nTime de engenharia certificado e com experiência em grandes sistemas\r\n\r\n10. Considerações Finais\r\n\r\nEsta solução foi desenhada para atender exatamente às dores expostas pela Luiza e pelos gestores do Elite:\r\n\r\nprofissionalizar a distribuição de conteúdo,\r\n\r\nproteger o material proprietário,\r\n\r\nelevar o engajamento dos alunos,\r\n\r\ngerar inteligência pedagógica,\r\n\r\ne preparar terreno para uma futura integração completa com o Atlas.\r\n\r\nA inovAI.lab se coloca à disposição para conduzir este projeto em parceria com o Elite, garantindo qualidade, velocidade e visão estratégica.	2025-12-11 17:07:46.579266
26	14	Fiz contato 16/12 porém está com muitas demandas pelo final de ano. Pediu para falar em janeiro.	2025-12-17 12:06:55.379632
27	15	Enviado essa documentação de projeto pra eles:\r\n\r\n\r\nCopiloto Operacional & Analítico da Rede Brasil\r\nProposto por: inovAI.lab\r\n Cliente: Rede Brasil Locadora de Veículos\r\n Versão: 1.0\r\n Status: Documento de Escopo e Arquitetura\r\n\r\n1. Visão Geral do Projeto\r\nA Rede Brasil opera hoje com um sistema de gestão robusto, porém altamente dependente de análises manuais, memória operacional e cruzamentos feitos “na cabeça” de pessoas-chave.\r\nO objetivo deste projeto é criar uma camada inteligente sobre o sistema atual, utilizando integração via API + Inteligência Artificial, para:\r\nCentralizar dados hoje dispersos\r\n\r\n\r\nAutomatizar análises críticas\r\n\r\n\r\nReduzir riscos operacionais, financeiros e jurídicos\r\n\r\n\r\nAumentar velocidade, previsibilidade e rastreabilidade das decisões\r\n\r\n\r\nO sistema não substitui o sistema atual, nem o julgamento humano — ele atua como um copiloto, organizando informações, detectando riscos e explicando cenários.\r\n\r\n2. Problema Atual (Diagnóstico)\r\nAtualmente, os processos críticos da Rede Brasil apresentam as seguintes características:\r\nDados espalhados em múltiplas telas e relatórios\r\n\r\n\r\nFalta de visão unificada (contratos × frota × manutenção × financeiro)\r\n\r\n\r\nAnálises feitas manualmente, caso a caso\r\n\r\n\r\nForte dependência de experiência individual\r\n\r\n\r\nDetecção tardia de erros, desvios e fraudes\r\n\r\n\r\nAlto custo cognitivo e operacional\r\n\r\n\r\nExemplos claros:\r\nAnálise de risco de cliente depende de interpretação manual de processos\r\n\r\n\r\nInvestigação de avarias exige reconstrução manual da linha do tempo do veículo\r\n\r\n\r\nRentabilidade por veículo não existe de forma consolidada\r\n\r\n\r\nFraudes internas só aparecem quando “algo dá errado”\r\n\r\n\r\nDisponibilidade futura é estimada de forma imprecisa\r\n\r\n\r\n\r\n3. Objetivo do Projeto\r\nCriar uma plataforma inteligente de análise e vigilância operacional, capaz de:\r\nLer todos os dados relevantes do sistema da Rede Brasil via API\r\n\r\n\r\nCorrelacionar esses dados em um modelo unificado\r\n\r\n\r\nExecutar análises automáticas e contínuas\r\n\r\n\r\nApresentar resultados de forma simples, explicável e acionável\r\n\r\n\r\n\r\n4. Princípios do Sistema\r\nSem RPA: toda integração via API\r\n\r\n\r\nIA explicável: nenhuma decisão “caixa-preta”\r\n\r\n\r\nHumano no loop: decisões críticas continuam humanas\r\n\r\n\r\nAuditoria e rastreabilidade por padrão\r\n\r\n\r\nModularidade: evolução por fases\r\n\r\n\r\nBaixa fricção operacional: não muda o fluxo atual das lojas\r\n\r\n\r\n\r\n5. Arquitetura Geral do Sistema\r\n5.1 Visão de Camadas\r\n[Sistema Rede Brasil / Autoban]\r\n           ↓ API\r\n[Camada de Integração de Dados]\r\n           ↓\r\n[Data Hub Unificado]\r\n           ↓\r\n[Motor de Regras + Anomalias]\r\n           ↓\r\n[Camada de Inteligência Artificial]\r\n           ↓\r\n[Aplicação (Dashboards, Alertas e Chat)]\r\n\r\n\r\n6. Camada 1 — Integração via API (Data Ingestion)\r\nObjetivo\r\nCapturar e atualizar continuamente todos os dados relevantes do sistema atual.\r\nFontes de dados previstas\r\nContratos\r\n\r\n\r\nClientes (PF / PJ)\r\n\r\n\r\nFrota\r\n\r\n\r\nOrdens de Serviço\r\n\r\n\r\nManutenções\r\n\r\n\r\nMultas\r\n\r\n\r\nAbastecimentos\r\n\r\n\r\nGuincho / Assistência 24h\r\n\r\n\r\nFinanceiro (receitas e despesas)\r\n\r\n\r\nAlterações de contratos\r\n\r\n\r\nHistórico de status dos veículos\r\n\r\n\r\nCaracterísticas técnicas\r\nSincronização incremental\r\n\r\n\r\nVersionamento de registros\r\n\r\n\r\nLog de alterações (audit trail)\r\n\r\n\r\nTratamento de inconsistências do sistema de origem\r\n\r\n\r\n\r\n7. Camada 2 — Data Hub Unificado\r\nObjetivo\r\nTransformar tabelas isoladas em uma base relacional inteligente.\r\nChaves principais\r\nID do veículo\r\n\r\n\r\nPlaca\r\n\r\n\r\nID do contrato\r\n\r\n\r\nID do cliente\r\n\r\n\r\nLoja\r\n\r\n\r\nDatas (início, fim, eventos)\r\n\r\n\r\nStatus\r\n\r\n\r\nBenefícios\r\nPermite cruzamentos complexos\r\n\r\n\r\nResolve lacunas de visão do sistema atual\r\n\r\n\r\nBase para análises históricas e preditivas\r\n\r\n\r\n\r\n8. Camada 3 — Motor de Regras e Anomalias\r\nObjetivo\r\nAutomatizar análises que hoje são feitas manualmente.\r\nTipos de regras\r\nDeterminísticas\r\nKm rodado sem registro de uso produtivo\r\n\r\n\r\nCarro ativo sem contrato\r\n\r\n\r\nOS aberta acima do tempo padrão\r\n\r\n\r\nContratos alterados retroativamente fora de padrão\r\n\r\n\r\nEstatísticas / Anomalias\r\nDesvio de padrão por loja\r\n\r\n\r\nDesvio por fornecedor\r\n\r\n\r\nFrequência anormal de manutenção\r\n\r\n\r\nCustos fora da curva por veículo ou contrato\r\n\r\n\r\n\r\n9. Camada 4 — Inteligência Artificial\r\nPapel da IA\r\nA IA não decide sozinha. Ela:\r\nResume dados\r\n\r\n\r\nExplica cenários\r\n\r\n\r\nPrioriza riscos\r\n\r\n\r\nSugere hipóteses\r\n\r\n\r\nOrganiza investigações\r\n\r\n\r\nPrincipais funções\r\nGeração de relatórios explicativos\r\n\r\n\r\nClassificação assistida de risco\r\n\r\n\r\nReconstrução automática de linhas do tempo\r\n\r\n\r\nDetecção contextual de inconsistências\r\n\r\n\r\nInterface conversacional com dados\r\n\r\n\r\n\r\n10. Módulos Funcionais do Sistema\r\n\r\nMódulo 1 — Copiloto de Cadastro e Risco de Cliente\r\nEntrada\r\nCliente (PF / PJ)\r\n\r\n\r\nModalidade (diária / mensal)\r\n\r\n\r\nDados cadastrais\r\n\r\n\r\nResultado de análise externa (CPF)\r\n\r\n\r\nSaída\r\nClassificação de risco\r\n\r\n\r\nResumo do histórico relevante\r\n\r\n\r\nPontos de atenção\r\n\r\n\r\nSugestão de decisão (aprovar / segurar / recusar)\r\n\r\n\r\nJustificativa rastreável\r\n\r\n\r\nBenefícios\r\nPadronização\r\n\r\n\r\nRedução de erro humano\r\n\r\n\r\nSegurança jurídica\r\n\r\n\r\nVelocidade de resposta\r\n\r\n\r\n\r\nMódulo 2 — Detetive de Avarias e Danos\r\nEntrada\r\nPlaca ou ID do veículo\r\n\r\n\r\nOrçamento ou OS\r\n\r\n\r\nProcessamento\r\nVarredura de todas as tabelas relacionadas\r\n\r\n\r\nReconstrução da linha do tempo\r\n\r\n\r\nIdentificação de janelas prováveis do dano\r\n\r\n\r\nSaída\r\nLinha do tempo visual\r\n\r\n\r\nContratos candidatos\r\n\r\n\r\nInconsistências detectadas\r\n\r\n\r\nSugestão de ação (cobrar / rachar / assumir)\r\n\r\n\r\n\r\nMódulo 3 — Cruzamento Contratos × Frota × Manutenção\r\nFunções\r\nIdentificar gargalos\r\n\r\n\r\nDetectar veículos parados indevidamente\r\n\r\n\r\nMonitorar OS abertas\r\n\r\n\r\nExpor causas reais de indisponibilidade\r\n\r\n\r\n\r\nMódulo 4 — Fraudes e Desvios Operacionais\r\nDetecta\r\nUso indevido de veículos\r\n\r\n\r\nKm inconsistentes\r\n\r\n\r\nAlterações suspeitas\r\n\r\n\r\nProcessos fora do fluxo\r\n\r\n\r\nAtua como\r\nSistema de vigilância contínua\r\n\r\n\r\nFila de investigação priorizada\r\n\r\n\r\n\r\nMódulo 5 — Disponibilidade Futura e Risco de Perda de Venda\r\nAnalisa\r\nReservas abertas\r\n\r\n\r\nHistórico de renovação\r\n\r\n\r\nContratos mensais vs diários\r\n\r\n\r\nSazonalidade\r\n\r\n\r\nResultado\r\nPrevisão realista de disponibilidade\r\n\r\n\r\nAlertas antecipados\r\n\r\n\r\nSuporte à decisão de remanejamento de frota\r\n\r\n\r\n\r\nMódulo 6 — Rentabilidade por Veículo e por Contrato\r\nConsolida\r\nReceita total\r\n\r\n\r\nCustos diretos\r\n\r\n\r\nCustos indiretos\r\n\r\n\r\nTempo parado\r\n\r\n\r\nEntrega\r\nRentabilidade por placa\r\n\r\n\r\nRentabilidade por contrato\r\n\r\n\r\nAnálise histórica de ROI\r\n\r\n\r\n\r\n11. Interface do Sistema\r\n11.1 Dashboards\r\nVisão executiva\r\n\r\n\r\nVisão operacional\r\n\r\n\r\nVisão financeira\r\n\r\n\r\nVisão de risco\r\n\r\n\r\n11.2 Central de Alertas\r\nAlertas priorizados\r\n\r\n\r\nStatus de investigação\r\n\r\n\r\nHistórico de decisões\r\n\r\n\r\n11.3 Chat Inteligente\r\nExemplos:\r\n“Faz uma varredura completa desse carro”\r\n\r\n\r\n“Quais contratos estão com maior risco hoje?”\r\n\r\n\r\n“Por que esse veículo está dando prejuízo?”\r\n\r\n	2025-12-17 15:19:10.201544
28	21	Enviado essa documentação do projeto pra eles:\r\n\r\nDOCUMENTO OFICIAL DE DESCRIÇÃO\r\nDO PROJETO\r\nAplicação inovAI.lab — Solução Integrada de Pesquisa, Estruturação de\r\nDados e Inteligência Institucional\r\nCliente: Charles River\r\nVersão: 1.0 — Para validação de escopo antes da proposta comercial\r\n\r\n1. Introdução\r\nO Charles River atua em um contexto de alta complexidade analítica, onde velocidade,\r\nprecisão e memória institucional são fatores determinantes de competitividade.\r\nO processo natural de investimento da casa depende de três movimentos fundamentais:\r\n1. Exploração ampla de temas e abertura de teses\r\n2. Estruturação e normalização de dados profundos, especialmente provenientes\r\nde relatórios financeiros complexos\r\n3. Tomada de decisão suportada por histórico, padrões e aprendizados\r\nacumulados\r\n\r\nHoje, parte crítica desse fluxo é realizada de forma manual, descentralizada e dependente\r\nda memória individual dos analistas, o que gera lentidão, inconsistência e perda de\r\nconhecimento.\r\nA inovAI.lab propõe uma solução completa para transformar este fluxo, criando um sistema\r\nintegrado que acelera pesquisas, estrutura dados, preserva conhecimento e habilita\r\ninteligência institucional contínua.\r\nEste documento tem como objetivo formalizar o escopo funcional, técnico e conceitual\r\ndo projeto, antes da apresentação da proposta comercial final.\r\n\r\n2. Objetivo Geral da Solução\r\nA aplicação inovAI.lab tem quatro objetivos principais:\r\n● Reduzir tempo e custo operacional em atividades de pesquisa e extração de\r\ndados.\r\n● Transformar conhecimento disperso em memória institucional estruturada,\r\npesquisável e reutilizável.\r\n● Criar um ciclo contínuo de aprendizado que fortalece o processo de investimento\r\na cada uso.\r\n● Estabelecer as bases para o desenvolvimento de um super agente conselheiro,\r\ncapaz de apoiar o comitê com análises e provocações inteligentes.\r\n\r\n3. Dores Estratégicas Identificadas\r\n3.1. Dor 1 — Pesquisa profunda e abertura de teses\r\nProblema:\r\nAs pesquisas temáticas iniciais são produzidas de forma artesanal, desconectada e não\r\nreaproveitada.\r\nImpactos:\r\n● Lentidão para abrir teses\r\n● Duplicidade de esforços\r\n● Perda de inteligência acumulada\r\n\r\nNecessidade:\r\nRealizar deep research rápida, integrada e reutilizável, transformando pesquisas em\r\nativos institucionais.\r\n\r\n3.2. Dor 2 — Extração de dados financeiros complexos\r\n\r\nProblema:\r\nRelatórios como ITR, Formulário de Referência e Notas Explicativas apresentam formatos\r\ninconsistentes e tabelas fragmentadas, tornando a extração manual demorada e suscetível\r\na erros.\r\nImpactos:\r\n● Dois ou mais dias de trabalho por relatório\r\n● Risco elevado de inconsistências\r\n● Gargalo operacional recorrente\r\n\r\nNecessidade:\r\nTransformar PDFs complexos em bases estruturadas, normalizadas e validadas,\r\nprontas para análise.\r\n\r\n3.3. Dor 3 — Inteligência institucional e apoio à decisão\r\nProblema:\r\nO conhecimento acumulado ao longo dos anos está distribuído em documentos, planilhas,\r\nanotações e na cabeça das pessoas.\r\nImpactos:\r\n● Risco de repetir erros passados\r\n● Redução da consistência analítica\r\n● Perda de histórico com rotatividade\r\n\r\nNecessidade:\r\nCriar um agente institucional capaz de entender o estilo da casa, identificar padrões e\r\napoiar o comitê com análises profundas.\r\n\r\n4. Estratégia de Solução: Etapas Progressivas e\r\nConectadas\r\nAs dores não são isoladas — elas formam um fluxo único.\r\nPor isso, a solução foi estruturada em três etapas cumulativas, que constroem\r\nprogressivamente a inteligência do sistema.\r\n\r\nEtapa Resultado Principal\r\nEtapa 1 Criação do esqueleto de memória institucional\r\nEtapa 2 Alimentação contínua desse esqueleto com dados confíaveis\r\nEtapa 3 Transformação disso em inteligência institucional e apoio\r\n\r\nestratégico\r\n\r\nO valor máximo emerge na conexão entre as três fases.\r\n\r\n5. Etapa 1 — Módulo de Pesquisa Profunda Temática\r\n(Deep Research)\r\nDescrição Geral\r\nUm módulo que permite ao analista definir um tema amplo, enquanto a aplicação executa\r\numa pesquisa profunda multiagente, utilizando motores externos avançados (como Manus).\r\nA saída é automaticamente organizada e armazenada no banco de conhecimento da casa.\r\nFluxo Operacional\r\n1. Definição do tema, pergunta central, recorte e formato desejado\r\n2. Orquestração da pesquisa via motor especializado\r\n3. Organização automática dos conteúdos em blocos estruturados\r\n4. Revisão e complementação pelo analista\r\n5. Armazenamento versionado no repositório institucional\r\n\r\nJustificativa Técnica\r\nMesmo com motores externos, o valor real está na organização e persistência do\r\nconhecimento:\r\n● Criação de memória institucional\r\n● Redução de retrabalho\r\n● Evolução de templates e prompts\r\n\r\n● Preparação para o agente conselheiro\r\n\r\nEntregáveis\r\n● Módulo completo de deep research\r\n● Biblioteca de prompts e templates\r\n● Banco versionado de pesquisas\r\n● Painel de histórico, temas e hipóteses\r\n\r\n6. Etapa 2 — Módulo de Extração Inteligente de PDFs\r\nDescrição Geral\r\nUma ferramenta que processa PDFs complexos, executando OCR, leitura de tabelas,\r\nnormalização semântica e montagem automática de bases estruturadas no padrão do\r\nCharles River.\r\nFluxo Operacional\r\n1. Upload dos PDFs\r\n2. Escolha opcional de template de extração\r\n3. Processamento técnico: OCR → extração → normalização\r\n4. Apresentação de incertezas para validação humana\r\n5. Armazenamento versionado da base resultante\r\n\r\nPor que é a segunda etapa\r\n● A Etapa 1 estabelece estrutura e semântica\r\n● A Etapa 2 alimenta essa estrutura com dados concretos, confiáveis e recorrentes\r\n\r\nEntregáveis\r\n\r\n● Módulo de processamento de PDFs\r\n● Pipeline de OCR + extração + validação\r\n● Templates específicos para relatórios financeiros\r\n● Histórico estruturado trimestral\r\n\r\n7. Etapa 3 — Super Agente Conselheiro Institucional\r\nVisão Geral\r\nUm agente que evolui progressivamente até se tornar um conselheiro capaz de:\r\n● compreender a tese da casa;\r\n● comparar novas ideias com padrões históricos;\r\n● alertar sobre riscos e repetições;\r\n● sugerir oportunidades coerentes com o estilo do fundo.\r\n\r\nArquitetura Evolutiva\r\nFase 3A — Versão Inicial (v1)\r\n● Uso dos dados estruturados das Etapas 1 e 2\r\n● Geração de análises comparativas e relatórios\r\n\r\nFase 3B — Normalização do Legado\r\n● Ingestão de planilhas, relatórios antigos e memórias de comitê\r\n● Ampliação da profundidade histórica do modelo\r\n\r\nFase 3C — Crescimento Guiado por Feedback\r\nO desempenho do conselheiro evolui com:\r\n● feedback da equipe\r\n\r\n● exemplos reais\r\n● correções de raciocínio\r\n● exposição a casos concretos\r\n\r\nAssim como um analista humano, o agente aprende pelo uso.\r\nEntregáveis\r\n● Agente conselheiro v1\r\n● Painel de comparações, provocações e alertas\r\n● Pipelines contínuos de ingestão e aprendizado\r\n● Roadmap de evolução (v2, v3, v4...)\r\n\r\n8. O Loop de Conhecimento — A Inteligência\r\nCumulativa\r\nA solução cria um ciclo virtuoso:\r\n1. Pesquisa (Etapa 1) gera insights e hipóteses\r\n2. Dados (Etapa 2) validam e enriquecem essas hipóteses\r\n3. Conselheiro (Etapa 3) analisa padrões e provoca novas perguntas\r\n4. As novas perguntas alimentam novas pesquisas\r\n\r\nQuanto mais o fundo usa o sistema, mais o sistema aprende sobre o fundo.\r\nE quanto mais ele aprende, mais valioso se torna para o processo decisório.\r\n\r\n9. Benefícios Estratégicos da Solução\r\n● Abertura de teses: de dias para horas\r\n● Redução massiva de retrabalho e custo operacional\r\n\r\n● Minimização de erros humanos\r\n● Rastreabilidade e consistência de dados\r\n● Preservação do conhecimento institucional\r\n● Inteligência cumulativa alinhada ao estilo do Charles River\r\n● Suporte direto à tomada de decisão estratégica\r\n\r\n10. Considerações Finais\r\nA solução aqui descrita não responde apenas às dores atuais — ela eleva estruturalmente\r\no processo de investimento do Charles River para um novo patamar de inteligência,\r\nvelocidade e consistência.\r\nA inovAI.lab está pronta para conduzir esse projeto de forma técnica, estratégica e\r\nprofunda, garantindo entrega de valor em cada etapa.	2025-12-17 15:20:44.660395
29	21	Enviado essa documentação do projeto pra eles:\r\n\r\nDOCUMENTO OFICIAL DE DESCRIÇÃO\r\nDO PROJETO\r\nAplicação inovAI.lab — Solução Integrada de Pesquisa, Estruturação de\r\nDados e Inteligência Institucional\r\nCliente: Charles River\r\nVersão: 1.0 — Para validação de escopo antes da proposta comercial\r\n\r\n1. Introdução\r\nO Charles River atua em um contexto de alta complexidade analítica, onde velocidade,\r\nprecisão e memória institucional são fatores determinantes de competitividade.\r\nO processo natural de investimento da casa depende de três movimentos fundamentais:\r\n1. Exploração ampla de temas e abertura de teses\r\n2. Estruturação e normalização de dados profundos, especialmente provenientes\r\nde relatórios financeiros complexos\r\n3. Tomada de decisão suportada por histórico, padrões e aprendizados\r\nacumulados\r\n\r\nHoje, parte crítica desse fluxo é realizada de forma manual, descentralizada e dependente\r\nda memória individual dos analistas, o que gera lentidão, inconsistência e perda de\r\nconhecimento.\r\nA inovAI.lab propõe uma solução completa para transformar este fluxo, criando um sistema\r\nintegrado que acelera pesquisas, estrutura dados, preserva conhecimento e habilita\r\ninteligência institucional contínua.\r\nEste documento tem como objetivo formalizar o escopo funcional, técnico e conceitual\r\ndo projeto, antes da apresentação da proposta comercial final.\r\n\r\n2. Objetivo Geral da Solução\r\nA aplicação inovAI.lab tem quatro objetivos principais:\r\n● Reduzir tempo e custo operacional em atividades de pesquisa e extração de\r\ndados.\r\n● Transformar conhecimento disperso em memória institucional estruturada,\r\npesquisável e reutilizável.\r\n● Criar um ciclo contínuo de aprendizado que fortalece o processo de investimento\r\na cada uso.\r\n● Estabelecer as bases para o desenvolvimento de um super agente conselheiro,\r\ncapaz de apoiar o comitê com análises e provocações inteligentes.\r\n\r\n3. Dores Estratégicas Identificadas\r\n3.1. Dor 1 — Pesquisa profunda e abertura de teses\r\nProblema:\r\nAs pesquisas temáticas iniciais são produzidas de forma artesanal, desconectada e não\r\nreaproveitada.\r\nImpactos:\r\n● Lentidão para abrir teses\r\n● Duplicidade de esforços\r\n● Perda de inteligência acumulada\r\n\r\nNecessidade:\r\nRealizar deep research rápida, integrada e reutilizável, transformando pesquisas em\r\nativos institucionais.\r\n\r\n3.2. Dor 2 — Extração de dados financeiros complexos\r\n\r\nProblema:\r\nRelatórios como ITR, Formulário de Referência e Notas Explicativas apresentam formatos\r\ninconsistentes e tabelas fragmentadas, tornando a extração manual demorada e suscetível\r\na erros.\r\nImpactos:\r\n● Dois ou mais dias de trabalho por relatório\r\n● Risco elevado de inconsistências\r\n● Gargalo operacional recorrente\r\n\r\nNecessidade:\r\nTransformar PDFs complexos em bases estruturadas, normalizadas e validadas,\r\nprontas para análise.\r\n\r\n3.3. Dor 3 — Inteligência institucional e apoio à decisão\r\nProblema:\r\nO conhecimento acumulado ao longo dos anos está distribuído em documentos, planilhas,\r\nanotações e na cabeça das pessoas.\r\nImpactos:\r\n● Risco de repetir erros passados\r\n● Redução da consistência analítica\r\n● Perda de histórico com rotatividade\r\n\r\nNecessidade:\r\nCriar um agente institucional capaz de entender o estilo da casa, identificar padrões e\r\napoiar o comitê com análises profundas.\r\n\r\n4. Estratégia de Solução: Etapas Progressivas e\r\nConectadas\r\nAs dores não são isoladas — elas formam um fluxo único.\r\nPor isso, a solução foi estruturada em três etapas cumulativas, que constroem\r\nprogressivamente a inteligência do sistema.\r\n\r\nEtapa Resultado Principal\r\nEtapa 1 Criação do esqueleto de memória institucional\r\nEtapa 2 Alimentação contínua desse esqueleto com dados confíaveis\r\nEtapa 3 Transformação disso em inteligência institucional e apoio\r\n\r\nestratégico\r\n\r\nO valor máximo emerge na conexão entre as três fases.\r\n\r\n5. Etapa 1 — Módulo de Pesquisa Profunda Temática\r\n(Deep Research)\r\nDescrição Geral\r\nUm módulo que permite ao analista definir um tema amplo, enquanto a aplicação executa\r\numa pesquisa profunda multiagente, utilizando motores externos avançados (como Manus).\r\nA saída é automaticamente organizada e armazenada no banco de conhecimento da casa.\r\nFluxo Operacional\r\n1. Definição do tema, pergunta central, recorte e formato desejado\r\n2. Orquestração da pesquisa via motor especializado\r\n3. Organização automática dos conteúdos em blocos estruturados\r\n4. Revisão e complementação pelo analista\r\n5. Armazenamento versionado no repositório institucional\r\n\r\nJustificativa Técnica\r\nMesmo com motores externos, o valor real está na organização e persistência do\r\nconhecimento:\r\n● Criação de memória institucional\r\n● Redução de retrabalho\r\n● Evolução de templates e prompts\r\n\r\n● Preparação para o agente conselheiro\r\n\r\nEntregáveis\r\n● Módulo completo de deep research\r\n● Biblioteca de prompts e templates\r\n● Banco versionado de pesquisas\r\n● Painel de histórico, temas e hipóteses\r\n\r\n6. Etapa 2 — Módulo de Extração Inteligente de PDFs\r\nDescrição Geral\r\nUma ferramenta que processa PDFs complexos, executando OCR, leitura de tabelas,\r\nnormalização semântica e montagem automática de bases estruturadas no padrão do\r\nCharles River.\r\nFluxo Operacional\r\n1. Upload dos PDFs\r\n2. Escolha opcional de template de extração\r\n3. Processamento técnico: OCR → extração → normalização\r\n4. Apresentação de incertezas para validação humana\r\n5. Armazenamento versionado da base resultante\r\n\r\nPor que é a segunda etapa\r\n● A Etapa 1 estabelece estrutura e semântica\r\n● A Etapa 2 alimenta essa estrutura com dados concretos, confiáveis e recorrentes\r\n\r\nEntregáveis\r\n\r\n● Módulo de processamento de PDFs\r\n● Pipeline de OCR + extração + validação\r\n● Templates específicos para relatórios financeiros\r\n● Histórico estruturado trimestral\r\n\r\n7. Etapa 3 — Super Agente Conselheiro Institucional\r\nVisão Geral\r\nUm agente que evolui progressivamente até se tornar um conselheiro capaz de:\r\n● compreender a tese da casa;\r\n● comparar novas ideias com padrões históricos;\r\n● alertar sobre riscos e repetições;\r\n● sugerir oportunidades coerentes com o estilo do fundo.\r\n\r\nArquitetura Evolutiva\r\nFase 3A — Versão Inicial (v1)\r\n● Uso dos dados estruturados das Etapas 1 e 2\r\n● Geração de análises comparativas e relatórios\r\n\r\nFase 3B — Normalização do Legado\r\n● Ingestão de planilhas, relatórios antigos e memórias de comitê\r\n● Ampliação da profundidade histórica do modelo\r\n\r\nFase 3C — Crescimento Guiado por Feedback\r\nO desempenho do conselheiro evolui com:\r\n● feedback da equipe\r\n\r\n● exemplos reais\r\n● correções de raciocínio\r\n● exposição a casos concretos\r\n\r\nAssim como um analista humano, o agente aprende pelo uso.\r\nEntregáveis\r\n● Agente conselheiro v1\r\n● Painel de comparações, provocações e alertas\r\n● Pipelines contínuos de ingestão e aprendizado\r\n● Roadmap de evolução (v2, v3, v4...)\r\n\r\n8. O Loop de Conhecimento — A Inteligência\r\nCumulativa\r\nA solução cria um ciclo virtuoso:\r\n1. Pesquisa (Etapa 1) gera insights e hipóteses\r\n2. Dados (Etapa 2) validam e enriquecem essas hipóteses\r\n3. Conselheiro (Etapa 3) analisa padrões e provoca novas perguntas\r\n4. As novas perguntas alimentam novas pesquisas\r\n\r\nQuanto mais o fundo usa o sistema, mais o sistema aprende sobre o fundo.\r\nE quanto mais ele aprende, mais valioso se torna para o processo decisório.\r\n\r\n9. Benefícios Estratégicos da Solução\r\n● Abertura de teses: de dias para horas\r\n● Redução massiva de retrabalho e custo operacional\r\n\r\n● Minimização de erros humanos\r\n● Rastreabilidade e consistência de dados\r\n● Preservação do conhecimento institucional\r\n● Inteligência cumulativa alinhada ao estilo do Charles River\r\n● Suporte direto à tomada de decisão estratégica\r\n\r\n10. Considerações Finais\r\nA solução aqui descrita não responde apenas às dores atuais — ela eleva estruturalmente\r\no processo de investimento do Charles River para um novo patamar de inteligência,\r\nvelocidade e consistência.\r\nA inovAI.lab está pronta para conduzir esse projeto de forma técnica, estratégica e\r\nprofunda, garantindo entrega de valor em cada etapa.	2025-12-17 15:20:57.644375
30	28	Proposta comercial enviada para o Eric\r\n\r\nProposta de Desenvolvimento de Sistema de Saúde Corporativa – 010/25\r\nCliente: Eric Reis\r\n Empresa: Coer\r\n Email: ericreis_49@hotmail.com\r\n Telefone: (21) 99500-5534\r\n\r\n1. Objetivo\r\nDesenvolver um Sistema Web de Saúde Corporativa para atender empresas clientes do consultório, permitindo a gestão administrativa, o trabalho dos profissionais de saúde e a participação ativa dos usuários (colaboradores das empresas).\r\nO sistema terá como foco a aplicação de formulários por ciclos periódicos, possibilitando o acompanhamento estruturado da evolução dos colaboradores ao longo do tempo, além de oferecer transparência ao próprio usuário sobre seus resultados e progresso.\r\n A arquitetura será desenvolvida de forma modular, preparada para expansões futuras.\r\n\r\n2. Escopo das Entregas – Sistema Inicial\r\n2.1 Perfis de Acesso\r\nO sistema contará com três níveis de acesso distintos:\r\nAdministrador:\r\n Responsável pela gestão completa do sistema, incluindo cadastro de empresas, profissionais, usuários, formulários, definição de ciclos, permissões e configurações gerais.\r\nProfissionais de Saúde:\r\n Acesso aos formulários, respostas e dados dos usuários atendidos, com visualização do histórico, resultados e evolução ao longo do tempo, permitindo acompanhamento clínico e análises comparativas entre ciclos.\r\nUsuários (Colaboradores):\r\n Preenchimento dos formulários conforme os ciclos definidos e acesso ao seu próprio acompanhamento, podendo visualizar seus resultados, histórico e evolução de forma clara, organizada e contínua.\r\n\r\n2.2 Cadastro de Empresas\r\nCadastro das empresas clientes do consultório.\r\n\r\n\r\nVinculação de profissionais de saúde a cada empresa.\r\n\r\n\r\nVinculação de usuários (colaboradores) às respectivas empresas.\r\n\r\n\r\n\r\n2.3 Cadastro de Profissionais\r\nCadastro individual dos profissionais de saúde.\r\n\r\n\r\nAssociação de formulários específicos por profissional.\r\n\r\n\r\nControle dos usuários atendidos por cada profissional.\r\n\r\n\r\n\r\n2.4 Sistema de Formulários\r\nFormulário Inicial (Cadastro Base):\r\n Formulário configurável, podendo ser definido pelo administrador ou profissional para:\r\nPreenchimento único (uma única vez), ou\r\n\r\n\r\nPreenchimento recorrente por ciclos, conforme a estratégia de acompanhamento adotada.\r\n\r\n\r\nFormulários por Ciclo:\r\nCriados pelos profissionais de saúde.\r\n\r\n\r\nAplicados periodicamente aos usuários.\r\n\r\n\r\nUtilizados para análise da evolução individual ao longo do tempo.\r\n\r\n\r\n\r\n2.5 Histórico e Evolução\r\nArmazenamento estruturado do histórico de respostas dos usuários.\r\n\r\n\r\nComparação de dados entre diferentes ciclos.\r\n\r\n\r\nVisualização da evolução tanto para profissionais quanto para os próprios usuários.\r\n\r\n\r\nBase de dados preparada para geração de relatórios e análises futuras.\r\n\r\n\r\n\r\n3. Cronograma Estimado\r\nPrazo estimado para desenvolvimento e implantação do sistema inicial:\r\n até 2 meses, incluindo desenvolvimento, testes e ajustes finais.\r\n\r\n4. Benefícios Esperados\r\nCentralização da gestão administrativa e operacional.\r\n\r\n\r\nMelhor organização dos atendimentos por empresa e por profissional.\r\n\r\n\r\nRedução de controles manuais e processos descentralizados.\r\n\r\n\r\nAcompanhamento estruturado da evolução dos colaboradores.\r\n\r\n\r\nTransparência para os usuários sobre seus próprios resultados e progresso.\r\n\r\n\r\nBase tecnológica preparada para crescimento e novas funcionalidades.\r\n\r\n\r\n\r\n5. Valores e Condições Comerciais\r\nDesenvolvimento do sistema:\r\n R$ 10.000,00 (dez mil reais).\r\nApós a entrega e entrada em produção:\r\n Licença mensal de R$ 1.500,00, referente à manutenção, suporte técnico e evolução contínua do sistema.\r\n\r\n6. Observações\r\nO sistema será desenvolvido de forma modular, permitindo a criação de novas frentes de automação e funcionalidades conforme a evolução da parceria.\r\n\r\n\r\nAjustes de escopo poderão ser realizados durante a fase de testes, mediante alinhamento entre as partes.\r\n\r\n\r\n	2025-12-17 15:36:02.759354
31	18	Fiz contato com eles 115/12 porém não me deram retorno. Janeiro vou falar com o Mario Chady novamente.	2025-12-18 20:06:40.872661
32	25	Falei com ele dia 15/12 e confirmou que retomará o assunto em janeiro. Essa época é muito agitada para eles. Felipe Elias(sócio)	2025-12-18 20:09:54.090687
33	27	Mandei msg dia 15/1. É muito meu amigo. Pediu para marcar para Janeiro. 	2025-12-18 20:21:03.653546
34	6	Vou reforçar em janeiro.	2025-12-18 20:22:19.229646
35	5	Cris está viajando vou contactar em janeiro	2025-12-18 20:22:45.408317
36	17	Felipe, quer que eu atue neste lead? Tenho contato lá com o Renato.	2025-12-18 20:24:14.831176
37	29	Felipe quer que acompanhe e reforçe este Lead?	2025-12-18 20:25:02.568316
38	7	Pediu para retomarmos em janeiro, estão muito lotados pelo BFriday e Natal.	2025-12-18 20:28:28.161916
39	13	Vou apresentar a solução para ela semana que vem. 22/12. A ideia é pegar todas as clínicas de fisioterapia que utilizam ERP Zenfisio e oferecer o produto CRM com setup e fee mensal.	2025-12-18 20:29:52.623619
40	9	Ronald ficou de fazer treinamento com equipe da Fernanda dia 18/12, após isto o produto estará totalmente entregue. Partiremos para a segunda automação em Janeiro. 	2025-12-18 20:34:06.067671
41	8	Proposta enviada. Rachel CEO pediu que retornemos o projeto em janeiro até que termine a integração deles com o novo ERP.	2025-12-18 20:35:26.777816
42	12	Retomar o projeto de licitação. Vou marcar reunião com Amilcar	2025-12-18 20:36:28.551584
43	29	Cobrar agenda com o Vitor sobre agenda de entendimento das dores. Segunda reunião. 	2025-12-23 14:55:23.638878
44	10	Gustavo pediu para retornar o contato em Janeiro. 	2025-12-23 14:56:01.010422
45	15	Proposta fechada e aceita. Valor total de R$40.000,00, dividido em 5 parcelas R$8.000,00. Apos o desenvolvimento taxa de manutenção e operação de R$1.500,00 mensal. 	2025-12-23 14:57:42.653801
46	20	Luiza pediu para retornar o contato na virada do ano para reunião de apresentação para os gerentes e diretores do grupo salta para explanção total do projeto e do orçamento. 	2025-12-23 14:58:57.395905
47	5	Mensagem dia 6/1 para retomar o Projeto.	2026-01-06 18:11:07.426144
48	27	6/1 Contato feito para agendar uma reunião.	2026-01-06 18:13:57.511335
49	7	5/1  - reunião marcada para solução B2B com Raphael e Fabio. Apresentação e alinhamento do Design. Reunião na Agenda Inovailab	2026-01-06 18:16:13.141078
50	13	7/1 - Apresentarei a solução para as sócias. 	2026-01-06 18:19:01.413692
51	27	Reunião agendada para dia13/1	2026-01-06 18:23:03.10965
52	14	6/1 - Contato Feito com Renato para agendar reunião.	2026-01-06 18:35:08.236091
53	30	6/1 - Contato feito com Sergio Brandão, sócio para agendar reunião. Aguardando retorno.	2026-01-06 18:38:16.353238
54	8	5/1 - Contato feito com CEO Raquel, avisou que só volta dia 21/1	2026-01-06 18:39:28.116334
55	17	Enviado mensagem para o Andre sugerindo o inicios dos testes com a frente no code com o Theo. 	2026-01-06 18:45:02.416644
56	6	6/1 - Contato feito com Luiz Carvalho, para retomar os projetos.	2026-01-06 18:45:04.898856
57	17	Andre foi para outro desafio e saiu da argo plan. Estou tentando contato com o Mathues que é o outro contato que tinhamos la	2026-01-06 18:50:02.737287
58	10	Mandei nova mensagem para o Gustavo para retomarmos as conversas agora na virada do ano. 	2026-01-06 18:50:34.398605
59	21	Enviado mensagem de feliz ano novo pro Saulo e solicitando a analise do que foi enviado e a retomada do contato. 	2026-01-06 18:52:03.763879
60	20	Enviado mensagem de ano novo e sugerindo a retomada da agenda com a reunião com os gerentes envolvidos. 	2026-01-06 18:55:10.075889
61	15	Enviado mensagem de feliz ano novo e sugestão de inicio dos trabalhos. 	2026-01-06 18:56:46.768385
62	12	6/1 - Mandei mensagem para marcar reunião.	2026-01-06 18:58:57.406325
63	30	Sergio retornou volta die viagem 20, ligar dia 21/1 para ir no escritório  22 ou 23/1, conforme combinado com ele.	2026-01-06 19:03:52.167919
64	25	6/1 - Contato feito com Felipe Sócio do Hotel para marcar uma reunião.	2026-01-06 19:11:15.762747
65	14	13/1 - Obtive retorno solicitando que fale depois do carnaval, pois está se fundindo com novo escritório.	2026-01-13 18:05:53.856266
66	25	13/1 - Reunião almoço, José Faveret viajará e pediu para falar depois do Carnaval. 	2026-01-13 18:07:27.5053
67	5	14/1 - 15hs - Reunião agendada com Cris. Apresentação de oportunidades.	2026-01-13 18:08:28.978367
68	18	13/1 - Novo contato com LM do Grupo Trigo.	2026-01-13 18:09:25.271422
69	29	Segunda reunião agendada para o dia 16 de janeiro de 2026. 	2026-01-14 15:28:53.973519
70	31	Volta de férias dia 27 de janeiro de 2026. ficou de vir no escritório conhecer. 	2026-01-14 15:29:50.82989
71	17	Falei com o Matheus, que é o outro contato de lá. Ele ficou de marcar uma reunião com a Luana - CEO da Argo - para entender os proximos direcionamentos de AI da empresa. Retomar contato 	2026-01-14 15:30:56.627577
72	32	Enviado mensagem pedindo a documentação que eles ficaram de enviar com as dores que ja tinha mapeadas. 	2026-01-14 15:32:14.952033
73	33	Criar um paper completo explicando a inovai.lab e uma lista com todos os nossos cases explicados. 	2026-01-14 15:32:46.227007
74	35	Segunda reunião agendada para dsia 15 de janeiro de 2026 as 15h	2026-01-14 15:34:31.798829
75	22	Enviado mensagem pergunta o status e se esta precisando de mais alguma coisa. 	2026-01-14 15:36:03.328388
76	23	Enviado mensagem pergunta o status e se esta precisando de mais alguma coisa.	2026-01-14 15:36:36.957654
77	24	Enviado mensagem pergunta o status e se esta precisando de mais alguma coisa.	2026-01-14 15:36:50.078014
78	26	Enviado mensagem no dia 14 de janeiro de 2026 pergunta o status e se colocando a disposição qualquer duvida. 	2026-01-14 15:40:00.477981
79	5	14/1- Reunião feita com Cris e Julia, apresentamos uma solução de CRM, elas apresentaram uma dor relacionado a inserção de nota fiscal.(Julia). Vamos enviar uma ideia de orçamento. para ela apresentar para diretoria.	2026-01-15 21:39:17.349655
80	35	Enviado a documentação abaixo de sugestão do projeto:\r\n\r\n# Plataforma NR Saúde & Segurança – Documentação Completa\r\n\r\n## 1. Visão Geral\r\n\r\nA Plataforma NR Saúde & Segurança é um sistema digital completo para gestão, aplicação, análise e acompanhamento das exigências da **NR-1**, com foco especial nos **riscos psicossociais relacionados ao trabalho**.\r\n\r\nA plataforma foi pensada para substituir processos manuais, fragmentados e pouco escaláveis por um **fluxo digital contínuo**, que permita não apenas cumprir a norma, mas **prevenir adoecimentos, reduzir riscos jurídicos e apoiar a gestão das empresas**.\r\n\r\nEla atua como infraestrutura tecnológica de apoio ao trabalho técnico de clínicas de medicina do trabalho, profissionais de segurança, psicólogos organizacionais e empresas.\r\n\r\n---\r\n\r\n## 2. Objetivo da Plataforma\r\n\r\n* Cumprir a NR-1 de forma estruturada e segura\r\n* Facilitar a identificação de riscos psicossociais\r\n* Reduzir resistência de empresários\r\n* Aumentar escala operacional das clínicas\r\n* Criar histórico e rastreabilidade\r\n* Apoiar ações preventivas contínuas\r\n\r\n---\r\n\r\n## 3. Usuários da Plataforma\r\n\r\n### 3.1 Administrador (Clínica / SST)\r\n\r\n* Cadastra empresas\r\n* Define metodologias e questionários\r\n* Acompanha resultados\r\n* Gera relatórios e planos de ação\r\n* Gerencia ciclos de avaliação\r\n\r\n### 3.2 Empresa (Gestores / RH)\r\n\r\n* Visualiza resultados consolidados\r\n* Acompanha planos de ação\r\n* Acessa documentos obrigatórios\r\n* Não acessa dados sensíveis individuais\r\n\r\n### 3.3 Colaborador\r\n\r\n* Responde questionários\r\n* Acessa treinamentos (quando aplicável)\r\n* Pode realizar relatos/denúncias\r\n* Não visualiza dados coletivos\r\n\r\n---\r\n\r\n## 4. Arquitetura Geral da Plataforma\r\n\r\nA plataforma é organizada em **módulos independentes**, permitindo ativação progressiva conforme a maturidade do cliente.\r\n\r\nMódulos:\r\n\r\n1. Gestão de Empresas\r\n2. Gestão de Colaboradores\r\n3. Avaliação NR-1 (Riscos Psicossociais)\r\n4. Interpretação e Diagnóstico\r\n5. Relatórios e Planos de Ação\r\n6. Acompanhamento Contínuo\r\n7. Canal de Relatos e Incidentes\r\n8. Treinamentos e Compliance\r\n9. Inteligência e Personalização\r\n\r\n---\r\n\r\n## 5. Módulo 1 – Gestão de Empresas\r\n\r\nFuncionalidades:\r\n\r\n* Cadastro de empresa\r\n* Segmento de atuação\r\n* Porte\r\n* Estrutura organizacional\r\n* Setores e áreas\r\n* Histórico de avaliações\r\n\r\nEsse módulo cria o contexto necessário para análise correta dos riscos.\r\n\r\n---\r\n\r\n## 6. Módulo 2 – Gestão de Colaboradores\r\n\r\nFuncionalidades:\r\n\r\n* Importação ou cadastro indireto\r\n* Associação a setores\r\n* Identificador anônimo\r\n* Gestão de convites\r\n\r\nPrincípios:\r\n\r\n* LGPD by design\r\n* Anonimato\r\n* Resultados sempre agregados\r\n\r\n---\r\n\r\n## 7. Módulo 3 – Avaliação NR-1 (Riscos Psicossociais)\r\n\r\n### 7.1 Metodologia\r\n\r\nA plataforma utiliza exclusivamente **instrumentos reconhecidos pelo Ministério do Trabalho**, como o HSR.\r\n\r\nNão há criação de metodologias próprias.\r\n\r\n### 7.2 Aplicação\r\n\r\n* Questionários digitais\r\n* Acesso via link\r\n* Interface simples e mobile\r\n* Tempo reduzido de resposta\r\n\r\n---\r\n\r\n## 8. Módulo 4 – Interpretação e Diagnóstico\r\n\r\nApós a coleta:\r\n\r\n* Processamento automático\r\n* Classificação por empresa e setor\r\n* Identificação de tipos de risco (ex: alta demanda, conflito de papel, pressão excessiva)\r\n* Classificação em níveis (baixo, médio, alto)\r\n\r\n---\r\n\r\n## 9. Módulo 5 – Relatórios e Planos de Ação\r\n\r\n### 9.1 Relatórios NR-1\r\n\r\nConteúdo:\r\n\r\n* Contexto da empresa\r\n* Metodologia utilizada\r\n* Diagnóstico geral\r\n* Diagnóstico por setor\r\n* Evidências\r\n\r\n### 9.2 Planos de Ação\r\n\r\n* Ações recomendadas por tipo de risco\r\n* Linguagem preventiva e não punitiva\r\n* Foco em mitigação e melhoria\r\n\r\n---\r\n\r\n## 10. Módulo 6 – Acompanhamento Contínuo\r\n\r\nFuncionalidades:\r\n\r\n* Ciclos recorrentes de avaliação\r\n* Alertas de reavaliação\r\n* Dashboards simples\r\n* Evolução histórica dos riscos\r\n\r\nObjetivo:\r\nTransformar a NR-1 em processo contínuo, não pontual.\r\n\r\n---\r\n\r\n## 11. Módulo 7 – Canal de Relatos e Incidentes\r\n\r\nFuncionalidades:\r\n\r\n* Canal de relato/denúncia\r\n* Opção anônima ou identificada\r\n* Classificação por tipo de incidente\r\n* Gestão de casos\r\n* Registro de ações e resoluções\r\n\r\nObjetivo:\r\nDar suporte prático ao plano de ação e à gestão de saúde mental.\r\n\r\n---\r\n\r\n## 12. Módulo 8 – Treinamentos e Compliance\r\n\r\nFuncionalidades:\r\n\r\n* Trilhas de treinamento\r\n* Conteúdos obrigatórios (NRs)\r\n* Conteúdos de saúde mental\r\n* Certificados\r\n* Evidências para auditoria\r\n\r\nModelo:\r\n\r\n* Ativação conforme necessidade da empresa\r\n\r\n---\r\n\r\n## 13. Módulo 9 – Inteligência e Personalização\r\n\r\nFuncionalidades:\r\n\r\n* Recomendação inteligente de ações\r\n* Planos de ação personalizados\r\n* Comunicação interna assistida\r\n* Análises de tendência de risco\r\n\r\nLimites:\r\n\r\n* Não realiza diagnóstico clínico\r\n* Não expõe indivíduos\r\n\r\n---\r\n\r\n## 14. Segurança, LGPD e Governança\r\n\r\n* Proteção de dados sensíveis\r\n* Anonimato dos colaboradores\r\n* Acesso controlado por perfil\r\n* Histórico auditável\r\n\r\n---\r\n\r\n## 15. Roadmap de Implantação\r\n\r\n### Fase 1 – Núcleo NR-1\r\n\r\n* Avaliação\r\n* Diagnóstico\r\n* Relatórios\r\n* Planos de ação\r\n\r\n### Fase 2 – Continuidade\r\n\r\n* Dashboards\r\n* Reavaliações\r\n* Histórico\r\n\r\n### Fase 3 – Compliance Ampliado\r\n\r\n* Treinamentos\r\n* Canal de relatos\r\n\r\n### Fase 4 – Inteligência\r\n\r\n* Recomendações\r\n* Personalização\r\n\r\n---\r\n\r\n## 16. Resumo Final\r\n\r\nA Plataforma NR Saúde & Segurança é uma solução completa para transformar a NR-1 em um processo digital, contínuo e preventivo.\r\n\r\nEla conecta obrigação legal, cuidado com pessoas e eficiência empresarial em um único ambiente seguro e escalável.\r\n	2026-01-17 23:26:54.852385
81	34	27/1- Enviei apresentação a pedido do cliente para agendar reunião.	2026-01-27 13:48:43.400924
82	6	27/1 - Contato feito com Luiz, me falou que um conselheiro entende muito de IA e está a frente deste assunto, pedi uma reunião com ele	2026-01-27 20:52:23.49635
83	7	27/1 - Mandei mensagem para o CEO para desenvolvermos mais soluções para a Taurus, Entrar no orçamento do ano.	2026-01-27 20:53:13.987831
84	13	27/1 - Falta  integração com o whatsapp e a sócia validar o orçamento.	2026-01-27 20:54:05.47943
85	8	27/1 - Entrei em contato com a Raquel, voltou de férias ontem. Vai verificar amanhã como está a implantação do ERP  e me retornar 	2026-01-27 20:55:49.313374
86	9	27/1 - contactei a Ana Gabriela para implementarmos a 2a etapa. Ela ficou de avaliar	2026-01-27 20:57:03.172826
\.


--
-- Data for Name: contato_files; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.contato_files (id, filename, original_name, mime_type, file_size, descricao, storage_path, created_at, contato_id, uploaded_by_id) FROM stdin;
1	8de8c844d17a4b43a27ff58e1c00e055.docx	Proposta_Automacao 1 _BR_Marinas_Inovailab.docx	application/vnd.openxmlformats-officedocument.wordprocessingml.document	98872		/home/runner/workspace/uploads/crm/contato_5/8de8c844d17a4b43a27ff58e1c00e055.docx	2026-01-19 18:30:15.288427	5	11
\.


--
-- Data for Name: contatos; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.contatos (id, nome_empresa, nome_contato, email, telefone, observacoes, estagio, data_criacao, data_atualizacao) FROM stdin;
18	Grupo Trigo	Mario/ Luis Marcelo LM	paulo@inovailab.com	11 93414-3341	Apresentar a solução feita para Spoleto Vitoria para a rede toda  do grupo Trigo. Solução caixinha petty cash	Leads Frios	2025-11-21 20:01:41.312458	2026-01-06 18:41:53.508797
9	AC Burlamaqui	Fernanda	paulo@inovailab.com	21 98326-1741	Automação dividida em 3 etapas. Primeira etapa a concluir.	VALIDAÇÃO PRODUTO	2025-11-21 17:16:35.533335	2025-11-25 13:34:39.211487
3	Br Marinas	Cristiana Snel	Paulo@inovailab.com	21 98746-5441	Primeiro contato telefone	<CrmStage Captação>	2025-11-19 19:26:53.448706	2025-11-19 19:26:53.448711
4	teste 	teste	teste@teste.com	21909888882	eteste	<CrmStage Captação>	2025-11-19 19:29:42.309207	2025-11-19 19:29:42.309211
22	B.O. do Lixo	Gelson Rodrigues	gelson@bodolixo.com	+55-21-9-9633-3793	Enviada a proposta na sexta, dia 28-11-2025	Propostas Enviadas	2025-11-29 20:19:41.638271	2025-11-29 20:19:41.638278
23	EcoRastro	Gelson Rodrigues	gelson@ecorastro.com.br	+55(21)9-96333793	Proposta enviada no sábado, dia 28-11-2025	Propostas Enviadas	2025-11-29 20:21:14.532855	2025-11-29 20:21:14.532859
6	Jockey Club	Luiz Eduardo Homem	paulo@inovailab.com	21 99572-5595	Reunião com Dir. Financeiro Roberto. Um dos presentes responsável pelo TI teve um problema sério de saúde. Estamos aguardando oportunidade para reativar o contato.	1a Reunião	2025-11-21 16:52:31.204058	2025-11-21 16:58:36.22962
7	Taurus - Urban Capacetes - 	Renato Lagden	paulo@inovailab.com	21 99620-1203	Primeira automação entregue.\r\nProjeto B2B em produção e apresentação para Equipe Taurus	Apresentação da POC	2025-11-21 16:55:45.2466	2025-11-21 16:59:27.67916
14	Renatão Advogado	Renato	paulo@inovailab.com	21 99988-2230	Primeiro contato, marcar reunião.	Captação	2025-11-21 17:31:33.109808	2025-11-21 17:31:33.109812
5	Br Marinas	Cristiana Snel	paulo@inovailab.com	21 98746-5441	Primeira reunião - apresentação da Inova e identificação de primeiras dores. Mencionou necessidade de melhoria  no check in dos barcos, CRM e melhorias na área adm financeira.	1a Reunião	2025-11-21 16:49:49.516766	2025-11-21 17:31:51.81671
17	Argo	Andre Polis	andre.pollis@argoplan.com	+55 21 99349-2013	A ArgoPlan é uma holding de administração de shopping centers (atualmente com cerca de 33 shoppings e meta de chegar a 50) que está em fase de consolidação da sua estratégia de automação e uso de IA. O André, que lidera essa frente, enxerga low-code/no-code (especialmente n8n) como peça central para ganhar velocidade e orquestrar tanto automações tradicionais quanto soluções com LLMs, em paralelo ao ecossistema Microsoft já adotado. A principal dor hoje é menos técnica e mais cultural: resistência interna, visão de tecnologia como custo e dificuldade de mostrar o ROI de automações de ponta a ponta. A empresa está num momento de “testar e provar valor” em 2025, com abertura para pilotos e testes em n8n com a inovAI.lab como parceira para estruturar roadmap, mapear automações por área e começar com casos práticos que evidenciem ganho real de eficiência.	1a Reunião	2025-11-21 17:46:40.407839	2025-11-21 17:46:40.407844
24	Arte Madeira	Gelson Rodrigues	gelson@artemadeira.com.br	+55(21)9-9633-3793	Proposta enviada no sabado, dia 29-11-2025	Propostas Enviadas	2025-11-29 20:22:24.804183	2025-11-29 20:22:24.804188
15	Rede Brasil	Paulo Nemer	paulo@inovailab.com	+552799981-1372	A RBR é uma locadora de veículos com 44 anos de operação, com processos complexos que envolvem desde o aluguel e recebimento dos carros até o faturamento e gestão de avarias. A empresa possui desafios significativos na automação e integração de processos internos, especialmente na conferência de checklists, análise de orçamentos, controle de manutenção e faturamento das locações. Outro ponto crítico é o CRM e o relacionamento comercial, onde acreditam perder oportunidades por falta de visibilidade e padronização no atendimento. Estão buscando a inovAI.lab para mapear profundamente a operação, identificar gargalos e desenvolver soluções personalizadas com IA e automações para liberar tempo, reduzir erros e aumentar receita.	Contratos Fechados	2025-11-21 17:41:26.21426	2025-12-23 14:57:47.044641
25	Hotel Janeiro	Felipe Elias	paulo@inovailab.com	21 99972-6918	Primeiro Contato para marcar 1a reunião. Ligar a partir do dia 8/12	Captação	2025-12-01 17:20:59.084378	2025-12-01 17:32:10.472692
11	Betunel	Wallace	paulo@inovailab.com	21 99988-2230	Identificação da necessidade	VALIDAÇÃO PRODUTO	2025-11-21 17:18:36.440773	2025-12-01 17:33:17.073057
12	Prudente Seguros	Amilcar	paulo@inovailab.com	21 98041-2500	Necessidade de automação para acesso a licitações e respectiva cotações.	Leads Frios	2025-11-21 17:21:37.002726	2025-12-01 17:34:50.402869
13	Inphysio	Lenita	paulo@inovailab.com	21 97986-6222	Criação de sistema de CRM integrado ao sistema Inphysio	Apresentação da POC	2025-11-21 17:22:56.381751	2025-12-01 17:35:33.677263
10	Box	Gustavo Amigo Gomes	paulo@inovailab.com	21 99988-2230	Automação na Guarda de documentos	Leads Frios	2025-11-21 17:17:46.455066	2026-01-14 15:33:20.008356
19	Villemor Amaral	Fernanda Branco	fernanda@villemoramaral.com.br	+55 21 98818-8283	Falar da solução desenvolvida para a ACBularmarqui de cadastro de processo no sistema. 	Leads Frios	2025-11-24 22:54:54.731691	2025-12-11 13:54:18.533729
8	Instituto da Criança	Rachel	paulo@inovailab.com	21 99111-6075	Projeto subsidiado pela Inovailab, Automação total do IC. Fixaremos um valor 3k mensal e entregaremos automações conforme verba mensal.\r\nReunião de apresentação do fluxo do trabalho  e alinhamento do contrato.	Propostas Enviadas	2025-11-21 17:04:46.937528	2025-12-11 14:02:32.173044
21	Charles River	Saulo Maia	smaia@charlesriver.com.br	21971497710	Reunião de conhecimento do fundo e das dores.  	Apresentação da POC	2025-11-26 15:07:22.182158	2025-12-17 15:17:46.975
26	WhatsApp-First	Flavio Silva	flavio@whatsappfirst.com	+5521981040404	Proposta para orçamento de projeto de edital da Faperj. \r\n\r\nProposta enviada:\r\n\r\n\r\nORÇAMENTO COMPLETO — Projeto 1Extra (MVP WhatsApp-First)\r\nProponente: inovAI.lab\r\n Cliente: 1Extra / Parceiros locais\r\n Objeto: desenvolvimento e implantação de MVP da plataforma 1Extra, com operação primária via WhatsApp e painel administrativo web.\r\n Valor total: R$ 185.000,00\r\n Prazo estimado: 10 a 12 semanas\r\n\r\n1. Escopo de Entrega (MVP)\r\n1.1 Canal WhatsApp (morador e prestador)\r\nEntrega de bot WhatsApp com fluxos completos:\r\nFluxo do Prestador\r\nCadastro guiado via WhatsApp:\r\n\r\n\r\nNome, contato, tipo de serviço, preço base, área de atuação\r\n\r\n\r\nDisponibilidade declarada\r\n\r\n\r\nUpload de fotos/links para portfólio\r\n\r\n\r\nAtualização de perfil via WhatsApp\r\n\r\n\r\nRecebimento automático de solicitações compatíveis\r\n\r\n\r\nFluxo do Morador\r\nSolicitação via WhatsApp (texto/áudio)\r\n\r\n\r\nColeta mínima de dados para qualificação (local/urgência/tipo)\r\n\r\n\r\nRetorno automático com lista de 3 a 5 profissionais recomendados\r\n\r\n\r\nEncaminhamento para contato direto\r\n\r\n\r\n\r\n1.2 Matching / recomendação (base MVP)\r\nClassificação de intenção e categoria do serviço solicitada\r\n\r\n\r\nRegras de matching:\r\n\r\n\r\nCategoria/serviço\r\n\r\n\r\nLocalidade / raio de atuação\r\n\r\n\r\nDisponibilidade declarada\r\n\r\n\r\nRanking simples por:\r\n\r\n\r\nAtividade recente\r\n\r\n\r\nAvaliação básica (quando existente)\r\n\r\n\r\n\r\n1.3 Painel Administrativo Web (React)\r\nLogin administrativo\r\n\r\n\r\nGestão de prestadores:\r\n\r\n\r\nAprovar / reprovar / bloquear\r\n\r\n\r\nVisualizar dados cadastrais e portfólio\r\n\r\n\r\nGestão de categorias/serviços\r\n\r\n\r\nMétricas operacionais básicas:\r\n\r\n\r\nNº de prestadores cadastrados\r\n\r\n\r\nNº de moradores ativos\r\n\r\n\r\nNº de solicitações realizadas\r\n\r\n\r\nConversão solicitação → recomendação → contato\r\n\r\n\r\n\r\n1.4 Backend e Banco de Dados\r\nBackend em NestJS (Node.js), arquitetura modular MVP\r\n\r\n\r\nAPIs para:\r\n\r\n\r\nUsuários (prestadores e moradores)\r\n\r\n\r\nCatálogo de serviços\r\n\r\n\r\nPedidos/solicitações\r\n\r\n\r\nMatching/recomendação\r\n\r\n\r\nAvaliação simples\r\n\r\n\r\nBanco relacional PostgreSQL\r\n\r\n\r\nLogs de uso e trilha mínima de auditoria\r\n\r\n\r\n\r\n1.5 Infraestrutura e Deploy\r\nDeploy em nuvem (ambiente produção MVP)\r\n\r\n\r\nBackup automático\r\n\r\n\r\nObservabilidade mínima (logs + alertas básicos)\r\n\r\n\r\nConfiguração de domínio / endpoints\r\n\r\n\r\nAdequação LGPD mínima:\r\n\r\n\r\nConsentimento\r\n\r\n\r\nRetenção básica de dados\r\n\r\n\r\nExportação simples sob demanda\r\n\r\n\r\n\r\n1.6 Piloto assistido\r\nPiloto real com grupo inicial\r\n\r\n\r\nMonitoramento de uso por 2 semanas\r\n\r\n\r\nCorreções de estabilidade e UX durante piloto\r\n\r\n\r\nRelatório de aprendizado + backlog recomendado para v1\r\n\r\n\r\n\r\n2. Itens do Orçamento (CAPEX)\r\nEtapa\r\nDescrição\r\nValor\r\n2.1\r\nDescoberta rápida + backlog fechado + wireframes\r\nR$ 12.000\r\n2.2\r\nUX Conversacional WhatsApp + UI do Admin\r\nR$ 18.000\r\n2.3\r\nDesenvolvimento Bot WhatsApp + integração BSP\r\nR$ 45.000\r\n2.4\r\nBackend NestJS + Banco + Matching base\r\nR$ 55.000\r\n2.5\r\nFrontend Admin React\r\nR$ 20.000\r\n2.6\r\nQA + testes + piloto assistido\r\nR$ 15.000\r\n2.7\r\nDevOps, deploy, segurança mínima, LGPD base\r\nR$ 10.000\r\n2.8\r\nGestão de projeto e governança\r\nR$ 10.000\r\n\r\nTOTAL GERAL: R$ 185.000,00\r\n\r\n3. Cronograma Macro (10–12 semanas)\r\nSemanas 1–2 — Planejamento e UX\r\n\r\n\r\nDescoberta rápida\r\n\r\n\r\nScript conversacional WhatsApp\r\n\r\n\r\nProtótipo do painel admin\r\n\r\n\r\nSemanas 3–6 — Bot + Backend\r\n\r\n\r\nIntegração WhatsApp Business API/BSP\r\n\r\n\r\nFluxos completos prestador e morador\r\n\r\n\r\nBackend core + banco + matching base\r\n\r\n\r\nSemanas 7–9 — Admin + Integração Final\r\n\r\n\r\nPainel administrativo completo\r\n\r\n\r\nAjustes de matching\r\n\r\n\r\nEstabilização geral\r\n\r\n\r\nSemanas 10–12 — QA + Piloto + Go-live\r\n\r\n\r\nTestes finais\r\n\r\n\r\nPiloto assistido 2 semanas\r\n\r\n\r\nCorreções e implantação final\r\n\r\n\r\n\r\n4. Forma de Pagamento\r\n30% na assinatura: R$ 55.500,00\r\n\r\n\r\n40% na entrega Bot + Backend (fim semana 6): R$ 74.000,00\r\n\r\n\r\n30% na entrega MVP + Piloto (fim semana 12): R$ 55.500,00\r\n\r\n\r\n\r\n5. Exclusões (fora do escopo deste orçamento)\r\nCustos de WhatsApp Business API / BSP (tarifas por conversa)\r\n\r\n\r\nCustos recorrentes de nuvem (infra) e IA (tokens, caso usados)\r\n\r\n\r\nApp nativo ou portal completo para prestadores\r\n\r\n\r\nAgenda inteligente avançada e automações de job complexas\r\n\r\n\r\nSistema robusto de reputação/moderação antifraude\r\n\r\n\r\nExpansão para outras comunidades\r\n\r\n\r\nSuporte contínuo pós-MVP (contrato separado)\r\n\r\n\r\n\r\n6. Custos Recorrentes Estimados (OPEX do MVP)\r\nEstimativa mensal após go-live:\r\nWhatsApp BSP / conversas: R$ 1.500 – 5.000 / mês\r\n\r\n\r\nInfra cloud MVP: R$ 800 – 2.000 / mês\r\n\r\n\r\nNLP/LLM leve (se ativado): R$ 300 – 1.500 / mês\r\n\r\n\r\nOPEX estimado: R$ 2.500 – 8.500 / mês\r\n\r\n7. Entregáveis finais\r\nAo final do projeto, a inovAI.lab entrega:\r\nMVP WhatsApp-first funcional\r\n\r\n\r\nPainel Admin web operacional\r\n\r\n\r\nBackend + banco em produção\r\n\r\n\r\nMatching base ativo\r\n\r\n\r\nPiloto concluído e validado\r\n\r\n\r\nDocumentação técnica essencial + guia de operação\r\n\r\n\r\n\r\n	Propostas Enviadas	2025-12-02 17:52:16.171828	2025-12-02 17:52:16.171831
27	J Faveret Advogados	José Faveret	paulo@inovailab.com	21 99988-2230	Apresentação Inovailab. Tem demanda para uma automação de contratos de compra de gás.	Captação	2025-12-10 17:47:55.025995	2025-12-10 17:47:55.026
20	Grupo Salta	Luiza Machado	luiza.machado@gruposaltaedu.com	21965027878	Indicação do Sylvio do bora bailar. Recebemos essa mensagem:\r\n\r\n\r\nAqui é a Luiza, meu marido Sylvio me indicou seu contato. \r\nEu trabalho numa rede de escolas nacional e olho para a parte de inovações da escola. \r\nQueria levar um projeto que transforma nosso site para alunos do pré vestibular (que hoje é landing page da Google) em um site com área de login do aluno, capaz de armazenar nossos conteúdos audiovisuais (aulas, vídeos, exercícios etc). \r\nSerá que consigo trocar uma ideia com você sobre isso? Para entender melhor como podemos fazer na prática	Propostas Enviadas	2025-11-25 19:58:38.369464	2025-12-11 17:07:54.776501
30	SBSC Shopping	Sergio Brandão	paulo@inovailab.com	21 99988-2230	Primeiro contato para reunião em Janeiro 26. Empresa gestora de Shopping centers.	Captação	2025-12-17 12:06:14.791751	2025-12-17 12:06:14.791755
29	Sisu - Golden Goal	Daniel Nascimento	daniel.nascimento@sisuvp.com	21-97134-1381	Cliente interessado em definir automações para area administrativa da empresa - Ja tem um valor aprovado para IA e automações para 2026	2a. Reunião	2025-12-11 13:50:36.852438	2025-12-23 14:55:34.663834
31	Elimar – Articulação Governamental	Elimar Macieira	felipe@inovailab.com	+55 21 96677-2111	Amigo próximo. Interesse em estruturar e vender soluções da inovAI.lab para o setor público (governo). Atua como articulador/parceiro estratégico, com foco em projetos de IA, automação e inovação para órgãos governamentais. Conversa em andamento para possível parceria comercial e estruturação de modelo de venda B2G.	Captação	2026-01-02 22:32:57.611649	2026-01-02 22:32:57.611654
32	Secretaria Municipal de Saúde do Rio de Janeiro	Aline	nucleoia.sap@gmail.com	5521980305757	Recebemos a indicaçào da Raphael, esposa do Andrey. A aline entrou em contato com a gente enviando essa mensagem:\r\n\r\nOi Felipe\r\nBoa tarde\r\nTudo bem?\r\nMeu nome é Aline e trabalho na Secretaria Municipal de Saúde do Rio de Janeiro e a Raphaela passou o seu contato.\r\nEstamos com um Núcleo de Inteligência Assistencial com a construção de dashboards com indicadores de saúde e trabalharemos com analise de desfechos e modelos presitivos.\r\nJá temos um datalke da Secretaria e estamos com um projeto para 2026 para criação de site com dashboards voltados para saúde. \r\n\r\nGostaríamos de conversar com vocês para obtermos uma proposta de orçamento para os nossos projetos.\r\nVocê teria disponibilidade de conversar com a nossa equipe essa semana?\r\n\r\nAgendamos o primeiro papo com eles para quarta feira, dia 7 de dezembro de 2026 para as primeiras apresentações. 	1a Reunião	2026-01-05 21:04:54.435253	2026-01-05 21:04:54.435257
33	Portogallo Family Office	Gustavo Infantini	gustavo@portogalloeuropa.net	11 98244-0414	Agendada primeira reunião para sexta feira, 9 de fevereiro de 2026 as 15h para devidas apresentações. Tanto da inovai.lab 	1a Reunião	2026-01-06 22:49:52.76639	2026-01-06 22:49:52.766394
34	Cartorio 9 ofício	Gustavo Mendes	paulo@inovailab.com	21 9 88448914	13/1 - Apresentei a Inovailab para implementar automações. Ele pediu uma apresentação para conversarmos na volta do feriado.	Captação	2026-01-13 21:58:13.998702	2026-01-13 21:58:13.998706
28	Coer	Eric Reis	ericreis_49@hotmail.com	(21) 995005534	Amigo da Giu, tem uma empresa de saude, monitoramento e educação em empresas. 	Leads Frios	2025-12-11 13:46:40.062677	2026-01-14 15:40:18.366593
16	Silvio 	Silvio Procopio	silproc@gmail.com	+55 11 99934-4656	Silvio está estruturando uma nova marca de moda, ainda em fase embrionária, com início das operações previsto de forma enxuta em bazares e e-commerce (Shopify como possibilidade). Ele busca diferenciar o negócio com soluções de IA voltadas para experiência do cliente e aumento de conversão, especialmente: um “vendedor virtual” que atenda o cliente por voz/chat no ponto de venda físico ou online (reduzindo dependência de vendedores humanos) e um provador virtual onde o cliente possa visualizar como ficaria usando as peças a partir de uma foto. Também demonstrou interesse em personalização de comunicação pós-compra e possíveis usos de visão computacional (câmeras inteligentes, mapa de calor em loja). No momento, o foco principal é entender escopo e custos para decidir quais dessas soluções cabem no orçamento inicial do projeto.	Leads Frios	2025-11-21 17:44:44.252191	2026-01-14 15:41:14.4477
36	GAVEA  LOGISTICS	Scott	paulo@inovailab.com	21 999882230	15/1 - Ligar dia 19/1 para agendar reunião. Apresentar a inovailab e as soluções.	Captação	2026-01-15 21:36:29.041956	2026-01-15 21:36:29.041961
35	NR Saúde e Segurança do Trabalho RJ	Maria	nrsaudeseguranca.01@gmail.com	55 21 99399-2907	Primeira reunião realizada para entendimento do projeto. A NR Saúde e Segurança atua com medicina e segurança do trabalho, atendendo empresas de diferentes portes, e apresentou como principal desafio a adequação à NR-1 (Riscos Psicossociais), que exige a avaliação da saúde mental dos colaboradores. Atualmente o processo é feito de forma manual, com aplicação de questionários e análise em planilhas, o que gera baixa escalabilidade e resistência de parte dos clientes. O objetivo é desenvolver uma plataforma digital automatizada, com aplicação de questionários via link, análise de dados e geração de diagnósticos por setor, com potencial de uso de IA para ampliar o valor da solução e evoluir para uma ferramenta estratégica de gestão de RH. Próximo passo alinhado: reunião de trabalho para aprofundar escopo e avançar para proposta.	Apresentação da POC	2026-01-14 13:46:33.157761	2026-01-17 23:27:08.33932
37	Binato Advogados associados	Luiz Binato	paulo@inovailab.com	21 99988-2230	REunião marcada 28/1 as 16hs São Conrado. Apresenta a Inovailab	Captação	2026-01-27 13:49:50.201203	2026-01-27 13:49:50.201223
\.


--
-- Data for Name: crm_stages; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.crm_stages (id, nome, ordem, is_fixed, created_at) FROM stdin;
1	Captação	1	t	2025-11-17 19:32:13.01074
2	1a Reunião	2	t	2025-11-17 19:32:13.010745
3	2a. Reunião	3	t	2025-11-17 19:32:13.010745
4	Apresentação da POC	4	f	2025-11-17 20:51:16.503894
5	VALIDAÇÃO PRODUTO	5	f	2025-11-25 13:34:12.201743
6	Propostas Enviadas	6	f	2025-11-29 20:17:25.338695
7	Leads Frios	7	f	2025-12-01 17:34:36.708586
9	Contratos Fechados	8	f	2025-12-23 14:56:20.368936
\.


--
-- Data for Name: file_categories; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.file_categories (id, nome, icone, cor, ordem, created_at) FROM stdin;
1	UX/Design	fa-palette	#8b5cf6	1	2025-12-09 20:21:55.979104
2	Documentação	fa-file-alt	#3b82f6	2	2025-12-09 20:21:56.034042
3	Desenvolvimento	fa-code	#10b981	3	2025-12-09 20:21:56.076568
4	Imagens	fa-image	#f59e0b	4	2025-12-09 20:21:56.119186
5	Vídeos	fa-video	#ef4444	5	2025-12-09 20:21:56.162353
6	Outros	fa-folder	#6b7280	6	2025-12-09 20:21:56.206176
\.


--
-- Data for Name: lead; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.lead (id, nome, empresa, email, telefone, cargo, origem, valor_estimado, etapa, convertido, perdido, motivo_perda, created_at, updated_at, observacoes, responsavel_id, converted_to_client_id) FROM stdin;
2	Test Lead Antigravity	Antigravity Corp	test_gravity@example.com	11999999999	\N	API Test	\N	Novo	f	f	\N	2025-12-18 23:39:50.956555	2025-12-18 23:39:50.956559	\N	\N	\N
\.


--
-- Data for Name: lead_interaction; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.lead_interaction (id, tipo, descricao, created_at, lead_id, user_id) FROM stdin;
\.


--
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.project (id, nome, transcricao, created_at, client_id, responsible_id, contexto_justificativa, descricao_resumida, problema_oportunidade, objetivos, alinhamento_estrategico, escopo_projeto, fora_escopo, premissas, restricoes, status, progress_percent, prazo) FROM stdin;
2	Apurador Fiscal (PIS/COFINS) e Demonstrativo por Shopping - Fabiano	\N	2025-08-26 14:58:12.235949	1	4	Desenvolver e evoluir um módulo de apuração fiscal (foco inicial em PIS/COFINS) que consolida receitas por shopping/filial, permite lançamentos (upload e manual), calcula a base e tributos conforme a planilha de referência, e exibe o demonstrativo por período (mês/trimestre/ano), com preparação para integrar ao TOTVS RM.	Desenvolver e evoluir um módulo de apuração fiscal (foco inicial em PIS/COFINS) que consolida receitas por shopping/filial, permite lançamentos (upload e manual), calcula a base e tributos conforme a planilha de referência, e exibe o demonstrativo por período (mês/trimestre/ano), com preparação para integrar ao TOTVS RM.	Hoje a apuração depende de planilhas manuais e processos dispersos; há risco de erro e retrabalho. O time quer substituir o Excel por um fluxo dentro do sistema. \r\n\r\nNecessidade de refletir regras de cálculo usadas na planilha “Apuração PIS/COFINS” (ex.: bases e deduções) no sistema. \r\n\r\nPreparar o terreno para integração com o RM, usando cadastros (ex.: CST) de forma compatível com obrigações acessórias.	Replicar no sistema a lógica da planilha de apuração (bases, deduções, cálculo de PIS/COFINS) e disponibilizar demonstrativos por período e por shopping. \r\n\r\nPermitir lançamentos de receitas via upload (BI/planilha) e via lançamento manual com tipos padronizados. \r\n\r\nImplantar rotina “Calcular Impostos” centralizada (seleção de shopping e período), gerando os lançamentos de tributos. \r\n\r\nTornar alíquotas “maleáveis” por shopping e cadastrar CSTs para futura integração com RM. \r\n\r\nEliminar dependência de Excel na operação diária.	Reduzir tempo de fechamento e risco de erro, preparando integração com o RM e com obrigações acessórias. \r\n\r\nMigrar do Excel para o sistema, melhorando usabilidade e governança de dados.	Demonstrativo fiscal por shopping/filial e por período (mês, trimestre, ano). \r\n\r\nUploads de dados de faturamento (arquivo padrão do BI/planilha). \r\n\r\nLançamento manual de receitas com tipos (ex.: aluguel, CDU, estacionamento, receita financeira etc.).\r\n\r\nCadastro de shopping com regime (lucro real/presumido) e edição. \r\n\r\nCadastro de CST (código/nome) para uso na apuração e integração futura. \r\n\r\nRotina “Calcular Impostos” centralizada (seleção de período/shopping, aplicar regras e registrar o cálculo).	Integração RM (implantar de imediato) — fica como etapa posterior. \r\n\r\nCálculo de outros tributos além do foco inicial (somente após estabilizar PIS/COFINS). \r\n	Planilha de referência de apuração está correta e será a “fonte da verdade” para validar o sistema. \r\n\r\nFabiano fornecerá siglas/categorias adicionais (ex.: incorporadoras/“32”) quando necessário. \r\n\r\nAlíquotas e CSTs podem variar e devem ser configuráveis.	Fórmulas de tributos ainda em ajuste; pedido para desconsiderar cálculo final enquanto a equipe estabiliza a rotina. \r\n\r\nDependência de insumos (planilhas e exemplos) enviados pelos usuários para testes/validação.	pausado	0	\N
8	Fluxo 360 — Tesouraria (Caixa Realizado & Previsto) - Yan	\N	2025-08-26 18:51:40.15372	1	4	Sistema web para substituir a planilha atual: importa diariamente o relatório do RM (despesas) e permite lançamento de receitas pela tesouraria, com classificação por Regional → Negócio → Empreendimento → Conta, regras de aportes entre empreendimentos e dashboards de caixa. Em etapa seguinte, inclui previsão (orçado) com travas no início do mês e equalização automática entre previsto e realizado.	Sistema web para substituir a planilha atual: importa diariamente o relatório do RM (despesas) e permite lançamento de receitas pela tesouraria, com classificação por Regional → Negócio → Empreendimento → Conta, regras de aportes entre empreendimentos e dashboards de caixa. Em etapa seguinte, inclui previsão (orçado) com travas no início do mês e equalização automática entre previsto e realizado.	Controle do caixa 100% em Excel pesado, com lançamentos manuais diários e alto risco de erro. \r\n\r\nReceitas hoje são validadas olhando o extrato na tela, sem um lançador simples e guiado. \r\n\r\nNecessidade de classificação granular (Regional/Negócio/Empreendimento/Conta) e de tratar fluxos apartados (ex.: JC, Site). \r\n \r\n\r\nFalta um mecanismo de previsão congelada no início do mês e reprojeção/ equalização diária entre previsto e realizado	Centralizar o caixa realizado e previsto em um sistema único (substituir a planilha). \r\n\r\nReduzir o esforço manual na conferência/lançamento diário de receitas e import de despesas do RM. \r\n\r\nPadronizar a classificação por Regional/Negócio/Empreendimento/Conta e tratar aportes com débito/crédito e data. \r\n \r\n\r\nMelhorar visibilidade com dashboards de saldos/movimentações por grupo/negócio/empreendimento. \r\n\r\nImplantar previsão (fase 2) com trava no início do mês e equalização automática por centro de custo.	Eficiência operacional (menos passos manuais na rotina da tesouraria). \r\n\r\nGovernança de dados (base única; trilha clara de classificação e aportes). \r\n \r\n\r\nEscalabilidade (multi-regional/negócio/empreendimento; previsões mensais consolidadas)	Fase 1 — Caixa Realizado (MVP)\r\n\r\nUpload diário do RM (ex.: relatório “21”) para despesas, ingestão “como vem”. \r\n\r\nLançador de Receitas: tela simples para a tesoureira lançar por Empreendimento/Conta (com seletores encadeados Regional → Negócio → Empreendimento → Conta). \r\n \r\n\r\nCadastros-mestre: Regionais, Negócios, Empreendimentos, Contas (vínculos e fluxos apartados como JC e Site). \r\n\r\nRegras de Aportes: crédito/debito entre empreendimentos com data (impacta saldos dos dois lados). \r\n\r\nDashboards: visão de saldos/movimentações por grupo/negócio/empreendimento/conta. \r\n\r\nFase 2 — Previsão (Orçado) + Equalização\r\n\r\nBase de previsões informada pelos negócios; trava no início do mês; equalização automática da diferença entre previsto e realizado por centro de custo; reprojeção diária. 	Automação de Fluig ou preenchimento automático no RM. \r\n\r\nRPA de remessas/borderôs, “baixas em lote” e outras rotinas bancárias. \r\n\r\nCaptura automática de extratos bancários ou leitura de PDFs de extrato.	Existe export diário do RM “bruto” que a tesouraria já usa (p.ex., relatório 21). \r\n\r\nA tesouraria seguirá lançando receitas no sistema (como hoje, porém guiado). \r\n\r\nHaverá tabela-mestre com o mapeamento Regional/Negócio/Empreendimento/Conta e marcação de fluxos apartados (JC, Site). \r\n \r\n\r\nOs campos obrigatórios do lançamento de receitas serão definidos pela área (lista a fornecer).	Sem integração RM no MVP: ingestão via upload permanece até mapeamento de API. \r\n\r\nPrevisão depende de envio/entrada de dados pelos negócios; sem isso, só realizado. \r\n\r\nComplexidade de classificações e fluxos apartados exige base-mestra bem definida. 	pausado	0	\N
11	BoraBailar App	\N	2025-08-26 19:21:00.606005	4	5	Aplicativo mobile de curadoria e “match” para experiências de dança e entretenimento (pessoas, professores, lugares e eventos), com onboarding de fricção quase zero, priorizando experiências offline e expansão por franquias regionais. 	Aplicativo mobile de curadoria e “match” para experiências de dança e entretenimento (pessoas, professores, lugares e eventos), com onboarding de fricção quase zero, priorizando experiências offline e expansão por franquias regionais. 	Pessoas (especialmente 30–50+) querem sair para dançar/se divertir com segurança, compatibilidade e baixa fricção; hoje a oferta é fragmentada entre aulas, bailes, casas e promoters. \r\n\r\nOceano azul: há espaço para um produto que comece pelo “match da dança” e possa expandir para experiências e conteúdo, evitando virar um “dating app”	V1 funcional em 90 dias, priorizando valor de entrada (home/match + curadoria + fluxo transacional mínimo). \r\n \r\n\r\nOnboarding leve: cadastro guiado por IA/áudio e login simples. \r\n\r\nConteúdo inicial curado (lugares, professores, eventos) via franqueados para evitar a “praça vazia”. \r\n\r\nPitch-ready: manter versão estável para demonstrações a parceiros/investidores.	Caminho de startup: fazer só o necessário no início e escalar por iterações. \r\n\r\nModelo de crescimento híbrido (online→offline) com franquias regionais para popular conteúdo local rapidamente.	Home de “match” misturando pessoas/lugares/professores/eventos com curadoria. \r\n\r\nOnboarding leve/IA e login simples; completar perfil só no que faltar. \r\n \r\n\r\nAdmin web (Python/Flask) para cadastrar parceiros, professores, eventos, tags e prioridades (liberado para teste). \r\n \r\n\r\nCuradoria local (início no RJ) fomentada por franqueados. \r\n\r\nPosicionamento de marca: “experiências boas/offline”; evitar conotação “adulto/dating”.	Rede social completa (feed robusto, concursos, uploads e “premium”) — itens para V2/V3+. \r\n\r\nChat social amplo (só quando necessário, pós-transação/suporte). \r\n\r\nApp focado em “encontros”/conteúdo adulto (posicionamento explícito contra).	O franqueado popula a região com lugares/professores/eventos para garantir valor inicial. \r\n\r\nPúblico inicial dança/entretenimento; produto pode pivotar conforme tração/uso. \r\n \r\n\r\nOnboarding/UX enxutos elevam conversão de primeira experiência.	Design não deve travar entregas (priorizar funcional até refinar o front). \r\n\r\nEstabilidade de login/demo crítica para pitches (corrigir falha vista em 26/08). \r\n\r\nBrand safety: evitar percepção de “adult/dating” na comunicação.	em_andamento	0	\N
10	Conselheiro IA da Presidência	\N	2025-08-26 19:10:10.015153	1	10	Construir um chat conversacional para a Presidência que consulta, cruza e analisa dados dos shoppings e da construtora, entregando respostas objetivas e análises sob demanda (KPIs, tendências, comparativos, projeções), com controle de acesso e trilha de auditoria.	Construir um chat conversacional para a Presidência que consulta, cruza e analisa dados dos shoppings e da construtora, entregando respostas objetivas e análises sob demanda (KPIs, tendências, comparativos, projeções), com controle de acesso e trilha de auditoria.	Problema: A Presidência precisa de respostas rápidas e confiáveis sobre operação e projetos, mas os dados estão dispersos em múltiplas fontes e dependem de times intermediários (BI/Analytics), gerando atrasos na tomada de decisão.\r\n\r\nOportunidade: Centralizar o acesso via chat com linguagem natural, com integração única às bases de shoppings e construtora, reduzindo tempo de resposta, padronizando análises e elevando a maturidade de dados da organização.	Disponibilizar MVP (consulta à view de Shoppings) imediatamente após a liberação da view pelo responsável, com respostas de perguntas factuais e relatórios rápidos.\r\n\r\nEntregar consultas e análises padrão (ex.: ocupação, vendas, fluxo, inadimplência, CAPEX vs. orçamento, status de obras) com explicabilidade (fonte, período e filtros usados).\r\n\r\nGarantir governança: controle de acesso por perfil, logs de perguntas/respostas e trilha de auditoria.\r\n\r\nConfiabilidade dos dados: checagens básicas, carimbo de data/hora da atualização e alerta quando a atualização estiver desatualizada.\r\n\r\nEscalabilidade: arquitetura preparada para incluir dados da Construtora (Fase 2) e novas fontes.	Velocidade de decisão da Presidência com base em dados confiáveis.\r\n\r\nPadronização de análises e indicadores-chave.\r\n\r\nGovernança e segurança de dados (LGPD, segregação por papéis).\r\n\r\nEficiência operacional, reduzindo dependências de solicitações ad hoc.	Fase 1 – Shoppings (MVP)\r\n\r\nIntegração de leitura na view única dos shoppings (liberação pendente).\r\n\r\nCamada semântica para consultas em linguagem natural (RAG/semantic search).\r\n\r\nConsultas padrão: ocupação, vendas, footfall, inadimplência, receita por shopping, metas vs. realizado, evolução mensal, top/bottom performers, etc.\r\n\r\nTemplates de análises: comparativos por período, por shopping, por categoria; projeções simples (médias móveis / tendência) onde houver dados suficientes.\r\n\r\nGovernança e segurança: RBAC por perfis da Presidência e diretoria; logs e auditoria.\r\n\r\nObservabilidade: painel interno de uso (perguntas mais feitas, latência, fontes consultadas).\r\n\r\nFase 2 – Construtora\r\n\r\nIntegração com bases/projetos da construtora (obras, CAPEX, cronogramas, orçamento vs. executado, riscos).\r\n\r\nAmpliação dos templates de análises para correlacionar desempenho dos shoppings com projetos (p. ex., impacto de obras/expansões).	Edição/alteração de dados-fonte (o chat é somente leitura).\r\n\r\nAções automatizadas em sistemas transacionais (ex.: criar ordens, contratos, aprovações).\r\n\r\nAutomação de decisões sem validação humana.\r\n\r\nCriações de apresentações 100% automáticas para terceiros (pode ser fase futura).	Liberação da view de dados dos shoppings (responsável: Hudson) com acesso de leitura e dicionário de dados.\r\n\r\nDados com atualização regular e metadados de período.\r\n\r\nAcesso a credenciais/VPN/ambiente seguro conforme política da empresa.\r\n\r\nEngajamento da Presidência para validação de casos de uso (perguntas prioritárias).\r\n\r\nDisponibilidade de ambiente de homologação antes de produção.	LGPD e segurança: segregação de acesso por papel; mascaramento/ocultação de dados sensíveis.\r\n\r\nSLA das fontes: qualidade e frequência de atualização limitam a qualidade das respostas.\r\n\r\nDependência da liberação da view para o MVP.\r\n\r\nOrçamento/infra: dimensionamento de recursos conforme volume de consultas.	em_andamento	0	\N
13	RPA de Faturamento Sá Cavalcante	\N	2025-08-26 20:57:38.806856	1	6	Desenvolvimento e implantação de uma solução de automação robótica de processos (RPA)\r\nutilizando Python e PyAutoGUI, responsável por executar de forma autônoma o processo de\r\nfaturamento dos shoppings administrados pela Sá Cavalcante. A solução realiza login no sistema\r\nlegado (VS), executa cálculos de encargos (água, energia e outros custos), gera boletos e realiza o\r\nenvio aos lojistas, obedecendo às regras específicas de cada tipo de faturamento.	Desenvolvimento e implantação de uma solução de automação robótica de processos (RPA)\r\nutilizando Python e PyAutoGUI, responsável por executar de forma autônoma o processo de\r\nfaturamento dos shoppings administrados pela Sá Cavalcante. A solução realiza login no sistema\r\nlegado (VS), executa cálculos de encargos (água, energia e outros custos), gera boletos e realiza o\r\nenvio aos lojistas, obedecendo às regras específicas de cada tipo de faturamento.	Problema atual: O faturamento é executado manualmente por analistas, demandando tempo\r\nelevado e sujeito a erros humanos, além de exigir repetição do mesmo fluxo em cada shopping e\r\npara cada modalidade de faturamento.\r\nOportunidade: Reduzir o tempo de processamento, eliminar erros operacionais e liberar os\r\nanalistas para tarefas de maior valor agregado por meio da automação RPA.	• Automatizar integralmente o processo de faturamento de todos os shoppings da Sá Cavalcante.\r\n• Garantir conformidade com as particularidades de cada tipo de faturamento (atípico,\r\npós-antecipado e antecipado).\r\n• Padronizar a execução dos processos, minimizando erros e atrasos.\r\n• Disponibilizar um sistema de controle interno (aplicativo servidor) para que os analistas possam\r\nescolher shopping, tipo de faturamento e ações a executar.\r\n• Reduzir custos operacionais e otimizar o tempo de entrega dos boletos	• Eficiência Operacional: Automatização de processos críticos para ganho de produtividade.\r\n• Confiabilidade: Redução de erros humanos e maior precisão nos cálculos.\r\n• Escalabilidade: Facilidade em replicar o processo para novos shoppings administrados.\r\n• Inovação: Adoção de tecnologias RPA alinhadas às tendências de transformação digital.	• Automação de login e navegação no sistema legado (VS).\r\n• Importação de encargos (água, energia e outros custos).\r\n• Execução de cálculos conforme regras definidas por shopping e tipo de faturamento.\r\n• Emissão de boletos.\r\n• Envio automático dos boletos para cada loja e shopping.\r\n• Interface de controle interno para analistas definirem parâmetros (shopping, tipo, ação).	• Alterações ou modernização do sistema legado (VS).\r\n• Emissão ou controle de notas fiscais.\r\n• Gestão financeira posterior ao pagamento (contas a receber, conciliações bancárias).\r\n• Suporte técnico a usuários finais (lojistas)	• Sistema legado (VS) estará disponível e funcional durante a execução da RPA.\r\n• Os dados de encargos serão corretamente disponibilizados para importação.\r\n• Os acessos ao sistema (usuários e senhas) estarão válidos e atualizados.\r\n• Ambiente servidor possui capacidade para rodar o robô em tempo hábil.	• Dependência do sistema VS, que é antigo e sujeito a instabilidades.\r\n• Necessidade de rodar cada tipo de faturamento em datas específicas (ex.: atípicos sempre no dia\r\n5).\r\n• Execução sequencial por shopping (não paralelizada).\r\n• Dependência do PyAutoGUI, que requer ambiente configurado e estável em termos de resolução\r\ne tempo de resposta.	em_andamento	0	\N
16	OÁZ FinOps AI — Inadimplência	\N	2025-09-02 18:49:48.04738	5	8	Desenvolver um sistema inteligente para automatizar o acompanhamento de inadimplência, integrando dados de múltiplos sistemas (NetSuite/“Netflix”, Microvix), vinculando boletos em PDF aos títulos, e disparando comunicações proativas via WhatsApp (pré e pós-vencimento). O sistema será agnóstico de ERP, operando a partir do banco/datalake da OÁZ, para não comprometer a futura troca de ERP.									em_andamento	0	\N
19	Banco de Imagens com Inteligência Artificial	\N	2025-09-05 22:10:43.264462	5	8	Desenvolvimento de uma solução simples e objetiva para renomear fotos de produtos em lote a partir de um mapa de coleção em Excel. O sistema permitirá o upload de imagens e a aplicação de regras de nomenclatura padronizadas, garantindo consistência e agilidade no processo de preparação das fotos para o e-commerce e marketplaces.	Sistema web de banco de imagens inteligente para varejo de moda, integrado à Carteira de Compras e ao SharePoint. Permite catalogar SKUs em larga escala, fazer match automático entre produtos e fotos, servir imagens em alta resolução via streaming e usar IA para gerar descrições e apoiar o time de marketing/compras.	Hoje as imagens de produto ficam dispersas em pastas, e-mails e planilhas, dificultando:\r\n\r\nlocalizar rapidamente fotos corretas por SKU/coleção;\r\n\r\ngarantir consistência entre Carteira de Compras e o material usado em e-commerce e marketing;\r\n\r\nreaproveitar imagens em múltiplos canais;\r\n\r\nusar IA de forma estruturada para análise e geração de conteúdo.\r\n\r\nHá oportunidade de centralizar o acesso às imagens, reduzir retrabalho de times de marketing/compras/estilo e criar uma base preparada para automações futuras (IA, relatórios, integrações com outros sistemas).	Criar um catálogo único de imagens de produto, com busca por SKU, coleção, marca, tags e status.\r\n\r\nIntegrar com o SharePoint para usar as imagens hi-res como fonte de verdade, evitando duplicação de arquivos.\r\n\r\nConectar o catálogo à Carteira de Compras, permitindo match automático de SKUs e controle de “com foto / sem foto”.\r\n\r\nDisponibilizar thumbnails otimizados para navegação rápida e streaming das imagens em alta resolução sob demanda.\r\n\r\nImplementar recursos de IA (análise e geração de descrições) integrados ao fluxo de produto/imagem.\r\n\r\nFornecer relatórios e auditoria sobre cruzamentos, pendências e divergências entre Carteira e banco de imagens.	Contribui diretamente para a estratégia da OÁZ de produtos digitais com IA aplicada a problemas reais de negócio.\r\n\r\nAumenta a eficiência operacional de clientes de varejo de moda, reduzindo tempo de lançamento de coleções e erros de publicação.\r\n\r\nCria uma plataforma reutilizável para outros clientes de varejo (modelo white-label), fortalecendo o portfólio da empresa.\r\n\r\nApoia a visão de dados e ativos centralizados, integrando informações de produto, imagens e analytics em um único fluxo.	Desenvolvimento e manutenção do aplicativo Flask (backend e frontend) do Banco de Imagens. \r\n\r\nIntegração com:\r\n\r\nCarteira de Compras (importação de Excel/CSV, criação de produtos, controle de lotes);\r\n\r\nSharePoint via Microsoft Graph (indexação de pastas, streaming de imagens hi-res).\r\n\r\nCatálogo de imagens com:\r\n\r\nagrupamento por SKU base;\r\n\r\nfiltros por coleção, marca, status e texto livre;\r\n\r\nvisualização de thumbnails e detalhes da imagem.\r\n\r\nLógica de SKU Matching entre Carteira e SharePoint, incluindo criação automática de coleções/marcas a partir da estrutura de pastas.\r\n\r\nMódulos de IA para análise e geração de descrições (front preparado; modelos/integrações configurados conforme escopo técnico).\r\n\r\nRelatórios e telas de auditoria (imagens ausentes, divergências, estatísticas de cruzamento).\r\n\r\nDeploy e operação em VM na GCP, com processo de atualização via git pull + serviço systemd.	Implementação de um ERP completo ou funcionalidades financeiras/fiscais.\r\n\r\nGestão de estoque físico, logística ou faturamento.\r\n\r\nFerramentas avançadas de edição de imagem (tratamento profissional, recorte complexo etc.).\r\n\r\nConstrução de um DAM corporativo genérico para todas as áreas; foco é varejo de moda e Carteira de Compras.\r\n\r\nIntegrações profundas com todos os canais de venda (marketplaces, OMS etc.) além do que for explicitamente priorizado.\r\n\r\nSuporte a múltiplos tenants de SharePoint em uma única instalação (neste momento, 1 cliente/tenant por instância do sistema).	O cliente disponibiliza ambiente SharePoint estruturado (pastas por coleção, marca, etc.) e credenciais de acesso via Microsoft Entra ID. \r\n\r\nREADME\r\n\r\nAs carteiras de produto são fornecidas em formato Excel/CSV com SKUs padronizados e consistentes com a nomenclatura das imagens.\r\n\r\nHá um ambiente de banco de dados (PostgreSQL/SQLite) disponível e acessível pela aplicação.\r\n\r\nUsuários-chave (marketing, compras, e-commerce) participam das validações de fluxo e regras de negócio.\r\n\r\nEquipe de infra do cliente ou da OÁZ apoia configuração de permissões no Microsoft Graph e na VM da GCP.	Dependência de permissões corretas no Microsoft Graph/SharePoint; qualquer mudança de política pode impactar o acesso às imagens.\r\n\r\nVolume elevado de arquivos pode exigir otimização de indexação e políticas de cache para manter boa performance.\r\n\r\nJanela de manutenção para deploys na VM da GCP deve respeitar horários de uso do cliente.\r\n\r\nTime de desenvolvimento enxuto, o que impõe priorização clara de funcionalidades frente ao roadmap de IA e integrações futuras.\r\n\r\nLimitações de licenças/planos do próprio SharePoint (tamanho máximo de arquivo, tráfego, etc.).	em_andamento	0	\N
18	PerfOps OÁZ – Monitoramento e Insights de Performance Digital	\N	2025-09-04 14:50:04.319442	5	10	Implementar uma solução integrada que consolida dados de GA4, Google Ads, Meta Ads e Magento, gerando relatórios diários e um dashboard unificado, além de alertas de anomalia em tempo real, permitindo decisões rápidas e redução da dependência de relatórios manuais.	Implementar uma solução integrada que consolida dados de GA4, Google Ads, Meta Ads e Magento, gerando relatórios diários e um dashboard unificado, além de alertas de anomalia em tempo real, permitindo decisões rápidas e redução da dependência de relatórios manuais.	Dados fragmentados e análises manuais em excesso.\r\n\r\nFalta de visão integrada do funil digital (tráfego, conversão, receita).\r\n\r\nAusência de alertas proativos para quedas de site, fim de budget, baixa qualidade de tráfego.\r\n\r\nOportunidade de liberar o time de performance para análise estratégica, em vez de tarefas operacionais.	Consolidar dados de GA4, Google Ads, Meta Ads e Magento em modelo único.\r\n\r\nGerar relatórios diários com KPIs principais.\r\n\r\nEmitir alertas de anomalias (queda de site, budget esgotado, spikes/baixa qualidade de tráfego).\r\n\r\nCriar dashboard unificado com visão de 7/30 dias por canal, campanha e criativo.\r\n\r\nDisponibilizar camada de consulta via RAG/linguagem natural.	Acelerar a tomada de decisão em marketing digital.\r\n\r\nEscalar a operação com menos dependência de relatórios manuais.\r\n\r\nAumentar eficiência e competitividade da operação digital da OÁZ.	Conectores fase 1 (manual via export): GA4, Google Ads, Meta Ads, Magento.\r\n\r\nConectores fase 2 (automática via API).\r\n\r\nModelagem de métricas: sessões, leads, add-to-cart, checkout, receita, CAC, ROAS.\r\n\r\nRelatórios diários automatizados.\r\n\r\nAlertas intradiários (queda de site, fim de verba, CTR/CPA fora do padrão).\r\n\r\nDashboard consolidado (últimos 7/30 dias).\r\n\r\nRAG para consultas inteligentes.	Automação ativa de campanhas (troca de criativos/públicos).\r\n\r\nFrentes de cobrança financeira ou RH.\r\n\r\nMigração completa de Adobe Analytics → GA4.	Liberação de acessos às plataformas (GA4, Ads, Meta, Magento).\r\n\r\nInstrumentação mínima já ativa no GA4.\r\n\r\nAcesso ao data lake da OÁZ para integração.	Capacidade do time limitada, dependência de acessos.\r\n\r\nQualidade dos dados varia até estabilização da instrumentação.\r\n\r\nPolíticas do Meta podem exigir conta pessoal.\r\n\r\nCustos de processamento em consultas avançadas (evitar enviar o banco inteiro a cada pergunta).	em_andamento	0	\N
23	Mapeamento de Processos Avsales	\N	2025-10-13 17:42:42.673997	3	7	Primeiro "Projeto" desenvolvido para a Avsales durante a primeira ida à Miami. 	Primeiro "Projeto" desenvolvido para a Avsales durante a primeira ida à Miami. 		Mapear os processos da Avsales para entender a criaçao e as etapas necessarias para a criaçao de quotations. Tanto no salesforce como tambem por meio do Pentagon (sistema antigo)						pausado	0	\N
22	Plataforma de Conferência de Benefícios do Departamento Pessoal (DP)	\N	2025-09-11 17:11:24.186677	1	4	Desenvolver uma plataforma única para (1) centralizar cadastros (Empregados, Particularidades e PJ), (2) importar mensalmente a “posição atual” da folha (RM) e (3) conciliar faturas das operadoras de benefícios (saúde, dental, etc.) com os dados internos, permitindo auditoria, rastreabilidade e exportação em Excel. (Confirmado na reunião: foco em parar de depender de PDFs e priorizar Excel; iniciar piloto com Bradesco Dental.) 	Desenvolver uma plataforma única para (1) centralizar cadastros (Empregados, Particularidades e PJ), (2) importar mensalmente a “posição atual” da folha (RM) e (3) conciliar faturas das operadoras de benefícios (saúde, dental, etc.) com os dados internos, permitindo auditoria, rastreabilidade e exportação em Excel. (Confirmado na reunião: foco em parar de depender de PDFs e priorizar Excel; iniciar piloto com Bradesco Dental.) 	Problema atual: as faturas chegam (muitas em PDF) e a extração via IA erra detalhes; conciliação é manual, lenta e sujeita a falhas. \r\n\r\nOportunidade: padronizar ingestão (preferencialmente Excel), automatizar o confronto fatura × folha (posição atual), reduzir retrabalho e dar visibilidade por pessoa/centro de custo. (Reunião: preferência por Excel e confronto mensal fatura vs. folha.)	Centralização de dados: manter base única de Empregados, Particularidades (pessoas fora do RM, dependentes, PJs) e Movimentação de PJ. \r\n\r\n\r\nConciliação mensal: importar “posição atual” da folha (RM) e confrontar automaticamente com faturas (começando por Bradesco Dental). \r\n\r\nRastreabilidade por centro de custo: discriminar valores por pessoa/centro de custo para checagens e ajustes. \r\n\r\n\r\nOperação sem planilhas, com exportação: operar os cadastros dentro da plataforma, com exportação para Excel quando necessário.	Eficiência operacional do DP: eliminar reconciliações manuais e erros.\r\n\r\nGovernança e auditoria: histórico e trilha de auditoria das mudanças e das diferenças entre fatura e folha.\r\n\r\nEscalabilidade: modelo por “mapeamento de operadora” para adicionar novos benefícios/formatos sem reescrever o fluxo.\r\n(Discussão de abandonar planilhas como “sistema de operação” e manter exportação quando preciso.)	Cadastros base\r\n* Empregados (do RM, incluindo desligados recentes para histórico).  \r\n* Particularidades (pessoas fora do RM, PJs e dependentes, com grau de parentesco). \r\n\r\n* Movimentação de PJ.  \r\nIngestão mensal\r\n* Importar posição atual da folha (relatório do RM) para confrontar com faturas do mês. \r\n\r\n* Importar faturas (prioridade piloto: Bradesco Dental; depois Bradesco Saúde, Unimed, seguro de vida, alimentação, transporte etc.). Formatos podem variar por operadora. \r\n\r\nConciliação & relatórios\r\n* Motor de diferenças (inclusões/exclusões, alterações de centro de custo, valores divergentes por pessoa). \r\n* Relatórios por empresa/centro de custo/pessoa e exportação para Excel.  \r\nAcesso & operação\r\n* Autenticação (login/senha) e perfis (DP pode incluir/editar registros sem depender de planilhas).  \r\n	Integrações diretas via API com operadoras/corretoras (importações serão por arquivos).\r\nAutomação de pagamento de faturas.\r\nOCR/IA de PDFs “genéricos” (somente se não houver opção Excel; caso haja, fica fora do MVP). \r\nAlterações em regras de folha (processamento do RM em si).	As operadoras/corretora conseguem fornecer dados em Excel (pelo menos Bradesco Dental já dispõe; Unimed e outras serão verificadas).\r\n\r\nO time enviará mensalmente a posição atual da folha (RM) para confronto.\r\n\r\nA base inicial (Empregados, Particularidades, PJ) será carregada e passará a ser mantida dentro da plataforma (com exportação quando necessário).\r\n	Variabilidade de layout entre operadoras (ex.: Bradesco vs. Unimed) exigirá mapeamentos específicos por fonte.\r\n\r\nCaso alguma operadora não entregue Excel, a ingestão via PDF será possível, porém mais lenta e sujeita a erro; prioriza-se Excel.\r\n\r\nNecessidade de não perder histórico ao atualizar cadastros; a plataforma deve versionar registros em vez de “sobrescrever sem trilha”. (Preocupação expressa na reunião sobre não perder informação ao migrar das planilhas.)\r\n	pausado	0	\N
9	Base de Dados de Contas a Pagar (RM → Camada de Dados para BI)	\N	2025-08-26 19:02:14.155251	1	6	Construção de uma base de Contas a Pagar a partir da API do TOTVS RM, aplicando padronização, classificação e limpeza dos dados para alimentar, de forma confiável e escalável, as saídas de BI já utilizadas pela equipe de shopping da Sá Cavalcante. A plataforma e seu funcionamento já foram definidos; próximo passo é gerar o primeiro dataset do RM para teste do Hudson.	Construção de uma base de Contas a Pagar a partir da API do TOTVS RM, aplicando padronização, classificação e limpeza dos dados para alimentar, de forma confiável e escalável, as saídas de BI já utilizadas pela equipe de shopping da Sá Cavalcante. A plataforma e seu funcionamento já foram definidos; próximo passo é gerar o primeiro dataset do RM para teste do Hudson.	Problema: dados de AP dispersos/inconsistentes no ERP dificultam análises consistentes e comparáveis no BI; esforço manual de reconciliação e classificação.\r\n\r\nOportunidade: criar camada de dados única, limpa e audível para acelerar análises de despesas/fornecedores, reduzir retrabalho e melhorar a governança (LGPD, trilhas de auditoria, versionamento).	Extrair dados de AP do RM (fornecedores, títulos, centros de custo, filiais, natureza/despesa) via API.\r\n\r\nTransformar & padronizar (tipos, datas, moedas, CNPJ, DRE/natureza, tags e taxonomia de classificação).\r\n\r\nDeduplicar e validar (regras de integridade, chaves compostas, consistência entre entidades).\r\n\r\nPersistir em schema analítico (camadas raw → staging → curated), pronto para consumo pelo BI atual.\r\n\r\nEntregar um primeiro recorte (amostra representativa) para UAT com o Hudson e iteração rápida.\r\n\r\nAutomatizar a atualização (jobs agendados, observabilidade e logs de cargas).	Eficiência Operacional: diminui retrabalho e tempo para fechar análises de despesas.\r\n\r\nGovernança de Dados: padronização, rastreabilidade e controles (LGPD).\r\n\r\nApoio à Decisão: BI alimentado por base confiável e atualizada.\r\n\r\nEscalabilidade: arquitetura reaproveitável para outras áreas/tabelas do RM.	Mapeamento de endpoints da API RM necessários para AP (títulos, fornecedores, centros de custo, naturezas, filiais).\r\n\r\nIntegração com RM (auth, paginação, limites, retries).\r\n\r\nETL/ELT: extração, normalização, enriquecimento (ex.: CNPJ, CEP), classificação (taxonomia acordada).\r\n\r\nRegras de qualidade: deduplicação, integridade referencial, checks de nulos/outliers.\r\n\r\nModelo de dados analítico (camadas raw/staging/curated) documentado.\r\n\r\nEntrega do primeiro dataset para testes (UAT com Hudson), + ajustes de classificação.\r\n\r\nConectores para o BI atual (exposição de views ou tabelas prontas).\r\n\r\nObservabilidade: logs de carga, métricas de qualidade e tabela de execuções.	Alterações em dashboards de BI (criação/revogação de relatórios).\r\n\r\nMudanças funcionais no ERP RM (cadastros, processos upstream).\r\n\r\nReconciliação contábil/fiscal manual caso-a-caso.\r\n\r\nIntegrações com sistemas além do RM/BI atual (nesta primeira fase).	Acesso estável à API do RM com credenciais e permissões adequadas.\r\n\r\nTaxonomia de classificação acordada com a Equipe de Shopping/BI (ou versão 1 aprovada).\r\n\r\nAmbiente de dados/warehouse disponível (ou provisionamento incluso nesta fase).\r\n\r\nO BI atual consegue consumir tabelas/views publicadas no schema acordado.\r\n\r\nHudson disponível para testes UAT do primeiro dataset.	LGPD/Segurança: criptografia em repouso/trânsito, PII mascarada nas áreas necessárias.\r\n\r\nLimites da API RM (rate limits, janelas, paginação).\r\n\r\nJanela de disponibilidade do RM (manutenções/paradas).\r\n\r\nPrazos internos do calendário do Shopping (fechamentos, cutoff de atualizações).\r\n\r\nInfraestruturas e ferramentas definidas pela TI do cliente.	pausado	0	\N
14	RPA de Conciliação de Shoppings	\N	2025-08-26 20:59:45.780662	1	6	Desenvolvimento e implantação de uma solução de automação robótica de processos (RPA),\r\nutilizando Python e PyAutoGUI, para realizar a conciliação financeira diária dos shoppings\r\nadministrados pela Sá Cavalcante no sistema legado (VS). A automação executa login, importa\r\narquivos bancários, realiza integrações e baixas conforme regras específicas de cada shopping,\r\ndiferenciando o processo para shoppings do Espírito Santo (Banco Santander, múltiplos arquivos\r\npor fase) e shoppings de outros estados (arquivos fixos por fase).	Desenvolvimento e implantação de uma solução de automação robótica de processos (RPA),\r\nutilizando Python e PyAutoGUI, para realizar a conciliação financeira diária dos shoppings\r\nadministrados pela Sá Cavalcante no sistema legado (VS). A automação executa login, importa\r\narquivos bancários, realiza integrações e baixas conforme regras específicas de cada shopping,\r\ndiferenciando o processo para shoppings do Espírito Santo (Banco Santander, múltiplos arquivos\r\npor fase) e shoppings de outros estados (arquivos fixos por fase).	Problema atual: O processo de conciliação é realizado manualmente, consumindo tempo\r\nsignificativo dos analistas e sendo altamente repetitivo. Além disso, as regras variam entre\r\nshoppings do Espírito Santo e de fora, aumentando a complexidade e o risco de erros.\r\nOportunidade: Automatizar o processo de conciliação para garantir consistência, reduzir erros,\r\notimizar o tempo de execução e garantir o cumprimento dos prazos diários.	• Automatizar a conciliação financeira diária dos shoppings.\r\n• Diferenciar o processo conforme a localização dos shoppings (ES vs. outros estados).\r\n• Garantir a importação e baixa de todos os arquivos obrigatórios, respeitando a ordem de\r\nportadores.\r\n• Reduzir a carga operacional dos analistas, permitindo foco em tarefas de maior valor agregado.\r\n• Assegurar consistência e padronização nas conciliações financeiras.	• Eficiência Operacional: Automatização diária dos processos críticos de conciliação.\r\n• Confiabilidade: Execução precisa das regras de importação e baixa por portador.\r\n• Escalabilidade: Possibilidade de incluir novos shoppings no processo sem grandes adaptações.\r\n• Transformação Digital: Modernização dos processos administrativos da Sá Cavalcante.	Incluído:\r\n• Automação de login no sistema legado (VS).\r\n• Execução do aplicativo de conciliação com seleção de shopping.\r\n• Importação de arquivos diários conforme disponibilidade.\r\n• Processamento de múltiplos arquivos por fase (empreendedor, condomínio, fundo).\r\n• Baixa de arquivos em portadores definidos para cada shopping.\r\n• Diferenciação entre shoppings do Espírito Santo (Banco Santander, múltiplos arquivos por fase) e\r\nshoppings de outros estados (arquivos fixos por fase).\r\n• Finalização automatizada do processo no aplicativo.	• Alterações ou modernização do sistema legado (VS).\r\n• Geração ou manipulação de relatórios financeiros.\r\n• Conciliação bancária posterior aos registros importados.\r\n• Suporte direto a bancos ou lojistas.	• Sistema legado (VS) disponível diariamente.\r\n• Arquivos bancários corretamente disponibilizados no prazo.\r\n• Regras de portadores definidas e estáveis para cada shopping.\r\n• Ambiente servidor disponível e configurado para rodar a RPA.	• Processo dependente do VS, sujeito a falhas do sistema.\r\n• Necessidade de execução diária, sem atrasos.\r\n• Processamento sequencial (um shopping por vez).\r\n• Diferenças de processo entre shoppings do Espírito Santo e de outros estados exigem\r\nmanutenção diferenciada.	em_andamento	0	\N
3	Conciliação PDV × Fiscal (SEFAZ/Relatório da Empresa) com AI - Leidiane	\N	2025-08-26 15:25:23.542846	1	4	Construir um fluxo de conferência automatizada entre as vendas/receitas do PDV e os registros fiscais (SEFAZ e relatório da empresa), com ingestão massiva de XML, separação por filial/relatório, dashboards/analytics e otimizações de desempenho (fila e upload zipado), usando AI para apoiar validação e análise.									pausado	0	\N
5	Plataforma de Conciliação Contábil & Fiscal – EVO + Extratos - Academia	\N	2025-08-26 16:25:54.584651	1	10	Construção de uma plataforma web (login, perfis e trilhas de auditoria) para:\r\n\r\nRateio/apropriação de receitas do EVO (Bodytech) substituindo a planilha atual com fórmulas/macros e gerando o fluxo mensal (parcelas, início/fim, conta contábil etc.);\r\n\r\nConciliação bancária x contabilidade padronizando extratos por banco e cruzando com relatórios do RM/balancete para apontar diferenças antes da integração contábil;\r\n\r\n(Próximo) Painel unificado de fechamento contábil + fiscal. 									pausado	0	\N
27	FGQuotes – Sistema Inteligente de Criação e Gestão de Cotações	\N	2025-10-14 17:03:00.176907	3	7	O FGQuotes é uma aplicação web desenvolvida para automatizar a geração, envio e acompanhamento de cotações comerciais.\r\nO sistema integra-se ao Salesforce e a serviços de e-mail para criar propostas com base em dados de clientes, histórico de vendas e condições personalizadas.	O FGQuotes é uma aplicação web desenvolvida para automatizar a geração, envio e acompanhamento de cotações comerciais.\r\nO sistema integra-se ao Salesforce e a serviços de e-mail para criar propostas com base em dados de clientes, histórico de vendas e condições personalizadas.	O processo de elaboração de cotações em diversas empresas ainda é manual, demorado e sujeito a erros, exigindo a coleta de dados dispersos em diferentes sistemas (CRM, planilhas e e-mails).\r\nHá uma oportunidade clara de automatizar esse fluxo, reduzindo tempo de resposta ao cliente e aumentando a taxa de conversão de propostas.	Automatizar a criação e o envio de cotações comerciais.\r\nReduzir o tempo médio de geração de propostas em até 70%.\r\nIntegrar o processo de cotação ao Salesforce, mantendo os dados sincronizados.\r\nUtilizar IA para sugerir valores competitivos e otimizar margens.\r\nPermitir acompanhamento e histórico completo das propostas enviadas.	Este projeto está alinhado à estratégia de transformação digital e automação de processos comerciais, apoiando a eficiência operacional e a inteligência de vendas.\r\nA solução também fortalece o posicionamento da empresa no uso de tecnologia e IA aplicada à área comercial.	Inclui:\r\n\r\nBackend em Python (Flask) com banco de dados relacional.\r\nMódulo de IA para sugestão automática de preços.\r\nIntegração com Salesforce e e-mail corporativo.\r\nInterface web para criação, edição e acompanhamento de cotações.\r\nPainel de controle com métricas de performance comercial.\r\nAutomação de envio e registro de status das propostas.	Fora do Escopo:\r\n\r\nIntegração com ERPs financeiros.\r\nGestão de contratos pós-fechamento.\r\nProcessamento de pagamentos.	O cliente fornecerá acesso ao ambiente Salesforce e às APIs de autenticação.\r\nA infraestrutura permitirá execução contínua de serviços assíncronos.\r\nTodos os usuários terão acesso autenticado via login corporativo.\r\nOs templates de e-mail e cotação serão aprovados previamente pelo cliente.	Limite de requisições por minuto às APIs externas (Salesforce e IA).\r\nDependência de conexão estável com serviços de terceiros.\r\nEscopo inicial limitado a cotações em moeda local.\r\nAmbiente de implantação restrito ao servidor autorizado pelo cliente.	em_andamento	0	\N
28	 Mapeamento e Automação de Processos Aeropool	\N	2025-10-14 17:12:57.812312	3	7	O projeto tem como objetivo mapear e otimizar os processos operacionais da Aeropool, replicando o modelo de automação já implementado na AVSales.\r\nA iniciativa busca centralizar as operações de reparo e manutenção diretamente dentro do Salesforce, eliminando a necessidade de uso de sistemas paralelos e garantindo rastreabilidade completa das demandas operacionais.	O projeto tem como objetivo mapear e otimizar os processos operacionais da Aeropool, replicando o modelo de automação já implementado na AVSales.\r\nA iniciativa busca centralizar as operações de reparo e manutenção diretamente dentro do Salesforce, eliminando a necessidade de uso de sistemas paralelos e garantindo rastreabilidade completa das demandas operacionais.	Atualmente, os processos de reparo e manutenção na Aeropool envolvem múltiplos sistemas e etapas manuais, o que gera retrabalho, lentidão e falta de visibilidade operacional.\r\nHá uma oportunidade de padronizar e automatizar esses fluxos dentro do Salesforce, trazendo mais eficiência, controle e integração entre as áreas envolvidas (técnica, logística e administrativa).	Mapear detalhadamente os processos operacionais da Aeropool;\r\nAutomatizar os fluxos de reparo e manutenção dentro do Salesforce;\r\nGarantir que todas as solicitações sejam gerenciadas por um único sistema;\r\nAumentar a eficiência e reduzir o tempo de resposta operacional;\r\nReaproveitar as boas práticas e estrutura da automação criada para a AVSales.	O projeto está alinhado à estratégia corporativa de transformação digital e unificação das plataformas operacionais.\r\nA centralização das operações no Salesforce fortalece o controle sobre o ciclo de manutenção, melhora a governança de dados e contribui diretamente para aumento da produtividade e redução de custos operacionais.	Levantamento e documentação de todos os processos operacionais da Aeropool;\r\nIntegração completa com Salesforce para gestão de reparos;\r\nAjustes e parametrizações específicas para os fluxos de manutenção;\r\nTestes e validações de ponta a ponta com as equipes de operação;\r\nTreinamento interno sobre o novo fluxo automatizado.	Desenvolvimento de novos módulos externos ao Salesforce;\r\nCustomizações não relacionadas aos fluxos operacionais;\r\nIntegrações com sistemas de terceiros fora do escopo atual.			pausado	0	\N
29	Sistema de Gestão de projetos  	\N	2025-10-14 19:44:25.949492	2	5										em_andamento	0	\N
33	Consultor Geral de IA + Comunicação Personalizada	\N	2025-10-26 20:15:32.714448	5	5	Desenvolvimento de um consultor inteligente baseado em IA capaz de interpretar dados de clientes e gerar comunicações personalizadas, recomendações e análises estratégicas. O projeto unifica as iniciativas de “Consultor Geral de IA” e “Comunicação Personalizada”, utilizando uma mesma base de dados estruturada para otimizar a automação e o relacionamento com o cliente.	Desenvolvimento de um consultor inteligente baseado em IA capaz de interpretar dados de clientes e gerar comunicações personalizadas, recomendações e análises estratégicas. O projeto unifica as iniciativas de “Consultor Geral de IA” e “Comunicação Personalizada”, utilizando uma mesma base de dados estruturada para otimizar a automação e o relacionamento com o cliente.	Atualmente, a OAZ possui dados estruturados, mas não utiliza plenamente o potencial da inteligência artificial para personalizar comunicações ou análises. Existe uma oportunidade de integrar a IA ao CRM para gerar insights automáticos, recomendações e mensagens sob medida para cada cliente, aumentando engajamento e eficiência operacional.	Criar um consultor inteligente que interprete dados e gere respostas contextualizadas.\r\n\r\nIntegrar o sistema à base de dados existente da OAZ (por loja, setor e função).\r\n\r\nAutomatizar comunicações personalizadas com base em dados reais e atualizados.\r\n\r\nEstabelecer um fluxo de análise contínuo para melhoria de processos e comunicação.	O projeto está alinhado à estratégia de digitalização e automação da OAZ, fortalecendo a posição da empresa como referência em uso de IA aplicada à gestão e comunicação. Também contribui para a meta de ampliar a eficiência operacional e a personalização no atendimento aos parceiros e clientes.	Mapeamento e integração da base de dados existente.\r\n\r\nDesenvolvimento do modelo de IA para análise e personalização de comunicações.\r\n\r\nCriação de interface para uso interno e monitoramento dos resultados.\r\n\r\nImplementação de testes com a equipe da OAZ e ajustes conforme feedback.\r\n\r\nCapacitação da equipe para utilização e ajustes contínuos da ferramenta.	Desenvolvimento de novas bases de dados externas.\r\n\r\nImplementações em sistemas de terceiros sem integração prévia.\r\n\r\nAutomação de comunicações em massa sem curadoria humana inicial.	Base de dados estruturada e acessível pela equipe técnica.\r\n\r\nApoio da equipe de tecnologia da OAZ durante a integração.\r\n\r\nValidação contínua de resultados pelos responsáveis de cada setor.\r\n\r\nUtilização da infraestrutura já existente da OAZ para testes iniciais.	Prazos dependem da disponibilidade dos dados e do time técnico.\r\n\r\nIntegração limitada aos sistemas com APIs acessíveis.\r\n\r\nAjustes no modelo de IA podem demandar reprocessamento de dados.	pausado	0	\N
36	Sistema de Transcrição e Identificação de Speakers — Conselho Sá Cavalcante	\N	2025-10-27 18:28:20.084002	1	2	Desenvolvimento de um sistema para captura, transcrição e organização das reuniões de conselho da Sá Cavalcante em um banco de dados estruturado. As reuniões são presenciais, e o sistema deverá identificar automaticamente os participantes (speakers) e vincular suas falas às transcrições, garantindo precisão, rastreabilidade e histórico centralizado das decisões.	Desenvolvimento de um sistema para captura, transcrição e organização das reuniões de conselho da Sá Cavalcante em um banco de dados estruturado. As reuniões são presenciais, e o sistema deverá identificar automaticamente os participantes (speakers) e vincular suas falas às transcrições, garantindo precisão, rastreabilidade e histórico centralizado das decisões.	Atualmente, as reuniões de conselho não possuem uma sistematização eficiente das discussões e decisões. As atas são produzidas manualmente e não há uma forma automatizada de identificar quem disse o quê. Essa ausência de estrutura dificulta o acompanhamento das deliberações e compromete a rastreabilidade de informações estratégicas.\r\nA oportunidade está em aplicar inteligência artificial e automação para transformar as gravações em dados estruturados, otimizando o processo e facilitando análises futuras.	Implementar um pipeline automático de transcrição das reuniões presenciais.\r\n\r\nIdentificar e rotular os participantes (speakers) de forma precisa.\r\n\r\nArmazenar as transcrições e metadados em um banco de dados organizado e pesquisável.\r\n\r\nPermitir buscas e filtros por data, tema ou participante.\r\n\r\nCriar dashboards e relatórios para consultas rápidas de decisões passadas.	O projeto está alinhado ao objetivo de modernizar a governança corporativa da Sá Cavalcante, promovendo transparência e eficiência na gestão das reuniões de conselho. Também reforça o uso de tecnologias de IA para otimização de processos internos, conforme a estratégia de digitalização do grupo.	Coleta de gravações das reuniões presenciais.\r\n\r\nTranscrição automática com uso de modelos de reconhecimento de voz.\r\n\r\nIdentificação e rotulagem dos speakers com base em padrões de voz.\r\n\r\nArmazenamento estruturado em banco de dados.\r\n\r\nInterface para consulta e gestão das transcrições.\r\n\r\nGeração de relatórios e insights com base nos dados transcritos.	Captação de áudio nas reuniões (o sistema parte de arquivos gravados previamente).\r\n\r\nTradução automática das transcrições.\r\n\r\nIntegração direta com sistemas externos de videoconferência.\r\n\r\nAnálise semântica avançada (fase futura).	As reuniões serão gravadas com boa qualidade de áudio.\r\n\r\nTodos os participantes consentem com o uso de gravações para fins internos.\r\n\r\nA equipe técnica terá acesso aos arquivos de áudio e metadados necessários.\r\n\r\nO ambiente de armazenamento será seguro e de uso restrito.	Limitações na qualidade do áudio podem impactar a acurácia da identificação dos speakers.\r\n\r\nO projeto deve seguir a LGPD e as políticas internas de privacidade da Sá Cavalcante.\r\n\r\nPrazo máximo de entrega da primeira versão funcional: 45 dias.	em_andamento	0	\N
39	Urban B2B	# Meeting Transcription\r\n\r\n  Meeting started: 30/10/2025, 14:47:31\r\n  Duration: 22 minutes\r\n  Participants: Felipe Gomes, Paulo Calarge, Raphael Banos, Renato Lagden\r\n\r\n  [View original transcript](https://app.tactiq.io/api/2/u/m/r/Ao81qXADQOvGGn6VY3sY?o=txt)\r\n\r\n    \r\n\r\n  \r\n\r\n  \r\n\r\n  ## Transcript\r\n\r\n  00:00 Paulo Calarge: tu quer fazer daqui a gente vai naquela parada de ainda\r\n00:23 Felipe Gomes: Ainda bem que eu não gostei.\r\n00:30 Paulo Calarge: Achei que tava no Paraná, cara.\r\n00:31 Felipe Gomes: E aí Renato, tudo bom cara?\r\n00:33 Renato Lagden: Tudo bem.\r\n00:34 Felipe Gomes: Tá pelo rio? Perguntei para ele.\r\n00:39 Renato Lagden: Estou de barco, né? Escritório está gelado para caramba. O Rafa já está entrando aí?\r\n00:55 Paulo Calarge: Estável aqui hoje aqui, não sei que tá vendo aí.\r\n00:58 Felipe Gomes: Já tá transcrevendo?\r\n01:01 Felipe Gomes: Olá, estou transcrevendo esta chamada com minha extensão Tactiq AI: https://tactiq.io/r/transcribe\r\n01:05 Renato Lagden: Tudo certo. Tudo certo correria aí pré black friday, já começou né?\r\n01:08 Paulo Calarge: Olá, estou transcrevendo esta chamada com minha extensão Tactiq AI: https://tactiq.io/r/transcribe\r\n01:15 Renato Lagden: Eu odeio Black Friday. É porque Pô, a gente acabou com o Natal que era uma era uma festa que a gente vendia um mês inteiro imagem toda nossa para passar a vender duas vezes mais sem imagem. Tá controlado tá controlado? A gente faz um planejamento prévio assim bem bem estruturado também bem tranquilo. O gargalo maior aqui acaba sendo produzido.\r\n01:56 Raphael Banos: Boa tarde Tudo bem.\r\n02:11 Paulo Calarge: Vamos lá Renato, se puder passar para gente. O que que você tem aí?\r\n02:16 Renato Lagden: Então, só só apresentando aqui, o Rafa, ele é o nosso gerente de marketing. contextualiza as marcas mas também toca um pouco do processo comercial de Urban, ele tá passando esse bastão para o Jairo gradativamente mas De fato ele faz o comercial também, porque ele tem um relacionamento, né forte com a rede, principalmente desse mundo custo. E Rafa Paulo Felipe enfim. Tem a inova aí aquela aquela solução que eles criaram lá para Franca, eu comentei.\r\n02:52 Renato Lagden: funcionou super bem super rápido super desenrolado sem Sem burocracia e aí ontem não. Não eu tava conversando ontem com o Rafa e compartilhei um catálogo com ele do Bahamas esportes. E ele teve uma ideia né de transformar esse catálogo para urbanmetsiclismo. Numa história mais interativa onde o cliente receber esse catálogo e pudesse digitar o seu pedido dentro do próprio catálogo e não apertar de botão, de repente a gente conseguir gerar tá o planilha que a gente faz o input, né saber porque o atacado também é desintegrado. A gente não tem um sistema de vendas é tudo feito no braço no Excel, tem um sisteminha lá meio que Para tapear isso, mas a gente não tem uma automação ou mesmo um sistema nativo para o atendimento de atacado. Ele é feito na unha.\r\n03:45 Raphael Banos: Falar que hoje o nosso sistema de venda para o bit to be é arcaico dentro de Urban é quase um eufemismo positivo, porque mais arcaico do que a gente faz. Só se fizesse anotado no papel de pão uma planilha de excel que tem código tem preço tem tem uma fotinho lá só para o cara entender a diferença entre os capacetes. Mas o negócio que já me irrita muito tempo. E aí ontem na hora que o Renato me mandou o catálogo me deu um estralo eu falei pô, por que que a gente não tem um catálogo interativo que eu mando o catálogo para o cara o cara entende um pouco da Vibe da marca, ele consegue ver os itens lá eu falo nem digitar o pedido é adicionar que nem um iFood da vida assim, olha esse eu quero dois daquele tamanho. Eu quero três.\r\n04:29 Raphael Banos: E na hora que o cara Esporte que ele deu entre ali ó pedido realizado e isso já Vá para nossa para o nosso comercial que faz o input. Se possível da forma mais. Automatizada de ser colocado né? Já o arquivo acho que se chama XLS que faz o input, né Renato?\r\n04:48 Renato Lagden: Eu acho que é um XLS não é?\r\n04:50 Raphael Banos: Eu acho que a XLS já no XLS que o nosso sapelê e a pessoa só tá lá para apertar o enter no nosso comercial e jogar aquilo para dentro tá o meu sonho na verdade. É que isso aí seja um dia online, a gente faz o cadastro online do cara. E aí online o cara entra no site já faz o pedido. Mas como isso não é possível. Eu falei pô. Tô cansado de ficar esperando uma solução do SAP para a gente poder tornar isso online. Então vamos fazer uma solução à parte que não seja um catálogo uma tabela XLS que é ridículo.\r\n05:21 Raphael Banos: Então o que eu pensei é algo que a gente não tô falando. Tem que ser uma interface da Com a parte de design funcional Interativo da Nasa não mas que dê para aplicar um layout que as pessoas entendam a vibe da marca olhando aquilo que o cliente que compra nossa, marca ele já entende um pouco do que a gente faz então um lugar que ele entre ele já reconheça que tá no ambiente nosso ele vê os produtos lá seja super interativo dele clicar e adicionando como se fosse um carrinho de compras virtual.\r\n05:49 Raphael Banos: Mesmo mas de alguma coisa mais voltada para o mobile e quando ele dá o enter já automatiza tudo lá para dentro da fábrica, só que a pessoa joga para dentro dessa P. A ideia é essa. Eu não sei se é possível como é fazível. Se não tem ideia disso foi só. A lampadinha que estourou na cabeça.\r\n06:09 Paulo Calarge: Não beleza especialistas\r\n06:20 Felipe Gomes: Cara, O Renato me mandou aqui o pdf já. Você tem esse PDF? Deixa eu deixa eu ver se eu entendi aqui você tem esse PDF hoje, você manda ele para os teus clientes e a partir desse PDF o cara vai te dizendo pô, eu quero tantos capacete do Flamengo tantos do Corinthians.\r\n06:35 Renato Lagden: Não esse PDF do Bahamas Sports.\r\n06:52 Raphael Banos: Esse PDF já é um negócio muito evoluído perto do que a gente faz para Urban\r\n08:42 Raphael Banos: helmets.\r\n08:42 Renato Lagden: Não tem nem isso é um Excel com fotinho no máximo vai ser. A gente vai ter que criar um desse bonitinho na vida.\r\n08:43 Raphael Banos: A ideia tem um catálogo para urbanas que o Urban Sports são os capacetes para patins skate.\r\n08:43 Renato Lagden: é\r\n08:43 Raphael Banos: Eu acho que cai a conexão deles.\r\n08:44 Paulo Calarge: É a nossa conexão até tirei a imagem. para facilitar\r\n08:44 Renato Lagden: Mas acho que o Felipe caiu mesmo, né? Ah não voltou. Não sei Felipe, tá vendo?\r\n08:44 Raphael Banos: Paulo volta que a gente também não fala duas vezes.\r\n08:44 Felipe Gomes: tá\r\n08:44 Raphael Banos: Paulo será que ele tá ouvindo a gente pelo menos?\r\n08:44 Renato Lagden: então\r\n08:44 Raphael Banos: Esse catálogo que o Renato É da Urban Sports que a nossa marca de capacete para mobilidade urbana patins e tudo mais a gente tem a Urban realme que tem capacetes para motociclismo e ainda tem alguns itens de Live Style, então tem boné tem vestuário tem alguma coisa de acessório tá a nossa ideia é que o nosso catálogo vá. Visual Não que seja idêntico. Mas você olha esse catálogo da Urbana realmente Sporting é um catálogo bonito da gosto de ver você, olha ali você entende? O que tá acontecendo é ter uma uma interface um aplicativo. Não sei como funciona isso. Tá? Mas ter algo que o cara entra ele vê um visual próximo a esse que é que traz a vibe da marca que transpiram que a marca faz isso a gente tem bastante bastante conteúdo tem bastante tipografia tem imagem foto para o cara entrar nesse ambiente, que seja um aplicativo ou um link ou fornece.\r\n09:21 Raphael Banos: E aí ele tá lá ele olhar Pô, esse capacete é que eu gostei clica nele. Ah desse aqui eu quero três unidades, ele só adiciona. Aquele carrinho ó mais um dois três e aí isso vai dando uma conta lá no final que ele vai saber quanto é o valor que ele vai receber. Ele olhou lá concordou apertou enter. Vai direto para fábrica. E aí isso eu vou poder eu usava vou poder passar para os meus representantes comerciais para facilitar a venda desse produto esse produto é um produto que tem a venda muito encravada ainda e eu quero tornar ela dinâmica. Como é o nosso produto Premium. Eu acho que é o produto que a gente pode começar a botar no Beat B um sistema mais moderno de fazer a venda. E aí através desse.\r\n09:59 Raphael Banos: Não sei não sei nem o nome que a gente pode dar para isso é um aplicativo chama Inteligência Artificial se é um link se é um forms. Mas é para isso que a gente tá precisando desenvolver o negócio.\r\n10:10 Felipe Gomes: Não você tá querendo criar isso é verdade?\r\n10:15 Raphael Banos: É seria um e-commercebit to be, mas eu não sei se isso necessariamente tem que ficar online, entendeu? Não sei também cara. Essa parte aí.\r\n10:25 Felipe Gomes: O cara vai fazer o coisa, entendeu? Como é o cara vai te mandar o pedido, mas o cara entendeu? Porque eu tava pensando aqui era criar um sistema para você subir os produtos lá, sei lá, você falou que você tem uma planilha de XLS que tem um Excel, né? Então, sei lá você subir esse celular ele carregava a base do produto lá estagmentos com a coisa toda certa, beleza? A partir daquilo dali. A gente criaria uma Hot Page para você igual é o pdf que seria um link. Ah quero 10 desses cinco desse três desse tá? Fecha aqui para me pedir fechou o pedido e demora o pedido fechado para o cara lá confirmar pedido confirmar aí você vê uma tela de administrador aí todos os pedidos que foram feitos e confirmados por essa por esse cara.\r\n11:09 Raphael Banos: Esse Hot link pode ser um link oculto na minha própria o site.\r\n11:14 Felipe Gomes: Pode acredito que sim, cara, tem que ver como é que é.\r\n11:18 Raphael Banos: .com/\r\n11:20 Renato Lagden: Como incluir o URL dentro?\r\n11:24 Felipe Gomes: Eu acho que isso\r\n11:26 Renato Lagden: Acho que a gente tem que ter para dar o suporte para o pessoal, imagina se tem\r\n11:28 Raphael Banos: Porque aí facilita muito tudo, né? Porque aí o representante está lá, pô, o que que você tem disponível aí sobe lá tem isso disponível. Ah, o que que tem de estoque a gente consegue atualizar o que tem estoque mais fácil. Sei lá o que eu estou pensando em facilitar tudo aqui porque realmente do jeito que tá deu.\r\n11:52 Renato Lagden: uma solução. Imagino que tenha é o catálogo que não é esse. Seria algo como esse. Para dar o quesito visual a planilha com todos os dados que a planilha do input de preço sku tamanho. E essa de estoque tem que ser alto atualizado Rafa ou você também faz venda sem ter estoque.\r\n12:14 Raphael Banos: Cara normalmente eu não faço venda sem ter estoque não, eu acho que talvez a gente vai ter que fazer uma manutenção. Daí a gente do que vai estar lá disponível mais frequentemente.\r\n12:24 Renato Lagden: mas isso\r\n12:26 Felipe Gomes: É onde que você vê essa essa informação do estoque. Mas você tem algum relatório que você consegue tirar de lá para saber o estoque? É a gente pode criar uma parada, tipo assim, pega esse relatório aqui, se for um xlsx organizado. E aí toda vez que você subir ele lá ele atualiza o estoque ele pega aquela posição de estoque ali que você tá subindo até depois Renato a gente pensar nisso integrar com essa IP direto que aí não precisa pegar isso. Eu acho que tem algum momento esse projeto tá gente? Não é um projeto assim a primeira versão seria você ter um lugar ali onde você sobe a planilha sobe? O estoque é. E aí ele vai gerar esse um catálogo de produtos para você e vai gerar um link, que que a gente pode botar aparência que tem aqui o pdf. Sem problema ou então até pensar numa nova num novo layout. A gente só não é bom em design, mas assim vocês criando a frente o que que vocês querem a gente consegue fazer de boa.\r\n13:24 Raphael Banos: Então completo que a gente faz que a parte do designer te Desenrola agora a parte da montagem.\r\n13:28 Felipe Gomes: Então perfeito, aí vai ter dentro dessa plataformazinha um lugar aonde você que a pessoa que tá naquele link que ele pode mas assim você manda para isso qualquer pessoa pode comprar por esse link.\r\n13:43 Renato Lagden: Não isso vai falar aqui agora tem dois dois dados que a gente tem que ter como regras de negócio, cadastro ativo e tabela fiscal. Porque dependendo do Estado incide ST ou não então, acho que a gente vai ter que ter uma.\r\n13:55 Felipe Gomes: Mas vocês têm uma lista de cadastros.\r\n13:58 Renato Lagden: Que também tá nessa P, isso aí dá para a gente fazer o mesmo fluxo que a gente faria para inventário até com menos carga de atualização, a gente faria para o banco de dados de clientes.\r\n14:10 Felipe Gomes: É a minha o que eu tô pensando aqui, como é que vocês gera uma facilidade para o usuário para ele entrar no link dele comprado o link dele que ele não precisa botar nome, não precisa botar nada, mas aí você tem um link para cada para cada cara que tá dentro seu entendeu? Não é difícil de fazer isso, mas aí ficaria complexo do comercial. Ah, eu vou mandar o link para fulano de tal.\r\n14:29 Felipe Gomes: Tem que ir lá no sistema e copiar o link de fulano de tal que aí o cara compra para aquele link ali, não precisa informar nada só ele lá e botar a quantidade que ele quer. Chega para a gente chega para vocês aqui e tudo mais porque a minha preocupação mais a gente saber quem tá pedindo.\r\n14:44 Renato Lagden: Esse forró com login e senha.\r\n14:48 Felipe Gomes: Cara aí para mim é só a preocupação de você dar mais uma uma etapa para o teu cara na compra aí o cara tem que fazer um.\r\n14:55 Raphael Banos: Renato eu acho que é o seguinte, esse aí é o mesmo risco da gente mandar um negócio aberto. Por um cliente que vai receber a tabela e não vai fazer compra o cara pode preencher pode fazer tudo. Se ele mandar para a gente ele não tiver cadastro comercial na prova o trabalho que o comercial vai ter é receber essa tabela ver se o cadastro tá ativo que é isso aí o nosso o nosso crime comercial já faz.\r\n15:17 Renato Lagden: Tá seria a versão Beta, depois a gente evolui para uma coisa mais.\r\n15:21 Raphael Banos: interativa\r\n15:24 Paulo Calarge: É porque também você\r\n15:25 Felipe Gomes: Aí o cara colocaria. Além do cara escolher os produtos ele colocaria o nome telefone CNPJ ou qualquer coisa do tipo que vocês precisam.\r\n15:34 Raphael Banos: Sim. Acho que botei no CNPJ já resolve porque aí já vem tudo o CNPJ contato e telefone.\r\n15:40 Felipe Gomes: Primeira depois que ele finalizar a compra.\r\n15:40 Raphael Banos: Mas eu acho que é o seguinte só a partir do momento que o cara deu enter ele bota só o CNPJ, porque começar colocando CNPJ é um cara. Ele escolhe tudo finalizar depois o CNPJ porque ele já preencheu tudo. Aí depois que ele preencheu tudo. Ele falou p*** agora não vou fazer porque tem CNPJ agora segundo negócio que começa com CNPJ o cara p*** não vou fazer.\r\n15:58 Felipe Gomes: É isso. Não não a gente a gente bota CNPJ. Só quando ele finalizar a compra.\r\n16:06 Raphael Banos: É porque aí o comercial recebe Confere o CNPJ vezes cadastro ativos cadastra Positivo e aí mete bronca no pedido, cara. Se isso funciona assim já é um adianto assim. Não é não é 100% interativo, não é 100% automatizado não é? Mas por enquanto ainda não vejo como a gente driblar essa questão do comercial até por integração, né?\r\n16:28 Renato Lagden: É o primeiro passo, cara. Que a mesma dor que o Rafa tem em Urban, o Jairo tem para talva só que o Urban vende 200 peças a Taurus vem de 120 mil.\r\n16:42 Felipe Gomes: Aí depois também você pode pensar numa integração com esse banco de dados que o Renato falou dentro da SAP. Por exemplo para o cara já fazer a compra ali o teu comercial. Nem precisar aprovar porque já foi lá cadastrou. Ele já viu que ele é um cara cadastrado que já tem todos esses cheques e tudo mais de um já prova a compra do cara já. Manda direto para fábrica, nem passa, entendeu?\r\n17:00 Renato Lagden: Eu acho que a gente pode fazer assim, então a gente faz esse protótipo para o\r\n17:03 Felipe Gomes: Se a gente consegue ler essa base de dados quando o cara botar o CNPJ consulta essa base de dado tá aqui tá aqui tem tudo que tem que tá até então beleza então já Manda direto para fora. Entendeu?\r\n17:16 Renato Lagden: ombro. Funcionou a gente começa a conectar banco de dados funcionou a gente propõe para o comercial.\r\n17:24 Felipe Gomes: Perfeito por mim perfeito.\r\n17:26 Paulo Calarge: Acho que seria uma versão 1.0, entendeu Renato?\r\n17:31 Renato Lagden: O negócio pronto a gente começa a rodar, depois a gente evolui.\r\n17:36 Paulo Calarge: E o que Você Quiser de arquivo aí que faltaria para acrescentar aí na\r\n17:41 Renato Lagden: Rafa a gente vai te incluir no grupo, tá?\r\n17:43 Raphael Banos: Tá bom.\r\n17:46 Renato Lagden: A gente quase pede desculpa quando fala isso não é mais um grupo, tá?\r\n17:49 Raphael Banos: Aqui no começo negócio de grupo do WhatsApp era muito divertido, só que hoje Qualquer ser humano normal que trabalha em empresa tem o 100 grupos diferentes de cada atividade, mas não tem jeito é uma ferramenta super prática. Deixa falar eu prefiro que me adiciona no grupo de WhatsApp que me adicione no círculo de e-mails.\r\n18:06 Felipe Gomes: Nem fala mandar e-mail para mim uma coisa que é difícil, cara, eu lembro.\r\n18:11 Raphael Banos: Para mim é a confirmação do que você faz por telefone.\r\n18:14 Felipe Gomes: Na hora que eu tô Ali chegou a mensagem da galera aqui estão me marcando é isso na hora não tem.\r\n18:19 Raphael Banos: Cara o e-mail para mim é só a formalização, não foi falado pelo telefone que são duas coisas que eu odeio o cara fala com você, aí depois como ele não acredita no que foi falado ele fala não agora eu preciso formalizar pelo e-mail. Eu falo meu Deus do céu, cara, como é anti-producente isso aí acaba sendo mais prático que falou ali tá formalizado tá escrito não tem mais como voltar atrás.\r\n18:42 Felipe Gomes: É isso eu tô contigo também não mas beleza cara, vamos deixa a gente internalizar aqui do comentar aqui pegar essa transcrição que a gente teve aqui o documentar tudo aí, mas entendi perfeitamente. O que que vocês querem com a necessidade de vocês?\r\n18:55 Raphael Banos: Os dois acho que no estoque é menos vergonhoso agora a lista dos produtos é\r\n18:58 Paulo Calarge: análise. A gente já pode pensar em você.\r\n19:01 Felipe Gomes: É o que você poderia mandar para a gente Rafa duas coisas. O primeiro é o arquivo que você usa para fazer o cheque do estoque e o segundo arquivo que você usa para fazer o teu os produtos na lista de produtos.\r\n19:19 Raphael Banos: bem ruinzinho, mas eu mando para vocês. Tá bom.\r\n19:29 Felipe Gomes: Ap. Tenta tirar cru do jeito que ele vem do shp para você não tentar nem trabalhar e ele na plataforma ele vai carregar e vai atualizar o estoque.\r\n19:34 Raphael Banos: tranquilo Tá bom.\r\n19:38 Felipe Gomes: beleza\r\n19:39 Raphael Banos: beleza\r\n19:41 Felipe Gomes: Então é isso galera.\r\n19:43 Renato Lagden: boa\r\n19:43 Raphael Banos: Esse arquivo que eu recebo diariamente com estoque todo dia tem uma pessoa que me manda por e-mail. Então essa pessoa que me manda por e-mail atualizar. Isso numa base de dados de vocês. Todo dia também não seria nada de outro mundo, né, Renato? Já tá mandando para toda equipe.\r\n19:58 Renato Lagden: noite Pode ser mas a ideia é que isso depois seja automático.\r\n20:04 Raphael Banos: Automático né? Mas eu acho que para a gente começar a trabalhar a gente já pode pensar nessa situação.\r\n20:09 Felipe Gomes: Não vão dar trabalho para essa pessoa não, vamos botar um e-mail, a gente cria um e-mail aqui só copia esse e-mail também. Toda vez que chegar o e-mail\r\n20:14 Raphael Banos: perfeito\r\n20:17 Felipe Gomes: que a inteligência artificial entender que aquilo é um e-mail de estoque ela vai lá pega aquilo dali faz o andamento naquilo dali e bota para dentro do estoque.\r\n20:28 Raphael Banos: Eu acho que tem que pensar em mobile, né?\r\n20:29 Renato Lagden: E um terceiro dever de casa que é nosso a gente já tem que criar esse layout.\r\n20:40 Raphael Banos: Acho que hoje você fala de vendedor vendedor hoje em dia na rua tá mostrando tudo com o celular para o cara, né? O catálogo já tem formato mobile.\r\n20:49 Renato Lagden: Sabe esse catálogo? Realmente Claro porque aí a gente vai transformar isso num uma espécie de sisteminha de pedido para o btb, tá bom perfeito. Eu acabei de fazer aquele posto que tem todos os capacetes.\r\n21:18 Raphael Banos: Não, mas eu tenho isso na lista já só precisa adicionar o 3DS.\r\n21:22 Renato Lagden: Tá bom. Fechou. Beleza. Pode ser bonito assim mesmo. Pode ser legal, ele pode botar os Dá para ter um respiros essas coisas que você gosta falar sobre o capacete em\r\n21:42 Raphael Banos: Então eu quero que ele eu já eu mesmo que o negócio que a pessoa consiga ver\r\n21:43 Renato Lagden: si. dicas de segurança\r\n21:48 Raphael Banos: e sentir a vibe da marca do negócio não aparecer um catálogo de\r\n21:52 Renato Lagden: Né, Lojas Americanas?\r\n21:59 Paulo Calarge: Feito então fala.\r\n22:02 Renato Lagden: Beleza Rafa, quando você puder você me chama que eu Tô vendo os e-mails que agora está com uma ferramenta nova de vídeo.\r\n22:04 Raphael Banos: Gente, obrigado.\r\n22:24 Renato Lagden: De configuração. Mas é isso boa, beleza. Gente, obrigado.\r\n22:40 Felipe Gomes: Tchau, tchau.\r\n22:41 Raphael Banos: Tchau, tchau.\r\n  	2025-10-31 19:00:14.931869	7	8	A discussão centra-se na necessidade de modernizar o sistema de vendas B2B da empresa Urban, que atualmente é considerado antiquado e ineficaz. O projeto é justificado pela demanda de uma solução mais interativa e eficiente para seus catálogos, especialmente devido ao volume de pedidos e a expectativa crescente de uma Black Friday, que obriga um planejamento prévio estruturado para evitar gargalos de produção.	A reunião discute a proposta de criar um sistema de catálogo interativo para a marca Urban, que permita aos clientes adicionar produtos a um 'carrinho de compras' virtual e gerar pedidos de forma automatizada, integrando com o sistema existente da empresa.	O problema identificado é o processo arcaico e ineficiente de vendas B2B, que utiliza planilhas Excel para gerenciar pedidos. A oportunidade é desenvolver uma plataforma mais moderna e interativa, que melhore a experiência do usuário e a eficiência do processo de vendas.	Desenvolver um catálogo interativo que permita aos clientes fazer pedidos diretamente, com uma integração futura talvez com o sistema existente para automatizar os processos e evitar a necessidade de aprovação manual do comercial.	O projeto se alinha ao objetivo estratégico de modernização dos processos internos para melhorar a experiência do cliente e aumentar a eficiência operacional, especialmente em períodos críticos como a Black Friday.	Criação de um catálogo interativo que possa ser acessado via mobile, permitindo que os clientes escolham produtos, adicionem a um carrinho de compras e efetuem pedidos, integrando com um banco de dados que verifica automaticamente se o cliente é cadastrado.	Automatização completa e integração imediata com o sistema SAP da empresa não está na fase inicial. O foco inicial é uma solução básica de geração e envio de pedidos.	Os clientes cadastrados na base de dados não precisarão de validação adicional ao fazer pedidos; o catálogo deve ser fácil de usar e acessível via dispositivos móveis.	A implementação inicial não pode incluir integração completa ou dependência de outras plataformas como SAP. O sistema deve funcionar de forma semi-autônoma com um nível aceitável de automação dentro das capacidades atuais da empresa.	em_andamento	0	\N
40	Inovai.Lab - Administrativo	\N	2025-11-03 16:43:24.387852	2	4										em_andamento	0	\N
38	EduChat - App de educação	\N	2025-10-27 21:22:14.037246	8	4										em_andamento	70	\N
34	RH / Avaliação de Proficiência em IA	\N	2025-10-26 20:17:59.768688	5	8	Criação e implementação de um formulário de avaliação para medir o nível de proficiência em Inteligência Artificial dos colaboradores da OAZ. O objetivo é mapear o conhecimento atual da equipe, identificar gaps de aprendizado e direcionar planos de capacitação personalizados, alinhados à função e setor de cada colaborador.									concluido	0	\N
24	Squad Urban	\N	2025-10-13 17:43:39.451305	7	8	Plataforma web (Replit) de Processamento de Dados que consolida diariamente pedidos do Shopify e pagamentos do Pagar.me em um Excel padronizado compatível com SAP (modelo-base). O sistema executa leitura inteligente (encoding/delimitador), classificação por origem, normalizações (telefone, CPF/CNPJ, CEP, datas, parcelas), parser de endereço (logradouro/número/complemento), enriquecimento financeiro (TID/NSU/Auth/Adquirente/Bandeira/Parcelas) e gera a planilha final com 91 colunas. Fluxo simples: login → upload → processar → download. Tempo de processamento: ~30s (antes ~90min por carga).	Plataforma web (Replit) de Processamento de Dados que consolida diariamente pedidos do Shopify e pagamentos do Pagar.me em um Excel padronizado compatível com SAP (modelo-base). O sistema executa leitura inteligente (encoding/delimitador), classificação por origem, normalizações (telefone, CPF/CNPJ, CEP, datas, parcelas), parser de endereço (logradouro/número/complemento), enriquecimento financeiro (TID/NSU/Auth/Adquirente/Bandeira/Parcelas) e gera a planilha final com 91 colunas. Fluxo simples: login → upload → processar → download. Tempo de processamento: ~30s (antes ~90min por carga).	Processos manuais diários (≈1h30 por carga) com risco de erro e retrabalho: colunas trocadas, perdas de zeros (CEP/CPF), datas inválidas, parcelas com ponto/vírgula, endereços misturados e rejeições pelo SAP. Oportunidade de eliminar trabalho repetitivo, padronizar qualidade dos dados e escalar a operação com governança e rastreabilidade.	- Reduzir o tempo por carga de ~90min para ~30s (redução ≈ 99,4%).\r\n- Alcançar >99% de aceitação no SAP (layout/abas, datas/CEP/parcelas como texto quando necessário).\r\n- Preencher colunas críticas via coalesce por linha (telefone, CPF/CNPJ, e-mail).\r\n- Garantir parser de endereço robusto (logradouro/numero/complemento) e preservação de zeros à esquerda.\r\n- Permitir upload diário de arquivos com nomes variados (múltiplos Shopify/Pagar.me) sem alterar o layout da UI.\r\n- Disponibilizar logs de auditoria e contadores de preenchimento.	Conecta-se aos pilares de eficiência operacional, governança de dados e integração contábil/fiscal com SAP. Reduz OPEX, aumenta previsibilidade dos fechamentos e prepara o terreno para integrações diretas por API (Shopify/Pagar.me/SAP) e automação completa.	- UI web existente (login simples) sem alterações visuais.\r\n- Upload de múltiplos CSVs (Shopify/Pagar.me) + planilha modelo SAP.\r\n- Smart reader (encoding/delimitador), classificação por origem e dicionário de sinônimos PT/EN (>90 cabeçalhos).\r\n- Normalizações: datas (padrões SAP), CEP (8 dígitos), parcelas (inteiro), CPF/CNPJ (11/14 dígitos), telefone (coalesce).\r\n- Parser de endereço (logradouro/numero/complemento) com regras brasileiras.\r\n- Enriquecimento financeiro: TID, NSU, Auth, Adquirente, Bandeira, Parcelas.\r\n- Propagação por Pedido Id (ffill/bfill) entre cabeçalho e itens.\r\n- Geração de Excel final (91 colunas), SAP-friendly (texto onde necessário, preservando zeros).\r\n- Logs em /tmp e documentação operacional.	- Integração direta online com APIs (Shopify/Pagar.me/SAP) e BAPIs do SAP.\r\n- Painéis de BI/analytics, trilhas de auditoria avançadas e RBAC complexo.\r\n- Processamento em tempo real, agendamentos automáticos e orquestração externa.\r\n- Suporte a gateways/marketplaces além de Pagar.me/Shopify.\r\n- Regras fiscais personalizadas além das normalizações previstas.\r\n- Hospedagem fora do Replit e SSO corporativo.	- Arquivos de entrada são exportações oficiais do Shopify/Pagar.me, com colunas padrão.\r\n- Modelo Excel SAP fornecido permanece estável (nomes/abas).\r\n- Ambiente Replit disponível e com acesso à internet.\r\n- Usuários autenticam via login simples; o cliente final não acessa o Replit.\r\n- Volume dentro dos limites de memória/tempo do Replit e do Excel.	- Limites do Replit (CPU/memória/timeout) e do Excel (tamanho/linhas).\r\n- Privacidade de dados: arquivos trafegam por sessão; sem retenção permanente.\r\n- Suporte apenas a CSV/XLSX; outros formatos fora do escopo.\r\n- Fuso horário padronizado para escrita no Excel (datas “timezone-unaware”).\r\n- Layout da UI não será modificado (posicionamento de botões, tema e fluxo).	concluido	100	\N
4	Faturamento das Academias — Bodytech (EVO)	\N	2025-08-26 16:11:20.023519	1	4	Construir uma plataforma que: (1) recebe a planilha mensal enviada pela Bodytech, trata CPF/formatos e gera a planilha padrão de importação no EVO; (2) recebe o arquivo de erros do EVO e retorna uma lista estruturada com todos os dados necessários para emissão das NFS-e; (3) evolui para automação da emissão via API de prefeituras (prioridade: Vila Velha) ou RPA quando não houver API; (4) adiciona um fluxo para enviar notas no EVO (seleção de período/unidade) de forma automatizada.	Construir uma plataforma que: (1) recebe a planilha mensal enviada pela Bodytech, trata CPF/formatos e gera a planilha padrão de importação no EVO; (2) recebe o arquivo de erros do EVO e retorna uma lista estruturada com todos os dados necessários para emissão das NFS-e; (3) evolui para automação da emissão via API de prefeituras (prioridade: Vila Velha) ou RPA quando não houver API; (4) adiciona um fluxo para enviar notas no EVO (seleção de período/unidade) de forma automatizada.	O processo atual é fragmentado e manual: tratamento de planilhas, importação no EVO, captura de erros por unidade e emissão manual em várias prefeituras. Há limitações de LGPD (tráfego de dados por domínio) e falhas de importação quando o cliente não existe na unidade. Oportunidade de padronizar tudo em um único fluxo, reduzir erros e acelerar faturamento/receita.	V1 (imediato):\r\n\r\nUpload da planilha “bruta” (Bodytech) → saída no padrão EVO.\r\n\r\nUpload do log de erros do EVO → saída estruturada com campos para NFS-e.\r\n\r\nV2:\r\n\r\nAutomatizar “Enviar Notas” dentro do EVO (mapear telas, rodar visível para validação e depois headless).\r\n\r\nV3 (duas frentes alternativas/complementares):\r\n\r\nAPI NFS-e onde existir (iniciar por Vila Velha).\r\n\r\nRPA para portais sem API.\r\n\r\nV4 (plano B estrutural):\r\n\r\nAvaliar com TOTVS/Bodytech a criação automática de “cliente visitante” na unidade para permitir faturar inteiramente pelo EVO, reduzindo dependência de prefeituras.\r\n\r\nSLA alvo: processamento diário/semana com mínima intervenção; emissão automatizada após validação.	Faz parte do programa Otimização do Contas a Receber com IA, reduz custo operacional, melhora compliance (LGPD), encurta o ciclo de faturamento e cria base para integrações futuras (ERP/Prefeituras).	Tela de upload da planilha original + tratamento de CPF zeros e formatos.\r\n\r\nGeração da planilha padrão EVO e armazenamento do histórico.\r\n\r\nTela de upload do arquivo de erros do EVO → geração de lista de emissão (campos prontos para prefeitura).\r\n\r\nAutomação do envio de notas no EVO (periodicidade diária sugerida às 17:00).\r\n\r\nIntegração API NFS-e quando disponível; RPA como fallback.\r\n\r\nLogs, auditoria básica e controle por unidade/competência.	Alterações no core do EVO/TOTVS.\r\n\r\nMudanças no processo comercial/contratual da Bodytech.\r\n\r\nSuporte fiscal/contábil às unidades (fora a automação).\r\n\r\nConciliação financeira (tratada em projeto específico).	Yan envia 3 amostras simuladas (por LGPD): (a) arquivo bruto recebido, (b) arquivo no padrão de importação EVO, (c) log de erros do EVO (sem pré-processar no GPT).\r\n\r\nExecução da plataforma dentro do domínio da Sá Cavalcante ou provisionamento de e-mail/acesso compatível (LGPD).\r\n\r\nPrefeituras: haverá pelo menos uma com API (ex.: Vila Velha) para iniciar.\r\n\r\nColaboração de TI Bodytech/TOTVS para avaliar o cadastro de “visitante” na unidade.	LGPD: proíbe envio de dados reais para domínios externos; uso de dados simulados nos testes.\r\n\r\nAusência de homologação para EVO/portais → validação em produção com “botão final” protegido.\r\n\r\nHeterogeneidade dos portais municipais (layouts, requisitos, indisponibilidades).\r\n\r\nDependência de credenciais e disponibilidade do suporte Bodytech/TOTVS.	concluido	100	\N
17	Reembolso Ágil CSC (MVP: App de Comprovantes) - Caixinha franquia	\N	2025-09-03 13:48:40.987692	1	10	Construir um aplicativo simples (mobile-first) para as unidades das franquias registrarem comprovantes por foto, com extração/classificação automática (IA) e um painel administrativo por filial para validação e consolidação de reembolsos. Num segundo passo, evoluir para gestão de caixa/fechamento e integrações com RM/Fluig.									em_andamento	0	\N
43	Game 360 – Avaliação de Cultura e Clima OAZ		2025-11-12 17:11:50.024213	5	8	\N	Sistema interno de Avaliação 360º da empresa, com frontend React/TS e backend Flask/SQLite (migração do backend antigo em Node/TS). Centraliza ciclos de avaliação (ex.: cultura/autoavaliação/avaliações de equipe e ciclo “open”), visões por perfil (admin/gestor/colaborador), acompanhamento de progresso e gestão de performance com rotinas de 1:1, além de timesheets com análise para apoiar o gestor. Inclui também integração de reuniões vinculadas ao timesheet (infra pronta para transcrição e pós-processamento) e um fluxo de migração Postgres → SQLite para consolidação do legado.	Problema: o processo de avaliação/feedback e acompanhamento de execução (tarefas/entregas) fica disperso em ferramentas e conversas, dificultando rastreabilidade, consistência entre ciclos e visão do gestor.\r\nOportunidade: padronizar e automatizar o ciclo de performance com: (1) avaliações 360 por ciclo/objetivo, (2) 1:1 como rotina de acompanhamento, (3) timesheet com análise para identificar gargalos e orientar próximos passos, e (4) integração de reuniões/transcrições para gerar insumos objetivos (com TTL para não “lotar” o banco).	Unificar Avaliação 360º em ciclos (incluindo ciclo OPEN para feedback voluntário e contínuo).\r\nEntregar ao gestor rotinas de 1:1 (criar, acompanhar atualizações, revisar, concluir).\r\nImplementar timesheet com regras/validações e análise heurística automática (alertas e recomendações para 1:1).\r\nIntegrar reuniões ao timesheet (endpoint existente) e evoluir para consulta de transcrição + processamento/IA, persistindo apenas o necessário e com limpeza (TTL).\r\nSustentar a migração do legado mantendo o contrato de rotas/API e consolidando o banco em SQLite (com fluxo de sync/import a partir do Postgres). 	Performance & Cultura: transforma feedback e avaliação em processo contínuo, com ciclos e acompanhamento estruturado (inclui avaliação anônima de cultura e ciclos por tipo).\r\nEficiência de gestão: timesheet com análise e recomendações reduz retrabalho e dá base objetiva para 1:1 e priorização.\r\nEvolução tecnológica/risco: migração para Flask/SQLite reduz dependências do stack anterior e simplifica operação (rotas preservadas).	Portal por perfis (admin/gestor/colaborador) com dashboards e contadores.\r\n\r\nCiclos de avaliação por tipo + ciclo OPEN (feedback contínuo). \r\n\r\nFluxo de 1:1 do gestor com o membro (criar, atualizar, revisar, concluir). \r\n\r\nTimesheet: criação por período, atividades (mín. 3, soma 100%), rascunho/submissão, revisão do gestor (aprova/rejeita) + análise heurística. \r\n\r\nReuniões vinculadas ao timesheet (criação via endpoint) e base de configuração para transcrição/TTL. \r\n\r\nAdministração e importação XLS (preview/execute) com smoke test idempotente para evitar duplicidade. \r\n\r\nMigração/sincronização de dados do Postgres (dump) para SQLite (import/sync), com validações. 	Funcionalidades do backend Node/TS original que não estejam “Flask-ready” (itens marcados como pendentes/planejados no mapa de API). \r\n\r\nArmazenar transcrições “para sempre”: a proposta é armazenamento temporário (TTL) e/ou persistir apenas a análise/resultados necessários. \r\n\r\nDependência de Node na VM de produção (a recomendação é operar com dist versionado e build desabilitado). 	O ambiente DEV usa Flask servindo UI+API e builda/valida o frontend quando necessário. \r\nO SQLite local é o banco alvo e é criado/seedado no primeiro start. \r\nIntegrações externas (ex.: transcrição e IA) dependem de variáveis de ambiente e chaves configuradas. \r\nImportação XLS seguirá fluxo de preview→execute e deve ser idempotente (sem duplicar). 	Manter contrato de rotas existente (/api/auth/*, /api/admin/*, /api/evaluations/*, /api/gestor/*, /api/timesheet/*, etc.). \r\n\r\nSQLite como destino (limitando algumas operações/concorrência vs Postgres). \r\nProdução sem Node: precisa do dist no repo e DISABLE_FRONTEND_BUILD=1 no ambiente. \r\nLimpeza de dados de transcrição em janela curta (ex.: 7 dias) para não crescer banco.	em_andamento	0	\N
15	RH.AI	\N	2025-09-02 16:56:40.660845	5	5	Desenvolver e implantar um MVP em 30 dias que automatize a triagem de currículos com base nos job descriptions enviados pelo RH, entregando uma shortlist de candidatos ranqueados para validação humana. O projeto também prepara terreno para registro de entrevistas e construção da base de dados de seleção. 	Sistema de recrutamento inteligente em Flask que automatiza a avaliacao de curriculos e vagas, usando GPT-5 para extracao de dados e uma pontuacao de 100 pontos com recomendacao de decisao (aprovar, banco de talentos ou rejeitar).	 Processos manuais de triagem sao lentos, pouco consistentes e sujeitos a vies; ha oportunidade de padronizar criterios, ganhar escala e aumentar a transparencia nas decisoes	Automatizar a analise de CVs vs requisitos da vaga; gerar pontuacao detalhada por dimensao; acelerar a triagem; oferecer justificativas e feedback; manter rastreabilidade e consistencia.	Apoia recrutamento baseado em dados, reduz vies, melhora qualidade das contratacoes e aumenta eficiencia operacional com auditoria e transparencia.	 Backend Flask + SQLAlchemy; processamento de PDF/DOC/DOCX; pipeline de IA (GPT-5) para extracao e avaliacao; scoring de 9 dimensoes; workflow de aprovacoes de vagas e selecao de candidatos; templates e envio de emails de rejeicao com feedback; interface web responsiva com dashboards.	 Entrevistas, testes tecnicos presenciais, decisao final de contratacao, onboarding e integracoes complexas de RH nao descritas na solucao atual.	Disponibilidade de chave OpenAI; CVs e vagas com conteudo suficiente; usuarios com perfis definidos (ADMIN, MANAGER, STORE_MANAGER); infraestrutura para armazenar arquivos localmente; SMTP configurado para envio de emails.	 Dependencia de APIs da OpenAI; qualidade do resultado varia com o conteudo do CV; limite de upload (16MB) e formatos suportados; necessidade de configuracao de ambiente (DATABASE_URL, SMTP, SESSION_SECRET); banco padrao SQLite em desenvolvimento.	em_andamento	0	\N
35	Análise de Fluxo de Conversão em Lojas Físicas	\N	2025-10-26 20:21:04.711975	5	5	Desenvolvimento de uma solução baseada em visão computacional para analisar o fluxo de clientes dentro das lojas físicas da OAZ. O projeto visa correlacionar o comportamento dos visitantes com indicadores de conversão, utilizando imagens de câmeras para mapear trajetórias, áreas de maior permanência e pontos de atenção no layout das lojas.	Desenvolvimento de um sistema em Python para análise de vídeo em loja física, realizando detecção e tracking de pessoas e contabilizando visitas/interações em regiões definidas por máscara (araras/expositores). O sistema gera métricas e relatórios sobre fluxo, permanência e pontos de maior interesse na loja.	Problema: ausência de dados sobre comportamento do cliente na loja (entrada, circulação, áreas mais visitadas), levando a decisões baseadas em percepção subjetiva.\r\nOportunidade: usar IA para mensurar o comportamento real no ambiente físico, criando indicadores que suportem otimização de layout, exposição de produtos, operação (equipe/horários) e ações comerciais.	Medir quantidade de pessoas que circulam no ambiente (contagem e fluxo).\r\n\r\nRealizar tracking para entender trajetórias, padrões e permanência.\r\n\r\nDefinir regiões de interesse (araras) via máscaras e medir:\r\n\r\nvisitas por arara\r\n\r\ntempo de permanência por região\r\n\r\nmapas de calor/ocupação (se aplicável)\r\n\r\nGerar relatórios e exportações (ex.: CSV/JSON) para análise do cliente.\r\n\r\nViabilizar um pipeline replicável para novas lojas/câmeras (com ajustes mínimos).	Data-driven retail: transformar operação física em dados para tomada de decisão.\r\n\r\nEficiência operacional: apoiar melhorias de layout, escala de equipe e reposição de produtos.\r\n\r\nMelhoria de performance comercial: identificar pontos quentes/frios e ajustar exposição e campanhas.\r\n\r\nInovação aplicada: uso de IA de forma prática para gerar valor direto ao negócio.	Ingestão de vídeo (arquivo ou stream gravado) e padronização de frames.\r\n\r\nDetecção de pessoas e tracking (ID persistente por pessoa no tempo).\r\n\r\nConfiguração de regiões de interesse (araras/expositores) por máscara/ROI.\r\n\r\nContabilização de métricas:\r\n\r\ncontagem de pessoas\r\n\r\nfluxo por área\r\n\r\nvisitas e permanência por arara\r\n\r\nGeração de outputs:\r\n\r\nrelatórios (tabelas e agregações)\r\n\r\narquivos exportáveis (CSV/JSON)\r\n\r\n(opcional) vídeo anotado com bounding boxes/IDs/ROIs\r\n\r\nDocumentação básica de uso e parâmetros (como ajustar máscaras/ROIs por loja).	Reconhecimento facial, identificação de pessoas ou qualquer dado pessoal.\r\n\r\nIntegração com PDV/ERP/CRM (vendas, estoque, etc.).\r\n\r\nRecomendação automática de layout (consultoria prescritiva completa).\r\n\r\nSuporte a múltiplas câmeras sincronizadas e reconstrução 3D (caso não esteja previsto).\r\n\r\nDashboard web completo em produção (se não for parte do projeto agora).	O vídeo tem qualidade mínima para detecção (iluminação, enquadramento, FPS).\r\n\r\nA câmera está posicionada de forma estável e com visão adequada das áreas relevantes.\r\n\r\nAs araras/regiões podem ser delimitadas previamente por máscara/ROI.\r\n\r\nO cliente fornecerá vídeos representativos (dias/horários relevantes).\r\n\r\nMétricas serão interpretadas como aproximações estatísticas, sujeitas a limitações do ambiente (oclusões, aglomeração, ângulos)	Oclusões (pessoas se escondendo atrás de outras/objetos) podem reduzir precisão.\r\n\r\nMudanças no layout/câmera exigem recalibração das máscaras/ROIs.\r\n\r\nLimitações de hardware para processamento (CPU/GPU) impactam tempo de análise.\r\n\r\nCondições de iluminação e reflexos podem afetar detecção e tracking.\r\n\r\nNecessidade de garantir conformidade com privacidade (evitar identificar indivíduos; manter dados agregados).	em_andamento	0	\N
46	Estrategico		2025-12-07 22:46:07.998374	2	2	\N	Lançamento da iniciativa no sistema para formalizar e comunicar a camada estratégica conduzida pela CEO da inovAI.lab. O foco é deixar claro o direcionamento macro do negócio, prioridades do ciclo atual, decisões-chave, e como isso se traduz em frentes de trabalho, entregas e metas. Esse lançamento serve como âncora de alinhamento interno e referência para acompanhamento de execução.	Problema: Sem um registro claro e centralizado da estratégia e das decisões de CEO, o time pode operar com interpretações diferentes sobre prioridades, escopo e critérios de sucesso. Isso gera retrabalho, desalinhamento entre squads e dificuldade de mensurar impacto real das iniciativas.\r\nOportunidade: Transformar a visão estratégica em um “artefato vivo” dentro do sistema, conectando plano → execução → métricas. Isso aumenta cadência de decisão, reduz ruído operacional e acelera o crescimento com foco.	Registrar oficialmente a direção estratégica do ciclo vigente (visão, foco, apostas e métricas).\r\n\r\nTraduzir o papel da CEO em ações práticas: decisões, priorizações, comunicação e acompanhamento.\r\n\r\nAlinhar todos os responsáveis/ squads sobre o que é prioridade e por quê.\r\n\r\nCriar um ponto único de consulta para atualizar estratégia conforme o negócio evolui.\r\n\r\nFacilitar acompanhamento de resultados (OKRs/ marcos) e ajustes de rota rápidos.	Esta iniciativa está diretamente ligada ao core da inovAI.lab: entregar automações e agentes de IA com impacto real em 30–45 dias, sustentando crescimento recorrente e reputação de excelência.\r\nO lançamento reforça os pilares estratégicos:\r\n\r\nExcelência operacional com velocidade (ritmo de entrega sem perder qualidade).\r\n\r\nEscalabilidade do modelo inovAI.lab (processos replicáveis e mensuráveis).\r\n\r\nFoco em ROI e dor real do cliente (prioridade para o que gera impacto).\r\n\r\nCultura orientada a dados e feedback (decidir, medir, ajustar).	Dentro deste lançamento, estão incluídos:\r\n\r\nDefinição/registro da estratégia do ciclo (prioridades, objetivos e indicadores).\r\n\r\nComunicação interna do direcionamento para squads e responsáveis.\r\n\r\nRitual de acompanhamento: checkpoints, revisão de prioridades e decisões.\r\n\r\nConexão das frentes estratégicas com tarefas/roadmaps do sistema.\r\n\r\nAtualizações estratégicas conforme aprendizados do mercado e clientes.	Não faz parte deste lançamento:\r\n\r\nExecução detalhada de cada tarefa operacional dos squads.\r\n\r\nProdução técnica das automações/agentes (código, integrações, etc.).\r\n\r\nRotinas administrativas/financeiras que não estejam ligadas ao direcionamento estratégico.\r\n\r\nMarketing tático do dia a dia (posts, peças, setup de campanhas), salvo quando for prioridade estratégica explícita.	A estratégia do ciclo atual já tem um direcionamento inicial definido (mesmo que seja versão 0.1).\r\n\r\nOs squads e responsáveis usarão o sistema como fonte principal de prioridades.\r\n\r\nExiste abertura para ajustes de rota com base em métricas e feedback de clientes.\r\n\r\nAs decisões da CEO serão registradas e comunicadas com cadência.\r\n\r\nO sucesso será avaliado por impacto no negócio, não só por volume de entregas.	Tempo limitado da CEO para acompanhamento profundo de todas as frentes → necessidade de priorização forte.\r\n\r\nDependência de informações de mercado e clientes para validar/ajustar apostas.\r\n\r\nCapacidade técnica e operacional dos squads determina velocidade real de execução.\r\n\r\nMudanças rápidas no cenário de IA podem exigir revisão estratégica fora do ciclo planejado.\r\n\r\nNecessidade de manter consistência entre visão de longo prazo e urgências de curto prazo.	em_andamento	0	\N
45	Plataforma de Avaliação 1:1 com Transcrição Automática (Gestor x Colaborador)		2025-11-27 17:47:14.496494	5	8	\N									em_andamento	0	\N
51	RPA de Cadastro Automático de Contratos (VS Comercial → VS Contratos)		2025-12-11 17:59:54.864396	1	6	\N	A Sá Cavalcante possui um processo manual e suscetível a erros para cadastrar contratos assinados no VS Contratos. Hoje, a TESc (Alice) copia dados do VS Comercial e insere manualmente no VS Contratos, o que gera inconsistências e retrabalho. O projeto propõe a criação de um RPA que execute automaticamente esse fluxo, garantindo precisão, agilidade e padronização.	Processo 100% manual, com alto risco de erros de digitação e datas.\r\n\r\nFalta de padronização na classificação dos contratos.\r\n\r\nRetrabalho e necessidade de conferências manuais via Excel.\r\n\r\nImpacto negativo em análises, dashboards e estudos de portfólio.\r\n\r\nOportunidade clara de automatizar e padronizar um fluxo crítico para o negócio.	Automatizar o cadastro de contratos assinados no VS Contratos.\r\n\r\nEliminar erros humanos em datas, valores e informações críticas.\r\n\r\nPadronizar o preenchimento dos campos de contrato.\r\n\r\nReduzir o tempo entre assinatura e cadastro definitivo.\r\n\r\nCriar base estruturada para auditorias e análises futuras.	Aumentar eficiência operacional através de automação inteligente.\r\n\r\nReduzir retrabalho e esforços manuais repetitivos.\r\n\r\nMelhorar qualidade da base de contratos, fundamental para decisões estratégicas.\r\n\r\nPreparar terreno para integrações avançadas e um futuro "Auditor de Contratos" automatizado.	Criar um RPA capaz de:\r\n\r\nIdentificar contratos aprovados e assinados no VS Comercial.\r\n\r\nExtrair informações relevantes (lojista, loja, datas, valores, índices, observações).\r\n\r\nAcessar o VS Contratos e cadastrar o contrato automaticamente.\r\n\r\nPreencher campos obrigatórios com padronização e validações.\r\n\r\nRegistrar logs operacionais e exceções.\r\n\r\nMarcar contratos processados para evitar duplicidade.\r\n\r\nCriar fila de pendências para contratos com inconsistências.	Alterações no VS Comercial ou VS Contratos.\r\n\r\nCriação ou modificação de regras de comitê ou aprovação.\r\n\r\nRevisão jurídica dos contratos.\r\n\r\nAutomação de processos anteriores à assinatura (CRM, propostas etc.).\r\n\r\nIntegrações profundas com banco de dados sem documentação (futuro possível, mas fora desta fase).	A equipe terá acesso às telas e ambientes do VS Comercial e VS Contratos.\r\n\r\nA Alice demonstrará o processo completo para mapeamento.\r\n\r\nCampos necessários estarão disponíveis nas interfaces visíveis ou exportáveis.\r\n\r\nO cliente concorda com a execução inicial em piloto controlado.	Sistemas legados instáveis podem influenciar o comportamento do RPA.\r\n\r\nMudanças de layout ou versão do VS podem exigir manutenção.\r\n\r\nAlguns campos do VS Contratos não possuem padronização rígida, exigindo definição com o Hudson.\r\n\r\nO RPA depende das permissões de acesso fornecidas pela TI do cliente.	em_andamento	0	\N
52	Sistema de Gerenciamento de Transporte		2025-12-11 18:04:35.927696	5	5	\N	Desenvolver um TMS focado em conciliação de fretes, utilizando automações com Playwright para coletar dados de transportadoras e ERP, padronizar essas informações e gerar relatórios consolidados (JSON/CSV). O sistema servirá como “camada de orquestração” entre portais de transportadoras, APIs e arquivos do ERP, reduzindo trabalho manual e aumentando a confiabilidade dos dados logísticos.	Hoje a conferência de fretes e faturas é feita de forma manual, acessando múltiplos portais, baixando arquivos e conferindo valores pedido a pedido. Isso gera retrabalho, risco de erro, baixa rastreabilidade e pouca visibilidade gerencial. Há oportunidade de automatizar a coleta, padronizar os dados e permitir uma conciliação mais rápida, auditável e escalável, abrindo espaço para renegociações de frete e redução de custos.	Automatizar a extração de dados de transportadoras e ERP em um fluxo único de ETL.\r\n\r\nPadronizar as informações em um modelo de dados comum, permitindo conciliação automática entre ERP x transportadoras.\r\n\r\nReduzir o tempo de conferência de fretes e faturas e aumentar a acurácia das informações para tomada de decisão.	O projeto está alinhado à estratégia de eficiência operacional e transformação digital, ao reduzir atividades manuais de baixo valor e aumentar a automação de processos logísticos. Contribui para melhoria de margem (redução de custos de frete não identificados), aumento de controle sobre o gasto logístico e criação de base de dados estruturada para análises futuras e possíveis integrações com outros sistemas corporativos.	Construção de um cliente Playwright reutilizável para login e navegação em portais de transportadoras.\r\n\r\nDesenvolvimento de adapters para principais transportadoras (ex.: Jamef, Favorita, Loggi, Correios) e para ERP via CSV/arquivos.\r\n\r\nImplementação do motor de conciliação ERP x transportadoras, com regras de matching por pedido, CNPJ, valor e data.\r\n\r\nGeração de artefatos estruturados (JSON/CSV) com dados brutos e relatórios de conciliação.\r\n\r\nCriação de CLI/rotinas para execução automatizada (scripts agendáveis).	Mudanças contratuais ou negociações de frete com transportadoras.\r\n\r\nConstrução de dashboard analítico completo ou front-end web para o usuário final (além dos arquivos gerados).\r\n\r\nIntegrações em tempo real com sistemas legados fora dos formatos previstos (APIs proprietárias não mapeadas neste projeto).\r\n\r\nGestão operacional do time de logística ou definição de políticas de frete.	Portais e/ou APIs das transportadoras permanecem acessíveis e estáveis para automação via Playwright/HTTP.\r\n\r\nO ERP consegue exportar os dados necessários em formato estruturado (ex.: CSV) dentro da periodicidade definida.\r\n\r\nHaverá ambiente com Python/Playwright disponível para execução dos robôs e armazenamento dos artefatos gerados.\r\n\r\nUsuários-chave de logística/financeiro estarão disponíveis para validação das regras de conciliação e testes de homologação.	Dependência de credenciais de acesso (usuário, senha, tokens) válidas para ERP e transportadoras.\r\n\r\nMudanças de layout, fluxo ou políticas de segurança nos portais das transportadoras podem impactar o funcionamento das automações.\r\n\r\nExecução limitada a ambientes com Playwright, Python e acesso à internet/redes internas devidamente liberado pelo time de TI.\r\n\r\nLimites de uso de APIs e regras de rate limit impostos por cada transportadora devem ser respeitados.\r\n\r\nProcessamento previsto em janelas específicas (batch), não contemplando conciliação em tempo real.\r\n\r\nArmazenamento e tratamento de dados devem seguir as políticas internas de segurança da informação e LGPD, restringindo o acesso apenas a perfis autorizados.	pausado	0	\N
47	OAZ — Sistema de Gestão de OKRs e Focos Semanais (v1 produção)		2025-12-08 15:59:05.158311	5	10	\N	Aplicação web para gestão de OKRs do cliente OAZ, permitindo cadastro de ciclos, objetivos e KRs hierárquicos, acompanhamento de progresso, dashboards por papel (admin/manager/colaborador) e registro de Focos Semanais vinculados a KRs, com interface moderna, responsiva e orientada a autonomia dos squads.	OAZ precisa de uma plataforma central para dar visibilidade, alinhamento e rastreabilidade a metas estratégicas e táticas, reduzindo dispersão em planilhas e rituais manuais. A solução cria um fluxo único para ciclos OKR, conectando objetivos a KRs e a focos semanais operacionais, com permissões por squad e papéis, garantindo privacidade entre times e clareza de ownership.	Disponibilizar um sistema OKR completo (CRUD de ciclos, objetivos e KRs) pronto para operação do cliente. \r\n\r\nreplit (1)\r\n\r\nImplantar acompanhamento semanal via Focos Semanais com tarefas (to-do list) e cálculo automático de progresso/status. \r\n\r\nSISTEMA_TODO_LIST\r\n\r\nGarantir visibilidade segmentada por squad e papel (admin/manager/colaborador), evitando vazamento de OKRs entre times. \r\n\r\nVISIBILIDADE_POR_SQUAD\r\n\r\nEntregar UX premium (frontend redesigned, responsivo, com feedback visual e dashboards claros) para alta adoção interna. \r\n\r\nFRONTEND_UX_DESIGN\r\n\r\nPreparar base técnica estável para evolução futura (multi-owners, multi-teams, activities em KRs, reports avançados).	O projeto suporta a estratégia do OAZ de fortalecer execução por metas, aumentando foco, accountability e cadência semanal. Conecta planejamento (OKRs) à operação (focos e tarefas), melhora a comunicação entre liderança e squads, e cria histórico de performance por ciclo para decisões futuras.	Escopo do Projeto\r\n\r\nImplementação do sistema OKR em Flask com banco relacional, autenticação e RBAC (Admin/Manager/Colaborador). \r\n\r\nreplit (1)\r\n\r\nGestão de ciclos OKR, objetivos hierárquicos e KRs com múltiplos tipos métricos. \r\n\r\nreplit (1)\r\n\r\nDashboards por papel com cards de status, progresso e visualização de objetivos/KRs. \r\n\r\nFRONTEND_UX_DESIGN\r\n\r\nFocos Semanais vinculados a KRs, com UX melhorado no dropdown (squad, objetivo, responsável) e cards completos. \r\n\r\nMELHORIAS_FOCOS_SEMANAIS\r\n\r\nTo-Do List dentro de cada foco semanal, com progresso automático e rotas AJAX para adicionar/toggle/deletar/complete tarefas. \r\n\r\nSISTEMA_TODO_LIST\r\n\r\nRegras de visibilidade por squad/ownership aplicadas nas listagens e formulários. \r\n\r\nVISIBILIDADE_POR_SQUAD\r\n\r\nFrontend redesenhado com design system (gradientes, badges, animações, responsividade). \r\n\r\nFRONTEND_UX_DESIGN\r\n\r\nPreparação para deploy em ambiente produtivo (Gunicorn, PostgreSQL). \r\n\r\nreplit (1)	Integrações com sistemas legados/ERP/CRM do cliente (não descritas nos docs).\r\n\r\nSSO corporativo ou autenticação externa além do Flask-Login padrão.\r\n\r\nApp mobile nativo (PWA/dark mode/real-time ficam como futuras melhorias sugeridas). \r\n\r\nFRONTEND_UX_DESIGN\r\n\r\nMigração histórica de OKRs antigos do OAZ (não documentada).	OAZ fornecerá usuários, estrutura de squads/teams e ciclos iniciais para seed/configuração.\r\n\r\nAmbiente produtivo terá PostgreSQL configurado e variáveis de ambiente corretas (SECRET_KEY, DATABASE_URL). \r\n\r\nreplit (1)\r\n\r\nPapéis e regras de visibilidade atuais são suficientes para o primeiro ciclo de uso. \r\n\r\nVISIBILIDADE_POR_SQUAD\r\n\r\nAdoção guiada via onboarding simples (login, criação de ciclo, objetivos, KRs e focos).	Stack fixa em Flask/Jinja/Bootstrap conforme base atual (mudanças grandes de arquitetura não previstas). \r\n\r\nreplit (1)\r\n\r\nRegras de segurança: usuários só manipulam focos/tarefas próprios, salvo admins. \r\n\r\nSISTEMA_TODO_LIST\r\n\r\nLimites de sistema definidos em config (ex.: itens por página, máximo de focos semanais por usuário). \r\n\r\nreplit (1)\r\n\r\nDependência de ciclo ativo para listagem de KRs/focos. \r\n\r\nVISIBILIDADE_POR_SQUAD	concluido	0	\N
49	Aeropool manuais 		2025-12-08 22:19:23.698783	3	7	\N	Projeto criado para estruturar os manuais e catálogos de peças do Humberto. O objetivo é proporcionar maior visibilidade, organização e acessibilidade às informações técnicas de cada peça.	Atualmente, os dados das peças estão dispersos, dificultando consultas rápidas, podendo gerar erros operacionais e atrasos no atendimento.\r\nOportunidade: criar uma plataforma/manual estruturado que melhore a eficiência e reduza retrabalho.\r\n	Criar um manual digital organizado contendo todas as peças.\r\n\r\nPadronizar nomes, códigos, descrições e imagens das peças.\r\n\r\nFacilitar o acesso da equipe de mecanicos, operação e de compras de peças.\r\n\r\nReduzir tempo de busca de informações e minimizar erros internos.\r\n	O projeto contribui para a modernização dos processos internos, melhoria da experiência do cliente e aumento da produtividade da equipe. Também reforça a estratégia da empresa de centralizar informação técnica e profissionalizar a gestão do conhecimento.	Levantamento de todas os manuais existentes.\r\n\r\nPadronização de nomenclaturas, códigos e categorias.\r\n\r\nRegistro fotográfico das peças (quando necessário).\r\n\r\nCriação e organização do manual digital.\r\n\r\nDefinição de estrutura para futuras atualizações.\r\n\r\nEntrega de versão navegável e amigável para uso interno.\r\n	Alteração física das peças.\r\n\r\nDesenvolvimento de sistemas complexos fora do manual digital.\r\n\r\nIntegração com ERP ou sistemas externos (a menos que solicitado em projeto posterior).\r\n	Todas as peças e informações necessárias serão fornecidas pelo Humberto.\r\n\r\nA equipe terá acesso às áreas e materiais para registro e documentação.\r\n\r\nO cliente aprovará a estrutura de organização proposta.\r\n	Dependência da disponibilidade do Humberto para envio das peças e informações.\r\n\r\nPossíveis limitações de tempo para coleta de material fotográfico.\r\n\r\nEscopo limitado ao conteúdo fornecido pelo cliente.\r\n	em_andamento	0	\N
53	OAZ Sistema de Gestão de OKR's		2025-12-26 21:51:32.635384	5	10	\N	Desenvolvimento de um sistema próprio de gerenciamento de OKRs para o OAZ, centralizando a definição de objetivos estratégicos, Key Results (KRs) e focos semanais, com gestão por times e squads, promovendo alinhamento, clareza de prioridades e acompanhamento contínuo de resultados.	Atualmente, a gestão de OKRs acontece de forma fragmentada, com baixa visibilidade, dificuldade de acompanhamento contínuo e pouco vínculo entre estratégia, execução semanal e times/squads.\r\nA oportunidade está em criar uma plataforma integrada que conecte estratégia → execução → acompanhamento, aumentando foco, alinhamento e performance organizacional.	Criar um sistema centralizado de gerenciamento de OKRs do OAZ\r\n\r\nPermitir que administradores gerenciem usuários, times e squads\r\n\r\nEstruturar objetivos estratégicos e seus respectivos KRs\r\n\r\nConectar KRs a focos semanais, facilitando a execução no dia a dia\r\n\r\nAumentar transparência, alinhamento estratégico e senso de prioridade\r\n\r\nFacilitar o acompanhamento da evolução dos KRs ao longo do tempo	O projeto está diretamente alinhado com a estratégia do OAZ de:\r\n\r\nAumentar maturidade em gestão por objetivos\r\n\r\nGarantir execução consistente da estratégia\r\n\r\nPromover autonomia com clareza de prioridades\r\n\r\nCriar uma cultura orientada a resultados e foco contínuo	Escopo do Projeto\r\n\r\nSistema com autenticação e login de administrador\r\n\r\nCadastro e gestão de usuários\r\n\r\nVinculação de usuários a times e squads\r\n\r\nCadastro de Objetivos estratégicos\r\n\r\nCriação e vinculação de Key Results (KRs) aos Objetivos\r\n\r\nCriação de focos semanais vinculados a KRs específicos\r\n\r\nEstrutura inicial para acompanhamento e organização dos OKRs	Avaliações de performance individuais automatizadas\r\n\r\nIntegrações com ferramentas externas (ex: Slack, Jira, Asana, etc.)\r\n\r\nDashboards avançados de analytics (BI) nesta fase\r\n\r\nAutomatizações complexas ou agentes de IA\r\n\r\nGestão financeira ou de metas não relacionadas a OKRs	Os usuários utilizarão o sistema como ferramenta principal de acompanhamento de OKRs\r\n\r\nA definição de Objetivos e KRs seguirá a metodologia de OKRs adotada pelo OAZ\r\n\r\nO admin será responsável pela governança inicial do sistema\r\n\r\nO foco semanal será o principal elo entre estratégia e execução	Desenvolvimento inicial focado em MVP funcional\r\n\r\nRecursos técnicos e de tempo limitados à fase atual\r\n\r\nNecessidade de simplicidade e usabilidade na primeira versão\r\n\r\nEvoluções futuras dependerão da validação do uso do sistema pelos times	concluido	0	\N
44	App in Sight	App in Sight é uma plataforma completa de monitoramento e gestão de robôs RPA, criada para dar visão total, controle e inteligência sobre operações de automação.\r\nCom ele, empresas acompanham seus robôs em tempo real, visualizam logs ao vivo, recebem screenshots instantâneas, enviam comandos e medem automaticamente o ROI de cada automação.\r\n\r\nSimples e poderoso, o App in Sight funciona como um centro de comando corporativo, permitindo que equipes de TI, operações e automação monitorem todos os robôs, processos e clientes em um só lugar, com segurança avançada e arquitetura multi-tenant.\r\n\r\nIdeal para empresas que precisam escalar automações com eficiência, comprovar valor gerado e garantir estabilidade operacional. O App in Sight transforma dados em insights, reduz custos e impulsiona o desempenho das operações digitais.	2025-11-25 16:09:30.873147	8	10	\N	O App in Sight é uma plataforma completa para monitoramento, gestão e análise de robôs RPA, permitindo acompanhar status em tempo real, visualizar logs, mensurar ROI e administrar múltiplos clientes em um ambiente seguro e escalável.	Empresas que utilizam automação RPA enfrentam falta de visibilidade, dificuldade em diagnosticar problemas, ausência de métricas claras de desempenho e desafios para comprovar o retorno financeiro das automações. O App in Sight transforma esse cenário, oferecendo controle centralizado, insights e governança completa.	Prover um centro de comando para monitoramento em tempo real dos robôs.\r\n\r\nFacilitar a gestão operacional e tomada de decisão baseada em dados.\r\n\r\nAutomatizar a mensuração de ROI e reduzir custos de manutenção.\r\n\r\nAumentar a confiabilidade e eficiência das operações de automação.\r\n\r\nGarantir segurança, escalabilidade e multi-tenancy corporativa.	O App in Sight apoia a estratégia das empresas ao:\r\n\r\nAumentar eficiência operacional.\r\n\r\nReduzir custos de mão de obra e retrabalho.\r\n\r\nAmpliar governança e compliance em automação.\r\n\r\nFortalecer iniciativas de transformação digital.\r\n\r\nFornecer insights para decisões estratégicas sobre automações.	Inclui:\r\n\r\nMonitoramento em tempo real via WebSocket.\r\n\r\nDashboard operacional e indicadores.\r\n\r\nGestão de robôs, clientes e usuários.\r\n\r\nSistema centralizado de logs e screenshots.\r\n\r\nMódulo de ROI com cálculo automático.\r\n\r\nAutenticação e autorização multi-nível.\r\n\r\nInterface web completa e responsiva.\r\n\r\nArmazenamento e organização de dados.\r\n\r\nFuncionalidades de comunicação robô-servidor.	Desenvolvimento de robôs RPA.\r\n\r\nExecução de automações dentro da plataforma.\r\n\r\nFerramentas de edição ou criação de fluxos RPA.\r\n\r\nSuporte a integrações externas não previstas no roadmap.\r\n\r\nManutenção de infraestrutura do cliente final (hardware/robôs).\r\n\r\nCustomizações profundas sem planejamento específico.	Os robôs conseguem enviar logs, sinais de status e screenshots.\r\n\r\nAs empresas possuem estrutura mínima de rede para comunicação.\r\n\r\nUsuários têm acesso autenticado e privilégios definidos.\r\n\r\nOs dados de ROI podem ser fornecidos ou extraídos via logs.\r\n\r\nA plataforma será usada em ambiente web com conexão estável.	Deve operar com segurança avançada e isolamento multi-tenant.\r\n\r\nDeve suportar alto volume de eventos em tempo real.\r\n\r\nArmazenamento de logs pode ter retenção limitada.\r\n\r\nNecessidade de manter compatibilidade com protocolo dos robôs.\r\n\r\nInterface obrigatoriamente em Português (PT-BR) na versão inicial.	concluido	0	\N
26	BankRecon Humberto – Sistema de Reconciliação Bancária Automatizada com IA	\N	2025-10-14 16:50:01.881951	3	7	O projeto BankRecon do Humberto, tem como objetivo desenvolver uma solução web para reconciliação bancária automatizada, utilizando inteligência artificial para processar, comparar e validar informações financeiras provenientes de diferentes fontes (extratos bancários em PDF, bases contábeis e planilhas internas).\r\nA aplicação realiza a leitura e análise de documentos financeiros, identifica divergências e gera relatórios de reconciliação de forma rápida, segura e auditável.	O projeto BankRecon do Humberto, tem como objetivo desenvolver uma solução web para reconciliação bancária automatizada, utilizando inteligência artificial para processar, comparar e validar informações financeiras provenientes de diferentes fontes (extratos bancários em PDF, bases contábeis e planilhas internas).\r\nA aplicação realiza a leitura e análise de documentos financeiros, identifica divergências e gera relatórios de reconciliação de forma rápida, segura e auditável.	Atualmente, o processo de reconciliação bancária é manual, sujeito a erros humanos e demanda elevado tempo de conferência.\r\nAs principais dificuldades incluem:\r\n\r\nLeitura e interpretação de diferentes layouts de extratos bancários (PDFs, CSVs, planilhas);\r\nCruzamento manual de informações contábeis;\r\nFalta de rastreabilidade e auditoria de alterações;\r\nDificuldade em identificar discrepâncias de forma automatizada.\r\nO projeto visa eliminar essas ineficiências e aumentar a confiabilidade do processo.	Automatizar o processo de reconciliação bancária entre extratos e registros internos;\r\nReduzir o tempo operacional necessário para fechamento financeiro;\r\nImplementar inteligência artificial para interpretar PDFs e identificar inconsistências;\r\nGarantir auditabilidade, rastreabilidade e geração de relatórios;\r\nProver interface web intuitiva para interação dos usuários financeiros e auditores.		Desenvolvimento de backend em Python (Flask) com integração ao banco de dados;\r\nImplementação de módulos de leitura e parsing de PDFs (pdf_parser_advanced.py, enhanced_parser_v2.py);\r\n\r\nIntegração com API da OpenAI para interpretação de texto financeiro;\r\nCriação de interface web (templates e static) para upload e análise de reconciliações;\r\nGeração de relatórios automatizados e dashboards de acompanhamento;\r\nConfiguração de ambiente em Replit ou servidor interno.	Integração direta com sistemas bancários em produção;\r\nFunções contábeis além da reconciliação (ex: fechamento, conciliação fiscal);\r\nProcessos de pagamento ou movimentação financeira real.		O sistema não realizará movimentações financeiras reais — apenas leitura e reconciliação de dados.\r\nLimitação de volume de processamento de arquivos de acordo com o plano de uso da API.\r\nDependência de conexão estável com a API da OpenAI para processamento de PDFs.\r\nManutenção inicial restrita à equipe de desenvolvimento interno (sem suporte externo).	concluido	0	\N
1	Automação de Evolução Fiscal (SÁ-SQ)	\N	2025-08-26 14:38:50.978595	1	6	Construção de uma aplicação que integra TOTVS RM e Fluig para automatizar a evolução fiscal: consulta e saneamento de lançamentos, atualização de status (inclusive cancelamentos) e notificações por e-mail para o solicitante, eliminando planilhas manuais e aumentando a visibilidade do processo. Hoje o Fluig envia para o RM, mas o RM não devolve status ao Fluig, o que gera retrabalho; o sistema proposto fecha essa “ponta” e centraliza as informações necessárias para conferência fiscal.	Construção de uma aplicação que integra TOTVS RM e Fluig para automatizar a evolução fiscal: consulta e saneamento de lançamentos, atualização de status (inclusive cancelamentos) e notificações por e-mail para o solicitante, eliminando planilhas manuais e aumentando a visibilidade do processo. Hoje o Fluig envia para o RM, mas o RM não devolve status ao Fluig, o que gera retrabalho; o sistema proposto fecha essa “ponta” e centraliza as informações necessárias para conferência fiscal.	Quebra de comunicação RM → Fluig: ausência de retorno de status e sem e-mails automáticos obriga equipes a manter planilhas compartilhadas. Oportunidade: automatizar o fluxo, notificar o usuário e registrar trilha de auditoria. \r\n \r\n\r\nDados incompletos para análise fiscal: falta base de cálculo, CST e CFOP de entrada na visão atual; anexos (PDF via chave de acesso) não estão disponíveis. Oportunidade: enriquecer o dataset para validar benefícios fiscais e conciliações. \r\n \r\n\r\nQualidade/escopo da carga: surgiram lotes antigos (ex.: 2003) e duplicidades do mesmo conjunto de notas em diferentes filiais, indicando necessidade de filtros (p.ex., últimos 12 meses) e ajustes de query.	Fechar o ciclo RM ↔ Fluig: ao evoluir ou cancelar uma solicitação, refletir o status no Fluig e disparar e-mail ao solicitante com justificativa. \r\n \r\n\r\nCompletar o modelo de dados fiscal: incluir base de cálculo, CST, CFOP de entrada e opção de anexar o PDF via chave de acesso da NF. \r\n \r\n\r\nSaneamento e performance de consulta: corrigir duplicidades entre filiais, restringir a janela temporal (últimos 12 meses) e otimizar a extração (query “demora muito”). \r\n \r\n\r\nMelhorar usabilidade e legibilidade: layout já evoluiu (v2), próximo passo é exibir nomes (cliente/fornecedor) em vez de códigos e destacar campos críticos. \r\n \r\n\r\nEntregar dentro do marco definido com Oliver (25/09/2025) com cronograma validado.	Eficiência operacional: reduz planilhas e trocas manuais, cria trilha auditável e encurta tempo de resposta ao solicitante. \r\n\r\nConformidade fiscal: adiciona campos essenciais (base de cálculo, CST, CFOP), permitindo conferência e aderência a benefícios fiscais. \r\n\r\nCompromisso com prazos do negócio: marco de 25/09/2025 gera foco e governança do backlog.	Consulta de lançamentos com filtros de período (últimos 12 meses), coligada/filial e saneamento de duplicidades. \r\n \r\n\r\nEnriquecimento de dados: base de cálculo, CST, CFOP de entrada, natureza orçamentária. \r\n \r\n\r\nResolução de identificadores: exibir nome de fornecedor/cliente (hoje aparecem códigos como g022).	Parametrizações estruturais no RM ou Fluig (além das integrações/consultas do projeto).\r\n\r\nRegras contábeis/tributárias novas (o sistema mostra e aciona processos; quem define regra é o ERP/área fiscal).\r\n\r\nAplicativos mobile dedicados.	Ambiente de homologação do RM ativo (já usado) e base de teste do Fluig “ligada” para validar cancelamentos/status sem risco à produção. \r\n\r\nSuporte do Maxwell/Time RM para acesso e performance de extrações. \r\n\r\nDisponibilidade dos usuários-chave (Ananda, Rosimere, Lucas, Lizandra) para ciclos rápidos de validação.	Desempenho da extração no RM (demora para “tirar o movimento”), exigindo otimização e filtros. \r\n\r\nQualidade e recência da base: presença de dados antigos (ex.: 2003) e duplicidades entre filiais até ajustes de query. \r\n \r\n\r\nDependência de ativação do ambiente de testes do Fluig para validar ponta a ponta.	pausado	0	\N
7	TributAI — Observatório & Planejador da Reforma Tributária.	\N	2025-08-26 17:11:11.003582	1	2	Construção de uma plataforma interna (login/senha) com chat baseado em RAG sobre um repositório curado de normas, leis, materiais oficiais e transcrições, para acompanhar diariamente a Reforma Tributária e planejar impactos por segmento (2026–2033). Na Fase 1, o chat responde apenas com base no acervo interno; fases seguintes adicionam captura diária do Portal da Reforma Tributária e outras fontes confiáveis, com curadoria pela Patrícia.	Construção de uma plataforma interna (login/senha) com chat baseado em RAG sobre um repositório curado de normas, leis, materiais oficiais e transcrições, para acompanhar diariamente a Reforma Tributária e planejar impactos por segmento (2026–2033). Na Fase 1, o chat responde apenas com base no acervo interno; fases seguintes adicionam captura diária do Portal da Reforma Tributária e outras fontes confiáveis, com curadoria pela Patrícia.	Problema: Pesquisa manual, difusa e não versionada; ausência de base organizada e reutilizável; necessidade de acompanhar normas e discutir impactos por segmento. \r\n\r\nOportunidade: Consolidar fontes oficiais (Portal da Reforma, leis, pareceres, perfis técnicos) e transformar em conhecimento acionável via chat, com histórico, curadoria e planejamento plurianual 2026–2033.	MVP funcional do chat RAG (Fase 1): usuário loga, consulta e obtém respostas com citações dos documentos internos. \r\n\r\nRepositório organizado: ingestão de leis/atos + upload de PDFs/links + transcrição de vídeos para texto. \r\n\r\nCuradoria diária (Fase 2): captura do Portal da Reforma e lista de itens “interessantes” para a Patrícia aprovar e incorporar. \r\n\r\nPlanejamento por segmento (2026–2033): estrutura para projetar impactos (ex.: locação) ano a ano.	Eleva eficiência e qualidade da análise tributária, reduz retrabalho e dependência de pesquisas ad-hoc.\r\n\r\nAcompanha a visão de entregar automações úteis em ciclos curtos (30–45 dias) e evoluir por fases incrementais (MVP → captura web → planejamento).	Fase 1 – MVP (interno, sem internet): \r\n\r\nRepositório inicial com leis e documentos fornecidos pela Patrícia.\r\n\r\nChat RAG (GPT via API) restrito ao acervo interno, com histórico de consultas.\r\n\r\nUpload de arquivos (preferência por texto; aceita PDF/PPT, quando possível convertido).\r\n\r\nTranscrição de vídeos/lives para texto e ingestão no acervo.\r\n\r\nFase 2 – Observatório (captura e curadoria): \r\n\r\nConector para Portal da Reforma Tributária (e outras fontes confiáveis definidas).\r\n\r\nFila diária de notícias/normas; a Patrícia marca “relevante” e o item entra no acervo.\r\n\r\nCatálogo de fontes confiáveis (ex.: perfis técnicos como o citado na conversa) para priorizar a ingestão. \r\n\r\nEstruturas de planejamento anual por segmento (2026–2033), com campos de impacto e ações	Robôs que navegam livremente pela internet sem lista de fontes confiáveis. \r\n\r\nGeração automática de obrigações fiscais/apuração oficial.\r\n\r\nIntegrações com ERP/Outlook/ECM.\r\n\r\nProjeto Societário (ficará para fase futura)	Patrícia fornecerá leis/links iniciais e a URL do Portal da Reforma (e perfis confiáveis) para priorização. \r\n\r\nMateriais devem estar em texto (ou serão transcritos) para excelente desempenho no RAG. \r\n\r\nUso de GPT via API para geração de respostas; embeddings para recuperação.	Fase 1 sem internet: respostas apenas do acervo interno, por decisão de qualidade/controle. \r\n\r\nDependência de curadoria para entrada de itens externos (fase 2). \r\n\r\nConfiabilidade jurídica: a ferramenta não substitui parecer humano nem fontes oficiais.	pausado	0	\N
20	OÁZ AutoPLM — Cadastro Inteligente a partir da Ficha Técnica	\N	2025-09-09 22:30:41.079399	5	5	Construir uma aplicação (“AutoPLM”) que lê a ficha técnica criada pela estilista (desenho + dados), extrai automaticamente os campos necessários e realiza o pré-cadastro no PLM (“Fluxograma”). Em seguida, evoluir para atualizações de ficha ao longo do fluxo (provas, lacre) e para gatilhos de notificação a compras.	Plataforma AutoPLM para cadastro inteligente de fichas técnicas de moda, com upload de PDF/imagens, extração automática de dados via IA, classificação de peças, geração de desenho técnico e gestão de coleções, fornecedores e status.	O cadastro de fichas técnicas é manual, lento e sujeito a inconsistências. Há oportunidade de padronizar informações, reduzir retrabalho e acelerar o ciclo de desenvolvimento com automação e centralização dos dados.	Automatizar a extração de dados de PDFs e imagens.\r\nClassificar automaticamente peças (grupo/subgrupo) com campos editáveis.\r\nGerar desenhos técnicos a partir de imagens.\r\nPadronizar fichas e reduzir tempo de cadastro.\r\nDar visibilidade ao processo com status e acompanhamento em tempo real.\r\nCentralizar gestão de coleções, fornecedores e usuários.	Digitalização e automação do processo de desenvolvimento de produto, aumento de produtividade e qualidade técnica, escalabilidade do time e criação de base de dados confiável para decisões e integração futura.\r\n\r\n	Upload de PDFs e imagens (processamento assíncrono).\r\nExtração de texto/imagens e análise por IA.\r\nGeração de desenhos técnicos (image-to-image).\r\nCadastro e edição de fichas técnicas.\r\nGestão de coleções e fornecedores.\r\nControle de status do produto.\r\nDashboards, busca e filtros.\r\nLogs e permissões por perfil.	Implementação e manutenção do sistema web em Flask com SQLAlchemy, integrações OpenAI, armazenamento de arquivos, geração de miniaturas, UI em português e fluxo completo de criação/edição/visualização de fichas técnicas.\r\n\r\nFora do Escopo\r\n\r\nE-commerce, pagamentos e logística.\r\nERP/estoque/PCP.\r\nModelagem 3D e simulação de peças.\r\nIntegrações com sistemas externos além OpenAI/RPA Monitor.\r\nAnálises financeiras avançadas.	API da OpenAI disponível e chave configurada.\r\nPDFs/imagens com qualidade mínima para extração.\r\nBanco SQL configurado e acessível.\r\nArmazenamento local ou compatível para arquivos e desenhos.\r\nUsuários treinados para revisar/ajustar campos.	Dependência de custos/limites da API OpenAI.\r\nTempo de processamento variável conforme tamanho/qualidade do arquivo.\r\nTamanho máximo de upload por arquivo (até 1GB).\r\nNecessidade de conexão estável e recursos de máquina	em_andamento	0	\N
54	Conciliação de Incorporadora		2026-01-05 20:14:47.202832	1	6	\N	Automação end-to-end do processo de conciliação de incorporadora, eliminando tarefas manuais, reduzindo erros operacionais e garantindo rastreabilidade diária dos arquivos e baixas realizadas no Aztronic.	O processo manual de conciliação bancária demandava alto esforço operacional, estava sujeito a falhas humanas, atrasos no processamento e inconsistências nas baixas financeiras.\r\nA automação surgiu como oportunidade para padronizar, escalar e garantir confiabilidade no processo diário.	Automatizar a geração diária do ZIP com arquivos bancários conforme regras estabelecidas\r\n\r\nExecutar a conciliação automática no sistema Aztronic\r\n\r\nRealizar a baixa correta dos títulos financeiros\r\n\r\nEnviar e-mails automáticos de notificação ao final do processo\r\n\r\nGerar relatórios e logs de execução para auditoria e acompanhamento	Eficiência operacional\r\n\r\nRedução de custos manuais\r\n\r\nAumento da confiabilidade dos processos financeiros\r\n\r\nDigitalização e automação de rotinas críticas	Coleta automática de arquivos bancários\r\n\r\nGeração diária de arquivo ZIP com todos os documentos do dia\r\n\r\nExtração e processamento dos arquivos conforme layout CNAB\r\n\r\nExecução de RPA para acesso e conciliação no Aztronic\r\n\r\nBaixa automática de títulos financeiros\r\n\r\nEnvio automático de e-mails via Gmail\r\n\r\nGeração de relatórios (last_report.json) e logs de execução	Análise manual de exceções financeiras\r\n\r\nAlterações nas regras de negócio do Aztronic\r\n\r\nTratamento contábil ou fiscal fora da conciliação\r\n\r\nDesenvolvimento de novos layouts bancários não previstos	Acesso válido e estável ao sistema Aztronic\r\n\r\nCredenciais de Google Drive e Gmail configuradas corretamente\r\n\r\nDisponibilidade diária dos arquivos bancários\r\n\r\nAmbiente de execução do RPA operacional	Dependência de estabilidade dos sistemas externos (Aztronic, Google)\r\n\r\nExecução condicionada à disponibilidade dos arquivos do dia\r\n\r\nAlterações no layout bancário podem exigir ajustes no RPA	concluido	100	2025-12-17
55	Amortização		2026-01-06 15:23:36.832187	1	6	\N	Automatização do processo mensal de amortização de dívidas atualmente executado de forma manual em planilhas e operacionalizado em um sistema legado (VS), por meio da implementação de um robô de RPA que realizará a execução automática, recorrente e padronizada do processo.	O processo atual de amortização de dívidas é altamente manual, dependente de planilhas para cálculo de juros, saldos e valores amortizados, além de exigir interação humana contínua com o sistema legado VS. Esse cenário gera riscos operacionais, como erros de digitação, inconsistências nos cálculos, retrabalho e dependência de conhecimento específico de operadores.\r\nA oportunidade está em automatizar o processo via RPA, garantindo maior confiabilidade, eficiência operacional, redução de erros e ganho de produtividade, além de permitir a execução recorrente e autônoma do processo.	Automatizar o processo mensal de amortização de dívidas no sistema VS\r\n\r\nEliminar atividades manuais repetitivas e suscetíveis a erro\r\n\r\nGarantir consistência e precisão nos cálculos de juros e amortizações\r\n\r\nReduzir o tempo operacional gasto na execução do processo\r\n\r\nPermitir execução automática e programada do processo uma vez por mês\r\n\r\nMelhorar a rastreabilidade e controle do processo	O projeto está alinhado à estratégia de eficiência operacional e transformação digital, promovendo automação de processos críticos, redução de riscos operacionais e melhor utilização dos recursos humanos. Além disso, contribui para a modernização indireta da operação ao integrar automação inteligente a sistemas legados sem necessidade de substituição imediata.	Análise do processo atual de amortização de dívidas\r\n\r\nUtilização da planilha base existente como fonte de dados (juros, saldos, valores amortizados)\r\n\r\nDesenvolvimento de um robô de RPA para:\r\n\r\nLer e validar os dados da planilha\r\n\r\nExecutar os cálculos conforme regras definidas\r\n\r\nAcessar o sistema legado VS\r\n\r\nRealizar a amortização mensal automaticamente\r\n\r\nConfiguração de agendamento para execução automática mensal\r\n\r\nGeração de logs e evidências da execução do processo\r\n\r\nTestes, validação e acompanhamento inicial da automação	Alterações funcionais ou estruturais no sistema legado VS\r\n\r\nRedesenho das regras de negócio de amortização\r\n\r\nCriação ou mudança do modelo financeiro de cálculo de juros\r\n\r\nIntegração via API ou modernização do sistema VS\r\n\r\nAutomação de processos não relacionados à amortização mensal de dívidas	O sistema VS continuará sendo utilizado pelo cliente\r\n\r\nA planilha utilizada no processo atual permanecerá como fonte oficial dos dados\r\n\r\nAs regras de cálculo de juros e amortização já estão validadas pelo negócio\r\n\r\nO ambiente permitirá execução agendada do RPA uma vez por mês\r\n\r\nCredenciais e acessos necessários ao sistema VS serão disponibilizados	Dependência da estabilidade e disponibilidade do sistema legado VS\r\n\r\nLimitações técnicas de interação com o sistema por se tratar de sistema legado\r\n\r\nExecução do processo restrita à periodicidade mensal\r\n\r\nEventuais mudanças na estrutura da planilha podem impactar o funcionamento do RPA\r\n\r\nNecessidade de atuação humana em casos de exceção ou falha operacional	em_andamento	0	2026-01-30
56	Copiloto de Cadastro e Análise de Crédito		2026-01-10 20:36:04.699203	10	10	\N	Desenvolvimento da primeira fase do Copiloto Operacional da Rede Brasil, focada na automação e padronização do processo de cadastro de clientes (PF e PJ) e análise de crédito, utilizando integração com sistemas existentes e Inteligência Artificial explicável para reduzir erros, acelerar decisões e aumentar a segurança operacional.	O processo atual de cadastro e análise de crédito depende fortemente de execução manual, múltiplas telas, conferência humana intensiva e interpretações individuais, o que gera:\r\n\r\nAlto custo operacional\r\n\r\nRisco de erro humano\r\n\r\nLentidão no atendimento\r\n\r\nFalta de padronização nas decisões de crédito\r\n\r\nDificuldade de rastreabilidade e auditoria\r\n\r\nA oportunidade é transformar esse fluxo em um processo assistido, padronizado e rastreável, sem substituir o sistema atual nem o julgamento humano.	Automatizar o fluxo de cadastro de clientes PF e PJ\r\n\r\nCentralizar documentos em uma plataforma própria\r\n\r\nExecutar pré-análise de crédito automática\r\n\r\nCriar filas inteligentes de aprovação (humano no loop)\r\n\r\nReduzir tempo de cadastro e análise\r\n\r\nAumentar segurança jurídica e previsibilidade\r\n\r\nPadronizar critérios operacionais entre unidades	O projeto está alinhado com a estratégia da Rede Brasil de:\r\n\r\nRedução de risco operacional e financeiro\r\n\r\nEscalabilidade do modelo de operação\r\n\r\nPadronização de processos entre lojas\r\n\r\nAumento de eficiência sem troca do sistema core (Autoban)\r\n\r\nPreparação para fases futuras de inteligência operacional e analítica\r\n\r\nEsse módulo é a base estrutural para os próximos copilotos do sistema	Plataforma web com login e controle de acesso\r\n\r\nUpload estruturado de documentos de clientes\r\n\r\nLeitura automática de documentos via IA\r\n\r\nExtração de dados cadastrais\r\n\r\nPré-análise de crédito automática (PF e PJ)\r\n\r\nIntegração assistida com:\r\n\r\nBrick (PF)\r\n\r\nSPC (PJ)\r\n\r\nCriação de filas de aprovação:\r\n\r\nAprovação automática\r\n\r\nAprovação humana (casos de risco)\r\n\r\nGeração de resumo explicável da análise\r\n\r\nExecução automática do cadastro no sistema Autoban após aprovação\r\n\r\nRegistro auditável de decisões	Reserva de veículos\r\n\r\nGestão de frota\r\n\r\nMódulos de avarias, fraudes, rentabilidade ou disponibilidade futura\r\n\r\nDashboards executivos avançados\r\n\r\nChat analítico com dados históricos\r\n\r\nIntegrações externas adicionais não discutidas	O sistema Autoban continuará sendo o sistema core\r\n\r\nA integração será feita via API quando possível e automação assistida quando necessário\r\n\r\nA IA atuará de forma explicável, sem decisões autônomas finais\r\n\r\nDecisões críticas sempre terão validação humana\r\n\r\nA Rede Brasil fornecerá acessos necessários aos sistemas (Autoban, Brick, SPC)\r\n\r\nO uso de IA terá custos variáveis repassados sem margem	Dependência técnica das integrações com sistemas de terceiros\r\n\r\nQualidade dos dados de origem influencia a precisão das análises\r\n\r\nAlgumas etapas exigem interação humana (biometria, exceções de crédito)\r\n\r\nLimitações impostas por sistemas externos (ex: SPC, Brick)\r\n\r\nEscopo restrito à primeira fase acordada (cadastro + crédito)	em_andamento	0	2026-02-14
25	FGbularmaci — RAG Jurídico (Extração Automática de Processos)	\N	2025-10-13 22:39:02.588316	6	8	Plataforma web para ingestão e gestão de processos a partir de PDFs (iniciais, notificações, atas e decisões), usando RAG para extrair campos jurídicos críticos (CNJ, órgão, Vara/Célula/Foro/Comarca/Estado, assunto/objeto, partes, prazos, audiência, tipo/resultado/fundamentação da decisão, etc.).\r\nO sistema realiza chunking + embeddings para busca semântica, aplica pós-processamento heurístico (regex/normalização) para cobrir lacunas e oferece tela de confirmação para revisão humana. Persistência em SQLite (dev) com opção de evoluir para Postgres+pgvector. Há logs/prints de debug em pontos críticos para rastreabilidade.	Plataforma web para ingestão e gestão de processos a partir de PDFs (iniciais, notificações, atas e decisões), usando RAG para extrair campos jurídicos críticos (CNJ, órgão, Vara/Célula/Foro/Comarca/Estado, assunto/objeto, partes, prazos, audiência, tipo/resultado/fundamentação da decisão, etc.).\r\nO sistema realiza chunking + embeddings para busca semântica, aplica pós-processamento heurístico (regex/normalização) para cobrir lacunas e oferece tela de confirmação para revisão humana. Persistência em SQLite (dev) com opção de evoluir para Postgres+pgvector. Há logs/prints de debug em pontos críticos para rastreabilidade.	- Problemas atuais do cliente: entrada manual e demorada de dados; informações espalhadas por TRTs, TJs e JF com formatos diferentes; campos essenciais faltando (ex.: prazos, audiência, decisão) → risco operacional e de perder prazos; baixa capacidade de busca/consulta semântica; inconsistência de nomenclatura (Vara × Célula × Foro).\r\n\r\n- Oportunidade: automatizar 80–90% da captura de dados com IA + regras, padronizar terminologia, acelerar onboarding de casos e dar visibilidade imediata a prazos e resultados, reduzindo custos e erros.	- Extrair automaticamente 100% dos campos-alvo do print (Cadastro, Andamento, Decisão, Sistema) com fallback determinístico quando a IA não achar.\r\n\r\n- Reduzir >70% do tempo de cadastro por processo.\r\n\r\n- Aumentar a confiabilidade dos dados (logs, validações e confirmação humana).\r\n\r\n- Habilitar busca semântica e sumarização por chunks.\r\n\r\n- Padronizar Vara/Célula/Foro/Comarca/Estado e Partes/Cliente para relatórios e integrações	- Eficiência operacional: menos retrabalho, menos SLA perdido.\r\n\r\n- Escalabilidade: arquitetura modular (extractors, serviço RAG, rotas, modelos) facilita evoluções e integrações (ex.: Hilo ID).\r\n\r\n- Qualidade de dados: normalização + confirmação humana mitigam alucinações da IA.\r\n\r\n- Time-to-value: roda em Replit/SQLite hoje e migra fácil para Postgres/pgvector quando crescer.	- Upload seguro de PDFs → extração de texto (PyPDF2; OCR pode ser plugado se necessário).\r\n\r\n- RAG (OpenAI) para análise de trechos + postprocess (extractors/) com regex/heurística para:\r\n\r\n- Cadastro: Célula (quando houver), Vara, Foro, Comarca, Estado, Cliente, Parte, Sistema/Órgão/Origem, Assunto/Objeto.\r\n\r\n- Notificação: Prazo, Tipo de Notificação.\r\n\r\n- Ata: Audiência inicial, Resultado da audiência, Prazos derivados.\r\n\r\n- Decisão: Tipo (Sentença/Acórdão), Resultado (Deferido/Indeferido), Fundamentação resumida.\r\n\r\n- Sistema: ID interno (Hilo) e Data/hora de cadastro (manual).\r\n\r\n- Tela de confirmação com edição de todos os campos (validação: preencher Vara ou Célula).\r\n\r\n- Persistência (models.py) e criação idempotente de colunas no SQLite (migração leve).\r\n\r\n- Busca semântica por chunks + análise consolidada do documento.\r\n\r\n- Logs/prints de debug e tratamento de exceções em cada etapa.\r\n\r\nClaud - 145,00 Reais\r\nChave api Gpt - Cliente vai criar sua própria chave	- Geração automática de petições/documentos jurídicos.\r\n\r\n- Protocolos em tribunais, captura robótica de andamentos, notificações por integrações externas.\r\n\r\n- Painéis gerenciais avançados (BI), SLA/cron jobs de monitoramento em produção.\r\n\r\n- Integração bidirecional completa com Hilo (mantemos apenas campo de vínculo).	- Disponibilidade do OPENAI_API_KEY e conectividade à API.\r\n\r\n- PDFs com texto extraível; se vierem somente imagem, OCR deverá ser acoplado.\r\n\r\n- Usuários autenticados (admin cria usuários).\r\n\r\n- Ambiente de execução com variáveis de ambiente corretas e diretório uploads/ acessível.\r\n\r\n- Confirmação humana permanece no fluxo (governança e qualidade).\r\n\r\n- Em produção, recomendado Postgres; SQLite atende dev/prova de conceito.	- Custos e limites da API de IA (taxa/latência).\r\n\r\n- Qualidade do PDF (escaneado/ruído) impacta a extração; OCR pode ser necessário.\r\n\r\n- Variedade terminológica entre ramos (TRT/TJ/JF) exige manutenção contínua das heurísticas.\r\n\r\n- Segurança/privacidade: PDFs podem conter dados sensíveis → controle de acesso, storage seguro e sigilo contratual.\r\n\r\n- Sem garantia de 100% de acerto da IA; por isso há fallback + revisão humana.	concluido	0	\N
50	Implementação do Data Lake BigQuery – OAZ		2025-12-11 17:46:51.067272	5	10	\N	A OAZ necessita de uma estrutura centralizada e robusta para armazenamento e processamento de dados. O projeto consiste na criação de um Data Lake corporativo no Google BigQuery, reunindo todas as fontes de dados críticas — GA4, Google Ads, Meta Ads, TikTok Ads, Pagar.me, catálogo de produtos, price intelligence e dados internos — permitindo análises avançadas, redução de custos, eliminação de dependências externas e habilitação de recursos de IA e automação.	A operação atual depende de múltiplas fontes desconectadas, planilhas, integrações instáveis e conectores externos como Supermetrics, tornando análises lentas, caras e sujeitas a erro.\r\nHá também dificuldade em integrar dados do catálogo de produtos e IA.\r\nA oportunidade é criar um ecossistema unificado em BigQuery que sirva como fonte única de verdade e permita automações, dashboards consistentes e a evolução para a V2 do 360.	Criar um Data Lake completo no BigQuery unificando todas as fontes de dados da OAZ.\r\n\r\nEliminar dependências externas (como Supermetrics) com integrações diretas via API.\r\n\r\nEstruturar camadas RAW, STAGING e BUSINESS no BigQuery.\r\n\r\nIntegrar GA4, Google Ads, Meta Ads, TikTok Ads e Pagar.me.\r\n\r\nIncorporar o catálogo de produtos e price intelligence ao Data Lake.\r\n\r\nPreparar ambiente para IA de tagueamento e insights automatizados.\r\n\r\nSustentar tecnicamente a V2 do 360 e futuros produtos da OAZ.	O projeto está alinhado com a estratégia da OAZ de centralizar dados, aumentar eficiência operacional, reduzir custos, melhorar inteligência competitiva e acelerar o uso de IA na operação. Também sustenta a evolução do produto 360 e melhora a capacidade de tomada de decisão baseada em dados confiáveis e atualizados em tempo real.	Criar ambiente oficial BigQuery da OAZ.\r\n\r\nConfigurar datasets, permissões e governança de dados.\r\n\r\nImplementar ingestão automática das seguintes fontes:\r\n\r\nGoogle Analytics 4\r\n\r\nGoogle Ads\r\n\r\nMeta Ads\r\n\r\nTikTok Ads\r\n\r\nPagar.me\r\n\r\nPrice Intelligence\r\n\r\nCatálogo de produtos (imagens + atributos)\r\n\r\nCriar camadas de dados: RAW, STAGING e BUSINESS.\r\n\r\nDefinir tabelas e visões analíticas.\r\n\r\nEstruturar pipelines de atualização horários/diários.\r\n\r\nDisponibilizar dados para dashboards e sistemas internos (ex.: 360).\r\n\r\nPreparar bases para integração de IA (tagueamento, insights, modelos).\r\n\r\nDocumentar arquitetura, fluxos e procedimentos de manutenção.	Construção de dashboards finais (ex.: Looker/Power BI), exceto integrações básicas.\r\n\r\nDesenvolvimento da V2 do 360 (apenas preparação de dados).\r\n\r\nConstrução de modelos avançados de IA (serão fases posteriores).\r\n\r\nSuporte contínuo de operação após entrega (pode ser contratado à parte).\r\n\r\nAjustes internos no ERP ou CRM da OAZ que não envolvam dados enviados ao BigQuery.	A OAZ fornecerá acesso às contas de GA4, Google Ads, Meta Ads, TikTok e Pagar.me.\r\n\r\nTime interno fornecerá credenciais e permissões no Google Cloud.\r\n\r\nAs APIs externas estarão ativas e autorizadas para uso.\r\n\r\nO time técnico da OAZ colaborará na validação dos modelos de dados.\r\n\r\nO catálogo de produtos será disponibilizado pelo time de Ronald.\r\n\r\nHaverá disponibilidade para reuniões semanais de alinhamento.	Limitações de acesso às contas Meta Ads/TikTok devido a validações de desenvolvedor.\r\n\r\nHistórico parcial de GA4 já existente, não sendo possível recuperar dados anteriores.\r\n\r\nDependência de times internos para liberação de acessos.\r\n\r\nCustos do BigQuery devem ficar dentro do budget acordado.\r\n\r\nPrazo pode ser afetado por dependências externas ou APIs instáveis.	concluido	0	\N
6	Sistema de Gestão de Dívidas e Debêntures.	\N	2025-08-26 16:57:29.26579	1	10	Construir um sistema leve e confiável para substituir a planilha consolidada atual, centralizando o ciclo de vida das dívidas (financiamentos e debêntures): cadastro de contratos, geração automática do fluxo projetado, registro de pagamentos realizados (baixas), conciliação mensal de saldos com extratos bancários, controle de liberações, parametrização de índices (CDI, pré e IPCA) e relatórios/dashboards de acompanhamento.	Construir um sistema leve e confiável para substituir a planilha consolidada atual, centralizando o ciclo de vida das dívidas (financiamentos e debêntures): cadastro de contratos, geração automática do fluxo projetado, registro de pagamentos realizados (baixas), conciliação mensal de saldos com extratos bancários, controle de liberações, parametrização de índices (CDI, pré e IPCA) e relatórios/dashboards de acompanhamento.	A planilha atual é pesada, lenta (até ~5 min para filtrar) e difícil de trabalhar, aumentando o risco operacional.\r\n\r\nProcessos-chave (projeções x realizados, ajustes de juros, conciliações e amortizações extraordinárias) exigem manipulação manual e conhecimento tácito.\r\n\r\nHá necessidade de lidar com diferentes naturezas (financiamentos vs. debêntures), regras de cálculo distintas e atualização de índices (CDI mensal hoje; IPCA no futuro).\r\n\r\nOportunidade: transformar o fluxo em um sistema com base única, rá	Substituir a planilha consolidada por um sistema web com base única e desempenho consistente. \r\n\r\nAutomatizar a geração de projeções de principal/juros a partir do contrato (no cadastro da dívida). \r\n\r\nRegistrar pagamentos realizados (baixas) e conciliar com o projetado, mantendo histórico e ajustes quando o cálculo bancário divergir. \r\n\r\nControlar liberações e vincular ao contrato/empreendimento. \r\n\r\nParametrizar índices (CDI mensal; pronto para IPCA e outros) e tipos de dívida (financiamento/debênture). \r\n\r\nRelatórios/dashboards: visão consolidada por banco, empreendimento/shopping, contrato e período.	Eficiência Operacional (Financeiro): reduzir tempo de processamento e retrabalho; padronizar cálculos/ajustes.\r\n\r\nGovernança & Risco: trilha de auditoria (quem alterou o quê, quando e por quê).\r\n\r\nEscalabilidade: acomodar novos contratos, naturezas (debêntures) e índices sem “estourar” planilhas.\r\n\r\nTime-to-Value: aproveitar a base já existente e migrar com mínima ruptura do processo atual.	Módulos (MVP+):\r\n\r\nCadastro de Dívidas/Contratos\r\n\r\nCampos: banco, empreendimento/shopping, tipo (financiamento ou debênture), índice (CDI/pré/IPCA), taxas, prazos, carência, calendário de parcelas, etc.\r\n\r\nGeração imediata do fluxo projetado (principal/juros) por parcela. \r\n\r\nPagamentos (Realizados / Baixas)\r\n\r\nLançamento de pagamentos de principal e juros; substitui projeção pelo realizado e preserva histórico de diferenças.\r\n\r\nAmortizações extraordinárias (ex.: 28/07, R$ 4 mi) impactam saldo/juros e reprojetam o restante. \r\n\r\nConciliação Mensal de Saldos\r\n\r\nComparação com extratos bancários; registro de divergências e justificativas/ajustes. \r\n\r\nLiberações (Drawdowns)\r\n\r\nRegistro e vinculação por contrato/empreendimento; impacto no saldo e cronograma. \r\n\r\nÍndices e Parâmetros\r\n\r\nTabela de índices (CDI mensal hoje; preparado para IPCA e outros). \r\n\r\nDebêntures\r\n\r\nTratamento próprio de cálculo (por PU/preço unitário), separado do fluxo padrão de financiamentos. \r\n\r\nRelatórios & Dashboard\r\n\r\nConsolidado por contrato/banco/empreendimento; visão projetado vs. realizado; calendário de vencimentos.	Integração automática com bancos (OFX/API) para importação de extratos.\r\n\r\nGestão documental jurídica de contratos (repositório de PDFs com workflow legal).\r\n\r\nForecast de caixa corporativo além das dívidas (tesouraria completa).\r\n\r\nSubstituição/integração profunda com ERP/contabilidade (lançamentos contábeis automáticos).\r\n\r\nAutomação de aprovação orçamentária corporativa fora do contexto das dívidas.\r\n(Estes itens podem compor uma fase posterior.)	A base atual contém dados suficientes para carga inicial (contratos, projeções, pagamentos realizados e liberações). \r\n\r\nO time financeiro atualizará CDI mensalmente (até futura automação). \r\n\r\nHaverá pelo menos 1 usuário power-user (Leonardo) para validar regras e exceções (como ajustes de juros e amortizações extraordinárias).	Qualidade e padronização dos dados legados (planilhas heterogêneas, fórmulas e chaves manuais). \r\n\r\nDesempenho: volume de linhas/parcelas e cálculos de juros indexados exigem modelagem eficiente.\r\n\r\nVariedade de regras (financiamentos vs. debêntures com cálculo por PU). \r\n\r\nPrazo curto para um MVP funcional, dada a urgência operacional destacada na reunião.	em_andamento	0	\N
57	Marketing & Comercial		2026-01-16 22:34:59.541931	2	11	\N									em_andamento	0	2026-04-30
58	PlanAi		2026-01-22 15:33:30.741921	11	14	\N									em_andamento	70	2026-02-13
\.


--
-- Data for Name: project_api_credentials; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.project_api_credentials (id, nome, provedor, descricao, api_key_masked, api_key_encrypted, ambiente, created_at, updated_at, project_id, created_by_id) FROM stdin;
\.


--
-- Data for Name: project_api_endpoints; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.project_api_endpoints (id, nome, url, metodo, descricao, headers, body_exemplo, documentacao_link, created_at, updated_at, project_id, credential_id, created_by_id) FROM stdin;
\.


--
-- Data for Name: project_api_keys; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.project_api_keys (id, project_id, user_id, name, prefix, key_hash, scopes_json, created_at, last_used_at, expires_at, revoked_at) FROM stdin;
\.


--
-- Data for Name: project_files; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.project_files (id, filename, original_name, mime_type, file_size, descricao, storage_path, created_at, project_id, category_id, uploaded_by_id) FROM stdin;
2	2a42931f47384068a09e776feb997009.xls	2 ano.xls	application/vnd.ms-excel	12800	Teste teste	/home/runner/workspace/uploads/project_25/2a42931f47384068a09e776feb997009.xls	2025-12-11 15:11:17.506307	25	3	1
3	67d97ea4c4754df38052ade2ffdd8342.pdf	Souq Store - Termo de Imissão na Posse de Espaço - 14082024 - assinado.pdf	application/pdf	945597		/home/runner/workspace/uploads/project_33/67d97ea4c4754df38052ade2ffdd8342.pdf	2025-12-11 15:16:00.782351	33	\N	5
\.


--
-- Data for Name: project_users; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.project_users (project_id, user_id) FROM stdin;
18	13
18	2
8	4
46	2
6	2
36	4
36	8
36	6
58	3
13	6
14	6
45	13
27	2
11	4
11	8
11	6
10	2
47	10
44	2
44	3
44	4
39	8
40	4
26	7
34	13
34	5
1	4
1	2
1	6
9	2
9	6
3	10
7	2
35	13
19	13
20	13
29	5
29	6
29	11
54	6
43	13
15	5
15	13
55	6
56	10
16	13
56	6
56	2
25	8
28	7
49	7
49	10
23	7
50	10
52	13
33	13
33	5
53	10
53	2
53	11
53	7
53	6
53	13
53	12
\.


--
-- Data for Name: system_api_keys; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.system_api_keys (id, user_id, name, prefix, key_hash, scopes_json, created_at, last_used_at, expires_at, revoked_at) FROM stdin;
5	1	chave_gomes1	SGoiN2Igsb	scrypt:32768:8:1$rvXGsmIuqiQ0uywF$d756897b936bda2bf45b45488f3b23de606968c3f0f74f9b6ba8f95f7e368924db100b40359f7716f873785fcc5f1b7c5a21306c23c702fb58b1ce4e62e08141	["clients:read", "clients:write", "projects:read", "projects:write", "tasks:read", "tasks:write", "users:read", "leads:read", "leads:write"]	2025-12-30 17:59:09.021047	2025-12-30 19:56:55.364871	\N	\N
3	1	GOMES_1	h7sbQYUjO9	scrypt:32768:8:1$6ceZ6Li1cEQtvsXh$d688a3332bcb1d795ee52469ca9602f998ad6b534b4027b0e341d8e70be2cfc82cf4a6bcfbcba01308f3b4337969980a03d7cd906c2543e1e620d4473951849a	["clients:read", "clients:write", "projects:read", "projects:write", "tasks:read", "tasks:write", "users:read", "leads:read", "leads:write"]	2025-12-18 22:30:06.290513	2025-12-30 16:57:55.508238	\N	\N
4	1	chave_gomes	REtcZgGkjG	scrypt:32768:8:1$iVinnv6HdLRDp7Zs$789f3f1d0041b351b7ba1a99e23e6792ad5d6dee7e0a43084a41fa5ae1ab36dd810fd608ddad3a6260540dc9b25275732c62812d31f4a28def4f2bf4be203fd5	["clients:read", "clients:write", "projects:read", "projects:write", "tasks:read", "tasks:write", "users:read", "leads:read", "leads:write"]	2025-12-30 17:05:55.324542	\N	\N	\N
\.


--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.task (id, titulo, descricao, status, data_conclusao, created_at, completed_at, project_id, assigned_user_id, disparada, disparada_at, ordem) FROM stdin;
21	Totais SEFAZ corrigidos (descoberta e correção da paginação), com separação por relatório e visualização consolidada.		concluida	2025-07-29	2025-08-26 15:25:50.135933	\N	3	4	f	\N	8
437	Automação Conciliação de incorporadora		concluida	2025-12-17	2026-01-05 20:16:13.301948	2026-01-05 20:18:52.721354	54	6	f	\N	0
14	Upload padrão do BI implementado; lançamento manual com tipos de receita disponível.		concluida	2025-07-29	2025-08-26 15:05:26.590821	\N	2	4	f	\N	1
13	Cadastro de shopping com regime (lucro real/presumido) e edição habilitada.		concluida	2025-07-29	2025-08-26 15:05:04.90108	\N	2	4	f	\N	0
28	Entrega do projeto e validação do Time de contas a receber		concluida	2025-08-21	2025-08-26 16:14:55.809906	\N	4	4	f	\N	0
370	Montando sistema no replit		concluida	2025-11-28	2025-11-25 15:20:16.728507	2025-12-08 20:10:52.459001	19	8	f	\N	3
354	Migrar toda a operaçao da Aeropool para o Salesforce	Finalizada a etapa dos formularios do David. Entender como recriar a operaçao da Aeropool dentro do Salesforce como foi feito na Avsales.	pendente	\N	2025-11-18 20:02:20.284163	\N	28	7	f	\N	0
372	IFRRJ - Campus Paracambi - Testes e Cadastro de alunos	Victor (parcerio dentro do IFRRJ) esta reliazando testes e conhecendo o app. Na seguida, irá ver a turma legal para começar a cadastrar 	concluida	2025-11-28	2025-11-25 16:16:09.939493	2026-01-16 22:32:24.997009	38	4	f	\N	2
371	Foco da semana 24/11 - 28/11	Desenvolver pagina web para primeiro contato com o futuro cliente.\n\nhttps://vt-appin-sight-felipe120.replit.app/\n	concluida	2025-11-28	2025-11-25 16:12:57.295581	2026-01-23 20:12:45.22316	44	4	f	\N	11
439	terminar de classificar os custos no sistema de reconciliaçao bancaria 	Terminar de nomear as transaçoes dos extartos do Humnberto, aproveitando o tempo dele no rio para isso.\n	concluida	2026-01-09	2026-01-05 21:36:53.33771	2026-01-13 16:36:18.725827	26	7	f	\N	0
438	melhorias no sistema de quotes	Melhorias do sistema depois da apresentaçao para o Humberto no dia 5/01/26. reaçao positiva para o sistema!	concluida	2026-01-16	2026-01-05 21:27:48.542381	2026-01-16 21:59:40.884291	27	7	f	\N	1
356	Foco da semana 17/11 - 21/11	Dia - dia das áreas administrativa da empresa Inovai.Lab	concluida	2025-11-21	2025-11-19 13:08:22.067266	2025-12-02 20:41:51.267681	40	4	f	\N	1
15	Demonstrativo fiscal por shopping/período exibido; lançamentos alimentam a visão (MVP).		concluida	2025-08-05	2025-08-26 15:06:38.102712	\N	2	4	f	\N	2
331	Foco da semana 10/11 - 21/11	Priorizar a realização da reunião técnica para definir o escopo e o mapeamento dos dados, que são os próximos passos cruciais para o avanço do projeto. O responsável deve garantir que a tarefa 'Fazer a leitura do banco de dados' seja concluída para que o mapeamento possa ser finalizado.\n\n-11/11 = O sistema ja puxa os dados do banco de dados.  \ndados puxados : \ndtmart.dim_colaborador \n\n→sk_colaborador\n Dados da loja:\nia_oaz.vw_localidades\n\nTotal vendas:\nia_oaz.vw_vendas_360 \n\n12/11 = vou falar com o mmatheus hj as 14h, entender esse processo . \nreuniao feita. vamos criar um chat para comunicaçao personalizada voltado à parte administrativa e burocrática da empresa, incluindo contratos, políticas internas e documentos (armazenados no SharePoint).\n\n\n- comunicaçao persolanizada- voltado à análise de vendas e comportamento de clientes, utilizando dados do banco de dados (Microvix/Sonal).	concluida	2025-11-14	2025-11-10 21:26:32.517479	2025-11-24 20:22:05.040795	33	5	f	\N	1
22	Definidas orientações de uso: subir múltiplas empresas em um único envio; identificado gargalo e necessidade de fila (um processamento por vez).		concluida	2025-07-31	2025-08-26 15:26:08.924126	\N	3	4	f	\N	14
16	Rotina “Calcular Impostos” (menu dedicado; aplicar regras e registrar lançamentos).		concluida	2025-08-07	2025-08-26 15:07:06.615991	\N	2	4	f	\N	3
17	Cadastro de CST e alíquotas maleáveis por shopping		concluida	2025-08-08	2025-08-26 15:07:59.313971	\N	2	4	f	\N	4
18	Padronização dos tipos de receita (separar “aluguel” e “CDU”).		concluida	2025-08-11	2025-08-26 15:08:20.815569	\N	2	4	f	\N	5
19	Validação final das fórmulas do PIS/COFINS (após ajustes).		concluida	2025-08-18	2025-08-26 15:09:01.42339	\N	2	4	f	\N	6
20	Integração RM (etapa posterior).		concluida	2025-08-21	2025-08-26 15:09:18.471705	\N	2	4	f	\N	7
501	Cobrar resposta do Humberto - Ele vai falar com David		pendente	2026-01-30	2026-01-26 20:05:51.842699	\N	28	7	f	\N	1
26	Criação da Primeira Versão		concluida	2025-08-12	2025-08-26 16:14:04.076741	\N	4	4	f	\N	1
505	Aumentar duraçao da janela de multi empresas na quote.	Aumentar a duraçao da janela de cadastro quando o contato esta em mais de uma empresa\r\n	em_andamento	2026-01-30	2026-01-28 19:51:40.085619	\N	27	7	f	\N	0
506	O usuario conseguir ajustar as informaçoes das quotes	AS vezes a main part vem com quanidade solicitada de 3 por exemplo mas humberto so tem 1. Ele precisa editar a quote no sistema para que a informaçao seja correta.\r\n	em_andamento	2026-01-30	2026-01-28 19:53:02.558007	\N	27	7	f	\N	0
23	Validação inicial: XML processando (lento); identificado ajuste do upload SEFAZ x relatório da empresa; coleta de arquivos de exemplo para correção.		concluida	2025-08-13	2025-08-26 15:26:30.068812	\N	3	4	f	\N	21
27	Correção da parte de classifdicação do Weelhub		concluida	2025-08-15	2025-08-26 16:14:28.18409	\N	4	4	f	\N	2
25	Mapeamento das funcionalidades		concluida	2025-08-05	2025-08-26 16:13:44.299596	\N	4	4	f	\N	3
3	Avaliação inicial (v1 com dados de demonstração) e coleta de requisitos fiscais: base de cálculo, CST, CFOP de entrada e PDF via chave de acesso; discussão de cancelamento/retorno ao Fluig e e-mails.		concluida	2025-07-30	2025-08-26 14:40:07.336599	\N	1	2	f	\N	37
507	Melhorar a forma que o sistema ve se a peça esta no banco de peças local	As vezes o sistema indica que a parte da quote esta no banco de dados local porem as vezes a condiçao solicitada nao esta.	em_andamento	2026-01-30	2026-01-28 19:54:16.314436	\N	27	\N	f	\N	0
377	Foco da semana 08/12 - 12/12	Andrey pediu para incluir o sistema de reconciliaçao dentro do RPA da INOV	concluida	2025-12-01	2025-11-28 20:20:58.685802	2025-12-10 19:42:45.968114	26	7	f	\N	0
1	Kickoff SÁ-SQ (alinhamento inicial da automação de evolução fiscal).		concluida	2025-07-24	2025-08-26 14:39:24.139676	\N	1	2	f	\N	25
2	Reunião de mapeamento dos próximos passos: sincronização/periodicidade, notificações e desenho de fluxo.		concluida	2025-07-28	2025-08-26 14:39:45.172176	\N	1	2	f	\N	35
4	Reunião de cronograma: definido marco de 25/09/2025 com Oliver e necessidade de cronograma detalhado.		concluida	2025-08-08	2025-08-26 14:40:29.58906	\N	1	2	f	\N	40
29	Reunião de mapeamento (kickoff contábil)		concluida	2025-07-31	2025-08-26 16:26:22.909503	\N	5	2	f	\N	27
350	login david salesforce	David nao esta conseguindo logar no salesforce para resolver os formularios.	concluida	2025-11-17	2025-11-14 17:30:10.943574	2025-12-01 16:36:42.10412	28	7	f	\N	0
24	Incluir a opção de filiais do Bobs e Spoleto para processamento de relatorio por empresa. 		concluida	\N	2025-08-26 15:28:02.771154	2025-09-02 18:30:31.07697	3	4	f	\N	29
508	Lisette pediu para adicionar as RFQ das quotes no salesforce.	Lisette trouxe um bom ponto que RFQ No da quote nao esta entrando no sistema	em_andamento	2026-01-30	2026-01-28 19:58:41.998118	\N	27	7	f	\N	0
51	Definição da hierarquia de classificação (Regional → Negócio → Empreendimento → Conta) e identificação de fluxos apartados (JC, Site).		concluida	2025-08-21	2025-08-26 18:52:36.839276	\N	8	2	f	\N	2
98	Reunião de exploração e definição da Fase 1		concluida	2025-09-02	2025-09-02 16:57:30.202151	\N	15	2	f	\N	0
52	Regra de Aportes (crédito/debito entre empreendimentos com data).		concluida	2025-08-22	2025-08-26 18:52:56.342958	\N	8	2	f	\N	3
53	Receber a base bruta do RM (layout/export “como vem”) e a tabela-mestre de Regionais/Negócios/Empreendimentos/Contas (incluindo marcações de fluxos apartados).		concluida	2025-08-22	2025-08-26 18:53:15.686053	\N	8	2	f	\N	4
54	Especificar campos obrigatórios do lançador de receitas (ex.: Empreendimento, Conta, Data, Valor, Centro de Custo).		concluida	2025-08-25	2025-08-26 18:53:32.120565	\N	8	2	f	\N	5
502	Andrey abrir demanda - Tarefas		em_andamento	2026-01-26	2026-01-26 20:15:39.926773	\N	56	10	f	\N	0
70	Definição do MVP (priorizar match/curadoria na V1).		concluida	2025-05-28	2025-08-26 19:22:17.955638	\N	10	5	f	\N	7
67	Mapeamento inicial do que será feito (escopo macro)	Conclusão mencionada; detalhes serão enriquecidos após análise das transcrições.	concluida	2025-08-15	2025-08-26 19:10:38.067176	\N	10	2	f	\N	12
332	Foco da semana 10/11 - 19/12	link de acesso - https://oaz-felipe120.replit.app\nusuario - admin senha ; admin123\n\n\nConcluir o "Desenvolvimento da Função de Desenho Técnico Automático" para que o piloto do AutoPLM possa ser iniciado e validado com as fichas técnicas coletadas\n\n-11/ 11 = contado com o matheus feito, ele esta numa imesão na empresa. amanha (12/11) ele vai passar o overview com a galera. \n\n- 17/11 = feedback recebido. vou implementar as mudanças .\n\n- falei com o matheus,  ele vai jogar para as meninas testarem \n\n28/11 - conseguimoss a API do fluxograma. vamos falar sobre no planning de hj. \n\n	concluida	2025-11-14	2025-11-10 21:27:32.037435	2026-01-16 22:11:14.186532	20	5	f	\N	7
365	Foco da semana 24/11 - 28/11	Finalizar V1 jate sexta - 28/11	concluida	\N	2025-11-24 20:21:23.515685	2025-11-25 20:12:00.399453	19	2	f	\N	0
378	teste	teste	concluida	2025-12-04	2025-12-01 18:18:59.376039	2025-12-01 18:19:20.391095	18	\N	f	\N	17
99	Definição do escopo incremental (MVP → entrevistas/transcrição → DP).		concluida	2025-09-02	2025-09-02 16:57:50.593204	\N	15	2	f	\N	1
69	Escopo com NDA + estratégia (franquias/online→offline/oceano azul).		concluida	2025-05-20	2025-08-26 19:22:00.340849	\N	11	5	f	\N	1
56	Definição de como a plataforma vai funcionar		concluida	2025-08-22	2025-08-26 19:02:47.154818	\N	9	2	f	\N	2
71	Alinhamento contratual (entrega funcional, sem travar no design).		concluida	2025-07-15	2025-08-26 19:22:41.759544	\N	11	5	f	\N	11
68	Liberação da view com dados dos shoppings		concluida	2025-10-08	2025-08-26 19:10:58.215872	2025-10-13 20:28:48.035859	10	2	f	\N	19
261	Agendar reunião técnica com Lucas Cavenco, Ronald e Mateus para alinhar funcionalidades e código.		concluida	\N	2025-10-26 20:10:46.212561	2025-11-05 19:48:48.476891	16	8	f	\N	5
366	Foco da semana 24/11 - 28/11		concluida	\N	2025-11-24 20:25:14.14011	2025-11-25 20:13:58.835413	18	10	f	\N	38
352	Foco da semana 17/11 - 21/11	Melhorar todo UX e Frontend\n\n18/11 - Comecei a entender melhor as telas do sistema e ja estudando como mudar o layout no stitch\n\n19/11 - montando as telas do dashboard de admin. falta duas telas para terminar  - fiz a atualização do design do sistema.  falta aepnas montar a parte do usuario. 	concluida	2025-11-21	2025-11-17 20:34:23.255674	2025-11-24 20:25:03.083119	18	5	f	\N	69
323	Foco da semana 10/11 - 28/11	Priorizar o fechamento do contrato para garantir a continuidade do projeto e a\nemissão da Nota Fiscal. Uma vez que o contrato esteja fechado, o foco deve ser a\nimplementação do RAG Jurídico, que é o core do projeto.	concluida	\N	2025-11-10 21:17:26.627312	2025-12-01 20:01:09.862733	25	8	f	\N	0
262	Integrar funcionalidades:		concluida	2025-11-07	2025-10-26 20:11:19.470108	2025-11-10 21:28:26.161359	16	8	f	\N	6
55	Protótipo do Sistema (Fase 1):		concluida	2025-08-26	2025-08-26 18:53:58.467207	2025-10-13 20:19:09.083755	8	4	f	\N	0
101	Reunião de alinhamento e levantamento de requisitos.		concluida	2025-09-02	2025-09-02 18:50:14.467642	\N	16	2	f	\N	7
102	Decisão de priorizar inadimplência como primeira frente do projeto.		concluida	2025-09-02	2025-09-02 18:50:30.802325	\N	16	2	f	\N	8
337	Foco da semana 10/11 - 14/11	Focar na implementação da segunda opção de upload para a planilha ADM e na\nfuncionalidade de espelhamento de juros e multas, que são as duas tarefas\npendentes e essenciais para a conclusão do MVP fiscal.	concluida	2025-11-14	2025-11-10 21:33:56.718632	2025-11-24 20:27:27.367111	2	4	f	\N	8
100	Desenvolvimento do MVP (login, upload, ranqueamento, shortlist).		concluida	2025-09-05	2025-09-02 16:58:15.026729	2025-09-08 13:41:37.724751	15	2	f	\N	2
57	Alinhamento inicial com Equipe de Shopping (escopo e objetivos)		concluida	2025-08-22	2025-08-26 19:03:11.993067	\N	9	2	f	\N	15
72	Kick-off do projeto com time ampliado.		concluida	2025-08-05	2025-08-26 19:23:02.182768	\N	11	5	f	\N	17
58	Identificação dos domínios de dados de AP no RM		concluida	2025-08-22	2025-08-26 19:03:27.533863	\N	9	2	f	\N	19
73	Admin web (Python/Flask) criado e liberado para testes.		concluida	2025-08-12	2025-08-26 19:23:17.872838	\N	11	5	f	\N	22
74	App com fluxo de onboarding/criação de conta apresentado.		concluida	2025-08-20	2025-08-26 19:23:33.182635	\N	11	5	f	\N	24
75	Apresentação inicial e alinhamento de formato ágil/escopo macro.		concluida	2025-05-14	2025-08-26 19:21:23.962217	2025-08-26 19:24:06.365087	11	5	f	\N	27
93	Criar a versão baseada no PowerPoint 		concluida	2025-09-02	2025-08-29 15:56:24.469367	2025-09-02 17:07:18.756616	11	5	f	\N	32
443	BUSCA DE SKU	Analisar como esta sendo feito a pesquisa dentro do sharepoint e validar \n\nbuscar na plataforma agora, ja que temos as imagens dentro dela	pendente	2026-01-16	2026-01-12 18:30:24.583122	\N	19	\N	f	\N	1
342	Foco da semana 10/11 - 21/11	Em contato com Yan, informou que vai entrar uma nova empresa no grupo que vai gerar uma demanda alta pra ele. Vai pausar o squad do 1pra5 e os projetos que ele esta de frente. A criação do sistema foi inciado mas os detalhes das informações (planilha deles) para tratar dentro do sistema, estão na mão deles.	concluida	2025-11-14	2025-11-10 21:42:17.263075	2025-11-24 20:30:29.649443	8	4	f	\N	6
503	Corrigir inconsistência do envio de email		pendente	\N	2026-01-26 20:19:38.433635	\N	13	6	f	\N	0
449	IMPLEMENTAR A LEITURA DAS PIS DE PRODUTOS IMPORTADOS		pendente	\N	2026-01-12 18:46:23.305862	\N	20	\N	f	\N	1
130	Exclusão múltipla de relatórios	Criar opção de selecionar e excluir vários relatórios de uma vez, em vez de excluir individualmente.	concluida	2025-09-10	2025-09-08 17:29:54.317621	2025-09-09 13:17:28.311041	3	4	f	\N	37
444	Cobrar thiago para utilizar e dar feedback		pendente	\N	2026-01-12 18:31:24.130284	\N	33	\N	f	\N	6
109	Reunião de alinhamento e mapeamento do problema		concluida	2025-09-03	2025-09-03 13:49:20.597282	\N	17	4	f	\N	3
441	LOGIN	https://oazbancoimagem.com.br/\r\n\r\nadmin\r\nadmin	pendente	\N	2026-01-12 18:26:04.983721	\N	19	\N	f	\N	0
110	Decisão de priorizar o MVP de comprovantes (App + Painel) antes do módulo de caixa/fechamento.		concluida	2025-09-03	2025-09-03 13:49:39.326959	\N	17	4	f	\N	15
111	Definição de abordagem: login por filial, captura por foto com IA para classificação/validação, lote de reembolso e pré-preenchimento		concluida	2025-09-03	2025-09-03 13:50:06.403011	\N	17	4	f	\N	20
114	Desenvolvimento do MVP		concluida	\N	2025-09-03 13:54:13.886943	2025-09-10 19:42:48.572599	17	4	f	\N	24
447	INTEGRACAO COM TEAMS	Estudar a integracao com o teams, para substituir o google meet	concluida	2026-01-14	2026-01-12 18:40:17.837443	2026-01-14 20:16:19.173797	43	\N	f	\N	0
103	Envio das bases (NetSuite/“Netflix” e Microvix) em CSV/XLSX		concluida	2025-09-29	2025-09-02 18:50:46.724576	2025-10-13 17:06:54.287631	16	2	f	\N	9
448	INTEGRACAO COM TEAMS	Estudar a integracao com o teams, para substituir o google meet	concluida	2026-01-14	2026-01-12 18:40:20.363286	2026-01-14 20:16:35.100453	43	\N	f	\N	1
445	LOGIN	https://www.oaz360.com.br/\nadmin@oaz.co\nadmin12345\nMudar@123 -> senha padrao dos outros usuarios\n	pendente	\N	2026-01-12 18:35:10.678267	\N	43	\N	f	\N	0
112	Coleta de insumos para o MVP		concluida	\N	2025-09-03 13:52:59.493317	2025-09-10 19:43:02.614513	17	4	f	\N	40
440	Semana de 12 a 16 de dezembro	Detalhamento das tarefas da semana entre os dias 12 e 16 de dezembro. 	pendente	2026-01-16	2026-01-12 15:38:12.232619	\N	46	2	f	\N	0
341	Cobrar Hudson restante dos dados		concluida	2025-11-14	2025-11-10 21:40:26.954317	2026-01-16 22:22:28.51152	10	10	f	\N	28
446	NORMALIZACAO DA BASE DE FUNCIONARIOS	Normalizar base de funcionarios e padronizar \n	concluida	2026-01-16	2026-01-12 18:36:30.174118	2026-01-16 22:09:05.364269	43	13	f	\N	6
96	Mostrar comunidades, professores e opções logo na entrada.		concluida	2025-09-01	2025-08-29 15:58:57.931628	2025-09-03 15:50:37.76193	11	5	f	\N	38
113	Desenho do fluxo de reembolso		concluida	2025-09-09	2025-09-03 13:53:55.826162	2025-09-09 15:56:01.68122	17	4	f	\N	30
133	Processamento - Tirar fila	Visualização Status de processamento está dobrando, está aparecendo o relatório que já foi processado e mais a que estou processando. Deixar somente a que estiver processando	concluida	2025-09-09	2025-09-09 13:40:47.497993	2025-09-09 13:50:32.339479	3	4	f	\N	33
353	Foco da semana 14/11 - 21/01	Abrir sub tarefas e ações	concluida	2025-11-21	2025-11-17 20:42:50.287304	2026-01-23 20:39:01.360572	13	6	f	\N	1
344	Foco da semana 10/11 - 12/12	Concluir a tarefa "Automação Conciliação de shopping remoto" para que o projeto\npossa ser finalizado e a solução entre em produção.	concluida	2025-11-14	2025-11-10 21:44:30.592771	2026-01-21 20:21:51.849681	14	6	f	\N	11
129	Visualização de notas rejeitadas	Incluir indicador/visualização específica para notas rejeitadas no Dashboard, facilitando monitoramento e análise.	concluida	2025-09-10	2025-09-08 17:29:16.718012	2025-09-09 13:27:41.014039	3	4	f	\N	43
115	Próxima demo/reunião		concluida	2025-10-10	2025-09-03 13:54:30.127861	2025-10-13 20:19:32.882542	17	4	f	\N	44
131	Gestão de Usuários e Acessos	Acesso simultâneo com a mesma senha\nValidar se mais de um usuário poderá acessar simultaneamente com a mesma credencial. Caso não, criar solução para senhas distintas ou outro modelo de autenticação.	concluida	2025-09-09	2025-09-08 17:30:13.875643	2025-09-09 13:33:48.659489	3	4	f	\N	47
380	Foco da semana 01/12 - 05/12 		concluida	2025-12-05	2025-12-01 20:10:34.60412	2025-12-04 20:49:04.311242	43	8	f	\N	5
143	Implementar dualidade de opções para inserção de dados do usuário	A reunião destacou a necessidade de oferecer duas alternativas para os usuários inserirem dados: por meio de gravação livre ou preenchimento de formulário. Esta ação visa aumentar a flexibilidade e a personalização da experiência do usuário. O objetivo mensurável é aumentar a taxa de conclusão dos perfis preenchidos em 40% nos próximos dois sprints. A metodologia envolve brainstorming para definições de interface, sessões de teste A/B para validar eficácia das opções, e ajustes contínuos baseados em feedback. As equipes UX, desenvolvimento, e análise de dados são stakeholders prioritários. Recursos necessários incluem software de análise de comportamento de usuário e tempo dedicado a sessões de feedback. Critérios de sucesso serão definidos pelo aumento na adesão dos usuários às novas funcionalidades e feedback positivo. Não existem dependências críticas imediatamente evidentes, exceto a revisão e aprovação do design pela equipe de produto. Podem surgir obstáculos na integração de backend necessária para suportar duas formas de entrada de dados.	concluida	\N	2025-09-11 13:48:28.182704	2025-09-17 17:07:04.297885	11	\N	f	\N	42
188	Ver com Fabiana os proximos passos do sistema academia impostos	Ver com equipe se esta ok o primeiro processo. Validando ve os proximos passos	concluida	2025-10-15	2025-10-14 19:40:22.594554	2025-10-15 19:38:52.272471	5	4	f	\N	10
324	Foco da semana 08/12 - 19/12	Concluir a tarefa "Formularios David" e iniciar a tarefa "Migrar toda a operaçao da Aeropool para o salesforce", que é a principal pendência para a automação\n\nProcesso David\n\nA data de entrega para os FAA compliant forms esta marcada para o dia 3/11. \n\nA data foi adiada novamente por conta do David. Humberto esta ciente e de acordo - 07/11/25\n\nA data foi adiada novamente por conta do David. Humberto esta ciente e de acordo - 14/11/25\n\nA nova data de entrega é dia 21/11/25\n\nA nova data de entrega é dia 28/11/25\n\nDevido a problemas do salesforce o prazo tera que ser adiado para proxima sexta dia 5.\n\nDavid estava tendo problemas para fazer login no sandbox entao prazo adiado para dia 12/12\n\n\n	concluida	2025-11-14	2025-11-10 21:19:14.215852	2026-01-05 20:09:50.359562	28	7	f	\N	1
381	Foco da semana 01/12 - 19/12		concluida	\N	2025-12-01 20:13:19.617864	2026-01-14 20:23:08.465808	45	8	f	\N	0
442	Corrigir analise do produto	A implementacao da feature onde a ia geraria as descricoes/metatags/informacoes para analisar todas as imagens e gerar uma informacao unificada para o produto e nao por imagem	pendente	2026-01-16	2026-01-12 18:29:50.587038	\N	19	\N	f	\N	3
142	Ajustar a interface inicial do BoraBailar App para melhorar a usabilidade	Durante a reunião, identificou-se que a interface inicial do aplicativo não está intuitiva para os usuários, especialmente no iOS. O objetivo é introduzir melhorias que clarifiquem as ações que o usuário deve realizar, como pressionar um botão para gravar livremente ou preencher um formulário. O projeto visa aumentar a satisfação do usuário, tornando a navegação e as interações mais claras. Mapeia-se a equipe de UI/UX como principal responsável, com colaboração dos desenvolvedores iOS. Recursos incluem feedback de usuários, ferramentas de prototipagem, e tempo de desenvolvimento alocado de 20 horas. Critérios de sucesso incluem testes de usabilidade mostrando um aumento na intuição de uso por 70%. Dependências incluem revisão dos designs pela equipe de design antes do desenvolvimento. O risco principal é a resistência a mudanças por parte de usuários que já se habituaram à interface atual.	concluida	\N	2025-09-11 13:48:28.182699	2025-09-17 17:06:40.532035	11	\N	f	\N	39
401	Atualização	Cruzamento de imagens\n\nCriar a rotina de cruzamento de dados da carteira de produtos com as imagens com o intuito de organizar melhor o banco por categorias de produtos\n\n\n\n\n	concluida	\N	2025-12-08 18:20:20.020149	2026-01-14 20:22:11.604751	19	8	f	\N	0
398	Atualização da forma de armazenamento	A logica de armazenamento utilizava SQLITE\r\n\r\nFoi implementado o uso do postgree (CLOUD)	concluida	\N	2025-12-08 18:17:20.240621	\N	34	8	f	\N	0
451	Encaminhar emails para o Andy		em_andamento	2026-01-30	2026-01-16 22:00:57.110882	\N	27	7	f	\N	0
144	Desenvolver tela intermediária de carregamento com soluções encontradas	Identificada a necessidade de criar uma tela que informe ao usuário sobre soluções personalizadas todas as vezes que uma busca for processada, proporcionando uma experiência melhorada e ancorada no engajamento. Esta tela não apenas melhora a expectativa do usuário, mas também comunica eficazmente o processamento em curso. Objetivo mensurável é reduzir a taxa de abandono nesta fase em 30%. Planeja-se usar ferramentas de animação para tornar a experiência visualmente atraente. Mapeia-se os times de design e frontend como principais responsáveis. Recursos incluem software de prototipagem e sessões de teste. Critérios de sucesso incluem a aceitação do usuário verificada por testes de usabilidade e análise de métricas de engajamento. Dependência crítica é a necessidade de aprovação conceitual pela gerência antes da implementação técnica. Riscos incluem possíveis complicações na sobrecarga do sistema devido à adição de animações.	concluida	\N	2025-09-11 13:48:28.182705	2025-09-17 17:06:11.335347	11	\N	f	\N	46
407	Semana 11 a 12 de dezembro	Primeiros passos do projeto de RPA de cadastro de contrato entre os modulos do VS. 	concluida	2025-12-12	2025-12-11 18:24:08.088187	2026-01-23 20:36:56.694483	51	6	f	\N	2
469	Aguardando Matheus - Esta testando		pendente	2026-01-22	2026-01-21 20:11:29.430694	\N	33	5	f	\N	9
453	Entregar o projeto		em_andamento	2026-01-23	2026-01-16 22:03:46.888978	\N	11	5	f	\N	2
468	Foco da semana 19/01 - 23/01	Finalizar completamente o processo de amortização	concluida	2026-01-23	2026-01-20 14:40:06.153786	2026-01-23 20:30:54.326427	55	6	f	\N	0
412	Terça - Cobrar matheus novas imagens para para teste	Garantir mais imagens com o TI (Matheus)	pendente	2026-01-27	2025-12-15 18:19:49.861887	\N	35	5	f	\N	0
402	Incrementar a função de SEO/descrição do produto	Reuniao de alinhamento	concluida	2025-12-09	2025-12-08 18:22:15.448811	2025-12-08 20:11:06.757594	19	\N	f	\N	1
410	Reuniao alinhamento de features 	Reunião 14:00 - Matheus Parra e Ronald. Alinhamento de funcoes para visualizacao de produto dentro do banco de imagem	concluida	2025-12-16	2025-12-15 18:17:36.464611	2026-01-12 18:21:40.488376	19	\N	f	\N	7
396	TREINAMENTO FINOPS	\n\nTreinamento:\n\nhttps://teams.microsoft.com/l/meetup-join/19%3ameeting_OTM3YmI0ZTEtMmQzYy00Njk4LWI1NGEtYzRlODU2ZTQ3OGNj%40thread.v2/0?context=%7b%22Tid%22%3a%22ef423586-492b-4ee4-9390-8a3dabeaf073%22%2c%22Oid%22%3a%229e2e7787-5969-4e5d-9fda-83991a6ce41e%22%7d	concluida	2025-12-09	2025-12-08 18:13:55.028843	2025-12-09 20:10:44.603941	16	\N	f	\N	2
408	Foco da semana 11/12 - 19/12		concluida	2025-12-12	2025-12-11 20:16:20.548071	2026-01-21 20:12:37.549839	50	10	f	\N	0
413	LOGIN	https://oaz-consultor.replit.app\r\n\r\nadmin@oaz.com\r\nsenha : Omega@536\r\n	pendente	\N	2025-12-15 18:21:50.069302	\N	33	\N	f	\N	0
414	[EMAIL]  RESEND -	CRIAR CONTA NA PLATAFORMA E ENVIAR ACESSO.	concluida	2025-12-16	2025-12-15 18:25:05.954448	2026-01-14 20:16:56.75911	43	13	f	\N	3
405	Foco da semana 08/12 - 19/12	Processando manuais	concluida	2025-12-12	2025-12-09 20:04:41.888388	2026-01-16 22:01:36.422494	49	10	f	\N	1
450	Migrar projeto	Migrar projeto do Replit para VM do google/Antigravity	concluida	2026-01-16	2026-01-14 20:25:30.228522	2026-01-16 22:16:18.782003	34	8	f	\N	6
403	Foco da semana 08/11 - 19/12	Andreu abrir demanda	concluida	2025-12-12	2025-12-08 20:16:43.330526	2026-01-23 20:23:45.389712	47	10	f	\N	4
470	Implementar modificações proposta pelo Leonardo no dashboard		concluida	2026-01-23	2026-01-21 20:13:36.313957	2026-01-23 20:23:08.53987	53	10	f	\N	31
386	Todos os funcionários regularizados emitindo NF	Payjota \r\n	pendente	2026-06-01	2025-12-02 18:02:38.322671	\N	40	12	f	\N	0
404	Foco da semana 08/12 - 19/12	Marcar reunião com Bento/Matheus	concluida	2025-12-12	2025-12-08 20:18:19.305641	2026-01-16 22:14:14.447766	18	10	f	\N	71
388	Foco da semana 01/12 - 05/12		concluida	2025-12-05	2025-12-03 19:20:10.16561	2025-12-03 20:16:37.294967	40	4	f	\N	2
393	8 a 12 de dezembro		concluida	2025-12-12	2025-12-07 22:47:13.115728	2025-12-16 14:49:29.201873	46	2	f	\N	0
452	Destravar o pdf de 5 mil paginas		concluida	2026-01-23	2026-01-16 22:01:55.973654	2026-01-26 19:47:24.462437	49	10	f	\N	73
176	Criação da estrutura do processo de faturamento de academia		concluida	2025-10-17	2025-10-14 16:50:25.627321	2025-10-15 21:24:15.826036	4	8	f	\N	5
399	Atualização da forma de armazenamento	A logica de armazenamento utilizava SQLITE\r\n\r\nFoi implementado o uso do postgree (CLOUD)	concluida	\N	2025-12-08 18:17:22.040952	\N	34	8	f	\N	1
392	Foco da semana 01/12 - 05/12		em_andamento	\N	2025-12-04 20:39:23.576853	\N	40	4	f	\N	2
384	LOGIN	https://oaz-felipe120.replit.app/\r\n\r\nlogin : admin \r\nsenha admin123	pendente	\N	2025-12-02 09:31:08.117026	\N	20	\N	f	\N	2
394	Documentação 	Documentação\n\nEnvio dos contratos de locação  SOUQ BH - 08/12\n\n\n\n	pendente	2025-12-23	2025-12-08 18:07:04.240466	\N	33	13	f	\N	3
173	Automação Conciliação de shopping remoto	Criação e configuração completa do servidor web de inicialização do robô de conciliação de shopping	concluida	2025-11-07	2025-10-14 16:47:16.243014	2025-11-10 21:44:12.330295	14	6	f	\N	4
189	Melhorias da semana - Sistema Gestão Inovai.Lab	31/10 - todas as tarefas feitas. 	em_andamento	2025-10-31	2025-10-14 19:45:04.016853	\N	29	5	f	\N	12
172	Adição e Análise de campos de dados		concluida	\N	2025-10-13 22:40:31.601398	2025-10-23 14:55:51.884435	25	8	f	\N	2
157	3 — Tela/intersticial de carregamento antes de mostrar as opções	Objetivo: comunicar personalização e evitar sensação de resultado “padrão”.\n\nPorquê: “na última tela… Fazer uma tela de carregamento… ‘Encontramos soluções pra você, veja quais são’”.\n\nEntregáveis:\n\nIntersticial com texto “Estamos preparando sugestões pra você…” e depois “Encontramos soluções pra você — veja quais são”.\n\nSkeletons das cartas/opções enquanto processa.\n\nCritérios de aceite:\n\nIntersticial aparece entre submissão e resultados, com transição suave.\n\nSome automaticamente quando os resultados chegam (sem travar).\n\nTempo mínimo de exibição (p. ex. 600–900 ms) para evitar “flash”	concluida	2025-09-11	2025-09-11 14:05:15.323471	2025-09-17 17:02:54.351295	11	5	f	\N	45
181	Aprimorar sistema de reconciliaçao bancaria 17/11-21/11	O sistema hoje consolida os extratos das empresas Aeropool, Avsales e mais recentemente consolida os extratos do Braga tambem.	concluida	\N	2025-10-14 18:20:32.871917	2025-11-28 18:49:56.707559	26	7	f	\N	0
160	Envio de fatura do Bradesco Dental (com coligadas) para teste — confirmado em 10/09/2025. 		concluida	2025-09-10	2025-09-11 17:12:41.679258	\N	22	2	f	\N	63
471	Detalhar tarefas de demanda		concluida	2026-01-23	2026-01-21 20:18:16.327701	2026-01-26 19:53:45.883115	56	10	f	\N	74
187	Ajustar baixa de relatório dos fluxos de caixa do caixainhas - Franquias Bobs e Spoleto	O adm do sistema conseguir baixar os relatórios com os filtros ref as prestações de contas dos caixinhas das franquias Bos e Spoleto	concluida	2025-10-31	2025-10-14 19:38:36.622015	2025-10-28 20:30:26.577643	17	4	f	\N	51
177	Criação de FAA compliant forms	Para que a operação da Aeropool fique como a da Avsales, tive que solicitar a criaçao de formularios da FAA para um funcionario externo, DAVID. 	concluida	\N	2025-10-14 17:24:34.185631	2025-10-20 19:41:50.324253	28	7	f	\N	0
161	Definição do piloto com Bradesco Dental e do confronto fatura × posição atual da folha		concluida	2025-09-10	2025-09-11 17:14:32.047768	\N	22	2	f	\N	64
329	Foco da semana 10/11 - 19/12	O foco principal deve ser a liberação de acesso às câmeras na loja piloto, pois esta é a premissa fundamental e a primeira tarefa pendente. Sem o acesso, as demais tarefas de desenvolvimento e teste não podem ser iniciadas. Deve-se garantir a autorização formal e o suporte técnico da equipe de TI local.\n\n- 11/11 = ainda nao peguei acesso .\n\n- 13/11 = Começei a fazer alguns testes para o desenvolvimento. consegui colocar um rastro mas nao esta tao bom. vou melhorar!\n\n- 01/12 = usarei uma nova abortagem, vou implementar o sam2. \n\n✅ Estatisticas salvas em: contagem_stats_20251203_165232.txt\n📊 Total de Entradas (clientes): 0\n👥 Clientes Unicos: 0\n👥 Media de clientes no ambiente: 0.51\n👥 Maximo de clientes simultaneos: 5\n🛍 Arara A: interacoes=79 | clientes unicos=79\n🛍 Arara B: interacoes=402 | clientes unicos=402\n🛍 Arara C: interacoes=338 | clientes unicos=338\n🛍 Arara D: interacoes=416 | clientes unicos=416\n	concluida	2025-11-14	2025-11-10 21:24:08.724528	2026-01-16 22:05:36.429813	35	5	f	\N	0
180	Aprimorar o FGQuotes 15/12 - 19/12	Irei pedir ajuda para o Andrey e Ronald para implementar os ajuste que ja mapiei do projeto	concluida	\N	2025-10-14 18:10:32.951757	2025-12-19 20:36:58.073672	27	7	f	\N	0
179	Migrar toda a operaçao da Avsales para o salesforce		concluida	\N	2025-10-14 18:06:57.61109	\N	23	7	f	\N	0
171	O processo necessario para a criaçao de uma quote	Here is a step-by-step guide for the full process from Quote to Invoice in AvSight using the internal process described in the uploaded document. I’ve broken it down clearly with indications of which person typically handles each part (Humberto or Lisette), and what is done in AvSight.\n________________________________________\n🔹 STEP 1: Customer Quote (Handled by Humberto)\n1.\tReceive RFQ (quote request) via email: humberto@avsalescorp.com.\n\n2.\tSearch Part Number in Inventory (Pentagon system):\n\n○\tPress W to check warehouse.\n\n○\tPress H to check price history.\n\n○\tIf outdated (>6–12 months), verify prices on ILS and confirm with Humberto.\n\n3.\tCreate Quote in AvSight:\n\n○\tNew Quote.\n\n○\tAdd customer, contact, and account terms.\n\n○\tIf it's a new customer:\n■\tAccount name and click auto assign\n■\tAdd customer billing address (found in the RFQ email)\ni.\tthen\n■\tTerms: ACH (USA), Wire Transfer (International), credit card\n■\tReference: RFQ Number (or just “email RFQ”).\n\n4.\tAdd Line Item:\n\n○\tChoose “Outright”, “Broker”.\n\n○\tEnter part number, quantity, and condition.\n\n○\tWarranty: 1 year if OH.\n\n○\tCondition from Pentagon (H): 145 tag, dual 8130 (if OH/RP/BC).\n\n○\tPrice is firm for 30 days.\ni.\tIf more than one item is being quoted you will need to add a new line in the QU!\nii.\tNew, repeat the steps\n\n5.\tGenerate Quote.\n\n6.\tSend Quote via email (CC Humberto).\n\n7.\tMark status as complete.\n\n8.\tErase processed email.\n\n________________________________________\n🔹 STEP 2: Vendor Purchase Order (PO) (Handled by Lisette)\n1.\tGo to the Purchase Order section in AvSight.\n2.\tClick New:\n\n○\tVendor: Aeropool Services.\n○\tTERMS ACH\n\n○\tPO Type: SPEC.\n\n○\tShip to: Avsales.\n○\tShip method, ups ground\n○\tShip terms FOB\n\n3.\tAdd Line:\n\n○\tPart number: Same as customer quote.\n\n○\tWarehouse: Avsales.\n\n○\tBusiness Category: Broker.\n\n○\tOwner Code: SPEC.\n\n○\tPurchase Type: Outright.\n\n○\t(Don’t add price for Aeropool.)\n○\tCheck \tPO DOCUMENT\n\n4.\tSave PO to get the PO Number.\n\n5.\tMark it as Sent to Vendor.\n\n________________________________________\n🔹 STEP 3: Convert Quote to Sales Order (SO) (Handled by Lisette)\n1.\tOnce Customer PO is received, go back to Customer Quote.\n\n2.\tConvert Quote to Sales Order.\n\n3.\tEnter Customer PO Number (Located in the received customer PO).\n○\tNow write down the Sales Order\n○\tAdd line for credit card\n\n4.\tIn SO, go to Operations for all next steps:\n○\tWrite down SO line located in SO (SOL-)\n\n○\tGo to Allocate tab:\n\n■\tStock from PO\n\n\n \n\n\n\nSTEP 4: Receive Inventory (Handled by Lisette)\n1.\tGo to Operations > Receiving.\n\n2.\tSearch by PO Number.\n\n3.\tSelect the line and press Receive:\n\n○\tEnsure Location = S/R.\n○\tTech data (to enter the trace)\n\n\n○\tIf issue with SN or inventory, check if unit is registered.\n○\tPart is received, go back to vendor PO and check all steps into complete.\n○\tFind purchase order line in the vendor purchase order all related\n\n________________________________________\n\n STEP 5: Release & Invoice Issues (Needs Attention) \n\n○\tGenerate Release (in SO):  (if account terms problem edit SO)\n○\tGENERATE release\n○\tIn releases find the release number and the release line (RLS-)\n○\tWhen more than one line - Combine releases\n○\tHead to OPERATIONS section and find the RLS (should already be there or else search)\n■\tClick on the release (currently in picking)\n■\tMass pick\n■\tNow its outbound QC (click again in RLS) (can print COFC)\n■\tPre verify\n■\tNow its shipping, select the RLS\n■\tSelect release\n■\tShip, (release shipped)\n■\tGo back to Sales order (status changed to invoice)\n\n○\tIn SO All Related:\n\n\n■\tGo to Invoice (right down invoice)\n■\tYou can now generate the preview invoice on ILID line\n________________________________________\n🔹 STEP 5: Release & Invoice Issues (Needs Attention)\n1.\tOn Release:\n\n○\tAccount Terms: ACH.\n\n○\tRelease Line often incomplete or blank — must be reviewed.\n\n2.\tAfter Release is created:\n\n○\tGo back to Operations > Invoicing.\n\n○\tGenerate Commercial Invoice from the Release.\n\n○\tAdd Part Number, Quantity, Trace, and Price manually if missing.\n\n________________________________________\n🔹 Final Notes / Tips\n●\tProforma Invoice: Use when a customer pays in advance or lacks terms.\n\n●\tDocuments Summary:\n\n○\tVendor PO: Part Number, Description, Price (if external vendor).\n\n○\tSales Order: Customer PO, Part No., Condition, Trace, Price.\n\n○\tInvoice: Ensure all values and traceability are complete.\n\n	concluida	2025-06-05	2025-10-13 18:49:39.095469	2025-10-14 18:07:06.576457	23	7	f	\N	0
415	[EMAIL]  RESEND		concluida	\N	2025-12-15 18:26:07.192706	2026-01-16 22:12:36.805213	16	13	f	\N	14
162	Inclusão do Vitor no grupo de automação / hand-off para tocar o projeto		concluida	2025-09-10	2025-09-11 17:14:52.650198	\N	22	2	f	\N	65
155	1 — Reformular a 1ª tela para ficar intuitiva no iOS (onboarding)	Objetivo: tornar óbvio como o usuário começa.\n\nPorquê: “na fase inicial ali na primeira tela… a interface não está intuitiva… que ele tem que gravar pressionar e grave livremente”.\n\nEntregáveis:\n\nLayout com título (“Como você quer começar?”) e descrição curta.\n\nBotão de gravar permanece (como está hoje).\n\nDois CTAs abaixo: (A) “Aperte o botão e grave livremente” e (B) “Preencha o formulário”.\n\nCritérios de aceite:\n\nEm iOS, o caminho para gravação está visível acima da dobra e compreensível sem tutorial.\n\nVoiceOver/ações de acessibilidade descrevem os CTAs corretamente.\n\nPermissões de microfone pedidas no momento certo, sem bloquear a UI.	concluida	2025-09-11	2025-09-11 14:03:48.026297	2025-09-11 17:22:10.16405	11	5	f	\N	44
175	Ler todas as abas de planilhas de filiais		concluida	2025-10-24	2025-10-14 16:49:31.016485	2025-10-27 20:11:05.584175	3	4	f	\N	57
158	Envio de planilhas-base do RM (Empregados), incluindo desligados dos últimos meses		concluida	2025-09-10	2025-09-11 17:12:03.415517	\N	22	2	f	\N	61
159	Envio das planilhas de Particularidades (pessoas fora do RM, PJs e dependentes com grau de parentesco)		concluida	2025-09-10	2025-09-11 17:12:20.623609	\N	22	2	f	\N	62
247	Formalizar acordo comercial		concluida	2025-11-14	2025-10-20 19:55:23.255299	2025-11-17 20:46:43.827449	24	4	f	\N	1
36	Protótipo inicial da interface e base de upload disponível e testada pelo Leonardo (layout elogiado; comparação com Excel pesado)		concluida	2025-08-21	2025-08-26 16:58:10.299007	\N	6	2	f	\N	9
252	Ajuste no faturamento de academia		concluida	2025-10-31	2025-10-23 20:45:40.274719	2025-10-29 20:21:42.842757	4	5	f	\N	4
251	Configurar o usuário rpa pra rodar como console offline		concluida	2025-10-31	2025-10-23 20:45:10.5748	2025-10-29 20:20:13.331627	14	6	f	\N	6
273	Buscar CNPJ e Razão social pela api de pessoas e linkar com a api de movements		concluida	2025-10-27	2025-10-27 19:55:56.505757	2025-10-27 20:12:33.955149	1	6	f	\N	7
248	Squad 2 - Automação mercado livre	Adicionar segunda automação desejada pelo cliente que envolve uma nova planilha do Mercado Livre.	concluida	2025-10-21	2025-10-20 19:59:51.659294	2025-10-27 20:24:53.106127	24	8	f	\N	2
418	Testes - Cobrar feedback do cliente	Apresentar o timesheet, criador de reunião.	pendente	2026-01-23	2025-12-15 18:32:16.19511	\N	45	8	f	\N	1
250	reuniao com o david sexta dia 3		concluida	2025-11-03	2025-10-21 20:11:29.644992	2025-11-03 19:02:36.298879	28	7	f	\N	0
246	Ajusta para puxar os dados de venda para a aba de Vendas		concluida	2025-10-27	2025-10-20 19:44:44.901452	2025-10-27 20:11:42.989358	5	4	f	\N	22
454	Liberar sistema para uso - Entrega final do projeto		concluida	2026-01-23	2026-01-16 22:09:50.792159	2026-01-23 20:22:02.809763	43	8	f	\N	7
280	Desenhar prioridades de desenvolvimento - EduChat	Land page - em construção\nhttps://edu-chat-felipe120.replit.app	concluida	2025-11-14	2025-10-27 21:26:32.057057	2026-01-16 22:32:26.625984	38	10	f	\N	25
238	Criar a parte de conciliação de acordo com o Arquivo retorno. 	Inlcuir a funcionalidade de conciliação bancária de acordo com os arquivos retornos enviados pelo Lucas. 	concluida	2025-10-24	2025-10-15 14:57:13.285567	2025-10-27 20:19:20.096236	16	8	f	\N	3
417	LOGIN	360: https://oaz-evaluation-system.replit.app\r\nlogin: admin@oaz.com\r\nsenha: Oaz@123	pendente	\N	2025-12-15 18:31:26.699743	\N	45	\N	f	\N	0
244	Cobrar fechamento do contrato	Ainda não gerou o contrato com o cliente	concluida	2025-11-14	2025-10-15 19:48:59.57415	2025-11-18 20:05:58.390243	25	4	f	\N	3
274	Acesso à nova base do RM		concluida	2025-10-27	2025-10-27 19:56:15.950896	2025-10-27 20:12:44.960009	1	6	f	\N	9
317	Sistema de admin e tela do cliente de seleção de produtos		concluida	2025-11-07	2025-11-05 19:54:16.746234	2025-11-10 21:51:07.248438	39	8	f	\N	0
339	Foco da semana 10/11 - 12/12	Focar na obtenção do acesso à API do RM e no mapeamento detalhado dos\nendpoints (Provisionar acesso à API do RM e Mapeamento detalhado de endpoints), pois são os pré-requisitos imediatos para iniciar o desenvolvimento do modelo analítico e do ETL.	concluida	2025-11-14	2025-11-10 21:37:51.0226	2026-01-21 20:20:07.805088	9	6	f	\N	12
260	Unificar projetos de conciliação (seu sistema atual e o do Lucas Cavenco) em uma plataforma única.	lucas tinha começado um, mas depois que mostrei o meu, ele disse que estava melhor e que preferiria o meu, pediu para adicionar outras funcionaldiades, mas que o meu sistema tava bom para eles também.	concluida	2025-11-05	2025-10-26 20:10:25.539045	2025-11-05 20:19:41.507164	16	8	f	\N	4
237	FRONT DO SISTEMA FISCAL - SÁ CAVALCANTE	O dani me passou uma missao de mudar algumas coisas basica no sistema de evoluçao fiscal 	concluida	2025-10-15	2025-10-15 14:35:09.032822	2025-10-15 19:41:14.679071	1	5	f	\N	26
245	Alteraçao de FAA forms	esperando a lisette evidenciar erros nos formularios para correçao.	concluida	2025-10-31	2025-10-16 17:15:08.782534	2025-12-01 16:36:48.518928	28	7	f	\N	0
310	Organizar compra das cadeiras 	Compra de cadeiras para o time - Comprar 8 cadeiras para o time da Imovai. 	concluida	2025-11-14	2025-11-03 16:46:25.359129	2025-12-10 20:30:16.572273	40	4	f	\N	3
387	Foco da semana 01/12 - 19/12	Ajustar erro em produção	concluida	2025-12-05	2025-12-02 20:20:16.629372	2026-01-23 20:08:19.720879	25	8	f	\N	5
30	Apresentação do MVP da aplicação		concluida	2025-08-04	2025-08-26 16:26:43.279164	\N	5	2	f	\N	35
31	Follow-up de testes & novos requisitos		concluida	2025-08-14	2025-08-26 16:27:00.478077	\N	5	2	f	\N	41
309	Faturamento Inovai		concluida	2025-11-07	2025-11-03 16:45:07.315442	2025-11-03 20:47:33.963698	40	4	f	\N	0
349	Foco da semana 10/11 - 19/12	Aguardando feedback proximos passos	concluida	2025-11-28	2025-11-10 21:51:27.460762	2026-01-16 22:29:59.04373	39	8	f	\N	1
240	Mapeamento do processo de evolução fiscal		concluida	2025-10-15	2025-10-15 17:26:11.336011	2025-10-15 19:41:48.825293	1	6	f	\N	14
421	Semana 15 a 19 de dezembro		concluida	2025-12-19	2025-12-16 14:50:05.584941	2025-12-22 14:06:14.987946	46	2	f	\N	0
335	Foco da semana 10/11 - 05/12	Priorizar a conclusão da tarefa "Confirmar envio do formulário aos colaboradores\naté o dia /" e, imediatamente após, iniciar a análise das respostas para mapear\no nível de conhecimento em IA.\n\n	concluida	2025-11-14	2025-11-10 21:31:19.606245	2025-12-02 20:29:18.835989	34	8	f	\N	3
255	Refinar o sistema RAG para que a IA traga análises textuais e visuais (gráficos/tabelas) sobre desempenho das campanhas.		concluida	2025-11-05	2025-10-26 20:08:53.073971	2025-11-12 20:15:59.955186	18	10	f	\N	2
32	Seleção de filial/CNPJ no upload e carga inicial da lista enviada.		concluida	2025-08-15	2025-08-26 16:33:42.835769	\N	5	2	f	\N	45
33	Correção do erro no botão “deletar tudo” (limpeza segura e logs).		concluida	2025-08-18	2025-08-26 16:34:01.550131	\N	5	2	f	\N	48
34	Upload de cancelamentos (EVO) e reconciliação com base processada.		concluida	2025-08-20	2025-08-26 16:34:22.246647	\N	5	2	f	\N	53
119	Coleta/liberação de acessos às plataformas (por Fabiana).		concluida	\N	2025-09-04 14:51:32.128685	2025-10-20 17:00:49.672448	18	2	f	\N	65
416	Troca com o Bento sobre o projeto		concluida	2025-12-18	2025-12-15 18:27:30.101118	2026-01-16 22:14:12.698502	18	\N	f	\N	70
289	Melhorias no sistema de evolução fiscal		concluida	2025-10-31	2025-10-28 21:42:42.776306	2025-10-29 20:22:15.196159	1	6	f	\N	5
458	CObrar feedback de uso com o cliente		concluida	2026-01-23	2026-01-16 22:14:40.154632	2026-01-21 20:16:08.912777	18	10	f	\N	72
327	Foco da semana 10/11 - 14/11	O projeto está com todas as tarefas concluídas. O foco deve ser na validação dos\nprocessos mapeados e na definição dos próximos passos para a Avsales,\npossivelmente criando um novo projeto para a implementação das melhorias\nidentificadas.	concluida	2025-11-14	2025-11-10 21:21:45.634575	2025-11-12 20:25:27.568347	23	7	f	\N	3
290	Emitir NF ja autorizado		concluida	2025-10-30	2025-10-30 14:41:13.247478	2025-11-03 20:57:53.136078	24	4	f	\N	0
330	Foco da semana 10/11 - 14/11	re detalhar o projeto completo com as novas orientações e definiçòes do projeto.	concluida	2025-11-14	2025-11-10 21:25:31.494057	2025-11-17 20:27:26.654941	19	2	f	\N	6
284	Terminar de preencher os proximos campos - RPA		concluida	2025-11-07	2025-10-28 20:44:03.36583	2025-11-07 20:00:35.669026	25	8	f	\N	4
288	Colocar a conciliação de construtora no ar no DNS novo		concluida	2025-10-28	2025-10-28 21:42:14.280009	2025-10-29 20:22:01.563422	14	6	f	\N	8
292	Estruturar com Hermom plano no Solar de final do ano	07/11 - Inovai - (Reativar os 20 alunos do 1° ano) - Feito Ok\n14/11 - Provas - (Estruturar para receber 2° e 3° ano) - Feito Ok\n21/11 - Inovai - (Ativar o 2° ano - média 35 alunos) - Feito - Ok\n28/11 - Inovai - (Ativar o 3 ano - média 25 alunos) - Provas finais recuperação	concluida	2025-11-14	2025-10-30 14:44:08.996783	2026-01-16 22:32:29.127413	38	4	f	\N	4
235	Desenvolvimento da Função de Desenho Técnico Automático	Thaís enviará para Felipe:\n\nExemplos de imagens de peças e dos desenhos técnicos resultantes.\n\nO prompt usado atualmente no ChatGPT ou outras ferramentas para gerar os desenhos.\n\nUm breve documento explicativo descrevendo o processo atual (“da foto ao vetor”).\n\nFelipe vai estudar:\n\nModelos de IA que gerem desenhos vetorizados a partir de fotos ou esboços.\n\nA melhor forma de integrar essa funcionalidade ao sistema, possivelmente automatizando a criação de desenhos técnicos no mesmo fluxo do upload da ficha técnica.	concluida	2025-11-14	2025-10-15 13:53:26.584639	2025-11-10 21:27:14.145503	20	5	f	\N	0
315	Melhor processamento sistema contabil academia	Andrey vai ajudar a tirar o tempo de processamento da planilha de vendas	concluida	2025-11-05	2025-11-05 17:50:56.115023	2025-11-05 20:15:38.142087	5	4	f	\N	6
457	Atualizar sistema para pegar as faturas do XML e associar os clientes		concluida	\N	2026-01-16 22:13:17.458183	2026-01-27 20:19:59.427914	16	\N	f	\N	15
316	Colocar para gerar relatório para admin das filiais Bobs e Spoleto		concluida	2025-11-05	2025-11-05 17:51:56.44122	2025-11-07 20:06:58.591186	17	4	f	\N	52
139	Coleta das fichas técnicas para o piloto (diversas categorias: tecido plano, malha etc.). Resp.: Amanda/Thaís/Bruna.		concluida	2025-09-30	2025-09-09 22:32:12.955206	2025-10-13 17:12:43.769305	20	2	f	\N	5
286	Preenchimento documento secretaria do ES		concluida	2025-10-31	2025-10-28 20:47:09.695202	2025-10-29 20:27:28.688194	38	2	f	\N	0
456	Entregar o projeto por completo		pendente	2026-01-16	2026-01-16 22:11:40.17135	\N	20	5	f	\N	4
282	Fazer a leitura do banco de dados	fiz a leitura do db, puxei as colunas de colaboradores mas nao deu para ve das slojas e vendas. \nfalei com o matheus e ele ta esperando o T.i iberar o acesso. 	concluida	2025-11-14	2025-10-28 20:42:09.462799	2025-11-11 15:13:50.635743	33	5	f	\N	0
319	Testar EduChat para ida ao Solar Sexta		concluida	2025-11-07	2025-11-06 17:48:10.824267	2025-11-17 20:23:20.226973	38	4	f	\N	1
345	Foco da semana 10/11 - 28/11	As tarefas pendentes de\n"Desenvolvimento do MVP" e as  tarefas não detalhadas no Kanban devem ser\npriorizadas para garantir a entrega do MVP no prazo, conforme a restrição de\n"Prazos de fechamento pressionam a entrega do MVP rapidamente". O engajamento\nda equipe de loja (premissa) deve ser monitorado.	concluida	2025-11-14	2025-11-10 21:46:29.720601	2026-01-16 22:26:24.62012	17	4	f	\N	59
140	Padronização/obrigatoriedade da ficha técnica (garantir campos completos). Resp.: Estilo/Produto. Prazo: imediato.		concluida	2025-10-03	2025-09-09 22:32:28.025886	2025-10-13 17:13:12.429472	20	2	f	\N	6
311	Resolver questao do Replit individual	Tirar da questao do replit do gomes comunitario para que cada funcionario tenha seu proprio replit.	em_andamento	2025-11-21	2025-11-03 19:02:03.259228	\N	40	7	f	\N	2
333	Foco da semana 10/11 - 12/12	Priorizar a conclusão da tarefa "Desenho de fluxos de WhatsApp (pré e pósvencimento)" para que a próxima etapa de "Integrar funcionalidades" possa ser\nfinalizada. É crucial alinhar a comunicação proativa antes de avançar na implementação técnica	concluida	2025-11-14	2025-11-10 21:28:48.465938	2025-12-09 20:10:36.728084	16	8	f	\N	0
283	Adicionar aba de cliente		concluida	2025-11-07	2025-10-28 20:42:58.758659	2025-11-04 20:11:30.282564	16	8	f	\N	1
291	Emitir NF		concluida	2025-10-30	2025-10-30 14:42:44.345195	2025-11-03 20:57:27.610657	25	4	f	\N	1
340	Foco da semana 10/11 - 21/11	O foco principal deve ser o desenvolvimento e implementação da funcionalidade de "Upload zipado" para mitigar o risco de travamento do sistema devido ao alto\nvolume de XMLs, conforme a restrição do projeto. Paralelamente, deve-se iniciar o\nmapeamento das chaves/colunas para o "Upload do relatório da empresa" para\ngarantir a correta ingestão dos dados.	concluida	2025-11-14	2025-11-10 21:39:42.399457	2025-11-24 20:28:39.213921	3	4	f	\N	63
336	Foco da semana 10/11 - 18/12	 - link de acesso = https://oaz-rh-ai-new.replit.app \n \n- nome de usuario  = admin , senha;  admin123\n\n\nCobrar a validação dos testes ao setor de RH na OAz\n\nPrioridade MUITO ALTA\n\nFinalizar a funcionalidade dos botões (5)\n\nSem Avançar / Rejeitar / Editar / Ver tabela, o fluxo de seleção não funciona na prática.\n\nIsso trava o dia a dia do RH e das gerentes.\n\nPrimeiro de tudo: sistema tem que fazer o básico bem.\n\nRegras de permissão e visibilidade bem formalizadas (6)\n\nGarante que cada gestor/gerente veja só o que pode (CC/Área) e evita bagunça e risco de compliance.\n\nSe isso estiver errado, dá confusão de gestão, vazamento de info e perda de confiança na ferramenta.\n\n Prioridade ALTA\n\nPadronizar mensagens automáticas (4)\n\nImpacta experiência do candidato e a imagem da empresa.\n\nTambém garante que o time inteiro fale a mesma “língua”.\n\nImportante pra já usar bem o robozinho de WhatsApp e o botão de rejeitar.\n\nDefinição detalhada dos critérios da IA (1)\n\nSem isso, o ranqueamento vira “caixa preta” ou pode ser incoerente.\n\nG&G precisa confiar na IA pra usar de verdade.\n\nVem depois do básico do sistema estar redondo, mas ainda é bem prioritário.\n\n Prioridade MÉDIA\n\nAutomatizar validação de orçamento (3)\n\nMuito bom pra reduzir trabalho manual do G&G e evitar erro humano.\n\nMas dá pra começar com um fluxo mais manual e automatizar depois.\n\nEu colocaria como melhoria de 2ª onda.\n\nEspecificar “análise detalhada” (2)\n\nÉ importante pra dar mais contexto dos candidatos.\n\nMas o sistema já pode funcionar com uma visão mais simples antes.\n\nDá pra evoluir isso como um módulo de refinamento depois que o resto estiver funcionando bem.	concluida	2025-11-14	2025-11-10 21:32:35.034352	2026-01-16 22:16:51.850742	15	5	f	\N	5
460	Marcar reunião com cliente e apresentar o primeiro prototipo		concluida	2026-01-23	2026-01-16 22:18:48.058521	2026-01-21 20:17:57.98052	56	10	f	\N	60
459	Entrega final do projeto		pendente	2026-01-16	2026-01-16 22:17:10.35748	\N	15	5	f	\N	0
348	Foco da semana 10/11 - 19/12	O foco da semana deve ser a Fase  - Observatório, que envolve a configuração do\nconector para o Portal da Reforma Tributária e a implementação da fila diária de\nnotícias/normas para curadoria da Patrícia. Com o MVP concluído, o próximo passo é garantir o fluxo de ingestão de dados externos para evoluir a base de conhecimento do RAG.	em_andamento	2025-11-14	2025-11-10 21:49:04.147725	\N	7	2	f	\N	0
347	Foco da semana 10/11 - 05/12	Concluir imediatamente a tarefa de "Entender o projeto como todo" e criar as\npróximas tarefas de planejamento e arquitetura (ex: Definição da Arquitetura de\nTranscrição e Speaker Diarization).	concluida	2025-11-14	2025-11-10 21:48:15.057502	2026-01-16 22:28:46.447002	36	2	f	\N	12
338	Foco da semana 10/11 - 12/12	Validar todas as telas e os dados do Fiscal junto com o time de Fiscal. Alem disso começar a entender a integração com o Fluig.,\n\n11/11 - Reunião onde mapeamos as pendências e vamos ter reunião na quinta pra bater	concluida	2025-11-14	2025-11-10 21:36:33.514767	2026-01-21 20:19:54.157046	1	6	f	\N	17
44	Reunião de discovery: mapeamento de necessidades; decisão por MVP com RAG; definição de que Fase 1 não consulta internet.		concluida	2025-08-15	2025-08-26 17:11:37.573941	\N	7	2	f	\N	13
45	Fontes priorizadas: Portal da Reforma Tributária, estrutura da lei e perfis técnicos (ex.: membro do comitê Adriano Subirá) como referências confiáveis para fase 2/curadoria.		concluida	2025-08-15	2025-08-26 17:12:01.194626	\N	7	2	f	\N	14
46	Estratégia de ingestão: aceitar PDF/PPT, preferir texto; incluir transcrições de vídeos (ex.: lives no YouTube).		concluida	2025-08-15	2025-08-26 17:12:18.014156	\N	7	2	f	\N	15
47	Envio de materiais iniciais pela Patrícia (leis, links do Portal e perfis confiáveis).		concluida	2025-08-19	2025-08-26 17:12:36.41676	\N	7	2	f	\N	16
48	MVP do TributAI (login/senha + chat RAG) com os documentos já recebidos.		concluida	2025-08-21	2025-08-26 17:12:55.948156	2025-09-01 13:27:23.113572	7	2	f	\N	18
49	Melhora do sistema de RAG para as buscas serem mais profundas e diretas dentro do documento. 		concluida	2025-08-22	2025-08-26 17:13:32.030439	2025-09-01 13:29:49.033663	7	2	f	\N	19
475	Incluir projeto no App In Sigth	a documentação esta em python e o app em react native. \nnao da para fazer o "pip"	em_andamento	2026-01-26	2026-01-23 20:12:03.311809	\N	11	5	f	\N	0
472	Sistema em teste pelo cliente - Acompanhar		em_andamento	2026-01-23	2026-01-22 20:07:20.874224	\N	58	14	f	\N	0
473	Incluir projeto do App in Sigth	frgdfg	concluida	2026-01-26	2026-01-23 20:08:45.837947	2026-01-27 20:31:30.700036	25	8	f	\N	6
480	Acompanhamento de uso		pendente	2026-01-26	2026-01-23 20:22:24.912354	\N	43	8	f	\N	1
477	Coloocar o projeto dentro do GitHub		concluida	2026-01-26	2026-01-23 20:15:25.059847	2026-01-26 17:41:36.594159	58	14	f	\N	0
373	Foco da semana 24/11 - 28/11		concluida	2025-11-28	2025-11-26 20:09:55.016807	2025-12-01 16:38:02.263136	43	8	f	\N	4
136	Reunião de entendimento do processo (Produto/PLM) — 09/09/2025, 14:30–15:33 BRT. Participantes: Amanda, Thaís, Bruna, Adelaide, Felipe.		concluida	2025-09-09	2025-09-09 22:31:12.7248	\N	20	2	f	\N	1
275	Entender o projeto como todo 		concluida	2025-10-31	2025-10-27 20:14:39.273249	2025-11-10 21:47:59.493257	36	2	f	\N	10
50	Decisão do MVP: começar por Caixa Realizado (upload RM + lançador de receitas).		concluida	2025-08-20	2025-08-26 18:52:18.048426	\N	8	2	f	\N	1
266	estar a nova versão do formulário de proficiência em IA, ajustado com feedback de Juliana e Bento.		concluida	2025-10-31	2025-10-26 20:18:31.684123	2025-10-28 20:40:01.934612	34	2	f	\N	4
124	Alinhamento inicial e definição da Fase 1 (renomeação de fotos como MVP).		concluida	2025-09-05	2025-09-05 22:11:17.58801	\N	19	2	f	\N	2
137	Mapeamento de fluxo no PLM e fichas (desenvolvimento, prova, lacre; tecido/combinação de materiais)		concluida	2025-09-09	2025-09-09 22:31:32.083846	\N	20	2	f	\N	2
125	Decisão sobre envio dos insumos (Excel + amostras de fotos + regra de nomenclatura).		concluida	2025-09-05	2025-09-05 22:11:37.261393	\N	19	2	f	\N	4
127	Definição do protótipo do renomeador		concluida	2025-10-01	2025-09-05 22:12:17.698954	2025-10-13 17:11:53.392112	19	2	f	\N	5
138	Definição do escopo inicial (POC): leitura da ficha técnica → pré-cadastro no PLM; evolução para atualizações. 09/09/2025. 		concluida	2025-09-09	2025-09-09 22:31:51.862809	\N	20	2	f	\N	3
141	Construção da 1ª versão do AutoPLM (upload da ficha → extração → pré-cadastro). Resp.: Felipe/inovAI.lab. Prazo: iniciar já, usar as fichas enviadas.		concluida	2025-10-03	2025-09-09 22:32:40.324787	2025-10-13 17:12:26.115114	20	2	f	\N	4
104	Envio de amostras de boletos PDF		concluida	2025-09-04	2025-09-02 18:51:00.145473	2025-09-08 13:44:49.428826	16	2	f	\N	10
105	Protótipo do portal (login + upload + visualização)		concluida	2025-09-30	2025-09-02 18:51:12.533446	2025-10-13 17:07:08.8545	16	2	f	\N	11
106	Normalização da carteira e chaves de correspondência		concluida	2025-10-01	2025-09-02 18:51:32.109461	2025-10-13 17:07:24.895164	16	2	f	\N	12
107	PoC de OCR para leitura de boletos		concluida	2025-10-01	2025-09-02 18:51:45.000373	2025-10-13 17:07:39.206869	16	2	f	\N	13
375	Foco da semana 01/12 - 12/12	Inicio do projeto - definição de tarefas, tarefas executadas até agora para o MVP	concluida	\N	2025-11-27 11:32:57.046352	2026-01-21 20:08:22.74748	44	10	f	\N	5
276	Definir os proximos passos		concluida	2025-10-31	2025-10-27 20:18:46.665708	2025-10-29 21:29:56.274382	11	2	f	\N	51
476	Colocar o projeto no Github o projeto do EduChat		concluida	2026-01-26	2026-01-23 20:14:19.460724	2026-01-26 17:41:39.169256	38	14	f	\N	1
374	Foco da semana 24/11 - 28/11		concluida	2025-11-28	2025-11-26 20:11:08.227949	2025-12-01 20:12:52.982405	18	10	f	\N	16
425	Ajustes estruturais 		concluida	\N	2025-12-23 21:08:17.992	2026-01-14 20:19:11.541638	19	\N	f	\N	0
346	Foco da semana 10/11 - 12/12	Concluir a tarefa "Melhorias da semana - Sistema Gestão Inovai.Lab" para liberar o\nprojeto.	concluida	2025-11-14	2025-11-10 21:47:24.093988	2026-01-16 22:27:40.442692	6	10	f	\N	55
397	Atualização da forma de armazenamento	A logica de armazenamento utilizava SQLITE\r\n\r\nFoi implementado o uso do postgree (CLOUD)	concluida	\N	2025-12-08 18:17:18.369325	\N	34	8	f	\N	2
419	Troca com a Helo	Puxar a Heloisa do RH, para analisar se o projeto ta atendendo a demanda e se ha necessidade de novas features 	concluida	\N	2025-12-15 18:34:10.127513	2025-12-23 21:22:46.124359	34	\N	f	\N	5
427	V2 - DO 360 COM NOVAS FUNCIONALIDADES	1:1\n	concluida	2026-01-14	2025-12-23 21:13:46.128721	2026-01-14 20:16:48.346233	43	\N	f	\N	2
436	Semana de 5 a 10 de dezembro	Detalhamento das tarefas da semana entre os dias 5 e 10 de dezembro. 	concluida	2026-12-10	2026-01-05 17:05:36.703245	2026-01-12 15:39:55.17016	46	2	f	\N	0
433	Tarefa Atualizada via POST API	Teste de update via POST com ID	concluida	\N	2025-12-30 16:36:26.057945	2026-01-16 22:26:27.627024	17	\N	f	\N	62
431	BRAINSTORM - WITH BENTO		pendente	\N	2025-12-23 21:27:19.121659	\N	52	\N	f	\N	7
76	Consertar fluxo de login e remover indicador de “processamento” visível na demo; conexão direta ao banco na versão de pitch.		concluida	2025-08-27	2025-08-26 19:24:26.138595	2025-08-27 18:17:10.426864	11	5	f	\N	30
434	Tarefa Atualizada via POST API	Teste de update via POST com ID	concluida	\N	2025-12-30 16:40:09.32072	2026-01-16 22:26:29.214037	17	\N	f	\N	67
423	Foco da semana 22 a 26 de dezembro		concluida	2025-12-26	2025-12-22 14:08:26.179016	2026-01-05 17:02:09.63346	46	2	f	\N	0
430	Envio de acesso para Matheus	https://oaz-rh-ai-new.replit.app/\nlogin: admin\nsenha: admin123\n	concluida	\N	2025-12-23 21:23:32.933907	2026-01-16 22:16:20.329047	34	8	f	\N	7
97	Diminuir fricção no onboarding do usuário.		concluida	2025-08-29	2025-08-29 15:59:21.710446	2025-09-08 17:33:32.660287	11	5	f	\N	34
77	Home de match unificando pessoas/lugares/professores/eventos com curadoria.		concluida	\N	2025-08-26 19:24:43.769803	2025-09-08 17:33:43.724492	11	5	f	\N	36
5	Validação v2 de layout (feedback positivo de usabilidade) e diagnóstico de duplicidades entre filiais.		concluida	2025-08-22	2025-08-26 14:40:55.737061	\N	1	2	f	\N	41
432	Aguardando o uso para desenvolver novas implementações se necessarias		concluida	\N	2025-12-29 18:25:12.068847	2026-01-16 22:16:50.124175	15	\N	f	\N	3
170	Verificar e Corrigir os bugs do sistema	O sylvio relatou alguns bugs no sistema. estou corrigindo isso	concluida	2025-10-13	2025-10-13 17:29:00.708635	2025-10-14 19:39:23.875088	11	5	f	\N	47
382	LOGIN	https://oaz-rh-ai-new.replit.app\nlogin: admin\nsenha: admin123	concluida	\N	2025-12-02 09:29:13.523282	2026-01-16 22:16:50.914394	15	\N	f	\N	4
243	Marcar encontro com Alain para bate app	mandei a mensagem no grupo. \neles vao fazer uma call antes para mostrar o que o design fez, vai acontecer hoje. depois vai rolar uma outra para apresentar para o alain. assim  poder fazer essa imersão. \n \n20/10 - mandei no grupo novamente, a bola ta com eles. \n\n	concluida	2025-10-23	2025-10-15 19:45:50.635144	2025-10-23 20:49:37.225792	11	5	f	\N	48
463	Cobrar o Léo o testes do sistema		concluida	2026-01-23	2026-01-16 22:27:59.582154	2026-01-26 19:54:03.873326	6	10	f	\N	75
318	Combrar front do Thomaz	Amanha (07/11) vamos marcar um papo com geral pra poder ve o que foi feito do novo sistema web do bora bailar. \n\nreuniao feita. 07/11	concluida	2025-11-07	2025-11-05 20:17:45.501862	2025-11-11 15:12:52.042135	11	5	f	\N	49
462	Cobrar cliente o uso		em_andamento	2026-01-23	2026-01-16 22:26:47.713604	\N	17	10	f	\N	1
281	Colocar o sistema evolução fiscal no ar fora do replit 		concluida	2025-10-28	2025-10-28 16:37:16.041588	2025-10-28 20:32:59.327962	1	6	f	\N	10
426	JSON - TOM DE VOZ AGENTES		pendente	2026-01-16	2025-12-23 21:11:35.183497	\N	19	13	f	\N	2
464	Cobrar Julia transcrição da reunião		em_andamento	2026-01-23	2026-01-16 22:29:10.011266	\N	36	2	f	\N	0
313	Foco da semana 10/11 - 12/12	Criar todos os casos de exceção do faturamento de academia	concluida	2025-11-07	2025-11-03 20:42:26.731325	2026-01-21 20:20:54.489664	4	6	f	\N	13
241	Consertar a chamada para as coligadas e movimentos certos 	Traduzir toda a página dos detalhes do movimento	concluida	2025-10-15	2025-10-15 19:42:26.502405	2025-10-20 19:42:33.414182	1	6	f	\N	15
242	Puxar corretamente os movimentos por coligadas		concluida	2025-10-15	2025-10-15 19:42:58.842088	2025-10-20 19:42:45.728308	1	6	f	\N	16
435	Tarefa Atualizada via POST API	Teste de update via POST com ID	concluida	\N	2025-12-30 16:42:30.856177	2026-01-16 22:26:30.011794	17	\N	f	\N	68
482	Colocar projeto no app in sigth		concluida	2026-01-26	2026-01-23 20:25:38.223209	2026-01-26 20:12:31.709336	20	5	f	\N	8
481	Colocar projeto no app in sigth		concluida	2026-01-26	2026-01-23 20:25:05.578857	2026-01-27 20:20:01.583255	16	8	f	\N	16
428	Alterações ja foram corrigidas, realizar novos testes		pendente	2025-01-26	2025-12-23 21:16:27.034729	\N	20	13	f	\N	3
429	TESTAR - SUBIR BASE DE CLIENTES 	Definir data com Ronald para testes e alimentar base de clientes	concluida	2025-12-26	2025-12-23 21:19:44.746749	2026-01-28 20:12:07.366722	16	\N	f	\N	17
487	Colocar projeto no app in sigth		em_andamento	2026-01-26	2026-01-23 20:32:35.650448	\N	1	6	f	\N	0
465	Cobrar arquivos de clientes, estoque e produtos		em_andamento	2026-01-23	2026-01-16 22:30:34.896956	\N	39	8	f	\N	0
328	Foco da semana 10/11 - 19/12	Foco total na conclusão da tarefa 'Combrar front do Thomaz' e, imediatamente\napós, iniciar a 'Implementar telas feitas pelo design ( UX)'. O objetivo é eliminar a\ndependência externa e integrar o design final para liberar a V para demonstrações\n(pitch-ready).\n\n- 11/11 reuniao feita, A apresentaçao do design do app foi boa. aguardando proximos passoss \n\n- 12/11  = As mudanças do app foram feitas, o thomaz ta so esperando o "ok " de geral para poder montar o site. \n\n- 17/11 = Reuniao hoje visando terminar a tela de "home " do app \n\n21/11 - Iniciando o desenvolvimento do app. Primeira tela = home.\n\n\n\n	concluida	2025-11-14	2025-11-10 21:22:28.963713	2025-12-15 20:15:23.571429	11	5	f	\N	50
314	cobrar Silvio próximos passos	BOla com Renan agora	concluida	2025-11-04	2025-11-03 20:54:51.021376	2025-11-05 20:16:53.164719	11	2	f	\N	52
169	Implementar telas feitas pelo design ( UX) 	As telas estao sendo feitas pelo o Thomaz, o nosso design. \n\n17/12 = ia ter reuniao hoje para  a continuaçao das telas, mas adiaram novamente. \n\n\n	concluida	\N	2025-10-13 17:25:44.168949	2026-01-16 22:03:25.561039	11	5	f	\N	53
484	Tirar projeto do Replit		concluida	2026-01-26	2026-01-23 20:29:14.147952	2026-01-26 20:13:58.398993	34	8	f	\N	8
483	Colocar projeto no app in sigth		concluida	2026-01-26	2026-01-23 20:28:36.897395	2026-01-26 20:13:59.888188	34	8	f	\N	9
466	Trabalhar no novo layout		em_andamento	2026-01-23	2026-01-16 22:33:31.502932	\N	38	14	f	\N	0
486	Colocar projeto no app in sigth		concluida	2026-01-26	2026-01-23 20:31:48.762989	2026-01-26 16:48:58.515994	55	6	f	\N	1
485	Terça - Rodar projeto com Alice		concluida	2026-01-26	2026-01-23 20:31:19.180644	2026-01-27 20:21:41.724716	55	6	f	\N	2
467	Entregar as duas apresentações (institucional e comercial) e a experiencia no escritório		em_andamento	2026-01-23	2026-01-16 22:36:05.810942	\N	57	11	f	\N	0
488	Colocar projeto no app in sigth		em_andamento	2026-01-26	2026-01-23 20:33:06.159177	\N	9	6	f	\N	0
478	Colocar projeto no app in sigth		em_andamento	2026-01-28	2026-01-23 20:19:32.319875	\N	35	5	f	\N	0
491	Colocar projeto no app in sigth		em_andamento	2026-01-26	2026-01-23 20:35:44.746064	\N	4	6	f	\N	0
492	Colocar projeto no app in sigth		em_andamento	2026-01-26	2026-01-23 20:37:07.137918	\N	51	6	f	\N	0
479	Colocar projeto no app in sigth		concluida	2026-01-26	2026-01-23 20:21:29.047056	2026-01-26 20:11:26.236215	33	5	f	\N	2
498	Implementação de features 		concluida	\N	2026-01-26 18:33:42.430235	2026-01-26 20:11:55.998108	43	\N	f	\N	8
489	Colocar projeto no app in sigth		concluida	2026-01-26	2026-01-23 20:33:52.384204	2026-01-27 20:22:14.910209	54	6	f	\N	1
500	REUNIÃO 27/01	Reunião com o time da fluxogama para entender a integração \r\n\r\n27/01 ter. 27 jan. 2026 14:00 - 15:00\r\nhttps://meet.google.com/mkd-vvda-qmr	pendente	\N	2026-01-26 18:36:42.409919	\N	20	\N	f	\N	0
406	LOGISTICA -> TMS	\n\nLOGIN E SENHAS \n\nJamef\n\n SITE    https://jamef.my.site.com/cliente/login\n LOGIN felipe.ferreira@oaz.co\nSENHA Transporte2024*\n\n\nFavorita\t  \nSITE      https://cliente.favorita.com.br/dashboard\t         \nLOGIN        felipe.ferreira@oaz.co\nSENHA\toaz2025\n\n\nCorreios\t     \nSITE  https://rastreamento.correios.com.br/app/index.php\t\nLOGIN 16945787000447\t\nSENHA wbgretail@2019\n\n\nCorreios Empresas\tSITE Correios Empresas\n LOGIN :16945787000447\nSENHA: wbgretail@2019\n\n\nLoggi - Ecommerce\tSITE https://app.loggi.com/envios-nacionais\nLOGIN : emily.souza@oaz.co\nSENHA: 95801089\n\n\n\nTMS - TRANSPORT MANAGENT SISTEM\n\nETL ->\n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\n\n\nJAMEF -> EMAIL \n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\nFAVORITA->\n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\nCORREIOS\n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\nLOGGI ->\n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\n	pendente	\N	2025-12-11 17:13:32.241166	\N	33	13	f	\N	5
420	Foco da semana 16/12 - 19/12	\n\nLOGIN E SENHAS \n\nJamef\n\n SITE    https://jamef.my.site.com/cliente/login\n LOGIN felipe.ferreira@oaz.co\nSENHA Transporte2024*\n\n\nFavorita\t  \nSITE      https://cliente.favorita.com.br/dashboard\t         \nLOGIN        felipe.ferreira@oaz.co\nSENHA\toaz2025\n\n\nCorreios\t     \nSITE  https://rastreamento.correios.com.br/app/index.php\t\nLOGIN 16945787000447\t\nSENHA wbgretail2019\n\n\nCorreios Empresas\tSITE Correios Empresas\n LOGIN :16945787000447\nSENHA: wbgretail2019\n\n\nLoggi - Ecommerce\tSITE https://app.loggi.com/envios-nacionais\nLOGIN : emily.souza@oaz.co\nSENHA: 95801089\n\n\n\nTMS - TRANSPORT MANAGENT SISTEM\n\nETL ->\n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\n\n\nJAMEF -> EMAIL \n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\nFAVORITA->\n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\nCORREIOS\n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\nLOGGI ->\n\nOQUE EU ENTREGO\nQUANTO CUSTOU\nE OCORRENCIAS\n\n	pendente	2025-12-16	2025-12-16 14:00:37.356612	\N	52	5	f	\N	8
37	Reunião de feedback e levantamento detalhado das necessidades (projeção vs. realizado, conciliação, liberações, índices, debêntures)		concluida	2025-08-21	2025-08-26 16:58:28.861747	\N	6	2	f	\N	13
38	Cadastro de Contratos (MVP) com geração automática do fluxo projetado.		concluida	\N	2025-08-26 16:59:00.238381	2025-09-01 13:30:20.21753	6	2	f	\N	18
116	Alinhamentos iniciais com equipe, definição de dores e expectativas.		concluida	2025-09-03	2025-09-04 14:50:29.71377	\N	18	2	f	\N	23
40	Módulo de Índices (tabela e tela de atualização).		concluida	2025-10-08	2025-08-26 16:59:32.027715	2025-10-13 20:22:51.62682	6	2	f	\N	26
117	Reunião de kickoff, priorização da frente de performance (relatórios, alertas, dashboard).		concluida	2025-09-03	2025-09-04 14:50:53.918948	\N	18	2	f	\N	32
461	Cobrar o Hudson restante dos dados e cobrar Augusto novos dados	- Construtora\n- Sá Investimentos	concluida	2026-01-23	2026-01-16 22:22:51.468138	2026-01-23 20:34:34.079993	10	10	f	\N	34
41	Liberações vinculadas ao contrato.		concluida	2025-10-08	2025-08-26 16:59:44.981768	2025-10-13 20:23:08.155849	6	2	f	\N	36
42	Relatórios básicos (por contrato/banco/empreendimento; agenda de vencimentos).		concluida	2025-10-08	2025-08-26 16:59:56.268296	2025-10-13 20:23:34.800742	6	2	f	\N	39
43	Debêntures (primeira versão) com cálculo dedicado.		concluida	2025-10-08	2025-08-26 17:00:06.742515	2025-10-13 20:23:50.769365	6	2	f	\N	42
118	Protótipos já testados: workflows no n8n, portal básico em SupaBase, mock de dashboard.		concluida	2025-09-03	2025-09-04 14:51:09.168744	\N	18	2	f	\N	46
39	Módulo de Pagamentos/Baixas com conciliação projetado x realizado e histórico de ajustes.		concluida	2025-09-04	2025-08-26 16:59:16.104697	2025-09-04 16:05:10.239947	6	2	f	\N	49
120	Definição de KPIs e eventos prioritários para relatórios/alertas.		concluida	\N	2025-09-04 14:51:45.540212	2025-10-20 17:01:01.145871	18	2	f	\N	50
121	Estruturação de ingestão fase 1 (manual via export).		concluida	2025-10-08	2025-09-04 14:52:01.201452	2025-10-13 17:09:03.786981	18	2	f	\N	54
132	Integração e Relatórios	Baixar relatórios da SEFAZ lendo todas as abas de uma vez\nCriar funcionalidade para importar todos os dados das abas de um relatório SEFAZ em um único fluxo, sem precisar abrir aba por aba.	concluida	2025-10-08	2025-09-08 17:30:34.54633	2025-10-13 20:29:36.740125	3	4	f	\N	56
35	Automatizar “base atualizar” e “não mexer” (replicar a lógica da macro para reduzir a necessidade de múltiplos uploads)		concluida	2025-10-10	2025-08-26 16:35:55.198605	2025-10-13 20:16:46.087399	5	2	f	\N	58
122	Início da modelagem de tabelas fato/dimensão.		concluida	2025-10-03	2025-09-04 14:52:14.796908	2025-10-13 17:10:10.231847	18	2	f	\N	61
343	Foco da semana 10/11 - 14/11	O foco principal deve ser a definição e o início da Fase  do projeto, que, conforme o\nescopo, deve abordar a Conciliação Bancária x Contabilidade e a padronização de\nextratos. É crucial realizar um novo mapeamento com a contabilidade para detalhar\nos layouts de extratos bancários e desenhar as telas de validação/visão para a\npróxima etapa.	concluida	2025-11-14	2025-11-10 21:43:37.939598	2025-11-24 20:30:44.227509	5	4	f	\N	64
254	Criar dashboards personalizados com gráficos e tabelas de desempenho (por plataforma e conjunto de anúncios).		concluida	2025-10-31	2025-10-26 20:08:31.058814	2025-11-05 20:18:37.24408	18	2	f	\N	66
490	Bater com Felipe para dar clareza no projeto - Depende disso para falar com o Leonardo		pendente	2026-01-26	2026-01-23 20:35:08.70353	\N	10	10	f	\N	0
494	Colocar projeto no app in sigth		concluida	2026-01-26	2026-01-23 20:38:35.367124	2026-01-26 16:48:45.875993	14	6	f	\N	18
496	Entender com Paulo e cliente o prazo de uso - Entender se vale tirar do Replit		concluida	2026-01-26	2026-01-23 20:41:48.149842	2026-01-26 20:19:06.331648	24	8	f	\N	3
493	Foco 26 - 30 - Abrir demanda		em_andamento	2026-01-26	2026-01-23 20:37:48.08122	\N	51	6	f	\N	1
495	Colocar projeto no app in sigth		concluida	2026-01-26	2026-01-23 20:40:24.746427	2026-01-27 20:23:53.745628	24	8	f	\N	4
497	Colocar projeto no app in sigth		concluida	2026-01-26	2026-01-23 20:42:30.564672	2026-01-28 20:15:21.177115	39	8	f	\N	2
\.


--
-- Data for Name: todo_item; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.todo_item (id, texto, completed, created_at, completed_at, task_id, due_date, comentario) FROM stdin;
596	Emitir Nf's clientes (Oaz, Sá, Burlamaqui e Taurus)	t	2025-11-03 20:47:30.564579	2025-11-03 20:47:30.563827	309	\N	\N
597	Enviar Nf'sclientes	t	2025-11-03 20:47:30.564581	2025-11-03 20:47:30.563961	309	\N	\N
5474	Fazer o de para de todos os campos que eles veem no RM com os que puxamos da api	t	2025-12-08 20:20:15.259586	2025-12-08 20:20:15.258687	338	\N	\N
5475	Aguardadno acesso a API - Gomes 18/11	t	2025-12-08 20:20:15.259588	2025-12-08 20:20:15.25882	338	\N	\N
1142	Configurar criação do usuário console robo_rpa	t	2025-11-10 21:44:12.373208	2025-11-10 21:44:12.372202	173	\N	\N
1143	Conseguir acesso do robo_rpa pra pasta dos arquivos	t	2025-11-10 21:44:12.37321	2025-11-10 21:44:12.372356	173	\N	\N
1144	Finalização a implementação e testar deslogado do RDP	t	2025-11-10 21:44:12.373211	2025-11-10 21:44:12.372394	173	\N	\N
1145	Testar execução de shoppings	t	2025-11-10 21:44:12.373212	2025-11-10 21:44:12.372427	173	\N	\N
1146	Criar loop pra rodar todos os shoppings em sequência	t	2025-11-10 21:44:12.373212	2025-11-10 21:44:12.372455	173	\N	\N
953	Implementar RPA	t	2025-11-07 20:00:27.348507	2025-11-07 20:00:27.346407	284	\N	\N
1147	Resolver inconsistência na troca de shopping	t	2025-11-10 21:44:12.373213	2025-11-10 21:44:12.372481	173	\N	\N
5310	Matheus em teste - 03/12	t	2025-12-04 20:49:04.355074	2025-12-04 20:49:04.354414	380	\N	\N
13	Envio de 3 exemplos de OC + dados/campos de validação contábil.	t	2025-09-10 19:43:02.659477	2025-09-10 19:43:02.657122	112	\N	\N
14	Lista de lojas e respectivos gerentes/supervisoras para provisionamento de acessos.	t	2025-09-10 19:43:02.65948	2025-09-10 19:43:02.657288	112	\N	\N
169	Adicionar um botão do Mercado livre e implementar a nova função	t	2025-10-27 20:24:53.155628	2025-10-27 20:24:53.155094	248	\N	\N
170	Apresentar para o cliente na sexta-feira	t	2025-10-27 20:24:53.155629	2025-10-27 20:24:53.155184	248	\N	\N
5476	Dani realizar teste	t	2025-12-08 20:20:15.259589	2025-12-08 20:20:15.258854	338	\N	\N
5477	Refazer toda a parte de consulta à api	t	2025-12-08 20:20:15.259589	2025-12-08 20:20:15.258883	338	\N	\N
5478	Puxar dados pela api de natureza orçamentárias e centro de custo	t	2025-12-08 20:20:15.25959	2025-12-08 20:20:15.25891	338	\N	\N
6401	17/12 - Nao mexi nesse projeto hoje. ele esta local na minha maquina.	t	2025-12-18 20:44:41.131989	2025-12-18 20:44:41.130625	329	\N	\N
6402	Agora que ja temos um base solida desse produto, vou refinar o codigo.	t	2025-12-18 20:44:41.13199	2025-12-18 20:44:41.130666	329	\N	terminando de refinar o contato das pessoas com a araras.
101	Analisar mais precisamente os campos Cliente/Parte	t	2025-10-23 14:55:51.927063	2025-10-23 14:55:51.92614	172	\N	\N
102	Espera do envio de arquivos por parte do cliente, para verificação de alguns campos restantes	t	2025-10-23 14:55:51.927065	2025-10-23 14:55:51.92625	172	\N	\N
103	Integração de rpa com o sistema produzido no replit	t	2025-10-23 14:55:51.927066	2025-10-23 14:55:51.926295	172	\N	\N
26	Tela de Upload do RM (despesas).	t	2025-10-13 20:19:09.129244	2025-10-13 20:19:09.128667	55	\N	\N
27	Tela de Lançamento de Receitas com seletores encadeados.	t	2025-10-13 20:19:09.129245	2025-10-13 20:19:09.128752	55	\N	\N
28	Cadastros-mestre e Dashboards iniciais.	t	2025-10-13 20:19:09.129246	2025-10-13 20:19:09.128784	55	\N	\N
104	Fazendo o sistema abrir o chormium e roda rpa após salvar processo e efetuar o login	t	2025-10-23 14:55:51.927067	2025-10-23 14:55:51.926344	172	\N	\N
6403	Esperando o retorno do matheus sobre os acessos da filmagem.	t	2025-12-18 20:44:41.131991	2025-12-18 20:44:41.130706	329	\N	\N
6933	Publicar app e liberar para testes do cliente	f	2026-01-05 23:00:22.035108	\N	404	\N	\N
6400	Para o refino do sistema, eu to tentando treinar um modelo personalizado do yolov11.	f	2025-12-18 20:44:41.131986	\N	329	2025-12-26	\N
105	Fazer o sistema criar processo no sistema da burlamaqui e preencher os dados com os dados do processo já adicionado no nosso sistema.	t	2025-10-23 14:55:51.927067	2025-10-23 14:55:51.92638	172	\N	\N
5479	Equipe sá validar - 02/12	f	2025-12-08 20:20:15.25959	\N	338	\N	\N
2690	Ajuste nos telhas	f	2025-11-25 16:14:15.407818	\N	371	\N	\N
6934	melhorias no sistema de chat IA	t	2026-01-05 23:00:22.035109	2026-01-05 23:00:22.034368	404	\N	\N
2691	Bater com Andrey o conteudo	f	2025-11-25 16:14:15.407821	\N	371	\N	\N
2692	Criar V1	t	2025-11-25 16:14:15.407821	2025-11-25 16:14:15.406935	371	\N	\N
4154	dar senha da lisette e login	t	2025-12-01 16:36:42.159698	2025-12-01 16:36:42.157833	350	\N	\N
4155	reuniao sexta com o david e lisette	t	2025-12-01 16:36:48.567659	2025-12-01 16:36:48.567075	245	\N	\N
6935	retirar projeto do replit e colocar no antigravity	t	2026-01-05 23:00:22.03511	2026-01-05 23:00:22.034411	404	\N	\N
4156	Em teste com equipe da Oaz	t	2025-12-01 16:38:02.312543	2025-12-01 16:38:02.312088	373	\N	\N
7327	Ajuste das perguntas para aparecer todas de uma unica vez, melhorando a dinamica	t	2026-01-26 20:11:53.68996	2026-01-26 20:11:53.689172	498	\N	\N
5480	Cobrar Gomes - 18/11	t	2025-12-08 20:20:36.668247	2025-12-08 20:20:36.667537	339	\N	\N
1706	Sufocar Yan - 18/11	f	2025-11-17 20:41:00.80905	\N	342	\N	\N
5481	Cobrando api - 19/11	t	2025-12-08 20:20:36.668248	2025-12-08 20:20:36.667632	339	\N	\N
59	Clone  e configuração do projeto na máquina do Ronald	t	2025-10-15 21:24:15.88906	2025-10-15 21:24:15.886692	176	\N	\N
60	Rpa fazendo login no evo	t	2025-10-15 21:24:15.889064	2025-10-15 21:24:15.886809	176	\N	\N
61	Rpa fazendo o processo até o penúltimo clique para envio	t	2025-10-15 21:24:15.889065	2025-10-15 21:24:15.886855	176	\N	\N
5482	Dani realizar teste	t	2025-12-08 20:20:36.668249	2025-12-08 20:20:36.667666	339	\N	\N
2066	Papo marcado com Fernanda sexta 15h	t	2025-11-18 20:21:49.173631	2025-11-18 20:21:49.172639	343	\N	\N
2067	Sistema ok. Fernanda entra de férias dia 17/11 e no retorno ja vai para uso. Unico detalhe é que em planilha com vlaume, demora um pouco mais o upload.	t	2025-11-18 20:21:49.173632	2025-11-18 20:21:49.172793	343	\N	\N
2068	Falar com Thaiara - 18/11	t	2025-11-18 20:21:49.173633	2025-11-18 20:21:49.172828	343	\N	\N
2069	Aguardando resposta	f	2025-11-18 20:21:49.173633	\N	343	\N	\N
931	Relatório para gestor das filiais	t	2025-11-06 20:03:22.591293	2025-11-06 20:03:22.590278	316	\N	\N
932	Relatório para admin	t	2025-11-06 20:03:22.591296	2025-11-06 20:03:22.590404	316	\N	\N
417	Enviar mensagem para o Silvio	t	2025-10-29 21:29:56.330666	2025-10-29 21:29:56.328617	276	\N	\N
418	Esperar resposta do Silvio	t	2025-10-29 21:29:56.330668	2025-10-29 21:29:56.328745	276	\N	\N
2743	Criar cadastro escola IFRRJ	t	2025-11-25 16:17:54.02366	2025-11-25 16:17:54.022809	372	\N	\N
2744	Passar cadastro de admin para Victor	t	2025-11-25 16:17:54.023663	2025-11-25 16:17:54.02291	372	\N	\N
2745	Apresentar o sistema para Victor junto com Andrey	t	2025-11-25 16:17:54.023663	2025-11-25 16:17:54.022945	372	\N	\N
2746	Victor testando - cobrar dia 25/11	f	2025-11-25 16:17:54.023664	\N	372	\N	\N
2747	Cadastrar alunos	f	2025-11-25 16:17:54.023665	\N	372	\N	\N
6404	vou mandar as filmagem das cameras para o gomes.	t	2025-12-18 20:44:41.131991	2025-12-18 20:44:41.130736	329	\N	\N
613	Pegar cartão cnpj com Giulliana ou cliente direto	t	2025-11-03 20:57:53.175567	2025-11-03 20:57:53.174889	290	\N	\N
614	Entender os valores para alimentar o FC	t	2025-11-03 20:57:53.17557	2025-11-03 20:57:53.174987	290	\N	\N
6405	Começar com o desenvovimento	t	2025-12-18 20:44:41.131992	2025-12-18 20:44:41.130764	329	\N	\N
6406	Rolar um debate na resenha do time - 19/11	t	2025-12-18 20:44:41.131993	2025-12-18 20:44:41.130792	329	\N	\N
2818	Cobrar retorno do teste na sexta - 25/11	t	2025-11-25 20:18:49.486986	2025-11-25 20:18:49.485847	345	\N	\N
2819	Agendar papo para finalizar os detalhes final	t	2025-11-25 20:18:49.486989	2025-11-25 20:18:49.486004	345	\N	\N
6407	Fazer a contabilização total de quantas pessoas passsam nass araras.	t	2025-12-18 20:44:41.131993	2025-12-18 20:44:41.130819	329	\N	\N
1148	Marcar reunião para mostrar o sistema e pegar feedbacks	t	2025-11-10 21:51:07.293026	2025-11-10 21:51:07.292224	317	\N	\N
1149	Resolver variedade de produtos	t	2025-11-10 21:51:07.293028	2025-11-10 21:51:07.29233	317	\N	\N
1073	desenho criado usando o DALL-e-3	t	2025-11-10 21:27:14.188366	2025-11-10 21:27:14.187339	235	\N	\N
6408	Rodar o modelo usando o SAM3.	t	2025-12-18 20:44:41.131994	2025-12-18 20:44:41.130844	329	\N	\N
6409	Rodar o modelo usando o SAM2.	t	2025-12-18 20:44:41.131994	2025-12-18 20:44:41.13087	329	\N	\N
1074	vou mudar  o modelo para gpt-image-1, mas preciso que o felipe faz uma verificaçao na openai para poder usar esse modelo.	t	2025-11-10 21:27:14.188367	2025-11-10 21:27:14.187433	235	\N	\N
1075	ajuste fino feito, vou mandar para teste. aguardando feedback	t	2025-11-10 21:27:14.188368	2025-11-10 21:27:14.187469	235	\N	\N
5210	Cancelar NF Burlamaqui e reemitir	t	2025-12-03 20:16:34.985561	2025-12-03 20:16:34.984899	388	\N	\N
1076	sinalizar um "carregamento" para uploads e geraçao do desenho tecnico.	t	2025-11-10 21:27:14.188368	2025-11-10 21:27:14.187497	235	\N	\N
1077	recebi o feedback,  vou fazzer uma reuniao com o matheus para poder entender melhor como podemos melhorar o projeto	t	2025-11-10 21:27:14.188369	2025-11-10 21:27:14.187524	235	\N	\N
1078	Implementar login para estilistas,	t	2025-11-10 21:27:14.18837	2025-11-10 21:27:14.187571	235	\N	\N
1079	categorização das coleções por fornecedor e página de administração para criação de usuários	t	2025-11-10 21:27:14.18837	2025-11-10 21:27:14.187598	235	\N	\N
1080	finalizando as mudanças no desenho tecnico.	t	2025-11-10 21:27:14.188371	2025-11-10 21:27:14.187623	235	\N	\N
1081	criar funcionalidades para tela de fornecedor	t	2025-11-10 21:27:14.188372	2025-11-10 21:27:14.187648	235	\N	\N
1082	Receber novos feedbacks das meninas da OAZ	t	2025-11-10 21:27:14.188373	2025-11-10 21:27:14.187673	235	\N	\N
1083	Conciliação bancária automática;	t	2025-11-10 21:28:26.203219	2025-11-10 21:28:26.20243	262	\N	\N
1084	Portal do cliente para emissão de boletos;	t	2025-11-10 21:28:26.203221	2025-11-10 21:28:26.202522	262	\N	\N
1085	Disparo de cobrança via WhatsApp.	t	2025-11-10 21:28:26.203222	2025-11-10 21:28:26.202555	262	\N	\N
5211	Abrir ordem de compra Sá	t	2025-12-03 20:16:34.985562	2025-12-03 20:16:34.984986	388	\N	\N
2357	Entender cada tela do sistema	t	2025-11-21 16:01:34.528469	2025-11-21 16:01:34.527369	352	\N	\N
5780	Pagar folha	t	2025-12-10 20:30:39.580117	2025-12-10 20:30:39.579448	392	\N	\N
5781	Ver com GOmes questão de criar api para os clientes	f	2025-12-10 20:30:39.580119	\N	392	\N	\N
2358	montando as telas do dashboard de admin	t	2025-11-21 16:01:34.528472	2025-11-21 16:01:34.527645	352	\N	\N
7331	Cobrar Humberto o contato com David	f	2026-01-27 20:07:29.261602	\N	501	\N	\N
6410	Abrir demanda - 03/12	t	2025-12-18 20:44:41.131995	2025-12-18 20:44:41.130895	329	\N	\N
5212	Cobrar Oaz	f	2025-12-03 20:16:34.985563	\N	388	\N	\N
6521	8)\tCriar uma área para que o Humberto crie um database de valores de peças para que os usuários possam consultar. Ae teremos o histórico de preço de quotes da salesforce e preços do Humberto!	t	2025-12-19 20:36:58.128577	2025-12-19 20:36:58.121771	180	\N	\N
2820	Fazer para admin relatório por filial, igual o funcionário de loja	t	2025-11-25 20:18:49.486989	2025-11-25 20:18:49.486048	345	\N	\N
2821	Verificar relatório hoje existente em admin - erro	t	2025-11-25 20:18:49.48699	2025-11-25 20:18:49.48608	345	\N	\N
2822	Processo de aprovação incluir nova etapa "Mais detalhes" - gestor solicita mais informação antes de aprovar	t	2025-11-25 20:18:49.486991	2025-11-25 20:18:49.486111	345	\N	\N
2021	formularios do david	f	2025-11-18 20:04:06.434806	\N	354	\N	\N
2022	entender sobre a operaçao da Aeropool a fundo	f	2025-11-18 20:04:06.434812	\N	354	\N	\N
2023	Buscar recriar a operaçao da Aeropool dentro do Salesforce	f	2025-11-18 20:04:06.434812	\N	354	\N	\N
2024	Alterar o sistema de quote (ja aprimorado) para cotizar emails da Aeropool tambem	f	2025-11-18 20:04:06.434813	\N	354	\N	\N
6522	9)\tEmails com peça que tiverem já preço no novo database do Humberto o sistema crie automaticamente a quote.	t	2025-12-19 20:36:58.128578	2025-12-19 20:36:58.1218	180	\N	\N
2025	Consolidar no sistema de quotes uma conexao com a api da salesforce aeropool	f	2025-11-18 20:04:06.434813	\N	354	\N	\N
6523	incluir no RPA	t	2025-12-19 20:36:58.128578	2025-12-19 20:36:58.121829	180	\N	\N
6524	Paginação de resultados de listas	t	2025-12-19 20:36:58.128579	2025-12-19 20:36:58.121856	180	\N	\N
6525	5)\tCriar uma área de cadastro para emails suspeitos de serem de concorrência (busca de preço de mercado). Markup de 15% para esses emails no valor das peças, incluir uma mensagem de entrar em contato para better offer. (incluir um alerta que avisa do endereço de email suspeito).	t	2025-12-19 20:36:58.128579	2025-12-19 20:36:58.121882	180	\N	\N
6526	4)\tMelhorar layout visual do Sistema (muita informação)	t	2025-12-19 20:36:58.12858	2025-12-19 20:36:58.121908	180	\N	\N
7332	colocar no RPA Monitor	f	2026-01-27 20:16:01.791167	\N	453	\N	\N
6936	conectar o sistema no big query - google e ga4	t	2026-01-05 23:00:22.03511	2026-01-05 23:00:22.034442	404	\N	\N
6937	Aguardando acesso ao big Query	t	2026-01-05 23:00:22.035111	2026-01-05 23:00:22.034469	404	\N	\N
7333	Reunião com o Cliente quinta	f	2026-01-27 20:16:01.791171	\N	453	\N	\N
7112	Atualizar todos os projetos da Base com o Andrey.	f	2026-01-15 18:37:30.951641	\N	440	\N	\N
7113	Montar semana de imersão da OAZ	f	2026-01-15 18:37:30.951646	\N	440	\N	\N
7334	reuniao para apresentar o app para o BB.	t	2026-01-27 20:16:01.791174	2026-01-27 20:16:01.785845	453	\N	eles estao com conflito com os horarios, esperando uma decisao deles
4612	Em teste com Andrey	t	2025-12-01 20:12:53.02429	2025-12-01 20:12:53.023829	374	\N	\N
7114	Montar proposta comercial da Charles River	f	2026-01-15 18:37:30.951646	\N	440	\N	\N
7115	Incluir Thiago correia no CRM e abrir uma agenda com ele essa semana.	f	2026-01-15 18:37:30.951647	\N	440	\N	\N
7116	Fechar o orçamento do PlaniAI com a Giu	f	2026-01-15 18:37:30.95165	\N	440	\N	\N
7117	Enviar proposta para a Charles River.	f	2026-01-15 18:37:30.951651	\N	440	\N	\N
7118	liberar o admin para a galera colocar os dado.	t	2026-01-16 22:03:20.336376	2026-01-16 22:03:20.333289	169	\N	\N
7119	vou implementar as telas que falta	t	2026-01-16 22:03:20.336378	2026-01-16 22:03:20.333399	169	\N	\N
7120	tela de onboarding / cadastro sem fricçao.	t	2026-01-16 22:03:20.336379	2026-01-16 22:03:20.333442	169	\N	\N
7121	tela de feed	t	2026-01-16 22:03:20.33638	2026-01-16 22:03:20.333476	169	\N	\N
7335	testes	t	2026-01-27 20:16:01.791175	2026-01-27 20:16:01.785898	453	\N	\N
7336	Reunião amanha 22/01 para alinhar	t	2026-01-27 20:16:01.791176	2026-01-27 20:16:01.785932	453	\N	\N
7337	finalizando as telass do borabailar	t	2026-01-27 20:16:01.791176	2026-01-27 20:16:01.785971	453	\N	\N
7338	Aguardando feedback do cliente	f	2026-01-27 20:16:35.499897	\N	472	\N	\N
7339	Isa abrir demanda	f	2026-01-27 20:16:35.499902	\N	472	\N	\N
7340	Apresentar pro time	f	2026-01-27 20:17:14.002539	\N	466	2026-01-29	\N
814	Agendar reunião com a Julia	f	2025-11-05 20:15:09.34253	\N	275	\N	\N
817	Ajustar tempo de processamento	t	2025-11-05 20:15:38.185791	2025-11-05 20:15:38.184907	315	\N	\N
818	Liberar para teste	t	2025-11-05 20:15:38.185793	2025-11-05 20:15:38.185052	315	\N	\N
7341	Trabalhar no novo layout	t	2026-01-27 20:17:14.002541	2026-01-27 20:17:14.001701	466	\N	\N
7342	Colocar o projeto no Git da Inovai.Lab	t	2026-01-27 20:17:14.002542	2026-01-27 20:17:14.001751	466	\N	\N
7343	Tirar do Replit o projeto	t	2026-01-27 20:17:14.002542	2026-01-27 20:17:14.001783	466	\N	\N
7274	Cobrar arquivos de produtos - Paulo falar com cilente	f	2026-01-23 20:42:18.894638	\N	465	\N	\N
2823	Criar sistema de notificação ou revisar o existente	t	2025-11-25 20:18:49.486991	2025-11-25 20:18:49.486139	345	\N	\N
2493	Aguardando reunião entre Matheus e Léo para entender a comunicação personalizada - 18/11 - 19/11	t	2025-11-24 20:22:00.127678	2025-11-24 20:22:00.126986	331	\N	\N
2494	Guardando perguntar pelo time da Oaz - 21/11	t	2025-11-24 20:22:00.12768	2025-11-24 20:22:00.127082	331	\N	\N
2824	Papo segunda as 15	t	2025-11-25 20:18:49.486992	2025-11-25 20:18:49.486173	345	\N	\N
2825	Entregar 17/11 sistema para teste final ja com a filial ao vivo - 17/11	t	2025-11-25 20:18:49.486992	2025-11-25 20:18:49.4862	345	\N	\N
2826	Aguardando ok final	t	2025-11-25 20:18:49.486993	2025-11-25 20:18:49.486227	345	\N	\N
2789	Detalhar os campos extraidos pela inteligencia artificial.	t	2025-11-25 20:12:00.439551	2025-11-25 20:12:00.43902	365	\N	\N
4342	Processar em lote elaw	t	2025-12-01 20:01:09.904395	2025-12-01 20:01:09.902865	323	\N	\N
4343	monitoramento rpa com o andrey	t	2025-12-01 20:01:09.904397	2025-12-01 20:01:09.903014	323	\N	\N
4344	subir e testar em produção	t	2025-12-01 20:01:09.904398	2025-12-01 20:01:09.903079	323	\N	\N
4345	Aguardando retorno da Fernnanda	t	2025-12-01 20:01:09.904399	2025-12-01 20:01:09.903111	323	\N	\N
4346	Ajustar e acrescentar fluxo pós preenchimento, para reclamadas extras	t	2025-12-01 20:01:09.9044	2025-12-01 20:01:09.90314	323	\N	\N
4347	tipo de pedidos	t	2025-12-01 20:01:09.904401	2025-12-01 20:01:09.903167	323	\N	\N
4967	Enviado mensagem para a Juliana cobrando os testes do sistema.	t	2025-12-02 20:29:18.878217	2025-12-02 20:29:18.87726	335	\N	\N
4968	Mathues testando com alguns usuários - aguardando feedback - 18/11	t	2025-12-02 20:29:18.878219	2025-12-02 20:29:18.877344	335	\N	\N
4969	LIberar versão final para Matheus - 26/11	t	2025-12-02 20:29:18.87822	2025-12-02 20:29:18.877412	335	\N	\N
1187	Mudar o sistema da inovai.lab. Não é possível editar a informações de documentaçào dos projetos	f	2025-11-11 14:59:07.679313	\N	330	\N	\N
7316	Finalizar a aba geral	f	2026-01-26 20:00:39.055878	\N	493	\N	\N
7122	Marcar reunião com a Juliana para mostrar o funcionamentos do timesheet, criador de reunião e analise de transcrição	f	2026-01-16 22:15:40.28694	\N	418	\N	\N
7232	Ronald abrir detalhes do projeto e migrar para fora do Replit	t	2026-01-23 20:08:18.302559	2026-01-23 20:08:18.297485	387	\N	\N
1196	criar um banco local para armazenar esses dados.	t	2025-11-11 15:13:50.675795	2025-11-11 15:13:50.674745	282	\N	\N
1197	leitura do banco feita. aguardando proximos passos.	t	2025-11-11 15:13:50.675797	2025-11-11 15:13:50.674832	282	\N	\N
1198	criar login de colaborador e gerente.	t	2025-11-11 15:13:50.675798	2025-11-11 15:13:50.674866	282	\N	\N
1199	puxar os dados do banco da oaz para cada gerente e funcionario	t	2025-11-11 15:13:50.675798	2025-11-11 15:13:50.674955	282	\N	\N
1200	criar  dashboard de gerente.	t	2025-11-11 15:13:50.675799	2025-11-11 15:13:50.674985	282	\N	\N
1201	Criar dashboard do colaborador	t	2025-11-11 15:13:50.6758	2025-11-11 15:13:50.675012	282	\N	\N
1026	Cobrar Paulo contrato	f	2025-11-10 18:20:34.688593	\N	244	\N	\N
1027	Cobrar acordo com o cliente	f	2025-11-10 18:20:53.670757	\N	247	\N	\N
4970	Colocar no ar sexta - 28/11	t	2025-12-02 20:29:18.878221	2025-12-02 20:29:18.87746	335	\N	\N
7252	reuniao com o fluxograma terça 27/01	f	2026-01-23 20:24:38.986526	\N	456	2026-01-27	\N
1203	Poder editar a Anaminnese	f	2025-11-11 16:45:51.498586	\N	319	\N	\N
1204	Ajustar foto perfil aluno	f	2025-11-11 16:45:51.498591	\N	319	\N	\N
7263	Adicionar funcionalidade de parar o robô via web	t	2026-01-23 20:38:59.23943	2026-01-23 20:38:59.238187	353	\N	\N
7264	Validação completa no mês de janeiro pra liberar o sistema web	t	2026-01-23 20:38:59.239431	2026-01-23 20:38:59.238288	353	\N	\N
7265	Teste do novo sistema no cálculo atípico	t	2026-01-23 20:38:59.239432	2026-01-23 20:38:59.238327	353	\N	\N
4971	fazer uma revisao com o andrey - (Ronald )	t	2025-12-02 20:29:18.878221	2025-12-02 20:29:18.877489	335	\N	\N
7266	Correção e implementações mais automatizadas para envio de email	t	2026-01-23 20:38:59.239433	2026-01-23 20:38:59.238361	353	\N	\N
7267	Criação e validação da geração de boleto no sistema web	t	2026-01-23 20:38:59.239434	2026-01-23 20:38:59.238392	353	\N	\N
7268	Validar operação na sexta	t	2026-01-23 20:38:59.239434	2026-01-23 20:38:59.238421	353	\N	\N
7269	Completa migração pro servidor web da parte de cálculos	t	2026-01-23 20:38:59.239435	2026-01-23 20:38:59.238449	353	\N	\N
7270	Teste e validação completa da parte de cálculos	t	2026-01-23 20:38:59.239436	2026-01-23 20:38:59.238477	353	\N	\N
7271	Evoluir os logs pra melhor visibilidade dos erros	t	2026-01-23 20:38:59.239436	2026-01-23 20:38:59.238505	353	\N	\N
7272	Adicionar última alteração de resolução na parte da realização final dos cálculos	t	2026-01-23 20:38:59.239437	2026-01-23 20:38:59.23859	353	\N	\N
7273	Finalizar o processo de cálculos por completo até dia 12/12	t	2026-01-23 20:38:59.239438	2026-01-23 20:38:59.238661	353	\N	\N
7275	CObrar os arquivos	t	2026-01-23 20:42:18.89464	2026-01-23 20:42:18.894096	465	2026-01-23	\N
7288	feito	t	2026-01-26 17:58:40.923107	2026-01-26 17:58:40.922372	482	\N	\N
7289	feito	t	2026-01-26 17:59:37.908621	2026-01-26 17:59:37.907723	479	\N	\N
7290	colocar no RPA Monitor	t	2026-01-26 17:59:37.908622	2026-01-26 17:59:37.907926	479	\N	\N
7291	Ajustar a busca de sku entre o sistema e o sharepoint	f	2026-01-26 18:32:24.049517	\N	443	\N	\N
7292	Ajustar a logica para procurar dentro da plataforma primeiro, depois dentro do sharepoint caso ela nao for encontrada	f	2026-01-26 18:32:24.049522	\N	443	\N	\N
7296	Refazer  logica de extração para nao travar com Redis linux	t	2026-01-26 19:47:22.210994	2026-01-26 19:47:22.203206	452	\N	\N
7297	Implementação do serviço em tkinter	t	2026-01-26 19:53:41.34717	2026-01-26 19:53:41.342716	471	\N	\N
7298	Novo layout Web usando o tkinter apenas como serviço	t	2026-01-26 19:53:41.347173	2026-01-26 19:53:41.342858	471	\N	\N
7299	Segundo robo especifico para monitorar se o cliente ja fez a biometria com envio de dados para o robo principal	t	2026-01-26 19:53:41.347176	2026-01-26 19:53:41.342904	471	\N	\N
7300	Fila de envio ao Autobhan	t	2026-01-26 19:53:41.347177	2026-01-26 19:53:41.342942	471	\N	\N
7301	Controle do processo de lote, permitir se recuperar de erros	t	2026-01-26 19:53:41.347177	2026-01-26 19:53:41.342982	471	\N	\N
7302	Construção total do layout web para deixar de usar o tkinter local	t	2026-01-26 19:53:41.347178	2026-01-26 19:53:41.34302	471	\N	\N
7317	Fazer a extração dos dados do pdf com regex	t	2026-01-26 20:00:39.05588	2026-01-26 20:00:39.055172	493	\N	\N
7318	Configurar o login	t	2026-01-26 20:00:39.055881	2026-01-26 20:00:39.055213	493	\N	\N
7123	aguardando reuniao de alinhamento para obter novas informações	t	2026-01-16 22:22:18.506999	2026-01-16 22:22:18.505897	341	\N	\N
7124	Felipe vai me passar o contato do augusto para alinhamento de como consumir os dados de faturamento	t	2026-01-16 22:22:18.507	2026-01-16 22:22:18.506044	341	\N	\N
7125	Implementar sistema de consulta por semantica	t	2026-01-16 22:22:18.507001	2026-01-16 22:22:18.506082	341	\N	\N
7126	Retirar app do replit e levantar o projeto no antigravity	t	2026-01-16 22:22:18.507002	2026-01-16 22:22:18.506115	341	\N	\N
7127	Cálculos exclusivamente no backend	t	2026-01-16 22:22:18.507003	2026-01-16 22:22:18.506147	341	\N	\N
7128	Realizando testes se esta ok de modo geral - 18/11	t	2026-01-16 22:22:18.507004	2026-01-16 22:22:18.506177	341	\N	\N
7344	Salvar o maximo de informação que for necessaria dentro do contexto da plafaforma	t	2026-01-27 20:19:57.621571	2026-01-27 20:19:57.620761	457	\N	\N
7345	SUBIR EM LOTE OS XMLS	t	2026-01-27 20:19:57.621572	2026-01-27 20:19:57.620857	457	\N	\N
7064	terminar de mapear as categorias das transaçoes	t	2026-01-13 16:36:18.771218	2026-01-13 16:36:18.770489	439	\N	\N
7346	Vai rodar amanha 27/01 com ALice	t	2026-01-27 20:21:39.001766	2026-01-27 20:21:39.001306	485	\N	\N
7086	Usar o tom de voz em json	f	2026-01-14 20:21:47.243225	\N	442	\N	\N
6199	Editar uma tarefa clicando nela, tirar botão de edição de tarefa	t	2025-12-16 19:17:08.979512	2025-12-16 19:17:08.975023	189	\N	\N
7087	ajustar import em grande escala	t	2026-01-14 20:22:11.651288	2026-01-14 20:22:11.649773	401	2025-12-26	\N
6200	Ordem alfabética pelo responsável da tarefa na hora de criar - Daniel	t	2025-12-16 19:17:08.979512	2025-12-16 19:17:08.97504	189	\N	\N
6201	Mudar tela de modo geral. Deixar igual o projeto do bobs spoleto. Coluna fixa do lado esquerdo - Vitor	t	2025-12-16 19:17:08.979512	2025-12-16 19:17:08.975056	189	\N	\N
6202	Dexiar apenas um botao de "confirmar" para excluir.	t	2025-12-16 19:17:08.979512	2025-12-16 19:17:08.975072	189	\N	\N
6203	Adicionar ordens de prioridade.	t	2025-12-16 19:17:08.979513	2025-12-16 19:17:08.9751	189	\N	\N
6204	Aparecer a data de criação do To do - 05/12	t	2025-12-16 19:17:08.979513	2025-12-16 19:17:08.975117	189	\N	\N
6205	Colocar o numero de To do no card da ação - 05/12	t	2025-12-16 19:17:08.979513	2025-12-16 19:17:08.975141	189	\N	\N
6206	Ajusta o salvamento na hora que edita o card. Ex: mudar qualquer detalhe ja fica atualizando dando bug - 05/12	t	2025-12-16 19:17:08.979514	2025-12-16 19:17:08.975159	189	\N	\N
6207	Adicionar ordens de prioridade. mover o card para colcar em ordem de prioridade	t	2025-12-16 19:17:08.979514	2025-12-16 19:17:08.975176	189	\N	\N
6208	Definir acesso de terrceiros no sistema de kanban	t	2025-12-16 19:17:08.979514	2025-12-16 19:17:08.975193	189	\N	\N
6209	CRM - Poder anexar arquivos nos cards dos contatos	t	2025-12-16 19:17:08.979515	2025-12-16 19:17:08.975208	189	\N	\N
6210	Organizar os to-do ( organizar por ordem de conclusão. )	t	2025-12-16 19:17:08.979515	2025-12-16 19:17:08.975229	189	\N	\N
6211	Verificar aa barra de conclusão dos projetos.	f	2025-12-16 19:17:08.979515	\N	189	\N	\N
7088	melhorar a descrição das imagens, ficou muito básico pegando somente do xls, porém custo de api será alto	t	2026-01-14 20:22:11.65129	2026-01-14 20:22:11.649954	401	2025-12-26	\N
7089	rotina de cruzamento de imagem com skus de xls importado	t	2026-01-14 20:22:11.65129	2026-01-14 20:22:11.650009	401	\N	\N
5483	Criar uma extração via API RM da base de dados do contas a pagar que estão baixado (data, c.c., natureza e valor)	f	2025-12-08 20:20:36.668249	\N	339	\N	\N
7090	Ronald abrir demanda	t	2026-01-14 20:23:08.51149	2026-01-14 20:23:08.510212	381	2025-12-19	\N
7091	Matheus em teste - 03/12	t	2026-01-14 20:23:08.511492	2026-01-14 20:23:08.510411	381	\N	\N
7092	Ajuste função 1v1 (Deve ficar dentro de cada cliclo gerenciado pelo gestor)	t	2026-01-14 20:23:08.511493	2026-01-14 20:23:08.510452	381	\N	\N
7093	testes para aprovar a funcionalidade	t	2026-01-14 20:23:08.511493	2026-01-14 20:23:08.510487	381	\N	\N
7094	Marcar reunião com Juliana - 09/12	t	2026-01-14 20:23:08.511494	2026-01-14 20:23:08.510522	381	\N	\N
7095	tirrar função de criar ciclos do gestor	t	2026-01-14 20:23:08.511495	2026-01-14 20:23:08.510555	381	\N	\N
7096	criar função que importe xls para cadastrar vários usuários de uma só vez	t	2026-01-14 20:23:08.511495	2026-01-14 20:23:08.510636	381	\N	\N
7097	mandar para Juliana testar e dar feedback	t	2026-01-14 20:23:08.511497	2026-01-14 20:23:08.510669	381	2025-12-11	\N
1285	Formatação do layout de saida para markdown	t	2025-11-12 19:18:05.12578	2025-11-12 19:18:05.123004	255	\N	\N
1286	Inclusão de regras para montagens de graficos	t	2025-11-12 19:18:05.125782	2025-11-12 19:18:05.123139	255	\N	\N
1287	Analise inteligente de prompts para divisão em subtarefas. Evita erros de processamento na API	t	2025-11-12 19:18:05.125784	2025-11-12 19:18:05.123196	255	\N	\N
1288	Conjunto de funçoes e regras para montagem de Dashboard	t	2025-11-12 19:18:05.125784	2025-11-12 19:18:05.123239	255	\N	\N
1289	Análise secundária para verificação de fidelidade na resposta	t	2025-11-12 19:18:05.125787	2025-11-12 19:18:05.123281	255	\N	\N
1290	Otimização de todas as funções, pois foi detectado gasto excessivo de tokens	t	2025-11-12 19:18:05.125788	2025-11-12 19:18:05.123317	255	\N	\N
1291	Normalização dos campos para diferentes plataformas	t	2025-11-12 19:18:05.125788	2025-11-12 19:18:05.123353	255	\N	\N
1292	Quando o periodo contempla inicio em um ano e termino em outro, a extração de data esta se perdendo	t	2025-11-12 19:18:05.125789	2025-11-12 19:18:05.123406	255	\N	\N
1293	O sistema não pode deixar o agente responder perguntas fora do contexto	t	2025-11-12 19:18:05.12579	2025-11-12 19:18:05.123454	255	\N	\N
7110	Liberação de quantidade de produto acima do limite de estoque	t	2026-01-14 20:28:55.588622	2026-01-14 20:28:55.587899	349	\N	\N
7111	Mostrar na tela do admin a quantidade de produtos pedida disponiveis em estoque/faltam em estoque	t	2026-01-14 20:28:55.588622	2026-01-14 20:28:55.587926	349	\N	\N
6527	e)\tSessao de update part mapped condition nao funciona.	t	2025-12-19 20:36:58.12858	2025-12-19 20:36:58.121934	180	\N	\N
4980	Fazer contato para ver condições para PJ	t	2025-12-02 20:41:25.784208	2025-12-02 20:41:25.783375	310	\N	\N
4981	Finalizar compra	t	2025-12-02 20:41:25.784209	2025-12-02 20:41:25.783497	310	\N	\N
4982	Aguardando a entrega final	t	2025-12-02 20:41:25.78421	2025-12-02 20:41:25.783532	310	\N	\N
4983	Enviar email de troca	t	2025-12-02 20:41:25.784211	2025-12-02 20:41:25.783561	310	\N	\N
3546	Melhorar o sitema de identificar os nomes das transaçoes	t	2025-11-28 18:49:56.749742	2025-11-28 18:49:56.749067	181	\N	\N
3547	dentro de transaçoes do extrato mostrar as seçoes de atm e debit	t	2025-11-28 18:49:56.749743	2025-11-28 18:49:56.749154	181	\N	\N
3548	mudar dentro do extrato os valores de transaçoes de R$ para $	t	2025-11-28 18:49:56.749743	2025-11-28 18:49:56.749179	181	\N	\N
3549	aidicionar catergorias para os withdrawals	t	2025-11-28 18:49:56.749743	2025-11-28 18:49:56.7492	181	\N	\N
3550	adicionar filtro de ano de extratos	t	2025-11-28 18:49:56.749744	2025-11-28 18:49:56.749219	181	\N	\N
7347	fdsfsdf	f	2026-01-27 20:31:30.74275	\N	473	\N	\N
6719	Preparar as informações do Educhat para a Viviane.	t	2026-01-05 17:02:09.701638	2026-01-05 17:02:09.698226	423	\N	\N
6720	Fechar com o Eric amigo da Giu	t	2026-01-05 17:02:09.701641	2026-01-05 17:02:09.698366	423	\N	\N
6721	Gerar o contrato da Rede Brasil	t	2026-01-05 17:02:09.701642	2026-01-05 17:02:09.698407	423	\N	\N
6722	Lançar o projeto de OKR da OAZ no nosso sistema.	t	2026-01-05 17:02:09.701643	2026-01-05 17:02:09.698442	423	\N	\N
6723	Passar e atualizar o CRM	t	2026-01-05 17:02:09.701646	2026-01-05 17:02:09.698479	423	\N	\N
6724	assinar NDA da Sá	t	2026-01-05 17:02:09.701646	2026-01-05 17:02:09.69851	423	\N	\N
6725	enviar mensagem para o Bento da OAZ cobrando os valores em aberto e a renovação do contrato.	t	2026-01-05 17:02:09.701647	2026-01-05 17:02:09.69854	423	\N	\N
6119	Mandar email vendo condições	t	2025-12-15 20:21:54.81709	2025-12-15 20:21:54.811139	311	\N	\N
6120	Fechar plano	t	2025-12-15 20:21:54.817097	2025-12-15 20:21:54.811238	311	\N	\N
4984	Aguradando resposta para saber os proximos passos	f	2025-12-02 20:41:25.784211	\N	310	\N	\N
4985	5 - 10 dias uteis - time ficar de olho	f	2025-12-02 20:41:25.784212	\N	310	\N	\N
6121	Em teste outro app - aguardando resposatas do time	t	2025-12-15 20:21:54.817098	2025-12-15 20:21:54.811263	311	\N	\N
7236	Sistema liberado - Cobrar teste	t	2026-01-23 20:22:01.532853	2026-01-23 20:22:01.531656	454	2026-01-23	\N
7253	Matheus não responde o Feedback - Cobrar para saber do uso	f	2026-01-23 20:30:07.739614	\N	459	2026-01-23	\N
2154	Marcar papo com Fabiano para estudar cenário - 19/11	t	2025-11-19 18:23:52.15527	2025-11-19 18:23:52.154606	337	\N	\N
2155	Aguardando retorno. Mensagem enviada	f	2025-11-19 18:23:52.155273	\N	337	\N	\N
7254	Criação das remessas (dependendo da Alice)	t	2026-01-23 20:30:52.943695	2026-01-23 20:30:52.942782	468	\N	\N
7255	Validação completa do produto	t	2026-01-23 20:30:52.943696	2026-01-23 20:30:52.942887	468	\N	\N
2158	Aujstar para ler valor liquido. Hoje esta puxando o valor bruto	f	2025-11-19 18:24:37.897577	\N	340	\N	\N
2159	Remarcar papo e liberar para uso direto tbm. Pode melhor o front	t	2025-11-19 18:24:37.897579	2025-11-19 18:24:37.896961	340	\N	\N
2160	Aguardando retorno do convite para bater o sistema	f	2025-11-19 18:24:37.897579	\N	340	\N	\N
7256	Cadastro dos valores de amortização no VS	t	2026-01-23 20:30:52.943697	2026-01-23 20:30:52.942924	468	\N	\N
7257	Cadastro dos valores de juros no VS	t	2026-01-23 20:30:52.943698	2026-01-23 20:30:52.942955	468	\N	\N
7258	Troca pra competência correta (sempre o mês seguinte)	t	2026-01-23 20:30:52.943698	2026-01-23 20:30:52.942984	468	\N	\N
7259	Geração do boleto	t	2026-01-23 20:30:52.943699	2026-01-23 20:30:52.943012	468	\N	\N
7303	Implementar loop para todos os clientes que precisam ser avaliados	t	2026-01-26 19:53:41.347179	2026-01-26 19:53:41.34457	471	\N	\N
7304	Obter todos os dados que serviram para decisão da IA, além de obter o nada consta	t	2026-01-26 19:53:41.347179	2026-01-26 19:53:41.344629	471	\N	\N
6122	Trocar todos os projetos do Replit	f	2025-12-15 20:21:54.817099	\N	311	\N	\N
4991	Abertura de conta Banco Bradesco - Pessoalmente na agencia - 19/11	t	2025-12-02 20:41:47.036559	2025-12-02 20:41:47.03422	356	\N	\N
4992	Cobrar OAZ - Nf atrasada - 19/11	t	2025-12-02 20:41:47.036561	2025-12-02 20:41:47.034443	356	\N	\N
4993	Emissão NF clientes	t	2025-12-02 20:41:47.036562	2025-12-02 20:41:47.034484	356	\N	\N
4994	Abertura de chamado pagamento Sá	t	2025-12-02 20:41:47.036563	2025-12-02 20:41:47.034513	356	\N	\N
4995	Cobrar Oaz - Atrasado	t	2025-12-02 20:41:47.036563	2025-12-02 20:41:47.034539	356	\N	\N
7305	Identificar e acionar a opção que gera o link de biometria	t	2026-01-26 19:53:41.34718	2026-01-26 19:53:41.344664	471	\N	\N
7306	Regra de IA para aprovação ou recusa de credito	t	2026-01-26 19:53:41.347181	2026-01-26 19:53:41.344694	471	\N	\N
3046	Estruturar alunos 2 e 3 ano e ensino fundamental Escola Menino de Luz	f	2025-11-26 19:44:48.145028	\N	292	\N	\N
3047	07/11 - Inovai - (Reativar os 20 alunos do 1° ano)	t	2025-11-26 19:44:48.14503	2025-11-26 19:44:48.144383	292	\N	\N
3048	Estruturar cadastro de escola com Andrey	t	2025-11-26 19:44:48.145031	2025-11-26 19:44:48.144429	292	\N	\N
7307	Leitura dos dados do processo e avaliação de IA	t	2026-01-26 19:53:41.347181	2026-01-26 19:53:41.344722	471	\N	\N
7308	Navegação por dentro dos processos caso existam	t	2026-01-26 19:53:41.347182	2026-01-26 19:53:41.344755	471	\N	\N
7309	Leogin, by pass aviso de consulta recente	t	2026-01-26 19:53:41.347182	2026-01-26 19:53:41.344782	471	\N	\N
7310	Configurações campos de login nos sites	t	2026-01-26 19:53:41.347183	2026-01-26 19:53:41.344808	471	\N	\N
7311	Tela de configurações com todos os parametros do usuario do sistema	t	2026-01-26 19:53:41.347184	2026-01-26 19:53:41.344835	471	\N	\N
7312	Iniciar navegação de analise de credito	t	2026-01-26 19:53:41.347184	2026-01-26 19:53:41.344861	471	\N	\N
7313	Processo de OCR para leitura de numeros, API do chat como fallback	t	2026-01-26 19:53:41.347185	2026-01-26 19:53:41.344887	471	\N	\N
7314	Processo de leitura de documentos digitalizados e PDF	t	2026-01-26 19:53:41.347185	2026-01-26 19:53:41.344913	471	\N	\N
6597	Montar proposta da Rede Brasil	t	2025-12-22 14:06:15.029732	2025-12-22 14:06:15.028932	421	\N	\N
6598	Passar todos os contatos do CRM	t	2025-12-22 14:06:15.029734	2025-12-22 14:06:15.029041	421	\N	\N
5571	cpf	t	2025-12-09 20:09:08.797927	2025-12-09 20:09:08.79696	313	\N	\N
5572	Esperando Katia validar questão dos CPF	t	2025-12-09 20:09:08.797929	2025-12-09 20:09:08.79706	313	\N	\N
5573	Entender com Katia Processo	t	2025-12-09 20:09:08.79793	2025-12-09 20:09:08.797099	313	\N	\N
5574	Finalizar parte de endereço (numero vazio)	t	2025-12-09 20:09:08.797931	2025-12-09 20:09:08.79713	313	\N	\N
5575	Finalizar parte do endereço (string no campo de número)	t	2025-12-09 20:09:08.797931	2025-12-09 20:09:08.797157	313	\N	\N
5576	Implementar o envio de email para caso seja erro de endereço e não seja nenhum desses casos	t	2025-12-09 20:09:08.797932	2025-12-09 20:09:08.797184	313	\N	\N
5577	Validar com a companheira Katia	f	2025-12-09 20:09:08.797932	\N	313	\N	\N
6599	Revisar proposta do Eric amigo da Giu	t	2025-12-22 14:06:15.029735	2025-12-22 14:06:15.02908	421	\N	\N
5587	Aguardadno revisão do Matheus - 18/11	t	2025-12-09 20:10:36.768575	2025-12-09 20:10:36.767779	333	\N	\N
5588	testar novos arquivos que pdf que o matheus enviou para ver se da match	t	2025-12-09 20:10:36.768576	2025-12-09 20:10:36.767888	333	\N	\N
5589	Organizar com Matheus envio dos arquivos de forma mais estruturada	t	2025-12-09 20:10:36.768577	2025-12-09 20:10:36.767922	333	\N	\N
5590	TEste em andamento - 28/11 - cobrar Matheus	t	2025-12-09 20:10:36.768578	2025-12-09 20:10:36.767951	333	\N	\N
7008	vou adicionar mais alguns campos daa ficha tecnica.	f	2026-01-12 14:07:16.235247	\N	332	\N	falta adicionar o upload de xlsx (tinha esquecido )
7009	aguardando o dominio da aplicaaçao	t	2026-01-12 14:07:16.235249	2026-01-12 14:07:16.232032	332	\N	vitor pediu para esperar
7010	fazer testes para validaçao e liberar para a galera da oaz	t	2026-01-12 14:07:16.23525	2026-01-12 14:07:16.232083	332	\N	\N
7011	Categorização de produtos importados: Sistema passará a gerenciar produtos importados incluindo roupas, decoração, acessórios, bijuteria e bolsas - será necessário criar sessão para importados com categorias apropriadas	t	2026-01-12 14:07:16.235251	2026-01-12 14:07:16.232116	332	\N	\N
7012	Campo "faixa de preço" deve ser opcional (não obrigatório) pensando em uploads em lote	t	2026-01-12 14:07:16.235253	2026-01-12 14:07:16.23217	332	\N	\N
7013	Campo "tecido principal" é equivalente a "matéria-prima e composição" - manter terminologia consistente	t	2026-01-12 14:07:16.235254	2026-01-12 14:07:16.2322	332	\N	\N
7014	Garantir que campos de fornecedor, corner, tecido principal e estilista capturem informações corretas	t	2026-01-12 14:07:16.235255	2026-01-12 14:07:16.232229	332	\N	\N
7015	Upload em lote: Implementar funcionalidade para subir múltiplos produtos de uma vez (similar ao que foi feito com currículos no RH)	t	2026-01-12 14:07:16.235256	2026-01-12 14:07:16.232266	332	\N	\N
7016	Renomear "kit de etiquetas" para "observações e aviamentos" para padronização com documentação	t	2026-01-12 14:07:16.235256	2026-01-12 14:07:16.232307	332	\N	\N
7017	Renan abrir demanda	t	2026-01-12 14:07:16.235257	2026-01-12 14:07:16.232343	332	\N	\N
7018	hoje tem treinamento as 14h com a equipe.	t	2026-01-12 14:07:16.235258	2026-01-12 14:07:16.232372	332	\N	\N
7019	17/12 - cobrei o matheus hoje dos testes	t	2026-01-12 14:07:16.235258	2026-01-12 14:07:16.2324	332	\N	\N
7020	Vou entender com o matheus como podemos integrar o fluxograma dentro do ficha tecnica	t	2026-01-12 14:07:16.235259	2026-01-12 14:07:16.232428	332	2025-12-10	\N
7021	Incluir grupos e sub grupos	t	2026-01-12 14:07:16.235259	2026-01-12 14:07:16.232541	332	\N	\N
7022	Incluir faixa de preço - P1 até P12	t	2026-01-12 14:07:16.23526	2026-01-12 14:07:16.232592	332	\N	\N
7023	Fazer pré cadastro de fornecedores	t	2026-01-12 14:07:16.23526	2026-01-12 14:07:16.232619	332	\N	\N
7024	Ajustar botão de cadastro de fornecedores	t	2026-01-12 14:07:16.235261	2026-01-12 14:07:16.232645	332	\N	\N
7025	Aguardando o overview do matheus com a galera da Oaz.	t	2026-01-12 14:07:16.235261	2026-01-12 14:07:16.23267	332	\N	\N
7026	Reunião 10/12 - ve e cobrar	t	2026-01-12 14:07:16.235262	2026-01-12 14:07:16.232696	332	\N	\N
7027	Filtro por materiais: Adicionar filtro de busca de fornecedores por materiais fornecidos (ex: filtrar fornecedores de linha)	t	2026-01-12 14:07:16.235263	2026-01-12 14:07:16.232723	332	\N	\N
7028	Aumento do limite de upload: Aumentar tamanho máximo de arquivos permitidos	t	2026-01-12 14:07:16.235263	2026-01-12 14:07:16.232749	332	\N	\N
7029	Campo de status do produto: Criar campo para indicar se produto está em desenvolvimento ou concluído, guardando datas de entrada e mudança de status para geração de relatórios futuros	t	2026-01-12 14:07:16.235264	2026-01-12 14:07:16.232776	332	\N	\N
7030	Modal de associações: Implementar visualização dos produtos associados a cada fornecedor (através do modal com ícone de três pontos)	t	2026-01-12 14:07:16.235264	2026-01-12 14:07:16.232805	332	\N	\N
7163	revisar cadastro de RPA	t	2026-01-21 20:08:20.50593	2026-01-21 20:08:20.503547	375	\N	\N
7164	criar dominio	t	2026-01-21 20:08:20.505933	2026-01-21 20:08:20.503762	375	\N	\N
7165	Recadastrar robos que estavem no bacno do Replit - Plano de migração	t	2026-01-21 20:08:20.505933	2026-01-21 20:08:20.503806	375	\N	\N
7166	Log de execuções de comandos	t	2026-01-21 20:08:20.505934	2026-01-21 20:08:20.503861	375	\N	\N
6460	Agendar reunião com Patricia esse semana - 18/11	f	2025-12-18 20:52:49.157451	\N	348	\N	\N
7167	Pagina para gerenciar comandos refeita	t	2026-01-21 20:08:20.505935	2026-01-21 20:08:20.503894	375	\N	\N
7168	Reordenação dos cards de RPA	t	2026-01-21 20:08:20.505935	2026-01-21 20:08:20.50394	375	\N	\N
7169	Atualização da LIB para suportar novos comandos	t	2026-01-21 20:08:20.505936	2026-01-21 20:08:20.503969	375	\N	\N
7170	Agendamento de comandos implementado no sistema	t	2026-01-21 20:08:20.505937	2026-01-21 20:08:20.504022	375	\N	\N
7171	Sistema de agendamento enviados a lib para que ela seja responsável pelo disparto do comando	t	2026-01-21 20:08:20.505937	2026-01-21 20:08:20.50405	375	\N	\N
7172	Segunda apresentação terça - 02/12	t	2026-01-21 20:08:20.505938	2026-01-21 20:08:20.504078	375	\N	\N
7173	Colocar o pypi.org	t	2026-01-21 20:08:20.505939	2026-01-21 20:08:20.504106	375	\N	\N
7174	MElhorar cronologia	t	2026-01-21 20:08:20.505939	2026-01-21 20:08:20.504142	375	\N	\N
7175	Esconder item "regras de automação"	t	2026-01-21 20:08:20.50594	2026-01-21 20:08:20.50417	375	\N	\N
7176	Correção do scroll do preview	t	2026-01-21 20:08:20.505941	2026-01-21 20:08:20.504198	375	\N	\N
7177	Criação de miniaturas para exibição em painel	t	2026-01-21 20:08:20.505941	2026-01-21 20:08:20.504226	375	\N	\N
7178	Corrigir erro na execução de comandos, quando publicado	t	2026-01-21 20:08:20.505942	2026-01-21 20:08:20.504253	375	\N	\N
7179	Elaboração do documento que servirá para o inicio do projeto	t	2026-01-21 20:08:20.505943	2026-01-21 20:08:20.504307	375	\N	\N
7180	Apresentação da documentação para o Felipe	t	2026-01-21 20:08:20.505943	2026-01-21 20:08:20.504335	375	\N	\N
7181	Inicio do desenvolvimento com a construção do layout	t	2026-01-21 20:08:20.505944	2026-01-21 20:08:20.504363	375	\N	\N
7182	Desenvolvimentos de todas as telas do layout	t	2026-01-21 20:08:20.505945	2026-01-21 20:08:20.504391	375	\N	\N
7183	Analise no sistema de socket para definir melhor funcionamento no Replit	t	2026-01-21 20:08:20.505945	2026-01-21 20:08:20.50442	375	\N	\N
6600	Enviar os documentos necessários para o IFES	t	2025-12-22 14:06:15.029736	2025-12-22 14:06:15.029114	421	\N	\N
7184	Criar documentação de apoio ao desenvolvedor	t	2026-01-21 20:08:20.505946	2026-01-21 20:08:20.504447	375	\N	\N
7185	construção da Lib de conexão e funções para o RPA client	t	2026-01-21 20:08:20.505947	2026-01-21 20:08:20.504474	375	\N	\N
6641	Esta em teste com Matheus	f	2025-12-23 21:17:41.992423	\N	394	2025-12-29	\N
6754	Aguardando retorno para desligar o atual	f	2026-01-05 19:38:29.60017	\N	344	\N	\N
7186	Apresentação do primeiro funcionamento de telemetria para o Wallace	t	2026-01-21 20:08:20.505947	2026-01-21 20:08:20.504502	375	\N	\N
7187	Apresentação validada, seguimos para o desenvolvimento dos comandos	t	2026-01-21 20:08:20.505948	2026-01-21 20:08:20.50453	375	\N	\N
7188	Comandos com e sem paraemtros	t	2026-01-21 20:08:20.505949	2026-01-21 20:08:20.504557	375	\N	\N
7189	Comandos agendados ou execuções imediatas	t	2026-01-21 20:08:20.505949	2026-01-21 20:08:20.504584	375	\N	\N
7237	aguardando demanda do cliente, pois ja esta em teste e ate agora tudo OK	t	2026-01-23 20:23:44.294074	2026-01-23 20:23:44.292183	403	\N	\N
7238	adição de mais um dominio para envio de mails	t	2026-01-23 20:23:44.294095	2026-01-23 20:23:44.292282	403	\N	\N
7239	correção nos resultados dos filtros	t	2026-01-23 20:23:44.294096	2026-01-23 20:23:44.292318	403	\N	\N
6755	Corrigir pequenos bugs de shoppings de fora do ES	t	2026-01-05 19:38:29.600174	2026-01-05 19:38:29.595289	344	\N	\N
7240	Inclusão de novos filtros	t	2026-01-23 20:23:44.294097	2026-01-23 20:23:44.292348	403	\N	\N
7241	Sistema em teste com o cliente	t	2026-01-23 20:23:44.294097	2026-01-23 20:23:44.292376	403	\N	\N
6267	Enviado mensagem para a Julia para reunião de BrainStorm.	t	2025-12-16 20:10:11.950822	2025-12-16 20:10:11.94962	347	\N	\N
7242	Aguardando teste - Andrey detalhar	t	2026-01-23 20:23:44.294098	2026-01-23 20:23:44.292403	403	\N	\N
7243	Limite de KRs aumentado - Agora voce pode criar ate 20 KRs por objetivo (antes era 5)	t	2026-01-23 20:23:44.294099	2026-01-23 20:23:44.29243	403	\N	\N
7244	Atividades dentro do KR - Cada KR agora tem uma lista de atividades/tarefas (checklist) para detalhar o que precisa ser feito. Voce pode adicionar, marcar como concluido e atribuir responsaveis	t	2026-01-23 20:23:44.294099	2026-01-23 20:23:44.292463	403	\N	\N
6268	Aguardando a Julia com a liberação da gravação da reunião de conselho de todos os participantes - 18/11	t	2025-12-16 20:10:11.950824	2025-12-16 20:10:11.949719	347	\N	\N
6269	Aguardando a primeira gravação e transcrição local do projeto.	t	2025-12-16 20:10:11.950825	2025-12-16 20:10:11.949754	347	\N	\N
6270	Aguardando Julia enviar NDA	f	2025-12-16 20:10:11.950825	\N	347	\N	\N
5699	Colocar no RPA da Inovai	t	2025-12-10 19:42:46.013297	2025-12-10 19:42:46.012626	377	\N	\N
5700	classificar as despesas com o Humberto	t	2025-12-10 19:42:46.013298	2025-12-10 19:42:46.012738	377	\N	\N
6768	Cobrar Humberto	t	2026-01-05 20:09:50.403599	2026-01-05 20:09:50.402519	324	\N	\N
6769	Problema no login do salesforce,	t	2026-01-05 20:09:50.4036	2026-01-05 20:09:50.402649	324	\N	\N
6770	Cobrar David	t	2026-01-05 20:09:50.403601	2026-01-05 20:09:50.402696	324	\N	\N
6771	Listar dentro do sistema todo o retorno exatamente igual ao AZtronic	t	2026-01-05 20:18:52.776004	2026-01-05 20:18:52.775042	437	\N	\N
6772	Executar o RPA completo fazendo as baixas com o zip disponível	t	2026-01-05 20:18:52.776005	2026-01-05 20:18:52.775174	437	\N	\N
6773	Baixar esse zip no servidor antes de começar a executar o RPA	t	2026-01-05 20:18:52.776006	2026-01-05 20:18:52.775209	437	\N	\N
6774	Buscar todos os arquivos diários disponibilizados e criar um zip	t	2026-01-05 20:18:52.776006	2026-01-05 20:18:52.775239	437	\N	\N
6775	Subir esse zip diariamente para o drive do Hub substituindo o zip anterior	t	2026-01-05 20:18:52.776007	2026-01-05 20:18:52.775266	437	\N	\N
6776	Criar um cron para rodar esse processo diariamente 8:05h	t	2026-01-05 20:18:52.776008	2026-01-05 20:18:52.775294	437	\N	\N
6777	Enviar os e-mails para a Sá e para as filiais de acordo com as regras estabelecidas	t	2026-01-05 20:18:52.776009	2026-01-05 20:18:52.775322	437	\N	\N
7245	Multiplos responsaveis - Tanto Objetivos quanto KRs agora aceitam varios responsaveis (nao apenas 1). Todos os co-responsaveis podem editar	t	2026-01-23 20:23:44.2941	2026-01-23 20:23:44.29249	403	\N	\N
7246	Multiplas equipes por KR - Um KR pode estar associado a varios Squads/Times para projetos cross-funcionais	t	2026-01-23 20:23:44.2941	2026-01-23 20:23:44.292517	403	\N	\N
7247	Focos Semanais corrigido - Agora puxa corretamente os KRs que voce criou e os que voce e co-responsavel	t	2026-01-23 20:23:44.294101	2026-01-23 20:23:44.292543	403	\N	\N
7248	Historico de focos dentro do KR - Ao abrir um KR, voce ve o historico de focos semanais relacionados ali mesmo	t	2026-01-23 20:23:44.294102	2026-01-23 20:23:44.29257	403	\N	\N
7249	Area vs Squad separados:  Area = estrutura fixa do usuario (Atacado, Estilo, Gente & Gestao, etc.) Squad = grupo multiarea para projetos (usuario pode participar de varios)	t	2026-01-23 20:23:44.294102	2026-01-23 20:23:44.292598	403	\N	\N
7035	Cadastrar a rede brasil como cliente no sistema e subir o primeiro projeto deles	t	2026-01-12 15:39:55.219747	2026-01-12 15:39:55.214518	436	\N	\N
7036	Finalizar e corrigir o contrato da rede brasil e enviar para assinatura	t	2026-01-12 15:39:55.219751	2026-01-12 15:39:55.214628	436	\N	\N
7037	Ler e responder o email do Alvaro da Faperj	t	2026-01-12 15:39:55.219752	2026-01-12 15:39:55.214666	436	\N	\N
7038	Fazer reunião e documento o primeiro projeto da Rede Brasil	t	2026-01-12 15:39:55.219752	2026-01-12 15:39:55.214698	436	\N	\N
7039	Entender melhor o sistema sugerido pela Juliana OAZ.	t	2026-01-12 15:39:55.219753	2026-01-12 15:39:55.214727	436	\N	\N
7040	Mandar mensagem para o Tanure, o Jean e o Hudson. Cada um com uma estrategia de retomada.	t	2026-01-12 15:39:55.219754	2026-01-12 15:39:55.21476	436	\N	\N
7041	Montar apresentação de Quinta Educhat com o feedback do Waltinho.	t	2026-01-12 15:39:55.219755	2026-01-12 15:39:55.214795	436	\N	\N
7042	Passar todos os contatos do CRM	t	2026-01-12 15:39:55.219755	2026-01-12 15:39:55.214839	436	\N	\N
7043	Montar a estrutura operacional do Time de programação, financeiro e QA	t	2026-01-12 15:39:55.219756	2026-01-12 15:39:55.21487	436	\N	\N
5449	Ronald abrir Demanda	t	2025-12-08 20:10:52.501885	2025-12-08 20:10:52.500953	370	\N	\N
5450	Ajustar pedidos da Júlia	t	2025-12-08 20:10:52.501886	2025-12-08 20:10:52.501055	370	\N	\N
5451	Criar carteira para importação CSV/EXCEL	t	2025-12-08 20:10:52.501887	2025-12-08 20:10:52.50109	370	\N	\N
5452	Criar produtos	t	2025-12-08 20:10:52.501888	2025-12-08 20:10:52.501119	370	\N	\N
5453	Cria coleção	t	2025-12-08 20:10:52.501888	2025-12-08 20:10:52.501146	370	\N	\N
5454	Função para criar produtos/coleção/marca ao importar CSV/EXCEL caso tenham esses dados	t	2025-12-08 20:10:52.501889	2025-12-08 20:10:52.501174	370	\N	\N
5455	Aguardando novos arquivos que será enviados pela julia para melhor mapeamentos e entendimento dos dados na utilização do sisttema	t	2025-12-08 20:10:52.50189	2025-12-08 20:10:52.501202	370	\N	\N
7044	Fazer a primeira reunião de UX do Educhat com o Thomaz	t	2026-01-12 15:39:55.219757	2026-01-12 15:39:55.214899	436	\N	\N
7045	Montar apresentação da Estrutura comercial	t	2026-01-12 15:39:55.219757	2026-01-12 15:39:55.214926	436	\N	\N
7046	Finalizar o posicionamento de Marca do EduChat com o Fabricio.	t	2026-01-12 15:39:55.219758	2026-01-12 15:39:55.214954	436	\N	\N
7047	Reunião de posicionamento de Marca Educhat.	t	2026-01-12 15:39:55.219759	2026-01-12 15:39:55.214981	436	\N	\N
7192	Felipe - Obter acesso do banco de dados do Bigcuery	t	2026-01-21 20:12:35.569123	2026-01-21 20:12:35.568572	408	\N	\N
7250	Importacao de usuarios via planilha - Faca upload de Excel/CSV com emails @oaz.co e o sistema envia convites automaticamente	t	2026-01-23 20:23:44.294103	2026-01-23 20:23:44.292626	403	\N	\N
7251	Auto-cadastro - Funcionarios @oaz.co podem solicitar acesso pela tela de login e recebem email com link para definir senha	t	2026-01-23 20:23:44.294104	2026-01-23 20:23:44.292652	403	\N	\N
7260	Reuniao com Alice para gravação e mapeamento do processo de cadastro do contrato entre o modulo de comercial e de contrato,.	t	2026-01-23 20:36:55.545763	2026-01-23 20:36:55.54492	407	\N	\N
7261	Reuniao de Brainstorm com o Hudson e Aninha	t	2026-01-23 20:36:55.545765	2026-01-23 20:36:55.545029	407	\N	\N
7262	Documentação do projeto.	t	2026-01-23 20:36:55.545766	2026-01-23 20:36:55.545094	407	\N	\N
7315	Inicio da navegação no Autbahn	t	2026-01-26 19:53:41.347186	2026-01-26 19:53:41.344941	471	\N	\N
6883	Aguardando novos direcionamentos para construção do novo EduChat	f	2026-01-05 22:59:42.371433	\N	280	\N	\N
6884	As avaliações agora usam dados do perfil para gerar uma avaliação adequada para o aluno	t	2026-01-05 22:59:42.371436	2026-01-05 22:59:42.369312	280	\N	\N
6885	Revisão geral na tela de Peril/Suas conquistas	t	2026-01-05 22:59:42.371437	2026-01-05 22:59:42.369358	280	\N	\N
6886	Acrescentado tela explicativa para o sistema de gamificação em (Perfil / Conquistas))	t	2026-01-05 22:59:42.371437	2026-01-05 22:59:42.36939	280	\N	\N
6887	Novo layout para tela de Configurar lembretes	t	2026-01-05 22:59:42.371438	2026-01-05 22:59:42.369421	280	\N	\N
6888	Central de Ajuda foi toda refeita	t	2026-01-05 22:59:42.371439	2026-01-05 22:59:42.369448	280	\N	\N
6889	Logado como ADM global, permitir ver e medir o desempenho do uso do sistema pelos alunos na escola.	t	2026-01-05 22:59:42.37144	2026-01-05 22:59:42.369476	280	\N	\N
6890	(Analytics de Engajamento) Logado como ADM global, permitir ver e medir o desempenho do uso do sistema pelos alunos na escola.	t	2026-01-05 22:59:42.37144	2026-01-05 22:59:42.369503	280	\N	\N
6891	Colocar chat para falar com a mochila	t	2026-01-05 22:59:42.371441	2026-01-05 22:59:42.369529	280	\N	\N
6892	Colocar chat para falar com a anaminese	t	2026-01-05 22:59:42.371442	2026-01-05 22:59:42.369558	280	\N	\N
6893	Usuário logar automaticamente ao clicar para logar com Google	t	2026-01-05 22:59:42.371442	2026-01-05 22:59:42.369586	280	\N	\N
6670	Vamos fazer um brainstorm com a garela da oaz para entender esse projeto.	f	2025-12-26 14:09:34.37017	\N	420	\N	\N
6671	Entender o processo, e como podemos extrair os dados das transportadoras.	t	2025-12-26 14:09:34.370173	2025-12-26 14:09:34.369582	420	\N	\N
6673	em testes	f	2025-12-26 14:10:23.593606	\N	336	\N	\N
6511	d) A condição do item nem sempre é salva corretamente, no salesforce /na cotações existentes.	t	2025-12-19 20:36:58.128564	2025-12-19 20:36:58.12115	180	\N	\N
6512	c)Em cotações existentes o filtro de invoice não funciona. *importante saber se o quote virou venda ou não. (coletar infor da salesforce e atualizar status da quote do sistema de quotes)	t	2025-12-19 20:36:58.128569	2025-12-19 20:36:58.121278	180	\N	\N
6513	7)\tTentar automatizar a coleta de emails para todo dia em um horário “x”.	t	2025-12-19 20:36:58.128569	2025-12-19 20:36:58.121338	180	\N	\N
6514	1) Mudar sistema de autenticação, aumentar janela de atualização.	t	2025-12-19 20:36:58.12857	2025-12-19 20:36:58.121378	180	\N	\N
6515	2)  \tAo sincronizar os emails a hora do email esta errada, o sistema tem que pegar a hora e data corretemente do email para que a ordem seja correta.	t	2025-12-19 20:36:58.128573	2025-12-19 20:36:58.121412	180	\N	\N
6516	3) Quotations/My quotations	t	2025-12-19 20:36:58.128574	2025-12-19 20:36:58.121443	180	\N	\N
6517	a) Mostra date created precisamos mostrar também a data do email original.	t	2025-12-19 20:36:58.128575	2025-12-19 20:36:58.121476	180	\N	\N
6518	b.\tItem code, mostrar em quotes com mais de uma peça todos os item codes já na quote.	t	2025-12-19 20:36:58.128575	2025-12-19 20:36:58.121644	180	\N	\N
6519	f.\tNa area de my quotations, ao filtrar os emails por part number, buyer/seller e date o usuário ao criar uma quote quando volta para a pagina de quotations ele perde o filtro existente. (criar uma memoria de filtro)	t	2025-12-19 20:36:58.128576	2025-12-19 20:36:58.121706	180	\N	\N
6520	6)\tCaso o usuário não faça a sincronização dos emails regularmente o sistema não tem uma logica de coletar os emails a partir do ultimo email processado no sistema. (Isso deixa emails antigos perdidos o que pode fazer com que Humberto perca negócios.)	t	2025-12-19 20:36:58.128577	2025-12-19 20:36:58.121741	180	\N	\N
6642	A Bola esta com o matheus. preciso de testes para validar, e mais documentos para treinar o consultor	t	2025-12-23 21:17:41.992425	2025-12-23 21:17:41.991508	394	2025-12-22	\N
6174	Criar orçamento, cronograma e documentação para o Saulo - Fundo Joaquim	t	2025-12-16 14:49:29.290911	2025-12-16 14:49:29.288046	393	\N	\N
6175	Criar o projeto de OKR da OAZ dentro do sistema de gestão	t	2025-12-16 14:49:29.290913	2025-12-16 14:49:29.288239	393	\N	\N
6176	Entender o novo projeto que a OAZ quer começar.	t	2025-12-16 14:49:29.290914	2025-12-16 14:49:29.288291	393	\N	\N
6177	Fazer ativação dos clientes e repassar o CRM	t	2025-12-16 14:49:29.290915	2025-12-16 14:49:29.288327	393	\N	\N
6178	Reunião de entendimento de proximos passos com o projeto de banco de imagens da OAZ( Reunião com a Julia)	t	2025-12-16 14:49:29.290918	2025-12-16 14:49:29.288358	393	\N	\N
6643	Estruturar a saida da resposta do chat.	t	2025-12-23 21:17:41.992426	2025-12-23 21:17:41.991652	394	\N	\N
6644	Ja iniciei o desenvolvimento do consultor geral. importei os arquivos, estou estruturando o chat para poder trazer as informaçoes	t	2025-12-23 21:17:41.992426	2025-12-23 21:17:41.991688	394	\N	\N
6645	Fazer testes de chuncks	t	2025-12-23 21:17:41.992427	2025-12-23 21:17:41.991718	394	\N	teste feito para verificar se a resposta esta vindo com contexto.
6646	fazer deploy do sistema e mandar para o matheus testar.	t	2025-12-23 21:17:41.992428	2025-12-23 21:17:41.991753	394	\N	\N
6059	Reelaboração de layout	t	2025-12-15 20:13:50.669914	2025-12-15 20:13:50.668914	405	\N	\N
6060	Implementeação de uso de Regex para extração de dados dos pdf´s	t	2025-12-15 20:13:50.669916	2025-12-15 20:13:50.669018	405	\N	\N
6061	Criar ambiente Batch para administrar o upload e processamento de arquivos	t	2025-12-15 20:13:50.669916	2025-12-15 20:13:50.66905	405	\N	\N
6179	Aprofundar a frente de produtos fechando documentação e primeiros passos para o primeiro produto.	t	2025-12-16 14:49:29.290919	2025-12-16 14:49:29.288387	393	\N	\N
6180	Liberar o acesso para testes do produto de monitoramento para o Wallace Betunel	t	2025-12-16 14:49:29.290919	2025-12-16 14:49:29.288417	393	\N	\N
6181	Montar proposta para o grupo Salta.	t	2025-12-16 14:49:29.29092	2025-12-16 14:49:29.288455	393	\N	\N
6182	Entender os dois novos projetos de shopping da Sá Cavalcante e incluir documentação no sistema	t	2025-12-16 14:49:29.290921	2025-12-16 14:49:29.288508	393	\N	\N
6183	Cobrar liberação da Verba da Faperj a Giu	t	2025-12-16 14:49:29.290921	2025-12-16 14:49:29.288539	393	\N	\N
6184	Subir o novo projeto de RPA da Sá Cavalcante no sistema de gerenciamento de projeto.	t	2025-12-16 14:49:29.290922	2025-12-16 14:49:29.288568	393	\N	\N
6186	Ajustar questão da senha ao aditar um usuário - Vitor	t	2025-12-16 19:17:08.979499	2025-12-16 19:17:08.974589	189	\N	\N
6187	Retirar o botao de "filtrar ". o flitro vai ser escolhido ao selecionar.	t	2025-12-16 19:17:08.979504	2025-12-16 19:17:08.974705	189	\N	\N
6188	Adicionar botão de editar cadastros de clientes.(admin)	t	2025-12-16 19:17:08.979504	2025-12-16 19:17:08.974737	189	\N	\N
6189	Adicionar botão de editar cadastros de clientes.(usuarios)	t	2025-12-16 19:17:08.979505	2025-12-16 19:17:08.974762	189	\N	\N
6190	Poder adicionar vários membros no projeto	t	2025-12-16 19:17:08.979507	2025-12-16 19:17:08.974784	189	\N	\N
6191	Ordenar a lista de projeto na hora de abrir uma tarefa	t	2025-12-16 19:17:08.979508	2025-12-16 19:17:08.974803	189	\N	\N
6192	Quando salvar o modal de detalhes de uma tarefa, ja atualizar sem ter que atualizar a pagina, tanto status quanto responsável quanto data - Daniel	t	2025-12-16 19:17:08.979509	2025-12-16 19:17:08.974822	189	\N	\N
6193	Entender e colocar o sistema do CRm criado pelo Gomes em modelo de aba em nosso sistema - Vitor	t	2025-12-16 19:17:08.979509	2025-12-16 19:17:08.974856	189	\N	\N
6194	Quando criar usuário, poder selecionar as abas que o usuário vai ter acesso - Vitor	t	2025-12-16 19:17:08.97951	2025-12-16 19:17:08.974891	189	\N	\N
6195	Poder arrastar card entre as colunas e classificar automaticamente (Pendente, Em andamento e Concluida) - Vitor	t	2025-12-16 19:17:08.97951	2025-12-16 19:17:08.974913	189	\N	\N
6062	Criar pesquisa dinâmica dos dados extraídos	t	2025-12-15 20:13:50.669917	2025-12-15 20:13:50.669107	405	\N	\N
6063	Criar controle de paralelismo para processamento de pdf´s	t	2025-12-15 20:13:50.669917	2025-12-15 20:13:50.669136	405	\N	\N
6064	Para v2 implmentar extração por chunk e reprocessamento de pdf´s para conversão em chunk e posteriormente conversa IA com os dados	f	2025-12-15 20:13:50.669918	\N	405	\N	\N
6065	Normalização dos arquivos a serem enviados para o sistema	t	2025-12-15 20:13:50.669918	2025-12-15 20:13:50.669173	405	\N	\N
6066	Acompanhar todo o processo de envio e processamento de pdf´s inicial	f	2025-12-15 20:13:50.669919	\N	405	\N	\N
6067	Nova função de busca por string no nome do PDF	t	2025-12-15 20:13:50.669919	2025-12-15 20:13:50.669242	405	\N	\N
6068	RPA	t	2025-12-15 20:13:50.669919	2025-12-15 20:13:50.669262	405	\N	\N
6069	Tirar do Replit o projeto	f	2025-12-15 20:13:50.66992	\N	405	\N	\N
6070	Reuniao feita - 12/11 = a galera junto com o thomaz  esta montando o app.	t	2025-12-15 20:15:23.620629	2025-12-15 20:15:23.6107	328	\N	\N
6071	17/11 = Reuniao hoje visando terminar a tela de "home " do app	t	2025-12-15 20:15:23.620634	2025-12-15 20:15:23.610786	328	\N	\N
6072	Implementar a primeira tela de home do BoraBailar	t	2025-12-15 20:15:23.620634	2025-12-15 20:15:23.61081	328	\N	\N
6073	Feita o desenvolvimento da home. hoje (24/11) vai ter uma reuniao para montar outra tela.	t	2025-12-15 20:15:23.620634	2025-12-15 20:15:23.610831	328	\N	\N
6074	trabalhar na logica do app.	t	2025-12-15 20:15:23.620635	2025-12-15 20:15:23.61085	328	\N	\N
6075	reuniao montagem de tela - 26/11	t	2025-12-15 20:15:23.620635	2025-12-15 20:15:23.610867	328	\N	\N
6076	Esperando Josias e Alan aprovarem - Bino cobrar - 02/12	t	2025-12-15 20:15:23.620636	2025-12-15 20:15:23.610885	328	\N	\N
6077	reuniao do BoraBailar hj - 02/12	t	2025-12-15 20:15:23.620636	2025-12-15 20:15:23.610902	328	\N	\N
6078	Renan abrir demana - 02/12	t	2025-12-15 20:15:23.620637	2025-12-15 20:15:23.61092	328	\N	\N
6079	Em relação do app, essa semana nao vamos ter mais nada.	t	2025-12-15 20:15:23.620637	2025-12-15 20:15:23.610937	328	\N	\N
6080	Segunda eu vamos ter outro papo para a montagem das telas.	t	2025-12-15 20:15:23.620637	2025-12-15 20:15:23.610952	328	\N	\N
6081	Fazendo as montagem da tela do BoraBailar : tela de home completa	t	2025-12-15 20:15:23.620638	2025-12-15 20:15:23.610969	328	\N	\N
6082	finalizar tela de queros	t	2025-12-15 20:15:23.620638	2025-12-15 20:15:23.610985	328	\N	\N
6083	tela de "dicas do dia"	t	2025-12-15 20:15:23.620639	2025-12-15 20:15:23.611004	328	\N	\N
6084	tela "momento dança feliz"	t	2025-12-15 20:15:23.620639	2025-12-15 20:15:23.611024	328	\N	\N
6196	Colocar filtro para para filtrar por Usuário tambem - Vitor	t	2025-12-16 19:17:08.979511	2025-12-16 19:17:08.974936	189	\N	\N
6197	Colocar filtros nas abas - Tarefas, Projetos, clientes e Usuários . - Vitor	t	2025-12-16 19:17:08.979511	2025-12-16 19:17:08.974954	189	\N	\N
6198	Adicionar botão para disparo de tarefas para os usuários - Vitor	t	2025-12-16 19:17:08.979511	2025-12-16 19:17:08.975004	189	\N	\N
7224	Patricia usando - Cobrar ate sexta	t	2026-01-23 20:08:18.302549	2026-01-23 20:08:18.297124	387	\N	\N
7225	Fernanda usando o sistema	t	2026-01-23 20:08:18.302551	2026-01-23 20:08:18.297237	387	\N	\N
7226	/Reunião com fernanda - quinta 18/12	t	2026-01-23 20:08:18.302552	2026-01-23 20:08:18.297286	387	\N	\N
7227	Subir para o Google Cloud	t	2026-01-23 20:08:18.302553	2026-01-23 20:08:18.297321	387	\N	\N
7228	testar o máximo de carga para verificação de funcionalidade final.	t	2026-01-23 20:08:18.302556	2026-01-23 20:08:18.29735	387	\N	\N
7229	Fernanda em teste - 04/12	t	2026-01-23 20:08:18.302556	2026-01-23 20:08:18.297378	387	\N	\N
7230	Colocando o processo na base de produção	t	2026-01-23 20:08:18.302557	2026-01-23 20:08:18.297408	387	\N	\N
7231	Mandei para a fernanda, segundo ela enviaria para "as meninas" testarem" sem retorno ainda	t	2026-01-23 20:08:18.302558	2026-01-23 20:08:18.297446	387	\N	\N
6894	Gerenciar Alunos - Último Acesso\tTempo Total\tDias Ativos funcionando    Controle de busca de alunos - layout padronizado	t	2026-01-05 22:59:42.371443	2026-01-05 22:59:42.369615	280	\N	\N
6895	Gerenciar Turmas - layout revisado, controle de busca implementado	t	2026-01-05 22:59:42.371444	2026-01-05 22:59:42.369643	280	\N	\N
6896	Gerenciar Conteúdo - layout revisado, controle de busca implementado	t	2026-01-05 22:59:42.371444	2026-01-05 22:59:42.369671	280	\N	\N
6897	Ajustes nos dados do anamnese que agora servem o prompt e ajusta a resposta do usuário	t	2026-01-05 22:59:42.371445	2026-01-05 22:59:42.369698	280	\N	\N
6898	Filtro de documentos, ajustes de layout na mochila	t	2026-01-05 22:59:42.371446	2026-01-05 22:59:42.369725	280	\N	\N
6899	Aumento de numero de questões para gerar de 5 a 8	t	2026-01-05 22:59:42.371447	2026-01-05 22:59:42.369753	280	\N	\N
6900	Suporte a markdown para respostas formatadas do chat	t	2026-01-05 22:59:42.371447	2026-01-05 22:59:42.369782	280	\N	\N
6901	O tutor agora conhece o aluno e todo o conteúdo que ele precisa aprener	t	2026-01-05 22:59:42.371448	2026-01-05 22:59:42.36981	280	\N	\N
6902	Criado regras de prompt para o tutor;	t	2026-01-05 22:59:42.371449	2026-01-05 22:59:42.369838	280	\N	\N
6903	Implementado indicadores de processamento em todo o projeto;	t	2026-01-05 22:59:42.371449	2026-01-05 22:59:42.369865	280	\N	\N
6904	Suporte a pesquisa aos documentos da mochila do usuário;	t	2026-01-05 22:59:42.37145	2026-01-05 22:59:42.369892	280	\N	\N
6905	Implementado nível de dificuldade para as trilhas (Facil, intermediário e dificil)	t	2026-01-05 22:59:42.37145	2026-01-05 22:59:42.36995	280	\N	\N
6906	Aguardando testes do cliente	f	2026-01-05 22:59:56.051816	\N	346	\N	\N
6907	liberado o desfazer em qualquer sequencia	t	2026-01-05 22:59:56.051818	2026-01-05 22:59:56.049911	346	\N	\N
6908	não calcular juros aos finais de semana	t	2026-01-05 22:59:56.051819	2026-01-05 22:59:56.049956	346	\N	\N
6909	retirar projeto do replit e colocar no antigravity	t	2026-01-05 22:59:56.051819	2026-01-05 22:59:56.049987	346	\N	\N
6910	implementar conceito de juros real e competencia	t	2026-01-05 22:59:56.05182	2026-01-05 22:59:56.050016	346	\N	\N
6911	criar tela de competencia para acompanhamentos dos juros	t	2026-01-05 22:59:56.051821	2026-01-05 22:59:56.050046	346	\N	\N
6912	buscar dados no banco central	t	2026-01-05 22:59:56.051821	2026-01-05 22:59:56.05008	346	\N	\N
6913	implementar detalhamento dos juros diarios	t	2026-01-05 22:59:56.051822	2026-01-05 22:59:56.050106	346	\N	\N
6914	Andrey testando em produção para liberar para o cliente	t	2026-01-05 22:59:56.051823	2026-01-05 22:59:56.050133	346	\N	\N
6915	Integração com API do banco central para obter CDI...	t	2026-01-05 22:59:56.051823	2026-01-05 22:59:56.05016	346	\N	\N
6916	Trava de desfazer\tRígida demais	t	2026-01-05 22:59:56.051824	2026-01-05 22:59:56.050187	346	\N	\N
6917	Competência (juros diários)\tNão existe	t	2026-01-05 22:59:56.051825	2026-01-05 22:59:56.050215	346	\N	\N
6918	Desconto por pontualidade	t	2026-01-05 22:59:56.051825	2026-01-05 22:59:56.050241	346	\N	\N
6919	CDI variável\tNão existe	t	2026-01-05 22:59:56.051826	2026-01-05 22:59:56.050268	346	\N	\N
6920	PRICE vs SAC\tMisturado, precisa formalizar	t	2026-01-05 22:59:56.051827	2026-01-05 22:59:56.050294	346	\N	\N
6921	Enviado mensagem pro Leo perguntando sobre os testes.	t	2026-01-05 22:59:56.051827	2026-01-05 22:59:56.050321	346	\N	\N
6922	Criar opção para campo de carencia para pagamento do principal - 18/11	t	2026-01-05 22:59:56.051828	2026-01-05 22:59:56.050347	346	\N	\N
6923	Correção das datas - 18/11	t	2026-01-05 22:59:56.051829	2026-01-05 22:59:56.050374	346	\N	\N
6924	Elaboração de cronograma - 18/11	t	2026-01-05 22:59:56.051829	2026-01-05 22:59:56.050402	346	\N	\N
6925	Marcar reunião com o Léo - 19/11	t	2026-01-05 22:59:56.05183	2026-01-05 22:59:56.050446	346	\N	\N
6926	reunião marcada para segunda - 24/11	t	2026-01-05 22:59:56.05183	2026-01-05 22:59:56.050473	346	\N	\N
6927	Finalizando a inclusão de contratos manualmente	t	2026-01-05 22:59:56.051831	2026-01-05 22:59:56.0505	346	\N	\N
6928	Andrey abrir demanada	t	2026-01-05 22:59:56.051832	2026-01-05 22:59:56.050528	346	\N	\N
6929	Adicionado metodo complementar de extração de pdf 100% IA	t	2026-01-05 22:59:56.051832	2026-01-05 22:59:56.050562	346	\N	\N
6930	Adição de novos campos nos formularios	t	2026-01-05 22:59:56.051833	2026-01-05 22:59:56.050588	346	\N	\N
6931	Controle de pagamento de parcelas com valores superior ou inferior, com 2 opções de propagação de saldo restante.	t	2026-01-05 22:59:56.051834	2026-01-05 22:59:56.050615	346	\N	\N
6932	TEste de desenvolverdor - Finalização	t	2026-01-05 22:59:56.051834	2026-01-05 22:59:56.050641	346	\N	\N
7074	Emails direcionados a aeropool sistema encaminhe automaticamente para o email do Andy.  (andy@avsalescorp.com)	f	2026-01-13 23:13:19.006175	\N	438	\N	\N
7075	Em cotaçoes existentes o sistema pega a informaçao de condiçao da peça errada. (Por exemplo foi quoted no SF SV e esta OH no sistema)	f	2026-01-13 23:13:19.006177	\N	438	\N	\N
7076	Sistema erra as vezes em criar a quote no SF. O sistema identifica corretamente a empresa e contato, checa no salesforce corretamente porem ao criar a quote no salesforce a empresa e diferente.	f	2026-01-13 23:13:19.006178	\N	438	\N	\N
7077	Deploy o sistema de quotes ate quarta!	f	2026-01-13 23:13:19.006179	\N	438	\N	\N
7078	Possibilitar que o usuario consiga cadastrar uma peça, condiçao, lead time, warranty e tag no banco de peças do sistema direto da tela de create in salesforce.	t	2026-01-13 23:13:19.006181	2026-01-13 23:13:19.00338	438	\N	\N
7079	No banco de peças , deixar que o usuario consiga cadastrar peças alternativas	t	2026-01-13 23:13:19.006182	2026-01-13 23:13:19.00342	438	\N	\N
7080	Hora de processamento de email esta errada "processado em" dentro de processamento de emails.	t	2026-01-13 23:13:19.006183	2026-01-13 23:13:19.003452	438	\N	\N
7081	adicionar data na seçao de cotaçoes existentes	t	2026-01-13 23:13:19.006184	2026-01-13 23:13:19.003495	438	\N	\N
7082	fazer com que o sistema leia todas as peças da quote e procure todas as peças no banco de peças	t	2026-01-13 23:13:19.006184	2026-01-13 23:13:19.003538	438	\N	\N
7083	receber o xls da base completa de usuários com emails e dados para subir a base	f	2026-01-14 20:17:48.913061	\N	446	\N	\N
7084	Usar o Json para dar o tom de voz para a ia analisar as imagens e gerar descrições baseadas nesse tom de voz	f	2026-01-14 20:19:54.373949	\N	426	\N	\N
7099	Clonar projeto no antigravity para ajustes/melhorias	f	2026-01-14 20:26:54.26595	\N	450	\N	\N
7100	backup da base de dados	f	2026-01-14 20:26:54.265951	\N	450	\N	\N
7101	criar instância na vm do google e subir projeto para produção lá	f	2026-01-14 20:26:54.265952	\N	450	\N	\N
7102	Subir git para a inova	t	2026-01-14 20:26:54.265953	2026-01-14 20:26:54.26534	450	\N	\N
7103	Receber planilhas padronizadas da base de estoque, produtos e clientes com cnpj	f	2026-01-14 20:28:55.588616	\N	349	\N	\N
7104	criar tela de login para clientes, calcular a taxa de entrega por estado integrada ao cnpj de cada cliente, atualizando o preço dos produtos automaticamente para cada um deles	f	2026-01-14 20:28:55.588618	\N	349	\N	\N
7105	Aguardar planilhas padronizadas de estoque/produto do Raphael, prazo de entrega até o final de semana	t	2026-01-14 20:28:55.588619	2026-01-14 20:28:55.587735	349	\N	\N
7106	Aguardando feedback do Renato - 18/11	t	2026-01-14 20:28:55.588619	2026-01-14 20:28:55.587773	349	\N	\N
7107	Aguardar reunião de sexta 21/11	t	2026-01-14 20:28:55.58862	2026-01-14 20:28:55.587817	349	\N	\N
7108	ROnald abrir demanda	t	2026-01-14 20:28:55.588621	2026-01-14 20:28:55.587844	349	\N	\N
7109	Visualização de estoque apenas para o admin no dashboard	t	2026-01-14 20:28:55.588621	2026-01-14 20:28:55.587872	349	\N	\N
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public."user" (id, nome, sobrenome, email, password_hash, is_admin, created_at, reset_token, reset_token_expires, acesso_clientes, acesso_projetos, acesso_tarefas, acesso_kanban, acesso_crm, receber_notificacoes) FROM stdin;
1	Administrador	Sistema	admin@sistema.com	scrypt:32768:8:1$L6NVjJUxY2e66vRg$445e656031053af0ec18a3413822cc90ec06f9346e208d57dd91b82ab4eb3aad3a8fc7d2a9db008a98ecfd889ee49680785fb5b85c4aa78e7a3b85aeaecccff3	t	2025-08-26 21:59:59.9196	\N	\N	t	t	t	t	t	t
3	aldo	lorenzo	aldo@inovailab.com	scrypt:32768:8:1$DXpTOxPe9gjuKp0Z$bc28770ee111da1b062d9080f99a792786256b93e393ff07b846f6ef57ade97764b569204c38817f712d6f44c77c94329cf1a6cf38ff8c10c623cb23be20df36	f	2025-08-25 18:05:14.786235	\N	\N	t	t	t	t	t	t
5	Renan	Gomes	renan@inovailab.com	scrypt:32768:8:1$akLtOJeXUiQQSsmA$e7036afe0509e74ace7804bdb5e0a076a89be6d7817e298be945011a40b7ed2648f48ec3ff48f92218b0ef653f930966d5264656eb065671a52abcbff1579041	f	2025-08-26 19:19:42.046212	\N	\N	t	t	t	t	t	t
4	vitor	gomes	vitor@inovailab.com	scrypt:32768:8:1$PKB1YIVESQk2hUnN$f8b3178a599bf5378db78083e81b329191a82add86240b0f2da2dd609b76f5774a0595978ce2a5063591e03e8c5f4c9cc01bc9e2da76b5dd2354f00fc9a69b8a	f	2025-08-25 19:33:26.525843	\N	\N	t	t	t	t	t	t
14	Isabella	Nascimento	isabella@inovailab.com	scrypt:32768:8:1$QtZbmwB2sSxDg4Zf$563adde47fa401c1c0cf1690d3aa328cf9bf2f5052143b7c2f3170b02772ec089785294a64eae801d8f01d2feab2f64eb13466f6b5bb434afdeeb64b5a63d166	f	2026-01-09 19:46:06.615766	\N	\N	t	t	t	t	t	t
8	Ronald	Mattos 	ronald@inovailab.com	scrypt:32768:8:1$MRmYcnBPaiTCXRl6$46c812e551528f522bf22ed9e16e7c4449e0c5d323da25347e9e033be2dd9b60cf60caafd52ae70c26a72604219f79d892d6488446073f9e5e08327f5b0ee9a5	f	2025-10-13 17:24:06.204848	\N	\N	t	t	t	t	t	t
15	Luiza 	Mayeur	luiza@inovailab.com	scrypt:32768:8:1$6cASQIr9BCaqPvdA$2067b165273b644db0ee6c8b1c6d331affe99f245673af95c48820be3b57950522f8c91ed3dac2d5fe862901cbaabe5d21b464062e526cb109fbd8d0b66094f7	t	2026-01-22 18:05:36.234969	\N	\N	t	t	t	t	t	t
7	joao	Clark	joao@inovailab.com	scrypt:32768:8:1$oaPBKeP17kix6JZl$dad551e7bed71a2e6596c362741a82d44aefa05b040aa8c1d93e7a23ab91878028111d02139acebfa913d159feb5b5c341aae08dc83dfde452ee8be1d9406137	f	2025-09-09 16:55:46.27304	-chZAkVa2453_72LR1S86r3dIGJKdloUoXAiisAFOOY	2025-10-14 17:38:19.45721	t	t	t	t	t	t
2	felipe	gomes	felipe@inovailab.com	scrypt:32768:8:1$QOZHsDj4wNK1DMMI$d09514bb1129499a0ec0500b197061a996ece75c5acaf6810b1860a5784146db6d8030e8f53466812fe20cbeeca69573e287fdc7e6144ad438db7ee4aff6855c	f	2025-08-25 14:20:03.996041	\N	\N	t	t	t	t	t	t
10	Andrey 	Barreto	andrey@inovailab.com	scrypt:32768:8:1$152SsTTpQPObVDhf$e73c9b2308bce6afea68e29e7f438ef397d0512b1c05b1070756ca11a1623af37dada0e034a299e9d1f85191a1d1c7c6307457fe04a9bb085ee90a9050b23d68	f	2025-10-30 17:13:20.692745	\N	\N	t	t	t	t	t	t
9	Renatta	Novaes	renatta@inovailab.com	scrypt:32768:8:1$qkSp0TRxlK1jf0Sn$5550e7f0fff558094c3c7b2beb31b63423567a02517ea2db0a0543b7d6823a18f6a94ec4a594fd4f136560dd746cbf89c37a8181fee3deca2231844eef118e55	f	2025-10-13 20:39:24.993375	\N	\N	t	t	t	t	t	t
12	Giulliana	alegretti	giulliana@bizarte.com.br	scrypt:32768:8:1$uIBNJv2WXNrxVbuI$c955ee609eae63d49de6b98369c25c1be597785305145c579f3fa23303eb4144e5a0a042f4a90f92a5b80ef6c67d528de1143b78d635984901739681ea1b4e04	f	2025-11-27 16:27:06.483284	\N	\N	f	f	t	t	f	t
6	Daniel	Libar	daniel@inovailab.com	scrypt:32768:8:1$AsuLbLTljiconewt$72f87222eee390ae4872b2c1d94909204cea3d7ae94b756238f06cf32391a7c1e33b47e713b5ecd3253d968915e662f701247510545c2f591e779ed193db55fd	f	2025-08-26 20:56:19.759054	\N	\N	t	t	t	t	t	t
13	matheus	parra	matheus.parra@oaz.co	scrypt:32768:8:1$zN8glV8euv9Rp52Q$af7341c1b69b9198cff9758c984a4b8705e808208c6d9debe27872ccd4dca78fd8d63ae3f612d7553c21637ced7d70b54067b6c3120c8047cd1e00afc50e122c	f	2025-12-01 17:19:43.809455	\N	\N	f	f	t	t	f	f
11	Paulo calarge	calarge	paulo@inovailab.com	scrypt:32768:8:1$4aT1s1uxjyUybdOC$a40c75bf2144c63e8d5f437a450e50a811545133f46b654d35feb190c03c911a1832f09b9aa4168b95a722c18384ab37e1ac66878e3fccb33b9f16bc5bdfcb5d	f	2025-11-17 15:28:21.168184	\N	\N	t	t	t	t	t	t
\.


--
-- Name: replit_database_migrations_v1_id_seq; Type: SEQUENCE SET; Schema: _system; Owner: neondb_owner
--

SELECT pg_catalog.setval('_system.replit_database_migrations_v1_id_seq', 14, true);


--
-- Name: client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.client_id_seq', 11, true);


--
-- Name: comentarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.comentarios_id_seq', 86, true);


--
-- Name: contato_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.contato_files_id_seq', 1, true);


--
-- Name: contatos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.contatos_id_seq', 37, true);


--
-- Name: crm_stages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.crm_stages_id_seq', 9, true);


--
-- Name: file_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.file_categories_id_seq', 6, true);


--
-- Name: lead_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.lead_id_seq', 2, true);


--
-- Name: lead_interaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.lead_interaction_id_seq', 2, true);


--
-- Name: project_api_credentials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.project_api_credentials_id_seq', 1, false);


--
-- Name: project_api_endpoints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.project_api_endpoints_id_seq', 1, false);


--
-- Name: project_api_keys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.project_api_keys_id_seq', 1, false);


--
-- Name: project_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.project_files_id_seq', 4, true);


--
-- Name: project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.project_id_seq', 58, true);


--
-- Name: system_api_keys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.system_api_keys_id_seq', 5, true);


--
-- Name: task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.task_id_seq', 508, true);


--
-- Name: todo_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.todo_item_id_seq', 7347, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.user_id_seq', 15, true);


--
-- Name: replit_database_migrations_v1 replit_database_migrations_v1_pkey; Type: CONSTRAINT; Schema: _system; Owner: neondb_owner
--

ALTER TABLE ONLY _system.replit_database_migrations_v1
    ADD CONSTRAINT replit_database_migrations_v1_pkey PRIMARY KEY (id);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- Name: client client_public_code_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_public_code_key UNIQUE (public_code);


--
-- Name: comentarios comentarios_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.comentarios
    ADD CONSTRAINT comentarios_pkey PRIMARY KEY (id);


--
-- Name: contato_files contato_files_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.contato_files
    ADD CONSTRAINT contato_files_pkey PRIMARY KEY (id);


--
-- Name: contatos contatos_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.contatos
    ADD CONSTRAINT contatos_pkey PRIMARY KEY (id);


--
-- Name: crm_stages crm_stages_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.crm_stages
    ADD CONSTRAINT crm_stages_pkey PRIMARY KEY (id);


--
-- Name: file_categories file_categories_nome_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.file_categories
    ADD CONSTRAINT file_categories_nome_key UNIQUE (nome);


--
-- Name: file_categories file_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.file_categories
    ADD CONSTRAINT file_categories_pkey PRIMARY KEY (id);


--
-- Name: lead_interaction lead_interaction_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.lead_interaction
    ADD CONSTRAINT lead_interaction_pkey PRIMARY KEY (id);


--
-- Name: lead lead_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.lead
    ADD CONSTRAINT lead_pkey PRIMARY KEY (id);


--
-- Name: project_api_credentials project_api_credentials_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_credentials
    ADD CONSTRAINT project_api_credentials_pkey PRIMARY KEY (id);


--
-- Name: project_api_endpoints project_api_endpoints_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_endpoints
    ADD CONSTRAINT project_api_endpoints_pkey PRIMARY KEY (id);


--
-- Name: project_api_keys project_api_keys_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_keys
    ADD CONSTRAINT project_api_keys_pkey PRIMARY KEY (id);


--
-- Name: project_files project_files_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_pkey PRIMARY KEY (id);


--
-- Name: project project_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (id);


--
-- Name: project_users project_users_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_users
    ADD CONSTRAINT project_users_pkey PRIMARY KEY (project_id, user_id);


--
-- Name: system_api_keys system_api_keys_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.system_api_keys
    ADD CONSTRAINT system_api_keys_pkey PRIMARY KEY (id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);


--
-- Name: todo_item todo_item_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.todo_item
    ADD CONSTRAINT todo_item_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: idx_replit_database_migrations_v1_build_id; Type: INDEX; Schema: _system; Owner: neondb_owner
--

CREATE UNIQUE INDEX idx_replit_database_migrations_v1_build_id ON _system.replit_database_migrations_v1 USING btree (build_id);


--
-- Name: ix_project_api_keys_prefix; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE UNIQUE INDEX ix_project_api_keys_prefix ON public.project_api_keys USING btree (prefix);


--
-- Name: ix_system_api_keys_prefix; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE UNIQUE INDEX ix_system_api_keys_prefix ON public.system_api_keys USING btree (prefix);


--
-- Name: client client_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public."user"(id);


--
-- Name: comentarios comentarios_contato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.comentarios
    ADD CONSTRAINT comentarios_contato_id_fkey FOREIGN KEY (contato_id) REFERENCES public.contatos(id);


--
-- Name: contato_files contato_files_contato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.contato_files
    ADD CONSTRAINT contato_files_contato_id_fkey FOREIGN KEY (contato_id) REFERENCES public.contatos(id);


--
-- Name: contato_files contato_files_uploaded_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.contato_files
    ADD CONSTRAINT contato_files_uploaded_by_id_fkey FOREIGN KEY (uploaded_by_id) REFERENCES public."user"(id);


--
-- Name: lead lead_converted_to_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.lead
    ADD CONSTRAINT lead_converted_to_client_id_fkey FOREIGN KEY (converted_to_client_id) REFERENCES public.client(id);


--
-- Name: lead_interaction lead_interaction_lead_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.lead_interaction
    ADD CONSTRAINT lead_interaction_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES public.lead(id);


--
-- Name: lead_interaction lead_interaction_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.lead_interaction
    ADD CONSTRAINT lead_interaction_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: lead lead_responsavel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.lead
    ADD CONSTRAINT lead_responsavel_id_fkey FOREIGN KEY (responsavel_id) REFERENCES public."user"(id);


--
-- Name: project_api_credentials project_api_credentials_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_credentials
    ADD CONSTRAINT project_api_credentials_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public."user"(id);


--
-- Name: project_api_credentials project_api_credentials_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_credentials
    ADD CONSTRAINT project_api_credentials_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- Name: project_api_endpoints project_api_endpoints_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_endpoints
    ADD CONSTRAINT project_api_endpoints_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public."user"(id);


--
-- Name: project_api_endpoints project_api_endpoints_credential_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_endpoints
    ADD CONSTRAINT project_api_endpoints_credential_id_fkey FOREIGN KEY (credential_id) REFERENCES public.project_api_credentials(id);


--
-- Name: project_api_endpoints project_api_endpoints_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_endpoints
    ADD CONSTRAINT project_api_endpoints_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- Name: project_api_keys project_api_keys_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_keys
    ADD CONSTRAINT project_api_keys_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- Name: project_api_keys project_api_keys_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_api_keys
    ADD CONSTRAINT project_api_keys_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: project project_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: project_files project_files_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.file_categories(id);


--
-- Name: project_files project_files_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- Name: project_files project_files_uploaded_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_uploaded_by_id_fkey FOREIGN KEY (uploaded_by_id) REFERENCES public."user"(id);


--
-- Name: project project_responsible_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_responsible_id_fkey FOREIGN KEY (responsible_id) REFERENCES public."user"(id);


--
-- Name: project_users project_users_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_users
    ADD CONSTRAINT project_users_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- Name: project_users project_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_users
    ADD CONSTRAINT project_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: system_api_keys system_api_keys_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.system_api_keys
    ADD CONSTRAINT system_api_keys_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: task task_assigned_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_assigned_user_id_fkey FOREIGN KEY (assigned_user_id) REFERENCES public."user"(id);


--
-- Name: task task_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- Name: todo_item todo_item_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.todo_item
    ADD CONSTRAINT todo_item_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

