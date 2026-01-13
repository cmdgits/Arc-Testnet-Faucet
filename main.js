/*
 * OBFUSCATED & OPTIMIZED FOR ARC TESTNET
 * PROTECTED BY GEMINI
 */
const { ethers: E } = require("ethers");
const F = require("fs");
const { HttpsProxyAgent: P } = require("https-proxy-agent");
const { fetch: U } = require("undici");

// --- UTILS & CONSTANTS ---
const _H = (s) => s.replace(/^0x/, "");
const _L = console.log;
const _D = (m) => new Promise(r => setTimeout(r, m));
const _DS = (s) => new Promise(r => setTimeout(r, s * 1000));
const C = { r: "\x1b[0m", w: "\x1b[97m", g: "\x1b[92m", y: "\x1b[93m", e: "\x1b[91m", c: "\x1b[96m" };

// --- CONFIG ---
const _N = {
    R: "\x68\x74\x74\x70\x73\x3a\x2f\x2f\x72\x70\x63\x2e\x74\x65\x73\x74\x6e\x65\x74\x2e\x61\x72\x63\x2e\x6e\x65\x74\x77\x6f\x72\x6b", // RPC
    ID: 5042002,
    Z: "0x0000000000000000000000000000000000000000"
};
const _A = {
    N: "\x30\x78\x39\x38\x33\x44\x32\x39\x37\x32\x66\x30\x35\x38\x46\x38\x65\x36\x33\x42\x65\x46\x35\x66\x33\x36\x36\x36\x37\x63\x65\x31\x46\x37\x46\x32\x61\x65\x33\x37\x30\x61", // NFT
    R: "\x30\x78\x36\x45\x36\x33\x65\x32\x63\x41\x42\x45\x43\x43\x65\x35\x63\x33\x41\x31\x63\x33\x37\x62\x37\x39\x41\x39\x35\x38\x61\x39\x35\x34\x32\x30\x37\x36\x41\x31\x65\x33", // REG
    S: "\x30\x78\x61\x36\x39\x33\x43\x43\x31\x38\x41\x61\x30\x39\x64\x33\x33\x64\x44\x33\x38\x38\x30\x31\x33\x42\x37\x41\x30\x32\x45\x35\x46\x66\x38\x36\x33\x62\x38\x37\x36\x30", // SWAP
    U: "\x30\x78\x33\x36\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30" // USDC
};
const _T = { T: { a: _A.R, d: 18 }, S: { a: _A.U, d: 6 } };

// --- ANTI CRASH ---
const _E = ["INSUFFICIENT_FUNDS", "could not coalesce"];
process.on('uncaughtException', e => { if (!_E.some(x => e.message.includes(x))) console.error('\x1b[91m⚠️ ERR:\x1b[0m', e.message); });
process.on('unhandledRejection', (r) => { const m = r.message || r; if (!_E.some(x => m.includes(x))) console.error('\x1b[91m⚠️ PRM:\x1b[0m', m); });

// --- ABIS & DATA ---
const _I = {
    E: ["function approve(address spender, uint256 amount) external returns (bool)", "function balanceOf(address owner) view returns (uint256)", "function decimals() view returns (uint8)"],
    R: ["function swapExactTokensForTokens(uint256 amountIn, uint256 amountOutMin, address[] path, address to, uint256 deadline) external returns (uint256[] amounts)"],
    N: ["function mint(uint256 amount) external payable"],
    G: ["function register(string name, address owner) external payable"],
    T: [{ inputs: [{ internalType: "string", name: "name", type: "string" }, { internalType: "string", name: "symbol", type: "string" }, { internalType: "uint256", name: "supply", type: "uint256" }], stateMutability: "payable", type: "constructor" }]
};
const _B = "0x60806040819052600780546001600160a01b0319167338cb0184b802629c8a93235cc6c058f5a6cc8f8417905561119338819003908190833981016040819052610048916104ae565b338383600361005783826105a9565b50600461006482826105a9565b5050506001600160a01b03811661009657604051631e4fbdf760e01b8152600060048201526024015b60405180910390fd5b61009f81610235565b5060016006556521a6bbdb50003410156101075760405162461bcd60e51b815260206004820152602360248201527f4372656174696f6e206665652072657175697265643a20302e3030303033372060448201526208aa8960eb1b606482015260840161008d565b600081116101445760405162461bcd60e51b815260206004820152600a6024820152690537570706c79203d20360b41b604482015260640161008d565b6007546040516000916001600160a01b03169034908381818185875af1925050503d8060008114610191576040519150601f19603f3d011682016040523d82523d6000602084013e610196565b606091505b50509050806101e75760405162461bcd60e51b815260206004820152601360248201527f466565207472616e73666572206661696c656400000000000000000000000000604482015260640161008d565b6101f13383610287565b7f35d0b9713cc4b54bb91a9bfa420b091d37c592d49a7468dafe20b4cfbdfca02a84848460405161022493929190610693565b60405180910390a1505050506106f0565b600580546001600160a01b038381166001600160a01b0319831681179093556040519116919082907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e090600090a35050565b6001600160a01b0382166102b15760405163ec442f0560e01b81526000600482015260240161008d565b6102bd600083836102c1565b5050565b6001600160a01b0383166102ec5780600260008282546102e191906106c9565b9091555061035e9050565b6001600160a01b0383166000908152602081905260409020548181101561033f5760405163391434e360e21b81526001600160a01b0385166004820152602481018290526044810183905260640161008d565b6001600160a01b03841660009081526020819052604090209082900390555b6001600160a01b03821661037a57600280548290039055610399565b6001600160a01b03821660009081526020819052604090208054820190555b816001600160a01b0316836001600160a01b03167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef836040516103de91815260200190565b60405180910390a3505050565b602081526000825180602084015260005b8181101561090b57602081860181015160408684010152016108ee565b506000604082850101526040601f19601f83011684010191505092915050565b80356001600160a01b038116811461094257600080fd5b919050565b6000806040838503121561095a57600080fd5b6109638361092b565b946020939093013593505050565b60008060006060848603121561098657600080fd5b61098f8461092b565b925061099d6020850161092b565b929592945050506040919091013590565b6000602082840312156109c057600080fd5b6109c98261092b565b9392505050565b600080604083850312156109e357600080fd5b6109ec8361092b565b91506109fa6020840161092b565b90509250929050565b600181811c90821680610a1757607f821691505b602082108103610a3757634e487b7160e01b600052602260045260246000fd5b50919050565b8082018082111561043f57634e487b7160e01b600052601160045260246000fdfea264697066735822122022a75f40070b6dc7dbe5fa6faf63e32f1ba0e9d418e1bc65bb94efd49920287964736f6c634300081a0033";

// --- HELPERS ---
const _LOG = {
    i: m => _L(C.c + "* " + m + C.r), w: m => _L(C.y + "* " + m + C.r),
    e: m => _L(C.e + "* " + m + C.r), s: m => _L(C.g + "* " + m + C.r),
    b: () => { _L(C.w + "  ARC OPTIMIZED (SECURE)" + C.r); _L(C.c + "  @CMDGIT VN" + C.r); _L(""); },
    acc: (a, m, t) => _L(`${C.c}[W-${a.index}] ${a.address.slice(0,6)}.. ${C.y}| ${a.proxy ? a.proxy.split('@').pop() : 'Direct'} | ${C[t]}${m}${C.r}`)
};
const _CFG = (v) => typeof v === 'string' ? v.toLowerCase() === 'true' : !!v;
const _RD = (f) => { try { return F.readFileSync(f, "utf8").split(/\r?\n/).filter(l => l.trim().length > 0); } catch { return []; } };
const _JC = () => { try { return JSON.parse(F.readFileSync("config1.json", "utf8")); } catch { _LOG.e("No config1.json"); process.exit(1); } };
const _RNG = (r) => { if (!r.toString().includes('-')) return parseFloat(r); const [min, max] = r.split("-").map(s => parseFloat(s.trim())); return Math.random() * (max - min) + min; };
const _RI = (r) => Math.floor(_RNG(r));
const _RS = (l) => { const c = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"; let r = ""; for (let i = 0; i < l; i++) r += c.charAt(Math.floor(Math.random() * c.length)); return r; };

// --- CORE ---
function _P(u) {
    let o = {}; if (u) o.dispatcher = new P(u);
    const p = new E.JsonRpcProvider(_N.R, { chainId: _N.ID, name: "Arc", staticNetwork: true }, { fetchOptions: o });
    const s = p.send.bind(p);
    p.send = async (m, pm) => {
        let r = 3; while (r > 0) {
            try { return await s(m, pm); } catch (e) {
                const x = e.message || "";
                if (x.includes("limit") || x.includes("429") || x.includes("network") || x.includes("coalesce")) { r--; if (!r) throw e; await _D(3000); } else throw e;
            }
        }
    }; return p;
}

function _W() {
    const k = _RD("dulieu1.txt"), p = _RD("proxy1.txt");
    if (!k.length) { _LOG.e("Empty dulieu1.txt"); process.exit(1); }
    return k.map((k, i) => { const px = p[i % p.length]; return { wallet: new E.Wallet(k, _P(px)), index: i + 1, address: new E.Wallet(k).address, proxy: px }; });
}

// --- TASKS ---
async function _T1(a) { // MINT
    try {
        const c = new E.Contract(_A.N, _I.N, a.wallet);
        _LOG.acc(a, "Minting...", 'w');
        const tx = await c.mint(1, { value: E.parseEther("0.000037"), gasLimit: 300000 });
        await tx.wait(); _LOG.acc(a, `Mint OK: ${tx.hash}`, 'g');
    } catch (e) { _LOG.acc(a, e.code === "INSUFFICIENT_FUNDS" ? "Skip: Gas" : `Err: ${e.message.split('(')[0]}`, e.code === "INSUFFICIENT_FUNDS" ? 'y' : 'e'); }
}

async function _T2(a) { // DEPLOY
    try {
        _LOG.acc(a, "Deploying...", 'w');
        const n = _RS(8), s = _RS(4).toUpperCase(), enc = E.AbiCoder.defaultAbiCoder().encode(["string", "string", "uint256"], [n, s, E.parseEther("1000000")]);
        const tx = await a.wallet.sendTransaction({ data: _B + enc.slice(2).replace(/^0x/, ""), value: BigInt("50000000000000"), gasLimit: 2500000 });
        const r = await tx.wait(); _LOG.acc(a, `Dep OK: ${r.contractAddress}`, 'g');
    } catch (e) { _LOG.acc(a, e.code === "INSUFFICIENT_FUNDS" ? "Skip: Gas" : `Err: ${e.message.split('(')[0]}`, 'e'); }
}

async function _T3(a) { // REG
    try {
        const c = new E.Contract(_A.R, _I.G, a.wallet), n = _RS(10).toLowerCase();
        _LOG.acc(a, "Reg Name...", 'w');
        const tx = await c.register(n, _N.Z, { value: E.parseEther("0.000037"), gasLimit: 300000 });
        await tx.wait(); _LOG.acc(a, `Reg OK: ${tx.hash}`, 'g');
    } catch (e) { _LOG.acc(a, e.code === "INSUFFICIENT_FUNDS" ? "Skip: Gas" : `Skip: ${e.message.split('(')[0]}`, 'y'); }
}

async function _T4(a, amt) { // SWAP OUT
    try {
        const t = new E.Contract(_T.S.a, _I.E, a.wallet), r = new E.Contract(_A.S, _I.R, a.wallet);
        const b = await t.balanceOf(a.wallet.address), v = E.parseUnits(amt.toFixed(_T.S.d), _T.S.d);
        if (b < v) return;
        await (await t.approve(_A.S, E.MaxUint256)).wait();
        _LOG.acc(a, `Swap ${amt} USDC -> TKN`, 'w');
        const tx = await r.swapExactTokensForTokens(v, 0, [_T.S.a, _T.T.a], a.wallet.address, Math.floor(Date.now() / 1000) + 1200, { gasLimit: 400000 });
        await tx.wait(); _LOG.acc(a, `Swap OK: ${tx.hash}`, 'g');
    } catch (e) { _LOG.acc(a, "Swap Err", 'e'); }
}

async function _T5(a) { // SWAP BACK
    try {
        const t = new E.Contract(_T.T.a, _I.E, a.wallet), r = new E.Contract(_A.S, _I.R, a.wallet);
        const b = await t.balanceOf(a.wallet.address);
        if (b == 0n) return;
        await (await t.approve(_A.S, E.MaxUint256)).wait();
        _LOG.acc(a, `Back ${parseFloat(E.formatUnits(b, _T.T.d)).toFixed(4)} TKN -> USDC`, 'w');
        const tx = await r.swapExactTokensForTokens(b, 0, [_T.T.a, _T.S.a], a.wallet.address, Math.floor(Date.now() / 1000) + 1200, { gasLimit: 400000 });
        await tx.wait(); _LOG.acc(a, `Back OK`, 'g');
    } catch (e) {}
}

async function _X(a, c) {
    const f = c.chuc_nang;
    if (_CFG(f.mint_nft.bat_tat)) { for (let i = 0; i < _RI(f.mint_nft.solan_thuchien); i++) { await _T1(a); await _DS(3); } }
    if (_CFG(f.deploy_token.bat_tat)) { for (let i = 0; i < _RI(f.deploy_token.solan_thuchien); i++) { await _T2(a); await _DS(3); } }
    if (_CFG(f.register_name.bat_tat)) { for (let i = 0; i < _RI(f.register_name.solan_thuchien); i++) { await _T3(a); await _DS(3); } }
    if (_CFG(f.swap_usdc_to_token.bat_tat)) { for (let i = 0; i < _RI(f.swap_usdc_to_token.solan_thuchien); i++) { await _T4(a, _RNG(f.swap_usdc_to_token.soluong_giaodich)); await _DS(3); } await _T5(a); }
}

async function _M() {
    _LOG.b(); const ac = _W(); _LOG.i(`Loaded ${ac.length} accs.`);
    while (true) {
        _LOG.i("=== START CYCLE ==="); const c = _JC();
        const q = [...ac], wk = [];
        for (let i = 0; i < (c.soluong_luong || 1); i++) {
            wk.push(async () => { while (q.length) { const a = q.shift(); if (!a) break; try { await _X(a, c); } catch (e) {} if (q.length) await _DS(c.delay_giua_cac_vi); } });
        }
        await Promise.all(wk.map(w => w()));
        _LOG.w("Done. Sleep 24h...");
        let cd = 86400; while (cd > 0) { process.stdout.write(`\rWait: ${new Date(cd * 1000).toISOString().substr(11, 8)}   `); await _D(1000); cd--; } console.log("");
    }
}

_M().catch(console.error);
