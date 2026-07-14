-- Run this once in the Supabase SQL Editor (dashboard -> SQL Editor -> New query -> paste -> Run)

create table if not exists ws_state (
    id int primary key default 1,
    turn int not null default 1,
    cap_gap int not null default 64,
    concession_modifier int not null default 0,
    narrative_modifier int not null default 0,
    doctrine text not null default 'rus',
    scenario_name text not null default '',
    scenario_desc text not null default '',
    treaty_flag boolean not null default false,
    win_win_active boolean not null default false,
    constraint single_row check (id = 1)
);
insert into ws_state (id) values (1) on conflict (id) do nothing;

create table if not exists ws_log (
    id bigint generated always as identity primary key,
    ts timestamptz not null default now(),
    turn int,
    callsign text,
    actor text,
    move_type text,
    source text,
    detail text,
    cap_gap_delta int
);

create table if not exists ws_arbitration (
    id bigint generated always as identity primary key,
    case_id text,
    status text not null default 'OPEN',
    violation text,
    asset text,
    stage int not null default 1,
    opened_by text,
    opened_at timestamptz not null default now()
);

-- Row Level Security: enabled with permissive policies so the anon key (used by the app)
-- can read/write. This app has no per-user auth -- the shared access code in app.py is the
-- only gate -- so these policies intentionally allow full read/write via the anon key.
alter table ws_state enable row level security;
alter table ws_log enable row level security;
alter table ws_arbitration enable row level security;

create policy "allow all on ws_state" on ws_state for all using (true) with check (true);
create policy "allow all on ws_log" on ws_log for all using (true) with check (true);
create policy "allow all on ws_arbitration" on ws_arbitration for all using (true) with check (true);
