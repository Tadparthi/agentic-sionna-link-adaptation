"""Sionna PHY LDPC-coded BLER simulation utilities."""
from __future__ import annotations
from typing import Iterable
import numpy as np, pandas as pd, torch

def to_numpy(x):
    if hasattr(x,'detach'): return x.detach().cpu().numpy()
    if hasattr(x,'numpy'): return x.numpy()
    return np.array(x)

def simulate_ldpc_bler_sionna(num_bits_per_symbol:int, code_rate:float, ebno_db_values:Iterable[float], n_codeword:int=1200, batch_size:int=80, num_batches:int=3, decoder_iterations:int=15, seed:int|None=42)->pd.DataFrame:
    """Run Sionna 5G LDPC-coded BLER simulation over AWGN."""
    from sionna.phy.channel import AWGN
    from sionna.phy.fec.ldpc import LDPC5GDecoder, LDPC5GEncoder
    from sionna.phy.mapping import Constellation, Demapper, Mapper
    from sionna.phy.utils import ebnodb2no
    if seed is not None:
        torch.manual_seed(seed); np.random.seed(seed)
    n=int(n_codeword); n=n-(n%num_bits_per_symbol)
    k=max(24,int(round(code_rate*n)))
    actual_code_rate=k/n
    encoder=LDPC5GEncoder(k=k,n=n,num_bits_per_symbol=num_bits_per_symbol)
    decoder=LDPC5GDecoder(encoder,num_iter=decoder_iterations,hard_out=True,return_infobits=True)
    constellation=Constellation('qam',num_bits_per_symbol)
    mapper=Mapper(constellation=constellation); demapper=Demapper('app',constellation=constellation); awgn=AWGN()
    rows=[]
    for ebno_db in ebno_db_values:
        no=ebnodb2no(ebno_db=ebno_db,num_bits_per_symbol=num_bits_per_symbol,coderate=actual_code_rate)
        total_blocks=block_errors=total_bits=bit_errors=0
        for _ in range(num_batches):
            u=torch.randint(low=0,high=2,size=(batch_size,k),dtype=torch.float32)
            c=encoder(u); x=mapper(c); y=awgn(x,no); llr=demapper(y,no); u_hat=decoder(llr)
            u_np=to_numpy(u).astype(int); uh_np=to_numpy(u_hat).astype(int)
            err=(uh_np!=u_np)
            bit_errors+=int(err.sum()); total_bits+=int(err.size)
            block_errors+=int(np.any(err,axis=1).sum()); total_blocks+=int(u_np.shape[0])
        rows.append({'modulation':f'{2**num_bits_per_symbol}-QAM','num_bits_per_symbol':num_bits_per_symbol,'target_code_rate':code_rate,'actual_code_rate':actual_code_rate,'k_info_bits':k,'n_codeword_bits':n,'ebno_db':ebno_db,'ber':bit_errors/total_bits,'bler':block_errors/total_blocks,'total_blocks':total_blocks,'block_errors':block_errors,'decoder_iterations':decoder_iterations})
    return pd.DataFrame(rows)

def run_mcs_profile_simulations(profiles:list[dict], n_codeword:int=1200, batch_size:int=80, num_batches:int=3, decoder_iterations:int=15, seed:int|None=42)->pd.DataFrame:
    all_results=[]
    for p in profiles:
        print(f"Running profile: {p['profile_name']}")
        df=simulate_ldpc_bler_sionna(p['num_bits_per_symbol'],p['code_rate'],p['ebno_values'],n_codeword,batch_size,num_batches,decoder_iterations,seed)
        df['profile_name']=p['profile_name']; df['mcs_like']=p['mcs_like']
        df['raw_spectral_efficiency_bpshz']=df['num_bits_per_symbol']*df['actual_code_rate']
        df['effective_spectral_efficiency_bpshz']=df['raw_spectral_efficiency_bpshz']*(1-df['bler'])
        all_results.append(df)
    return pd.concat(all_results,ignore_index=True)

def build_threshold_table(ldpc_results:pd.DataFrame, target_bler:float=0.10)->pd.DataFrame:
    rows=[]
    for name in ldpc_results['profile_name'].unique():
        s=ldpc_results[ldpc_results['profile_name']==name].copy().sort_values('ebno_db')
        valid=s[s['bler']<=target_bler]
        if len(valid)>0:
            threshold=valid.iloc[0]['ebno_db']; found=True
        else:
            threshold=np.nan; found=False
        rows.append({'profile_name':name,'mcs_like':s['mcs_like'].iloc[0],'modulation':s['modulation'].iloc[0],'num_bits_per_symbol':s['num_bits_per_symbol'].iloc[0],'actual_code_rate':s['actual_code_rate'].iloc[0],'raw_spectral_efficiency_bpshz':s['raw_spectral_efficiency_bpshz'].iloc[0],'approx_10pct_bler_ebno_db':threshold,'threshold_found':found})
    return pd.DataFrame(rows).sort_values('raw_spectral_efficiency_bpshz')
