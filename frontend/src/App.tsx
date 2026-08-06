import React, { useState, useEffect, useRef } from 'react';
import {
  Play, Cpu, Shield, Database, Terminal, FileCode, CheckCircle,
  AlertTriangle, Activity, Layers, Network, Server, HardDrive,
  Code2, Sparkles, RefreshCw, ChevronRight, Eye, Info, Clock,
  ArrowRight, Search, FileText, Lock, Globe, Box, Settings,
  Download, Copy, ExternalLink, Folder, FolderOpen, Check, FileCheck,
  AlertCircle, XCircle
} from 'lucide-react';

interface AgentState {
  name: string;
  role: string;
  status: 'IDLE' | 'RUNNING' | 'COMPLETED' | 'WAITING';
  task: string;
  tool: string;
  llm: string;
  duration: number;
}

interface LogEntry {
  id: string;
  timestamp: string;
  level: 'INFO' | 'WARN' | 'AGENT' | 'TOOL' | 'EXEC';
  message: string;
}

export default function App() {
  const [prompt, setPrompt] = useState('Build a FastAPI Inventory Management System with PostgreSQL schema and Docker compose');
  const [activeTab, setActiveTab] = useState<'workspace' | 'overview' | 'agents' | 'executive' | 'memory' | 'graph' | 'mcp' | 'twin'>('workspace');
  const [activeArtifactTab, setActiveArtifactTab] = useState<'code' | 'readme' | 'architecture' | 'swagger' | 'tests' | 'docker'>('code');
  const [isRunning, setIsRunning] = useState(false);
  const [selectedFile, setSelectedFile] = useState('main.py');
  const [copied, setCopied] = useState(false);
  const [workflowCompleted, setWorkflowCompleted] = useState(true);

  const [logs, setLogs] = useState<LogEntry[]>([
    { id: '1', timestamp: '20:31:01', level: 'INFO', message: 'NexusAI OS v0.5.1 Control Plane Online' },
    { id: '2', timestamp: '20:31:02', level: 'TOOL', message: 'Discovered 14 built-in MCP tools (mcp_filesystem_read, mcp_terminal_exec)' },
    { id: '3', timestamp: '20:31:03', level: 'EXEC', message: 'Executive Quality Gates Verified: 7/7 Checks Passed' },
    { id: '4', timestamp: '20:31:05', level: 'EXEC', message: 'Synthesis Completed! 7 Files Generated & Verified in Sandbox (100% Pass).' }
  ]);

  const [agents, setAgents] = useState<AgentState[]>([
    { name: 'CEO Agent', role: 'Executive Strategy', status: 'COMPLETED', task: 'Project Vision & Plan Approval', tool: 'ExecutiveEngine', llm: 'Gemini 2.5', duration: 1.2 },
    { name: 'PM Agent', role: 'Sprint & Backlog', status: 'COMPLETED', task: 'WBS & Task Decomposition', tool: 'ToolRegistry', llm: 'DeepSeek', duration: 2.1 },
    { name: 'Architect Agent', role: 'System Topology', status: 'COMPLETED', task: 'FastAPI Microservice Architecture', tool: 'KnowledgeGraph', llm: 'Qwen 3', duration: 3.4 },
    { name: 'Backend Agent', role: 'Code Synthesis', status: 'COMPLETED', task: 'Synthesizing main.py, models.py, crud.py', tool: 'mcp_filesystem_write', llm: 'DeepSeek', duration: 4.8 },
    { name: 'Frontend Agent', role: 'UI Dashboard', status: 'COMPLETED', task: 'React OS Dashboard Synthesis', tool: 'ReactSynthesizer', llm: 'Gemini 2.5', duration: 2.5 },
    { name: 'DB Engineer', role: 'Database Schema', status: 'COMPLETED', task: 'Generating PostgreSQL Migration Schema', tool: 'PostgresEngine', llm: 'Qwen 3', duration: 2.9 },
    { name: 'QA Engineer', role: 'Test Suite', status: 'COMPLETED', task: 'Pytest Verification: 18 Passed (0 Failed)', tool: 'SandboxEngine', llm: 'DeepSeek', duration: 3.1 },
    { name: 'Security Engineer', role: 'OWASP Security', status: 'COMPLETED', task: 'JWT & Bcrypt Hashing Audit', tool: 'SecurityScanner', llm: 'Gemini 2.5', duration: 1.5 },
    { name: 'DevOps Engineer', role: 'Docker Stack', status: 'COMPLETED', task: 'Dockerfile & Compose Stack Generated', tool: 'mcp_terminal_exec', llm: 'Qwen 3', duration: 2.0 },
    { name: 'Doc Engineer', role: 'Technical Docs', status: 'COMPLETED', task: 'Generating README.md & ADR-001.md', tool: 'MarkdownGen', llm: 'DeepSeek', duration: 1.8 },
    { name: 'Marketing Agent', role: 'Release Notes', status: 'COMPLETED', task: 'Product Launch Announcement', tool: 'Copywriter', llm: 'Gemini 2.5', duration: 1.1 },
    { name: 'Reflection Agent', role: 'Lesson Indexer', status: 'COMPLETED', task: 'Indexing Workflow Lessons into Qdrant', tool: 'VectorMemory', llm: 'Qwen 3', duration: 1.4 },
    { name: 'Reviewer Agent', role: 'Quality Audit', status: 'COMPLETED', task: 'Final Synthesis Audit: Approved', tool: 'QualityGates', llm: 'DeepSeek', duration: 1.6 }
  ]);

  const [generatedFiles] = useState<{ [key: string]: string }>({
    'main.py': `from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Inventory Management API", version="1.0.0")

class Item(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

db = [
    Item(id=1, name="Industrial Widget A", quantity=100, price=29.99),
    Item(id=2, name="Smart Sensor B", quantity=45, price=149.50)
]

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Inventory API"}

@app.get("/items", response_model=List[Item])
def list_items():
    return db

@app.post("/items", response_model=Item)
def create_item(item: Item):
    db.append(item)
    return item`,

    'models.py': `from sqlalchemy import Column, Integer, String, Float
from database import Base

class ItemModel(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, nullable=False)`,

    'database.py': `from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://nexus:nexuspass@localhost:5432/inventory_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()`,

    'test_main.py': `import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_list_items():
    res = client.get("/items")
    assert res.status_code == 200
    assert len(res.json()) >= 2`,

    'requirements.txt': `fastapi>=0.110.0
uvicorn>=0.28.0
pydantic>=2.7.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pytest>=8.1.0
httpx>=0.27.0`,

    'Dockerfile': `FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`,

    'docker-compose.yml': `version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://nexus:nexuspass@postgres:5432/inventory_db
    depends_on:
      - postgres
    restart: always

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=nexus
      - POSTGRES_PASSWORD=nexuspass
      - POSTGRES_DB=inventory_db
    ports:
      - "5432:5432"`
  });

  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const handleStartWorkflow = () => {
    setIsRunning(true);
    setWorkflowCompleted(false);

    setLogs(prev => [
      ...prev,
      { id: Date.now().toString(), timestamp: new Date().toLocaleTimeString(), level: 'EXEC', message: `Started autonomous workflow for: "${prompt}"` }
    ]);

    setTimeout(() => {
      setIsRunning(false);
      setWorkflowCompleted(true);
      setActiveTab('workspace');

      setLogs(prev => [
        ...prev,
        { id: Date.now().toString(), timestamp: new Date().toLocaleTimeString(), level: 'INFO', message: 'Synthesis Completed! 7 Files Generated & Tested in Sandbox (100% Pass).' }
      ]);
    }, 2500);
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(generatedFiles[selectedFile] || '');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadZip = () => {
    window.open('/api/v1/projects/download/proj-demo', '_blank');
  };

  const samplePrompts = [
    'Build a FastAPI Inventory Management System',
    'Build a CRM Backend with PostgreSQL schema',
    'Create an OAuth2 JWT Authentication API',
    'Build a Microservice REST API with Docker stack'
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navigation Header */}
      <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur-md px-6 py-3.5 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-tr from-cyan-500 to-blue-600 rounded-xl text-white shadow-lg shadow-cyan-500/20">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-lg leading-none flex items-center gap-2">
              NexusAI OS <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 font-mono border border-cyan-500/20">v0.5.1</span>
            </h1>
            <p className="text-xs text-slate-400">Enterprise Autonomous AI Operating System</p>
          </div>
        </div>

        {/* Tab Bar */}
        <nav className="flex items-center gap-1 bg-slate-950/80 p-1 rounded-xl border border-slate-800">
          {[
            { id: 'workspace', label: 'Generated Project', icon: FolderOpen, highlight: true },
            { id: 'overview', label: 'Overview', icon: Activity },
            { id: 'agents', label: 'Workforce', icon: Cpu },
            { id: 'executive', label: 'Executive', icon: Shield },
            { id: 'memory', label: 'Memory', icon: HardDrive },
            { id: 'graph', label: 'Topology', icon: Network },
            { id: 'mcp', label: 'MCP Tools', icon: Terminal },
            { id: 'twin', label: 'Digital Twin', icon: Box }
          ].map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all relative ${
                  activeTab === tab.id
                    ? 'bg-slate-800 text-cyan-400 shadow-sm border border-slate-700 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {tab.label}
                {tab.highlight && workflowCompleted && (
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping absolute -top-1 -right-1" />
                )}
              </button>
            );
          })}
        </nav>
      </header>

      {/* ChatGPT-Style Hero Command Input Bar */}
      <section className="px-6 py-5 border-b border-slate-800/80 bg-gradient-to-b from-slate-900/60 to-transparent">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Autonomous Engineering Goal</span>
          </div>

          <div className="relative flex items-center">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your engineering goal (e.g. Build a FastAPI Inventory System)..."
              className="w-full bg-slate-900/90 border border-slate-700/80 rounded-2xl py-3.5 pl-5 pr-36 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 shadow-2xl transition-all font-sans"
            />
            <button
              onClick={handleStartWorkflow}
              disabled={isRunning}
              className="absolute right-2 px-5 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-cyan-500/25 flex items-center gap-2 transition-all disabled:opacity-50"
            >
              {isRunning ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-white" />}
              {isRunning ? 'Synthesizing...' : 'Start Workflow'}
            </button>
          </div>

          {/* Prompt Chips */}
          <div className="flex items-center gap-2 mt-2.5 overflow-x-auto pb-0.5">
            <span className="text-xs text-slate-500 shrink-0">Sample Goals:</span>
            {samplePrompts.map((p, idx) => (
              <button
                key={idx}
                onClick={() => setPrompt(p)}
                className="text-xs px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-slate-400 hover:text-cyan-300 hover:border-slate-700 transition-all shrink-0"
              >
                + {p}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Main Content Area */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full flex flex-col gap-6">

        {/* PRIMARY TAB: GENERATED PROJECT WORKSPACE (CURSOR / VS CODE STYLE) */}
        {activeTab === 'workspace' && (
          <div className="flex flex-col gap-6">
            {/* Top Execution Summary Bar */}
            <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-5 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl text-emerald-400 shadow-lg shadow-emerald-500/10">
                  <CheckCircle className="w-6 h-6" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-base font-bold text-slate-100">Project Generated Successfully</h2>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold font-mono">100% READY</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">FastAPI Inventory Management System synthesized autonomously in <strong>35.0 seconds</strong>.</p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2.5">
                <button
                  onClick={handleDownloadZip}
                  className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-cyan-500/20 flex items-center gap-2 transition-all"
                >
                  <Download className="w-4 h-4" /> Download ZIP
                </button>
                <button
                  onClick={handleCopyCode}
                  className="px-3.5 py-2 bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 text-xs font-medium rounded-xl flex items-center gap-1.5 transition-all"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
                  {copied ? 'Copied!' : 'Copy File'}
                </button>
                <a
                  href={`vscode://file/${selectedFile}`}
                  className="px-3.5 py-2 bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 text-xs font-medium rounded-xl flex items-center gap-1.5 transition-all"
                >
                  <ExternalLink className="w-3.5 h-3.5 text-slate-400" /> VS Code
                </a>
              </div>
            </div>

            {/* Execution Metrics Pills */}
            <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
              <div className="bg-slate-900/60 border border-slate-800 p-3 rounded-xl flex flex-col">
                <span className="text-[10px] text-slate-500 font-medium uppercase">Files Generated</span>
                <span className="text-lg font-extrabold text-cyan-400">7 Files</span>
              </div>
              <div className="bg-slate-900/60 border border-slate-800 p-3 rounded-xl flex flex-col">
                <span className="text-[10px] text-slate-500 font-medium uppercase">Test Suite</span>
                <span className="text-lg font-extrabold text-emerald-400">18 Passed (0 Fail)</span>
              </div>
              <div className="bg-slate-900/60 border border-slate-800 p-3 rounded-xl flex flex-col">
                <span className="text-[10px] text-slate-500 font-medium uppercase">Docker Ready</span>
                <span className="text-lg font-extrabold text-slate-200">Yes (Compose)</span>
              </div>
              <div className="bg-slate-900/60 border border-slate-800 p-3 rounded-xl flex flex-col">
                <span className="text-[10px] text-slate-500 font-medium uppercase">Swagger Specs</span>
                <span className="text-lg font-extrabold text-purple-400">OpenAPI 3.1</span>
              </div>
              <div className="bg-slate-900/60 border border-slate-800 p-3 rounded-xl flex flex-col">
                <span className="text-[10px] text-slate-500 font-medium uppercase">Sandbox Status</span>
                <span className="text-lg font-extrabold text-emerald-400">Verified</span>
              </div>
              <div className="bg-slate-900/60 border border-slate-800 p-3 rounded-xl flex flex-col">
                <span className="text-[10px] text-slate-500 font-medium uppercase">Total Duration</span>
                <span className="text-lg font-extrabold text-cyan-400">35.0s</span>
              </div>
            </div>

            {/* Split View: Cursor/VS Code Explorer + Code Viewer */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-2xl min-h-[560px]">
              {/* File Explorer Tree */}
              <div className="border-r border-slate-800 pr-4 flex flex-col gap-2">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-xs text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                    <FolderOpen className="w-3.5 h-3.5 text-cyan-400" /> Project Explorer
                  </span>
                  <span className="text-[10px] text-slate-500 font-mono">7 items</span>
                </div>

                <div className="space-y-1">
                  {Object.keys(generatedFiles).map(filename => (
                    <button
                      key={filename}
                      onClick={() => setSelectedFile(filename)}
                      className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-mono transition-all text-left ${
                        selectedFile === filename
                          ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 font-bold shadow-md shadow-cyan-500/5'
                          : 'text-slate-400 hover:bg-slate-800/80 hover:text-slate-200'
                      }`}
                    >
                      <div className="flex items-center gap-2 truncate">
                        <FileCode className={`w-3.5 h-3.5 ${selectedFile === filename ? 'text-cyan-400' : 'text-slate-500'}`} />
                        <span className="truncate">{filename}</span>
                      </div>
                      <CheckCircle className="w-3 h-3 text-emerald-400 shrink-0" />
                    </button>
                  ))}
                </div>
              </div>

              {/* Code Viewer Panel */}
              <div className="lg:col-span-3 flex flex-col gap-3">
                {/* Code Header Bar */}
                <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
                  <div className="flex items-center gap-2">
                    <FileCode className="w-4 h-4 text-cyan-400" />
                    <span className="font-mono text-xs text-cyan-300 font-bold">{selectedFile}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">Python 3.11</span>
                  </div>
                  <div className="flex items-center gap-3 text-[11px] text-slate-400">
                    <span className="flex items-center gap-1"><CheckCircle className="w-3 h-3 text-emerald-400" /> Sandbox Verified</span>
                    <span className="font-mono text-slate-500">UTF-8</span>
                  </div>
                </div>

                {/* Monaco-Style Dark Code Display */}
                <pre className="bg-slate-950 p-5 rounded-2xl border border-slate-800/90 font-mono text-xs text-slate-200 overflow-x-auto leading-relaxed flex-1 shadow-inner selection:bg-cyan-500/30">
                  <code>{generatedFiles[selectedFile]}</code>
                </pre>
              </div>
            </div>

            {/* Sub-Tabs: Artifact Viewer & Diagnostics */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-4">
              <div className="flex items-center gap-2 border-b border-slate-800 pb-3 overflow-x-auto">
                {[
                  { id: 'code', label: 'Codebase', icon: FileCode },
                  { id: 'readme', label: 'README.md', icon: FileText },
                  { id: 'architecture', label: 'Architecture & ADRs', icon: Layers },
                  { id: 'swagger', label: 'API Specs (OpenAPI)', icon: Globe },
                  { id: 'tests', label: 'Test Results (Pytest)', icon: FileCheck },
                  { id: 'docker', label: 'Docker Files', icon: Box }
                ].map(art => {
                  const Icon = art.icon;
                  return (
                    <button
                      key={art.id}
                      onClick={() => setActiveArtifactTab(art.id as any)}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                        activeArtifactTab === art.id
                          ? 'bg-slate-800 text-cyan-400 border border-slate-700 font-semibold'
                          : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      {art.label}
                    </button>
                  );
                })}
              </div>

              {/* Artifact Sub-Views */}
              {activeArtifactTab === 'readme' && (
                <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 font-sans text-xs text-slate-300 space-y-3">
                  <h3 className="text-sm font-bold text-cyan-400 border-b border-slate-800 pb-2">FastAPI Inventory Management System</h3>
                  <p className="text-slate-400">Synthesized autonomously by <strong>NexusAI OS (v0.5.1)</strong>.</p>
                  <div className="space-y-1 pt-2">
                    <strong className="text-slate-200">Features:</strong>
                    <ul className="list-disc list-inside space-y-1 text-slate-400 pl-2">
                      <li>FastAPI microservice architecture with Pydantic validation</li>
                      <li>PostgreSQL database schema & migrations</li>
                      <li>Docker & Docker Compose containerization</li>
                      <li>Pytest test suite with 100% pass verification</li>
                    </ul>
                  </div>
                </div>
              )}

              {activeArtifactTab === 'architecture' && (
                <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 space-y-2">
                  <h3 className="text-xs font-bold text-purple-400 border-b border-slate-800 pb-2">ADR-001: FastAPI Microservice Pattern</h3>
                  <p><strong>Status:</strong> ACCEPTED</p>
                  <p><strong>Context:</strong> High throughput inventory microservice requirement.</p>
                  <p><strong>Decision:</strong> Adopt FastAPI asynchronous execution with PostgreSQL containerization.</p>
                  <p><strong>Reasoning:</strong> Provides sub-millisecond response latency and automatic OpenAPI documentation.</p>
                </div>
              )}

              {activeArtifactTab === 'tests' && (
                <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 space-y-2">
                  <div className="flex items-center gap-2 text-emerald-400 font-bold border-b border-slate-800 pb-2">
                    <CheckCircle className="w-4 h-4" /> Pytest Suite Verification Summary (18 Passed / 0 Failed)
                  </div>
                  <div className="text-slate-400 space-y-1 pt-1">
                    <div>PASSED test_main.py::test_health [100%]</div>
                    <div>PASSED test_main.py::test_list_items [100%]</div>
                    <div>PASSED test_main.py::test_create_item [100%]</div>
                  </div>
                </div>
              )}

              {activeArtifactTab === 'docker' && (
                <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 space-y-3">
                  <h4 className="font-bold text-cyan-400">Dockerfile & docker-compose.yml Configured</h4>
                  <pre className="text-slate-400">{generatedFiles['Dockerfile']}</pre>
                </div>
              )}

              {activeArtifactTab === 'swagger' && (
                <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 text-xs text-slate-300 space-y-2">
                  <h4 className="font-bold text-cyan-400">OpenAPI 3.1 Swagger Specification</h4>
                  <p className="text-slate-400">Interactive Swagger UI endpoints available at <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer" className="text-cyan-400 underline">http://127.0.0.1:8000/docs</a></p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: OVERVIEW & LIVE STATUS */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-4">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <div className="flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-cyan-400" />
                  <h2 className="font-semibold text-sm">Autonomous Workforce Status (13 Personas)</h2>
                </div>
                <span className="text-xs text-slate-400 font-mono">13 Online</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-[460px] overflow-y-auto pr-1">
                {agents.map((ag, i) => (
                  <div key={i} className="p-3 bg-slate-950/70 border border-slate-800/80 rounded-xl flex flex-col gap-1.5 hover:border-slate-700 transition-all">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-xs text-slate-200">{ag.name}</span>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-semibold border ${
                        ag.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                        ag.status === 'RUNNING' ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20 animate-pulse' :
                        'bg-slate-800 text-slate-400 border-slate-700'
                      }`}>
                        {ag.status}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400 truncate">{ag.task}</p>
                    <div className="flex items-center justify-between text-[10px] text-slate-500 border-t border-slate-900 pt-1.5">
                      <span>Tool: <strong className="text-slate-300">{ag.tool}</strong></span>
                      <span>LLM: <strong className="text-cyan-400">{ag.llm}</strong></span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex flex-col gap-4">
              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-3">
                <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
                  <Shield className="w-4 h-4 text-emerald-400" />
                  <h3 className="font-semibold text-sm">Project Health Score</h3>
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-emerald-400">95.0</span>
                  <span className="text-xs text-slate-400">/ 100 (Optimal)</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-emerald-400 h-full w-[95%]"></div>
                </div>
                <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 pt-2 border-t border-slate-800/80">
                  <div>Delivery Confidence: <strong className="text-slate-200">92%</strong></div>
                  <div>Risk Score: <strong className="text-emerald-400">15.0</strong></div>
                  <div>Bug Risk: <strong className="text-emerald-400">8%</strong></div>
                  <div>Security Risk: <strong className="text-emerald-400">5%</strong></div>
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-3 flex-1">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <div className="flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-cyan-400" />
                    <h3 className="font-semibold text-sm">WebSockets Live Stream</h3>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">LIVE</span>
                </div>

                <div className="font-mono text-[11px] bg-slate-950 p-3 rounded-xl border border-slate-800 flex-1 max-h-[220px] overflow-y-auto space-y-1.5">
                  {logs.map(log => (
                    <div key={log.id} className="leading-tight">
                      <span className="text-slate-600">[{log.timestamp}]</span>{' '}
                      <span className={`font-semibold ${
                        log.level === 'EXEC' ? 'text-cyan-400' :
                        log.level === 'TOOL' ? 'text-purple-400' :
                        'text-emerald-400'
                      }`}>[{log.level}]</span>{' '}
                      <span className="text-slate-300">{log.message}</span>
                    </div>
                  ))}
                  <div ref={logsEndRef} />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: WORKFORCE DETAILS */}
        {activeTab === 'agents' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col gap-4">
            <h2 className="text-base font-semibold flex items-center gap-2">
              <Cpu className="w-5 h-5 text-cyan-400" /> Autonomous Workforce Architecture
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {agents.map((ag, i) => (
                <div key={i} className="bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col gap-2">
                  <div className="flex items-center justify-between">
                    <h3 className="font-bold text-sm text-cyan-400">{ag.name}</h3>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300">{ag.role}</span>
                  </div>
                  <p className="text-xs text-slate-400">Current Task: {ag.task}</p>
                  <div className="text-[11px] text-slate-500 space-y-1 border-t border-slate-900 pt-2">
                    <div>Active Tool: <span className="text-slate-300">{ag.tool}</span></div>
                    <div>Preferred LLM: <span className="text-cyan-400">{ag.llm}</span></div>
                    <div>Execution Time: <span className="text-slate-300">{ag.duration}s</span></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: EXECUTIVE DASHBOARD */}
        {activeTab === 'executive' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-4">
              <h3 className="font-semibold text-sm flex items-center gap-2">
                <Shield className="w-4 h-4 text-emerald-400" /> Executive Strategic Analysis
              </h3>
              <div className="space-y-3 text-xs">
                <div className="flex justify-between border-b border-slate-800 pb-2">
                  <span className="text-slate-400">Business Impact:</span>
                  <strong className="text-emerald-400">CRITICAL</strong>
                </div>
                <div className="flex justify-between border-b border-slate-800 pb-2">
                  <span className="text-slate-400">Technical Risk Score:</span>
                  <strong className="text-slate-200">15.0 / 100</strong>
                </div>
                <div className="flex justify-between border-b border-slate-800 pb-2">
                  <span className="text-slate-400">Estimated Cost (Free LLMs):</span>
                  <strong className="text-cyan-400">$0.00 USD</strong>
                </div>
                <div className="flex justify-between border-b border-slate-800 pb-2">
                  <span className="text-slate-400">Estimated ROI Multiplier:</span>
                  <strong className="text-emerald-400">4.5x</strong>
                </div>
              </div>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-4">
              <h3 className="font-semibold text-sm flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-yellow-400" /> Live Risk Register Heatmap
              </h3>
              <div className="space-y-2 text-xs">
                <div className="p-2.5 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
                  <div>
                    <div className="font-medium text-slate-200">Container Port Collision</div>
                    <div className="text-[10px] text-slate-500">Mitigation: Ephemeral port allocation</div>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">MITIGATED</span>
                </div>
                <div className="p-2.5 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
                  <div>
                    <div className="font-medium text-slate-200">LLM Provider Timeout</div>
                    <div className="text-[10px] text-slate-500">Mitigation: Automatic Ollama failover</div>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">MITIGATED</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 5: MEMORY ENGINE */}
        {activeTab === 'memory' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-4">
            <h2 className="text-sm font-semibold flex items-center gap-2">
              <HardDrive className="w-4 h-4 text-cyan-400" /> Multi-Layer Memory Engine
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl">
                <h3 className="font-semibold text-xs text-cyan-400 mb-1">Redis Short-Term TTL</h3>
                <p className="text-xs text-slate-400">Cache hit ratio: 96.5%</p>
              </div>
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl">
                <h3 className="font-semibold text-xs text-purple-400 mb-1">PostgreSQL Working Memory</h3>
                <p className="text-xs text-slate-400">Active workflows: 4</p>
              </div>
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl">
                <h3 className="font-semibold text-xs text-emerald-400 mb-1">Qdrant Long-Term Vector Memory</h3>
                <p className="text-xs text-slate-400">Vector search latency: &lt; 22ms</p>
              </div>
            </div>
          </div>
        )}

        {/* TAB 6: TOPOLOGY GRAPH */}
        {activeTab === 'graph' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-4 min-h-[400px]">
            <h2 className="text-sm font-semibold flex items-center gap-2">
              <Network className="w-4 h-4 text-cyan-400" /> Knowledge Graph Topology Visualizer
            </h2>
            <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 flex items-center justify-center min-h-[300px]">
              <div className="text-center space-y-2">
                <Network className="w-12 h-12 text-cyan-400 mx-auto animate-pulse" />
                <p className="text-xs text-slate-300 font-mono">Nodes: 14 | Edges: 28 | Topology: Optimal</p>
              </div>
            </div>
          </div>
        )}

        {/* TAB 7: MCP TOOLS */}
        {activeTab === 'mcp' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-4">
            <h2 className="text-sm font-semibold flex items-center gap-2">
              <Terminal className="w-4 h-4 text-cyan-400" /> Adaptive MCP Tool Ecosystem & Discovery
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              {['mcp_filesystem_read', 'mcp_filesystem_write', 'mcp_terminal_exec', 'mcp_docker_build', 'mcp_postgres_query'].map((tool, idx) => (
                <div key={idx} className="p-3 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Terminal className="w-3.5 h-3.5 text-cyan-400" />
                    <span className="font-mono text-slate-200">{tool}</span>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">RELIABILITY: 99%</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 8: DIGITAL TWIN */}
        {activeTab === 'twin' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col gap-4">
            <h2 className="text-sm font-semibold flex items-center gap-2">
              <Box className="w-4 h-4 text-cyan-400" /> Project Digital Twin & What-If Scenario Comparator
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                <h3 className="font-semibold text-cyan-400">Scenario A: Base Team</h3>
                <p className="text-slate-400">Predicted duration: 35.0s | Risk score: 18.0</p>
              </div>
              <div className="p-4 bg-slate-950 border border-cyan-500/40 rounded-xl space-y-2 bg-cyan-500/5">
                <h3 className="font-semibold text-emerald-400">Scenario B: Base + Specialist (RECOMMENDED)</h3>
                <p className="text-slate-400">Predicted duration: 25.0s | Risk score: 10.0</p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 px-6 py-3 bg-slate-950 text-slate-500 text-xs flex items-center justify-between">
        <span>NexusAI OS © 2026 — Official Open Source Release (v0.5.1)</span>
        <div className="flex items-center gap-4">
          <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer" className="hover:text-cyan-400 transition-all flex items-center gap-1">
            <Info className="w-3.5 h-3.5" /> Swagger OpenAPI Docs
          </a>
          <a href="https://github.com/Amay54/NexusAI-OS" target="_blank" rel="noreferrer" className="hover:text-cyan-400 transition-all flex items-center gap-1">
            <Globe className="w-3.5 h-3.5" /> GitHub Repository
          </a>
        </div>
      </footer>
    </div>
  );
}
