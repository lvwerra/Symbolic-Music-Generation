__all__ = ['sample_full_midi', 'sample_full_step', 'gen_broken']

# `平凡之路
sample_full_midi = 'TimeSig_4/4 Tempo_120 <bar> <melody> p_7/2 d_1 p_2/4 d_1/2 p_10/3 d_1/2 p_3/2 d_1 p_3/4 d_1/2 p_10/3 ' \
              'd_1/2 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_10/2 d_1/2 p_5/3 d_1/2 p_2/4 d_1/2 p_10/3 d_1/2 ' \
              'p_9/3 d_1/2 p_10/3 d_1/2 p_12/3 d_1/2 p_5/3 d_1/2 <bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_7/2 d_1 '\
              'p_2/4 d_1/2 p_10/3 d_1/2 p_3/3 d_1 p_3/4 d_1/2 p_10/3 d_1/2 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> ' \
              'p_10/2 d_1/2 p_5/3 d_1/2 p_2/4 d_1/2 p_10/3 d_1/2 p_9/3 d_1/2 p_10/3 d_1/2 p_12/3 d_1/2 p_5/3 d_1/2 ' \
              '<bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_7/2 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_7/5 d_1/4 p_7/5 d_1/4 '\
              'p_7/5 d_1/2 p_10/4 d_1/2 p_12/4 d_1/2 p_2/5 d_1/2 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_2/5 d_4 ' \
              '<bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_7/5 d_1/2 p_7/5 d_3/4 '\
              'p_5/5 d_1/4 p_5/5 d_3/4 p_3/5 d_1/4 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_2/5 d_4 <bass> p_10/2 ' \
              'd_2 p_5/2 d_2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1 p_7/5 d_1/2 p_10/4 d_1/2 p_12/4 d_1/2 ' \
              'p_2/5 d_1/2 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_2/5 d_4 <bass> p_10/2 d_2 p_5/2 d_2 <bar> ' \
              '<melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_10/4 d_1/4 p_3/5 d_1/4 p_3/5 d_1/2 p_3/5 d_1/2 p_3/5 ' \
              'd_1/2 p_2/5 d_1/2 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_10/4 d_4 <bass> p_10/2 d_2 p_5/2 d_2 ' \
              '<bar> <melody> p_10/4 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_7/5 d_1/4 p_7/5 d_1/4 p_7/5 d_1/2 p_10/4 d_1/2 ' \
              'p_12/4 d_1/2 p_2/5 d_1/2 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_2/5 d_4 <bass> p_10/2 d_2 p_5/2 ' \
              'd_2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_7/5 d_1/2 p_7/5 d_3/4 p_5/5 d_1/4 p_5/5 d_3/4 '\
              'p_3/5 d_1/4 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_2/5 d_4 <bass> p_10/2 d_2 p_5/2 d_2 <bar> ' \
              '<melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1 p_7/5 d_1/2 p_10/4 d_1/2 p_12/4 d_1/2 p_2/5 d_1/2 <bass> ' \
              'p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_2/5 d_4 <bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_2/5 d_1/2 ' \
              'p_2/5 d_1/2 p_2/5 d_1/2 p_10/4 d_1/2 p_3/5 d_1/2 p_3/5 d_1/4 p_3/5 d_1/4 p_3/5 d_1/2 p_2/5 d_1/2 ' \
              '<bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_10/4 d_2 p_10/4 d_1/2 p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 ' \
              '<bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/4 p_5/5 d_1/4 p_7/5 ' \
              'd_1/2 p_7/5 d_1 p_5/5 d_1/2 p_3/5 d_1/4 p_2/5 d_1/4 <bass> p_7/2 d_1 p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 ' \
              'd_1 p_10/3 d_1/2 p_3/2 d_1/2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/4 p_12/4 ' \
              'd_1/4 p_12/4 d_1/2 p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> ' \
              'p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/4 p_5/5 d_1/4 p_7/5 d_1/2 p_7/5 d_1 p_7/5 d_1/2 p_10/5 d_1/4 ' \
              'p_10/5 d_1/4 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/2 p_12/5 ' \
              'd_1/2 p_12/5 d_3/4 p_5/5 d_1/4 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 d_1 p_5/3 d_1/2 p_10/2 d_1/2 ' \
              'p_5/2 d_2 <bar> <melody> p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_1/2 p_2/6 d_1/2 p_7/6 d_3/4 p_5/6 d_1/4 ' \
              'p_5/6 d_1/2 p_3/6 d_1/2 <bass> p_7/2 d_1 p_2/3 d_1/2 p_7/2 d_1/2 p_3/2 d_2 <bar> <melody> p_2/6 d_1 ' \
              'p_2/6 d_1/2 p_12/5 d_1/2 p_12/5 d_1 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 d_1 p_5/3 d_1/2 p_10/2 d_1/2 '\
              'p_5/2 d_2 <bar> <melody> p_10/5 d_1 p_10/5 d_1/2 p_12/5 d_1/2 p_10/5 d_3/4 p_10/5 d_1/4 p_9/5 d_1/2 ' \
              'p_10/5 d_1/2 <bass> p_7/2 d_1 p_2/3 d_1/2 p_7/2 d_1/2 p_3/2 d_2 <bar> <melody> p_12/5 d_1 p_10/5 d_1 ' \
              'p_10/5 d_1 p_5/4 d_1 <bass> p_5/2 d_2 p_10/2 d_2 <bar> <melody> p_7/2 d_1 p_2/4 d_1/2 p_10/3 d_1/2 ' \
              'p_3/3 d_1 p_3/4 d_1/2 p_10/3 d_1/2 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_10/2 d_1/2 p_5/3 d_1/2 ' \
              'p_2/4 d_1/2 p_10/3 d_1/2 p_9/3 d_1/2 p_10/3 d_1/2 p_12/3 d_1/2 p_5/3 d_1/2 <bass> p_10/2 d_2 p_5/2 d_2 '\
              '<bar> <melody> p_7/2 d_1 p_2/4 d_1/2 p_10/3 d_1/2 p_3/3 d_1 p_3/4 d_1/2 p_10/3 d_1/2 <bass> p_7/2 d_2 ' \
              'p_3/2 d_2 <bar> <melody> p_10/2 d_1/2 p_5/3 d_1/2 p_2/4 d_1/2 p_10/3 d_1/2 p_9/3 d_1/2 p_10/3 d_1/2 ' \
              'p_12/3 d_1/2 p_5/3 d_1/2 <bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_7/2 d_1/2 p_2/5 d_1/2 p_2/5 ' \
              'd_1/2 p_7/5 d_1/4 p_7/5 d_1/4 p_7/5 d_1/2 p_10/4 d_1/2 p_12/4 d_1/2 p_2/5 d_1/2 <bass> p_7/2 d_2 p_3/2 '\
              'd_2 <bar> <melody> p_2/5 d_4 <bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 ' \
              'd_1/2 p_7/5 d_1/2 p_7/5 d_3/4 p_5/5 d_1/4 p_5/5 d_3/4 p_3/5 d_1/4 <bass> p_7/2 d_2 p_3/2 d_2 <bar> ' \
              '<melody> p_2/5 d_4 <bass> p_10/2 d_1 p_5/3 d_1/2 p_10/2 d_1/2 p_5/2 d_2 <bar> <melody> p_2/5 d_1/2 ' \
              'p_2/5 d_1/4 p_2/5 d_1/4 p_2/5 d_1 p_7/5 d_1/2 p_10/4 d_1/4 p_10/4 d_1/4 p_12/4 d_1/2 p_2/5 d_1/2 ' \
              '<bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> p_2/5 d_4 <bass> p_10/2 d_1 p_5/3 d_1/2 p_10/2 d_1/2 p_5/2 ' \
              'd_1 p_9/3 d_1/4 p_5/2 d_1/4 p_9/3 d_1/2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_10/4 ' \
              'd_1/2 p_3/5 d_1/2 p_3/5 d_1/4 p_3/5 d_1/4 p_3/5 d_1/2 p_2/5 d_1/2 <bass> p_7/2 d_1 p_10/3 d_1/2 p_7/2 ' \
              'd_1/2 p_3/2 d_1 p_3/2 d_1 <bar> <melody> p_10/4 d_1 p_5/4 d_1 p_5/4 d_1/2 p_5/5 d_1/2 p_7/5 d_1/2 ' \
              'p_9/5 d_1/2 <bass> p_10/2 d_1 p_10/2 d_1 p_5/2 d_1 p_5/2 d_1 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 ' \
              'p_10/5 d_1/4 p_5/5 d_1/4 p_7/5 d_1/2 p_7/5 d_1 p_5/5 d_1/2 p_3/5 d_1/4 p_2/5 d_1/4 <bass> p_7/2 d_1 ' \
              'p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 d_1 p_10/3 d_1/2 p_3/2 d_1/2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 ' \
              'p_2/5 d_1/2 p_2/5 d_1/4 p_12/4 d_1/4 p_12/4 d_1/2 p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 ' \
              'd_3/4 p_10/2 d_5/4 p_5/2 d_1/2 p_5/5 d_1/4 p_5/2 d_1/4 p_9/3 d_1/2 p_5/2 d_1/2 <bar> <melody> p_10/5 ' \
              'd_1/2 p_10/5 d_1/2 p_10/5 d_1/4 p_5/5 d_1/4 p_7/5 d_1/2 p_7/5 d_1 p_7/5 d_1/2 p_10/5 d_1/4 p_10/5 ' \
              'd_1/4 <bass> p_7/2 d_1 p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 d_1 p_10/3 d_1/2 p_3/2 d_1/2 <bar> <melody> ' \
              'p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/2 p_12/5 d_1/2 p_12/5 d_3/4 p_5/5 d_1/4 p_7/5 d_1/2 p_9/5 d_1/2 ' \
              '<bass> p_10/2 d_1 p_10/2 d_1 p_5/2 d_1 p_5/2 d_1 <bar> <melody> p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_1/2 ' \
              'p_2/6 d_1/2 p_7/6 d_3/4 p_5/6 d_1/4 p_5/6 d_1/2 p_3/6 d_1/2 <bass> p_7/2 d_1 p_7/2 d_1 p_3/2 d_1 p_3/2 '\
              'd_1 <bar> <melody> p_2/6 d_1 p_2/6 d_1/2 p_12/5 d_1/2 p_12/5 d_1 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 '\
              'd_1/2 p_r d_1/4 p_10/2 d_1/4 p_10/3 d_1/2 p_10/2 d_1/2 p_5/2 d_1 p_5/2 d_1 <bar> <melody> p_10/5 d_3/4 '\
              'p_10/5 d_1/4 p_10/5 d_1/2 p_12/5 d_1/2 p_10/5 d_3/4 p_10/5 d_1/4 p_9/5 d_1/2 p_10/5 d_1/2 <bass> p_7/2 '\
              'd_1 p_10/3 d_1 p_3/2 d_1 p_3/2 d_1 <bar> <melody> p_12/5 d_1 p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_2 ' \
              '<bass> p_5/2 d_2 p_10/2 d_1 p_10/2 d_1 <bar> <melody> p_10/4 d_1/2 p_9/4 d_1/4 p_10/4 d_1/4 p_10/4 ' \
              'd_1/2 p_9/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_10/4 d_1/2 p_10/4 d_1/2 p_5/4 d_1/2 <bass> p_10/2 d_1 ' \
              'p_2/4 d_1/2 p_10/3 d_1/2 p_10/3 d_3/4 p_10/3 d_1/4 p_10/3 d_1 <bar> <melody> p_10/4 d_1/2 p_9/4 d_1/2 ' \
              'p_10/4 d_3/4 p_10/4 d_1/4 p_9/4 d_1/4 p_10/4 d_1/2 p_7/4 d_1/4 p_10/4 d_1/2 p_10/4 d_1/2 <bass> p_10/2 '\
              'd_4 <bar> <melody> p_10/4 d_1 p_10/4 d_3/4 p_10/4 d_1/4 p_10/4 d_1/2 p_10/4 d_1/4 p_10/4 d_1/4 p_12/4 ' \
              'd_1/2 p_5/4 d_1/2 <bass> p_10/2 d_4 <bar> <melody> p_10/4 d_1/2 p_9/4 d_1/2 p_10/4 d_3/4 p_10/4 d_1/4 ' \
              'p_12/4 d_1 p_12/4 d_1 <bass> p_10/2 d_4 <bar> <melody> p_12/4 d_1/2 p_9/4 d_1/2 p_10/4 d_3/4 p_10/4 ' \
              'd_1/4 p_10/4 d_1/2 p_10/4 d_1/2 p_10/4 d_1/2 p_5/4 d_1/2 <bass> p_7/2 d_4 <bar> <melody> p_5/4 d_1/2 ' \
              'p_5/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_5/4 d_1/4 p_10/4 d_1/4 p_9/4 d_1/4 p_10/4 d_3/4 p_10/4 d_1 ' \
              '<bass> p_10/2 d_4 <bar> <melody> p_10/4 d_1 p_10/4 d_1/2 p_9/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_12/4 ' \
              'd_1/4 p_2/5 d_1/4 p_3/5 d_1/2 p_2/5 d_1/2 <bass> p_10/2 d_4 <bar> <melody> p_10/4 d_1/2 p_9/4 d_1/4 ' \
              'p_10/4 d_1/4 p_12/4 d_1/2 p_5/4 d_1/4 p_10/4 d_1/4 p_12/4 d_1/4 p_2/5 d_1/4 p_3/5 d_1/2 p_2/5 d_1 ' \
              '<bass> p_10/2 d_4 <bar> <melody> p_2/5 d_1/2 p_9/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_9/4 d_1/4 p_10/4 ' \
              'd_1/4 p_10/4 d_1/2 p_10/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_5/4 d_1/2 <bass> p_10/2 d_4 <bar> <melody> '\
              'p_10/4 d_1 p_10/4 d_1/2 p_9/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_10/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 ' \
              'p_5/4 d_1/2 <bass> p_10/2 d_4 <bar> <melody> p_10/4 d_1/2 p_9/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_9/4 ' \
              'd_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_10/4 d_1/2 p_10/4 d_1/2 p_12/4 d_1/2 <bass> p_10/2 d_4 <bar> ' \
              '<melody> p_12/4 d_1/2 p_9/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_5/4 d_1/4 p_10/4 d_1/4 p_9/4 d_1/4 ' \
              'p_10/4 d_1/4 p_12/4 d_1/2 p_12/4 d_1 <bass> p_7/2 d_4 <bar> <melody> p_12/4 d_1/2 p_12/4 d_1/4 p_2/5 ' \
              'd_1/4 p_2/5 d_1/2 p_12/4 d_1/4 p_2/5 d_1/4 p_2/5 d_1/2 p_2/5 d_1/4 p_3/5 d_1/4 p_7/5 d_1/2 p_5/5 d_1/2 '\
              '<bass> p_10/2 d_4 <bar> <melody> p_5/5 d_1/2 p_5/5 d_1/4 p_7/5 d_1/4 p_5/5 d_1/2 p_3/5 d_1/4 p_2/5 ' \
              'd_1/4 p_3/5 d_1/2 p_2/5 d_1/4 p_12/4 d_1/4 p_2/5 d_1/2 p_10/4 d_1/2 <bass> p_10/2 d_4 <bar> <melody> ' \
              'p_10/4 d_1/2 p_9/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_9/4 d_1/4 p_10/4 d_1/4 p_10/4 d_1/2 p_12/4 d_1/4 ' \
              'p_2/5 d_1/4 p_3/5 d_1/2 p_2/5 d_1/2 <bass> p_10/2 d_4 <bar> <melody> p_2/5 d_1/2 p_10/4 d_1/4 p_12/4 ' \
              'd_1/4 p_2/5 d_1/2 p_5/5 d_1/2 p_12/4 d_1/4 p_2/5 d_1/4 p_3/5 d_1/2 p_2/5 d_1 <bass> p_10/2 d_4 <bar> ' \
              '<melody> p_2/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1 p_10/5 d_1/2 p_10/5 d_1/2 p_12/5 d_1/2 p_10/5 d_1/2 ' \
              '<bass> p_7/2 d_1 p_7/3 d_1/2 p_7/2 d_1/2 p_3/2 d_1 p_3/2 d_1 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 ' \
              'p_10/5 d_1/2 p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_1/2 <bass> p_10/2 d_1 p_10/2 ' \
              'd_1 p_5/2 d_1/2 p_5/2 d_1/2 p_9/3 d_1/2 p_5/2 d_1/2 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 ' \
              'd_1 p_10/5 d_1/2 p_10/5 d_1/2 p_12/5 d_1/2 p_10/5 d_1/2 <bass> p_7/2 d_2 p_3/2 d_1 p_3/2 d_1 <bar> ' \
              '<melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_1/2 p_9/5 d_1/2 ' \
              'p_10/5 d_1/2 <bass> p_10/2 d_1 p_10/2 d_1 p_5/2 d_1 p_5/2 d_1 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 '\
              'p_10/5 d_1 p_10/5 d_1/2 p_10/5 d_1/2 p_12/5 d_1/2 p_10/5 d_1/2 <bass> p_7/2 d_1 p_7/2 d_1 p_3/2 d_1 ' \
              'p_3/2 d_1 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_1/2 ' \
              'p_9/5 d_1/2 p_10/5 d_1/2 <bass> p_10/2 d_1 p_10/2 d_1 p_5/2 d_1 p_5/2 d_1 <bar> <melody> p_10/5 d_1/2 ' \
              'p_10/5 d_1/2 p_10/5 d_1 p_10/5 d_1/2 p_10/5 d_1/2 p_12/5 d_1/2 p_10/5 d_1/2 <bass> p_7/2 d_1 p_7/2 d_1 '\
              'p_3/2 d_3/4 p_3/2 d_1/4 p_10/3 d_1/2 p_3/2 d_1/2 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/2 '\
              'p_10/5 d_1/2 p_9/5 d_1/2 p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 d_1 p_10/2 d_1 p_5/2 d_1 ' \
              'p_5/2 d_1 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/4 p_5/5 d_1/4 p_7/5 d_1/2 p_7/5 d_1 ' \
              'p_5/5 d_1/2 p_3/5 d_1/4 p_2/5 d_1/4 <bass> p_7/2 d_1 p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 d_3/4 p_3/2 d_1/4 ' \
              'p_3/2 d_1/2 p_3/2 d_1/2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/4 p_12/4 d_1/4 ' \
              'p_12/4 d_1/2 p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 d_1 p_10/2 d_1 p_5/2 d_2 <bar> <melody> '\
              'p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/4 p_5/5 d_1/4 p_7/5 d_1/2 p_7/5 d_1 p_7/5 d_1/2 p_10/5 d_1/4 ' \
              'p_10/5 d_1/4 <bass> p_7/2 d_1 p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 d_1 p_3/2 d_1 <bar> <melody> p_10/5 d_1/2 '\
              'p_10/5 d_1/2 p_10/5 d_1/2 p_12/5 d_1/4 p_12/5 d_1/4 p_12/5 d_1/2 p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 ' \
              '<bass> p_10/2 d_1 p_10/2 d_1/4 p_10/2 d_1/4 p_5/2 d_1/2 p_5/2 d_2 <bar> <melody> p_10/5 d_1/2 p_9/5 ' \
              'd_1/2 p_10/5 d_1/2 p_2/6 d_1/2 p_7/6 d_3/4 p_5/6 d_1/4 p_5/6 d_1/2 p_3/6 d_1/2 <bass> p_7/2 d_1 p_10/3 '\
              'd_1/2 p_7/2 d_1/2 p_3/2 d_1 p_3/2 d_1 <bar> <melody> p_2/6 d_1 p_2/6 d_1/2 p_12/5 d_1/2 p_12/5 d_1 ' \
              'p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 d_1 p_10/2 d_1 p_5/2 d_1/2 p_9/3 d_1/4 p_5/2 d_1/4 p_9/3 d_1/2 ' \
              'p_5/2 d_1/2 <bar> <melody> p_10/5 d_3/4 p_10/5 d_1/4 p_10/5 d_1/2 p_12/5 d_1/2 p_10/5 d_3/4 p_10/5 ' \
              'd_1/4 p_9/5 d_1/2 p_10/5 d_1/2 <bass> p_7/2 d_1/2 p_r d_1/4 p_7/2 d_1/4 p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 '\
              'd_1 p_3/2 d_1 <bar> <melody> p_12/5 d_1 p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_2 <bass> p_5/2 d_1 p_5/3 ' \
              'd_1/2 p_5/2 d_1/2 p_10/2 d_1 p_10/2 d_1 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/4 p_5/5 ' \
              'd_1/4 p_7/5 d_1/2 p_7/5 d_1 p_5/5 d_1/2 p_3/5 d_1/4 p_2/5 d_1/4 <bass> p_7/2 d_1 p_7/2 d_1 p_3/2 d_1 ' \
              'p_3/2 d_1 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/4 p_12/4 d_1/4 p_12/4 d_1/2 ' \
              'p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 d_3/4 p_10/2 d_1/4 p_10/3 d_1/2 p_10/2 d_1/2 p_5/2 ' \
              'd_3/4 p_5/2 d_1/4 p_9/3 d_1/2 p_5/2 d_1/2 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/4 p_5/5 ' \
              'd_1/4 p_7/5 d_1/2 p_7/5 d_1 p_7/5 d_1/2 p_10/5 d_1/4 p_10/5 d_1/4 <bass> p_7/2 d_1 p_7/2 d_1 p_3/2 d_1 '\
              'p_3/2 d_1 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/2 p_12/5 d_1/4 p_12/5 d_1/4 p_12/5 d_1/2 '\
              'p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 d_1 p_10/2 d_1 p_5/2 d_3/4 p_5/2 d_1/4 p_9/3 d_1/4 ' \
              'p_5/2 d_1/4 p_9/3 d_1/2 <bar> <melody> p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_1/2 p_2/6 d_1/2 p_7/6 d_3/4 ' \
              'p_5/6 d_1/4 p_5/6 d_1/2 p_3/6 d_1/2 <bass> p_7/2 d_1 p_10/3 d_1/2 p_5/2 d_1/2 p_3/3 d_3/4 p_3/3 d_1/4 ' \
              'p_10/3 d_1/2 p_3/3 d_1/2 <bar> <melody> p_2/6 d_1 p_2/6 d_1/2 p_12/5 d_1/2 p_12/5 d_1 p_7/5 d_1/2 ' \
              'p_9/5 d_1/2 <bass> p_10/2 d_3/4 p_10/2 d_1/4 p_10/3 d_1/2 p_10/2 d_1/2 p_5/2 d_3/4 p_5/2 d_1/4 p_9/3 ' \
              'd_1/2 p_5/2 d_1/2 <bar> <melody> p_10/5 d_3/4 p_10/5 d_1/4 p_10/5 d_1/2 p_12/5 d_1/2 p_10/5 d_3/4 ' \
              'p_10/5 d_1/4 p_9/5 d_1/2 p_10/5 d_1/2 <bass> p_7/2 d_3/4 p_7/2 d_1/4 p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 ' \
              'd_1 p_3/2 d_1 <bar> <melody> p_12/5 d_1 p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_2 <bass> p_5/2 d_1 p_5/2 d_1 '\
              'p_10/2 d_1 p_10/2 d_1 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/4 p_5/5 d_1/4 p_7/5 d_1/2 ' \
              'p_7/5 d_1 p_5/5 d_1/2 p_3/5 d_1/4 p_2/5 d_1/4 <bass> p_7/2 d_1 p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 d_3/4 ' \
              'p_3/2 d_1/4 p_10/3 d_1/2 p_3/2 d_1/2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/4 ' \
              'p_12/4 d_1/4 p_12/4 d_1/2 p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 <bass> p_10/2 d_1 p_10/2 d_1 p_5/2 d_3/4 '\
              'p_5/2 d_1/4 p_9/3 d_1/2 p_5/2 d_1/2 <bar> <melody> p_10/5 d_1/2 p_10/5 d_1/2 p_10/5 d_1/4 p_5/5 d_1/4 ' \
              'p_7/5 d_1/2 p_7/5 d_1 p_7/5 d_1/2 p_10/5 d_1/4 p_10/5 d_1/4 <bass> p_7/2 d_3/4 p_7/2 d_1/4 p_10/3 ' \
              'd_1/2 p_7/2 d_1/2 p_3/2 d_3/4 p_3/2 d_1/4 p_10/3 d_1/2 p_3/2 d_1/2 <bar> <melody> p_10/5 d_1/2 p_10/5 ' \
              'd_1/2 p_10/5 d_1/2 p_12/5 d_1/4 p_12/5 d_1/4 p_12/5 d_1/2 p_5/5 d_1/2 p_7/5 d_1/2 p_9/5 d_1/2 <bass> ' \
              'p_10/2 d_3/4 p_10/2 d_1/4 p_10/3 d_1/2 p_10/2 d_1/2 p_5/2 d_3/4 p_5/2 d_1/4 p_9/3 d_1/2 p_5/2 d_1/2 ' \
              '<bar> <melody> p_10/5 d_1/2 p_9/5 d_1/2 p_10/5 d_1/2 p_2/6 d_1/2 p_7/6 d_3/4 p_5/6 d_1/4 p_5/6 d_1/2 ' \
              'p_3/6 d_1/2 <bass> p_7/2 d_3/4 p_7/2 d_1/4 p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 d_3/4 p_3/2 d_1/4 p_10/3 ' \
              'd_1/2 p_3/2 d_1/2 <bar> <melody> p_2/6 d_1 p_2/6 d_1/2 p_12/5 d_1/2 p_12/5 d_1 p_7/5 d_1/2 p_9/5 d_1/2 '\
              '<bass> p_10/2 d_3/4 p_10/2 d_1/4 p_10/3 d_1/2 p_10/2 d_1/2 p_5/2 d_2 <bar> <melody> p_10/5 d_3/4 ' \
              'p_10/5 d_1/4 p_10/5 d_1/2 p_12/5 d_1/2 p_10/5 d_3/4 p_10/5 d_1/4 p_9/5 d_1/2 p_10/5 d_1/2 <bass> p_7/2 '\
              'd_1 p_10/3 d_1/2 p_7/2 d_1/2 p_3/2 d_1 p_3/2 d_1 <bar> <melody> p_12/5 d_1 p_10/5 d_1/2 p_9/5 d_1/2 ' \
              'p_10/5 d_2 <bass> p_5/2 d_1 p_5/2 d_1 p_10/2 d_2 <bar> <melody> p_2/3 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 ' \
              'p_7/5 d_1/4 p_7/5 d_1/4 p_7/5 d_1/2 p_10/4 d_1/2 p_12/4 d_1/2 p_2/5 d_1/2 <bass> p_7/2 d_2 p_3/2 d_2 ' \
              '<bar> <melody> p_2/5 d_4 <bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 ' \
              'd_1/2 p_7/5 d_1/2 p_7/5 d_3/4 p_5/5 d_1/4 p_5/5 d_3/4 p_3/5 d_1/4 <bass> p_7/2 d_2 p_3/2 d_2 <bar> ' \
              '<melody> p_2/5 d_4 <bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/4 p_2/5 d_1/4 ' \
              'p_2/5 d_1 p_7/5 d_1/2 p_10/4 d_1/2 p_12/4 d_1/2 p_2/5 d_1/2 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> ' \
              'p_2/5 d_4 <bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_2/5 d_1/2 p_2/5 d_1/2 p_2/5 d_1/2 p_10/4 d_1/4 ' \
              'p_3/5 d_1/4 p_3/5 d_1/2 p_3/5 d_1/2 p_3/5 d_1/2 p_2/5 d_1/2 <bass> p_7/2 d_2 p_3/2 d_2 <bar> <melody> ' \
              'p_10/4 d_4 <bass> p_10/2 d_2 p_5/2 d_2 <bar> <melody> p_10/4 d_2 p_r d_2 <bass> p_r d_4 </s> '

sample_full_step = 'TimeSig_1/4 Tempo_115 <bar> <melody> p_r d_1/2 p_2/5_C d_1/2 <bass> <tup> p_r p_11/3_B p_11/2_B ' \
                   'd_1 </tup> <bar> <melody> p_2/5_C d_1 <bass> p_11/2_B d_1 <bar> <melody> p_2/5_C d_1 <bass> ' \
                   'p_11/2_B d_1 <bar> <melody> p_2/5_C d_1 <bass> p_11/3_B d_1/4 p_r d_3/4 <bar> <melody> p_2/5_C ' \
                   'd_1/4 p_10/3_A d_1/4 p_1/5_C d_1/2 <bass> p_6/4_F d_1/4 p_6/2_F d_1/4 p_6/2_F d_1/2 <bar> ' \
                   '<melody> p_1/5_C d_1 <bass> p_6/2_F d_1 <bar> <melody> p_1/5_C d_1 <bass> p_6/2_F d_1 <bar> ' \
                   '<melody> p_1/5_C d_1 <bass> p_6/2_F d_1/2 p_r d_1/2 <bar> <melody> p_1/5_C d_1/4 p_r d_1/4 ' \
                   'p_11/4_B d_1/2 <bass> p_r d_1/2 p_7/2_F d_1/2 <bar> <melody> p_11/4_B d_1 <bass> p_7/2_F d_1 ' \
                   '<bar> <melody> p_11/4_B d_1 <bass> p_7/2_F d_1 <bar> <melody> p_11/4_B d_1 <bass> p_7/4_F d_1 ' \
                   '<bar> <melody> p_11/4_B d_1/2 p_11/4_B d_1/2 <bass> <tup> p_r p_6/2_F p_r d_1 </tup> <bar> ' \
                   '<melody> p_11/4_B d_1 <bass> p_4/4_E d_1 <bar> <melody> p_11/4_B d_1/2 p_1/5_C d_1/2 <bass> <tup> ' \
                   'p_r p_6/3_F p_6/3_F d_1 </tup> <bar> <melody> p_6/5_F d_1/4 p_6/5_F d_3/4 <bass> p_6/3_F d_1/4 ' \
                   'p_r d_3/4 <bar> <melody> p_1/5_C d_1/4 p_r d_1/4 p_2/5_C d_1/2 <bass> <tup> p_6/4_F p_11/2_B ' \
                   'p_11/2_B d_1 </tup> <bar> <melody> p_2/5_C d_1 <bass> p_11/2_B d_1 <bar> <melody> p_2/5_C d_1 ' \
                   '<bass> p_11/2_B d_1 <bar> <melody> p_2/5_C d_1 <bass> p_11/3_B d_1/4 p_r d_3/4 <bar> <melody> ' \
                   'p_2/5_C d_1/2 p_1/5_C d_1/2 <bass> p_6/4_F d_1/4 p_6/2_F d_1/4 p_6/2_F d_1/2 <bar> <melody> ' \
                   'p_1/5_C d_1 <bass> p_6/2_F d_1 <bar> <melody> p_1/5_C d_1 <bass> p_6/2_F d_1 <bar> <melody> ' \
                   'p_1/5_C d_1 <bass> p_6/2_F d_1/2 p_r d_1/2 <bar> <melody> p_1/5_C d_1/2 p_11/4_B d_1/2 <bass> ' \
                   '<tup> p_r p_7/3_F p_7/2_F d_1 </tup> <bar> <melody> p_11/4_B d_1 <bass> p_7/2_F d_1 <bar> ' \
                   '<melody> p_11/4_B d_1 <bass> p_7/2_F d_3/4 p_7/2_F d_1/4 <bar> <melody> p_11/4_B d_1 <bass> ' \
                   'p_7/4_F d_1 <bar> <melody> p_11/4_B d_1/4 p_10/3_A d_1/4 p_10/4_A d_1/2 <bass> <tup> p_r p_6/2_F ' \
                   'p_r d_1 </tup> <bar> <melody> p_10/4_A d_1 <bass> p_6/4_F d_1 <bar> <melody> <tup> p_r p_1/5_C ' \
                   'p_6/5_F d_1 </tup> <bass> <tup> p_r p_6/4_F p_6/3_F d_1 </tup> <bar> <melody> p_6/5_F d_1 <bass> ' \
                   'p_6/3_F d_1/4 p_6/4_F d_3/4 <bar> <melody> p_6/5_F d_1/4 p_r d_1/4 p_6/5_F d_1/4 p_r d_1/4 <bass> ' \
                   'p_6/4_F d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_2/5_C d_1 <bass> p_11/2_B d_3/4 p_11/4_B ' \
                   'd_1/4 <bar> <melody> p_2/5_C d_1 <bass> p_11/4_B d_1/2 p_11/2_B d_1/2 <bar> <melody> p_2/5_C d_1 ' \
                   '<bass> p_11/2_B d_1 <bar> <melody> p_2/5_C d_1/4 p_r d_1/4 p_1/5_C d_1/2 <bass> p_11/2_B d_1/4 ' \
                   'p_r d_1/4 p_6/2_F d_1/2 <bar> <melody> p_1/5_C d_1 <bass> p_6/2_F d_3/4 p_r d_1/4 <bar> <melody> ' \
                   'p_1/5_C d_1 <bass> p_10/4_A d_1/2 p_6/2_F d_1/2 <bar> <melody> p_1/5_C d_1 <bass> p_6/2_F d_1 ' \
                   '<bar> <melody> p_1/5_C d_1/4 p_r d_1/4 p_1/5_C d_1/4 p_r d_1/4 <bass> p_11/4_B d_1/4 p_r d_1/4 ' \
                   'p_4/2_E d_1/2 <bar> <melody> p_11/4_B d_1 <bass> p_4/2_E d_1 <bar> <melody> p_11/4_B d_1 <bass> ' \
                   'p_7/4_F d_1/2 p_4/2_E d_1/2 <bar> <melody> p_11/4_B d_1 <bass> p_4/2_E d_1 <bar> <melody> ' \
                   'p_11/4_B d_1/4 p_r d_1/4 p_1/5_C d_1/2 <bass> p_4/2_E d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> ' \
                   '<melody> p_2/5_C d_1/4 p_r d_1/4 p_1/5_C d_1/4 p_r d_1/4 <bass> p_6/2_F d_1 <bar> <melody> ' \
                   'p_1/5_C d_1 <bass> p_10/4_A d_1/2 p_6/2_F d_1/2 <bar> <melody> p_6/5_F d_1 <bass> p_6/2_F d_1 ' \
                   '<bar> <melody> p_4/5_E d_1/4 p_r d_1/4 p_6/5_F d_1/2 <bass> p_6/2_F d_1/4 p_r d_1/4 p_11/2_B ' \
                   'd_1/2 <bar> <melody> p_6/5_F d_1 <bass> p_11/2_B d_1/2 p_11/4_B d_1/2 <bar> <melody> p_6/5_F d_1 ' \
                   '<bass> p_11/4_B d_1/2 p_11/2_B d_1/2 <bar> <melody> p_6/5_F d_1 <bass> p_11/2_B d_1 <bar> ' \
                   '<melody> p_6/5_F d_1/4 p_r d_1/4 p_6/5_F d_1/2 <bass> p_2/5_C d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> ' \
                   '<melody> p_6/5_F d_1 <bass> p_6/2_F d_3/4 p_r d_1/4 <bar> <melody> p_6/5_F d_1 <bass> p_12/4_B ' \
                   'd_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> <melody> p_6/5_F d_1 <bass> p_6/2_F d_1 <bar> <melody> ' \
                   'p_6/5_F d_1/4 p_r d_1/4 p_2/5_C d_1/2 <bass> p_11/4_B d_1/4 p_r d_1/4 p_4/2_E d_1/2 <bar> ' \
                   '<melody> p_2/5_C d_1 <bass> p_4/2_E d_3/4 p_r d_1/4 <bar> <melody> p_2/5_C d_1 <bass> p_7/4_F ' \
                   'd_1/2 p_4/2_E d_1/2 <bar> <melody> p_2/5_C d_3/4 p_r d_1/4 <bass> p_4/2_E d_1 <bar> <melody> ' \
                   'p_11/4_B d_1/4 p_r d_1/4 p_6/5_F d_1/2 <bass> p_r d_1/2 p_6/2_F d_1/2 <bar> <melody> p_6/5_F d_1 ' \
                   '<bass> p_6/2_F d_3/4 p_r d_1/4 <bar> <melody> p_6/5_F d_1 <bass> p_1/5_C d_1/4 p_r d_1/4 p_6/2_F ' \
                   'd_1/2 <bar> <melody> p_6/5_F d_1 <bass> p_6/2_F d_1 <bar> <melody> p_6/5_F d_1/4 p_r d_1/4 ' \
                   'p_11/5_B d_1/2 <bass> p_1/5_C d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_11/5_B d_3/4 p_r ' \
                   'd_1/4 <bass> p_11/2_B d_1 <bar> <melody> p_2/5_C d_1 <bass> p_11/2_B d_1/4 p_r d_1/4 p_11/2_B ' \
                   'd_1/2 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_1/6_C d_1/4 p_r d_1/4 <bass> p_11/2_B d_1 <bar> ' \
                   '<melody> p_11/5_B d_1/4 p_r d_1/4 p_10/5_A d_1/4 p_r d_1/4 <bass> p_6/4_F d_1/2 p_6/2_F d_1/2 ' \
                   '<bar> <melody> p_6/5_F d_1/4 p_r d_1/4 p_6/5_F d_1/4 p_r d_1/4 <bass> p_6/2_F d_1 <bar> <melody> ' \
                   'p_4/5_E d_1/4 p_r d_1/4 p_6/5_F d_1/2 <bass> p_6/2_F d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> <melody> ' \
                   'p_4/5_E d_1/4 p_r d_1/4 p_6/5_F d_1/4 p_r d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_4/5_E d_1/4 ' \
                   'p_r d_1/4 p_6/5_F d_1/2 <bass> p_6/2_F d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_6/5_F ' \
                   'd_1/2 p_10/5_A d_1/2 <bass> p_11/2_B d_1 <bar> <melody> p_10/5_A d_1/4 p_r d_1/4 p_2/4_C d_1/2 ' \
                   '<bass> p_11/2_B d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_10/5_A d_1/4 p_r d_1/4 p_10/5_A ' \
                   'd_1/4 p_r d_1/4 <bass> p_11/2_B d_1 <bar> <melody> p_10/5_A d_1/4 p_r d_1/4 p_10/5_A d_1/4 p_r ' \
                   'd_1/4 <bass> p_11/2_B d_1/4 p_r d_1/4 p_1/3_C d_1/2 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 ' \
                   'p_1/6_C d_1/4 p_r d_1/4 <bass> p_1/5_C d_1 <bar> <melody> p_10/5_A d_1/4 p_r d_1/4 p_11/5_B d_1/4 ' \
                   'p_r d_1/4 <bass> p_1/5_C d_1/2 p_1/3_C d_1/2 <bar> <melody> p_7/5_F d_1/4 p_r d_1/4 p_r d_1/2 ' \
                   '<bass> p_1/3_C d_1/4 p_r d_3/4 <bar> <melody> p_4/5_E d_1/4 p_r d_1/4 p_6/5_F d_1/2 <bass> p_r ' \
                   'd_1/2 p_11/2_B d_1/2 <bar> <melody> p_6/5_F d_1/2 p_11/5_B d_1/2 <bass> p_11/2_B d_1/2 p_r d_1/2 ' \
                   '<bar> <melody> p_11/5_B d_1/2 p_2/4_C d_1/2 <bass> p_2/5_C d_1/2 p_11/2_B d_1/2 <bar> <melody> ' \
                   'p_11/5_B d_1/4 p_r d_1/4 p_1/6_C d_1/4 p_r d_1/4 <bass> p_11/2_B d_3/4 p_r d_1/4 <bar> <melody> ' \
                   'p_11/5_B d_1/4 p_r d_1/4 p_10/5_A d_1/4 p_r d_1/4 <bass> p_2/5_C d_1/4 p_r d_1/4 p_6/2_F d_1/2 ' \
                   '<bar> <melody> p_6/5_F d_1 <bass> p_1/5_C d_1 <bar> <melody> p_6/5_F d_1 <bass> p_1/5_C d_1/2 ' \
                   'p_6/2_F d_1/2 <bar> <melody> p_6/5_F d_1 <bass> p_6/2_F d_1 <bar> <melody> p_6/5_F d_1/2 p_6/5_F ' \
                   'd_1/4 p_r d_1/4 <bass> p_6/2_F d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_11/4_B d_3/4 p_r ' \
                   'd_1/4 <bass> p_11/2_B d_1/4 p_r d_3/4 <bar> <melody> p_11/4_B d_1/4 p_r d_1/4 p_2/5_C d_1/2 ' \
                   '<bass> p_r d_1/2 p_11/2_B d_1/2 <bar> <melody> p_2/5_C d_1 <bass> p_11/2_B d_1 <bar> <melody> ' \
                   'p_1/5_C d_1/4 p_r d_1/4 p_1/5_C d_1/2 <bass> p_11/4_B d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> ' \
                   '<melody> p_1/5_C d_1 <bass> p_6/2_F d_1/2 p_r d_1/2 <bar> <melody> p_1/5_C d_1/4 p_r d_1/4 ' \
                   'p_11/4_B d_1/2 <bass> p_10/4_A d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> <melody> p_10/4_A d_1/2 ' \
                   'p_6/5_F d_1/4 p_r d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_5/5_E d_1/4 p_r d_1/4 p_6/5_F d_1/4 ' \
                   'p_r d_1/4 <bass> p_6/2_F d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 <bar> <melody> p_2/5_C d_1 ' \
                   '<bass> p_6/3_F d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 <bar> <melody> p_2/5_C d_1 <bass> ' \
                   'p_11/4_B d_1/2 p_11/2_B d_1/4 p_r d_1/4 <bar> <melody> p_2/5_C d_1 <bass> p_6/3_F d_1/4 p_r d_1/4 ' \
                   'p_11/2_B d_1/4 p_r d_1/4 <bar> <melody> p_2/5_C d_1/4 p_r d_1/4 p_1/5_C d_1/2 <bass> p_11/4_B ' \
                   'd_1/4 p_r d_1/4 p_6/2_F d_1/4 p_r d_1/4 <bar> <melody> p_1/5_C d_1 <bass> p_6/3_F d_1/4 p_r d_1/4 ' \
                   'p_6/2_F d_1/4 p_r d_1/4 <bar> <melody> p_1/5_C d_1 <bass> p_10/4_A d_1/2 p_6/2_F d_1/4 p_r d_1/4 ' \
                   '<bar> <melody> p_1/5_C d_1 <bass> p_6/3_F d_1/4 p_r d_1/4 p_6/2_F d_1/4 p_r d_1/4 <bar> <melody> ' \
                   'p_1/5_C d_1/4 p_r d_1/4 p_1/5_C d_1/4 p_r d_1/4 <bass> p_11/4_B d_1/4 p_r d_1/4 p_4/2_E d_1/4 p_r ' \
                   'd_1/4 <bar> <melody> p_11/4_B d_1 <bass> p_4/3_E d_1/4 p_r d_1/4 p_4/2_E d_1/4 p_r d_1/4 <bar> ' \
                   '<melody> p_11/4_B d_1 <bass> p_7/4_F d_1/2 p_4/2_E d_1/2 <bar> <melody> p_11/4_B d_1 <bass> ' \
                   'p_4/3_E d_1/4 p_r d_1/4 p_4/2_E d_1/4 p_r d_1/4 <bar> <melody> p_11/4_B d_1/4 p_r d_1/4 p_2/5_C ' \
                   'd_1/4 p_r d_1/4 <bass> p_7/4_F d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 <bar> <melody> p_2/5_C ' \
                   'd_1/4 p_r d_1/4 p_2/5_C d_1/4 p_r d_1/4 <bass> p_6/3_F d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 ' \
                   '<bar> <melody> p_1/5_C d_1/2 p_2/5_C d_1/4 p_r d_1/4 <bass> p_10/4_A d_1/2 p_11/2_B d_1/4 p_r ' \
                   'd_1/4 <bar> <melody> p_6/5_F d_1 <bass> p_6/3_F d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 <bar> ' \
                   '<melody> p_4/5_E d_1/4 p_r d_1/4 p_6/5_F d_1/2 <bass> p_r d_1/2 p_11/2_B d_1/4 p_r d_1/4 <bar> ' \
                   '<melody> p_6/5_F d_1 <bass> p_6/3_F d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 <bar> <melody> ' \
                   'p_6/5_F d_1 <bass> p_11/4_B d_1/2 p_11/2_B d_1/4 p_r d_1/4 <bar> <melody> p_6/5_F d_1 <bass> ' \
                   'p_6/3_F d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 <bar> <melody> p_6/5_F d_1/4 p_r d_1/4 p_6/5_F ' \
                   'd_1/2 <bass> p_6/3_F d_1/4 p_r d_1/4 p_6/2_F d_1/4 p_r d_1/4 <bar> <melody> p_6/5_F d_1 <bass> ' \
                   'p_6/3_F d_1/4 p_r d_1/4 p_6/2_F d_1/4 p_r d_1/4 <bar> <melody> p_6/5_F d_1 <bass> p_1/5_C d_1/2 ' \
                   'p_6/2_F d_1/4 p_r d_1/4 <bar> <melody> p_6/5_F d_1 <bass> p_6/3_F d_1/4 p_r d_1/4 p_6/2_F d_1/4 ' \
                   'p_r d_1/4 <bar> <melody> p_6/5_F d_1/4 p_r d_1/4 p_2/5_C d_1/2 <bass> p_11/4_B d_1/4 p_r d_1/4 ' \
                   'p_4/2_E d_1/4 p_r d_1/4 <bar> <melody> p_2/5_C d_1 <bass> p_4/3_E d_1/4 p_r d_1/4 p_4/2_E d_1/4 ' \
                   'p_r d_1/4 <bar> <melody> p_2/5_C d_1 <bass> p_7/4_F d_1/2 p_4/2_E d_1/4 p_r d_1/4 <bar> <melody> ' \
                   'p_2/5_C d_3/4 p_r d_1/4 <bass> p_4/3_E d_1/4 p_r d_1/4 p_4/2_E d_1/2 <bar> <melody> p_11/4_B ' \
                   'd_1/4 p_r d_1/4 p_4/5_E d_1/2 <bass> p_4/3_E d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 <bar> ' \
                   '<melody> p_2/5_C d_1 <bass> p_6/3_F d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 <bar> <melody> ' \
                   'p_1/5_C d_1/2 p_2/5_C d_1/4 p_r d_1/4 <bass> p_1/5_C d_1/4 p_r d_1/4 p_11/2_B d_1/4 p_r d_1/4 ' \
                   '<bar> <melody> p_1/5_C d_1 <bass> p_6/3_F d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_2/5_C ' \
                   'd_1/4 p_r d_1/4 p_2/6_C d_1/2 <bass> p_6/3_F d_1/4 p_r d_1/4 p_7/2_F d_1/2 <bar> <melody> p_2/6_C ' \
                   'd_1 <bass> p_7/2_F d_1 <bar> <melody> p_2/6_C d_1/2 p_11/5_B d_1/2 <bass> p_7/2_F d_1 <bar> ' \
                   '<melody> p_11/5_B d_1/2 p_1/6_C d_1/4 p_r d_1/4 <bass> p_7/2_F d_3/4 p_r d_1/4 <bar> <melody> ' \
                   'p_11/5_B d_1/4 p_r d_1/4 p_9/5_G d_1/2 <bass> p_11/3_B d_1/4 p_r d_1/4 p_2/3_C d_1/2 <bar> ' \
                   '<melody> p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> <melody> p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> ' \
                   '<melody> p_9/5_G d_3/4 p_r d_1/4 <bass> p_2/3_C d_3/4 p_r d_1/4 <bar> <melody> p_4/5_E d_1/4 p_r ' \
                   'd_1/4 p_10/5_A d_1/2 <bass> p_r d_1/2 p_6/2_F d_1/2 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F ' \
                   'd_1 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F ' \
                   'd_1/4 p_r d_1/4 p_6/4_F d_1/2 <bar> <melody> p_10/5_A d_1/4 p_r d_1/4 p_11/5_B d_1/2 <bass> ' \
                   'p_1/4_C d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_11/5_B d_1/2 p_1/6_C d_1/4 p_r d_1/4 ' \
                   '<bass> p_11/2_B d_1 <bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1 <bar> <melody> p_11/5_B d_1 ' \
                   '<bass> p_11/2_B d_1/4 p_r d_1/4 p_11/3_B d_1/4 p_r d_1/4 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 ' \
                   'p_2/6_C d_1/2 <bass> p_11/3_B d_1/4 p_r d_1/4 p_7/2_F d_1/2 <bar> <melody> p_2/6_C d_1 <bass> ' \
                   'p_7/2_F d_1 <bar> <melody> p_2/6_C d_1/2 p_11/5_B d_1/2 <bass> p_7/2_F d_1 <bar> <melody> ' \
                   'p_11/5_B d_1/2 p_1/6_C d_1/4 p_r d_1/4 <bass> p_7/2_F d_1/2 p_2/4_C d_1/2 <bar> <melody> p_11/5_B ' \
                   'd_1/4 p_r d_1/4 p_9/5_G d_1/2 <bass> p_11/3_B d_1/4 p_r d_1/4 p_2/3_C d_1/2 <bar> <melody> ' \
                   'p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> <melody> p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> <melody> ' \
                   'p_9/5_G d_3/4 p_6/4_F d_1/4 <bass> p_2/3_C d_1/4 p_r d_1/4 p_9/3_G d_1/4 p_r d_1/4 <bar> <melody> ' \
                   'p_4/5_E d_1/4 p_r d_1/4 p_10/5_A d_1/2 <bass> p_9/3_G d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> ' \
                   '<melody> p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> ' \
                   '<melody> p_10/5_A d_1 <bass> p_6/2_F d_3/4 p_r d_1/4 <bar> <melody> p_10/5_A d_1/4 p_r d_1/4 ' \
                   'p_11/5_B d_1/2 <bass> p_1/4_C d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_11/5_B d_1 <bass> ' \
                   'p_11/2_B d_1 <bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1 <bar> <melody> p_11/5_B d_1 <bass> ' \
                   'p_11/2_B d_1 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_11/6_B d_1/2 <bass> p_11/2_B d_1/2 ' \
                   'p_11/2_B d_1/4 p_6/6_F d_1/4 <bar> <melody> p_6/6_F d_1/4 p_11/5_B d_1/4 p_11/6_B d_1/4 p_6/6_F ' \
                   'd_1/4 <bass> p_11/3_B d_1/4 p_r d_1/4 p_2/4_C d_1/4 p_r d_1/4 <bar> <melody> p_2/6_C d_1/4 ' \
                   'p_11/5_B d_1/4 p_11/6_B d_1/4 p_6/6_F d_1/4 <bass> p_11/3_B d_1/4 p_r d_1/4 p_2/4_C d_1/4 p_r ' \
                   'd_1/4 <bar> <melody> p_6/6_F d_1/4 p_11/5_B d_1/4 p_11/6_B d_1/4 p_6/6_F d_1/4 <bass> p_11/3_B ' \
                   'd_1/4 p_r d_1/4 p_2/4_C d_1/2 <bar> <melody> p_6/6_F d_1/4 p_11/5_B d_1/4 p_10/6_A d_1/4 p_6/6_F ' \
                   'd_1/4 <bass> p_11/3_B d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> <melody> p_1/6_C d_1/4 p_10/5_A d_1/4 ' \
                   'p_10/6_A d_1/4 p_6/6_F d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_1/6_C d_1/4 p_10/5_A d_1/4 ' \
                   'p_10/6_A d_1/4 p_6/6_F d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_1/6_C d_1/4 p_10/5_A d_1/4 ' \
                   'p_10/6_A d_1/4 p_6/6_F d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_1/6_C d_1/4 p_10/5_A d_1/4 ' \
                   'p_11/6_B d_1/4 p_7/6_F d_1/4 <bass> p_6/2_F d_1/4 p_r d_1/4 p_4/2_E d_1/2 <bar> <melody> p_2/6_C ' \
                   'd_1/4 p_11/5_B d_1/4 p_11/6_B d_1/4 p_7/6_F d_1/4 <bass> p_4/2_E d_1 <bar> <melody> p_2/6_C d_1/4 ' \
                   'p_11/5_B d_1/4 p_11/6_B d_1/4 p_7/6_F d_1/4 <bass> p_4/2_E d_1 <bar> <melody> p_2/6_C d_1/4 ' \
                   'p_11/5_B d_1/4 p_11/6_B d_1/4 p_7/6_F d_1/4 <bass> p_4/2_E d_1/2 p_4/4_E d_1/2 <bar> <melody> ' \
                   'p_2/6_C d_1/4 p_11/5_B d_1/4 p_1/7_C d_1/4 p_10/6_A d_1/4 <bass> p_11/3_B d_1/4 p_r d_1/4 p_6/2_F ' \
                   'd_1/2 <bar> <melody> p_6/6_F d_1/4 p_1/6_C d_1/4 p_1/7_C d_1/4 p_10/6_A d_1/4 <bass> p_6/2_F d_1 ' \
                   '<bar> <melody> p_6/6_F d_1/4 p_1/6_C d_1/4 p_1/7_C d_1/4 p_10/6_A d_1/4 <bass> p_6/2_F d_1 <bar> ' \
                   '<melody> p_6/6_F d_1/4 p_1/6_C d_1/4 p_1/7_C d_1/4 p_10/6_A d_1/4 <bass> p_6/2_F d_3/4 p_10/3_A ' \
                   'd_1/4 <bar> <melody> p_6/6_F d_1/4 p_1/6_C d_1/4 p_11/6_B d_1/2 <bass> p_6/3_F d_1/4 p_r d_1/4 ' \
                   'p_11/2_B d_1/2 <bar> <melody> p_6/6_F d_1/4 p_11/5_B d_1/4 p_11/6_B d_1/4 p_6/6_F d_1/4 <bass> ' \
                   'p_11/2_B d_1 <bar> <melody> p_2/6_C d_1/4 p_11/5_B d_1/4 p_11/6_B d_1/4 p_6/6_F d_1/4 <bass> ' \
                   'p_11/2_B d_1 <bar> <melody> p_6/6_F d_1/4 p_11/5_B d_1/4 p_11/6_B d_1/4 p_6/6_F d_1/4 <bass> ' \
                   'p_11/2_B d_1/4 p_r d_1/4 p_2/4_C d_1/2 <bar> <melody> p_6/6_F d_1/4 p_11/5_B d_1/4 p_10/6_A d_1/4 ' \
                   'p_6/6_F d_1/4 <bass> p_11/3_B d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> <melody> p_1/6_C d_1/4 p_10/5_A ' \
                   'd_1/4 p_10/6_A d_1/4 p_6/6_F d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_1/6_C d_1/4 p_10/5_A d_1/4 ' \
                   'p_10/6_A d_1/4 p_6/6_F d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_1/6_C d_1/4 p_10/5_A d_1/4 ' \
                   'p_10/6_A d_1/4 p_6/6_F d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_1/6_C d_1/4 p_10/5_A d_1/4 ' \
                   'p_11/6_B d_1/4 p_7/6_F d_1/4 <bass> p_6/2_F d_1/4 p_r d_1/4 p_4/2_E d_1/2 <bar> <melody> p_2/6_C ' \
                   'd_1/4 p_11/5_B d_1/4 p_11/6_B d_1/4 p_7/6_F d_1/4 <bass> p_4/2_E d_1 <bar> <melody> p_2/6_C d_1/4 ' \
                   'p_11/5_B d_1/4 p_11/6_B d_1/4 p_7/6_F d_1/4 <bass> p_4/2_E d_1 <bar> <melody> p_2/6_C d_1/4 ' \
                   'p_11/5_B d_1/4 p_11/6_B d_1/4 p_7/6_F d_1/4 <bass> p_4/2_E d_1/2 p_4/4_E d_1/2 <bar> <melody> ' \
                   'p_2/6_C d_1/4 p_11/5_B d_1/4 p_1/7_C d_1/4 p_10/6_A d_1/4 <bass> p_11/3_B d_1/4 p_r d_1/4 p_6/2_F ' \
                   'd_1/2 <bar> <melody> p_6/6_F d_1/4 p_1/6_C d_1/4 p_1/7_C d_1/4 p_10/6_A d_1/4 <bass> p_6/2_F d_1 ' \
                   '<bar> <melody> p_6/6_F d_1/4 p_1/6_C d_1/4 p_1/7_C d_1/4 p_10/6_A d_1/4 <bass> p_6/2_F d_1 <bar> ' \
                   '<melody> p_6/6_F d_1/4 p_1/6_C d_1/4 p_1/7_C d_1/4 p_10/6_A d_1/4 <bass> p_6/2_F d_3/4 p_10/3_A ' \
                   'd_1/4 <bar> <melody> p_6/6_F d_1/4 p_1/6_C d_1/4 p_2/6_C d_1/2 <bass> p_6/3_F d_1/4 p_r d_1/4 ' \
                   'p_7/2_F d_1/2 <bar> <melody> p_2/6_C d_1 <bass> p_7/2_F d_1 <bar> <melody> p_2/6_C d_1/2 p_11/5_B ' \
                   'd_1/2 <bass> p_7/2_F d_1 <bar> <melody> p_11/5_B d_1/2 p_1/6_C d_1/4 p_r d_1/4 <bass> p_7/2_F ' \
                   'd_3/4 p_r d_1/4 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_10/5_A d_1/4 p_r d_1/4 <bass> p_11/3_B ' \
                   'd_1/4 p_r d_1/4 p_2/3_C d_1/2 <bar> <melody> p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> <melody> ' \
                   'p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> <melody> p_9/5_G d_3/4 p_r d_1/4 <bass> p_2/3_C d_3/4 p_r ' \
                   'd_1/4 <bar> <melody> p_4/5_E d_1/4 p_r d_1/4 p_10/5_A d_1/2 <bass> p_r d_1/2 p_6/2_F d_1/2 <bar> ' \
                   '<melody> p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> ' \
                   '<melody> p_10/5_A d_1 <bass> p_6/2_F d_1/4 p_r d_1/4 p_6/4_F d_1/2 <bar> <melody> p_10/5_A d_1/4 ' \
                   'p_r d_1/4 p_11/5_B d_1/2 <bass> p_1/4_C d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_11/5_B ' \
                   'd_1/2 p_1/6_C d_1/4 p_r d_1/4 <bass> p_11/2_B d_1 <bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1 ' \
                   '<bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1/4 p_r d_1/4 p_11/3_B d_1/4 p_r d_1/4 <bar> ' \
                   '<melody> p_11/5_B d_1/4 p_r d_1/4 p_2/6_C d_1/2 <bass> p_11/3_B d_1/4 p_r d_1/4 p_7/2_F d_1/2 ' \
                   '<bar> <melody> p_2/6_C d_1 <bass> p_7/2_F d_1 <bar> <melody> p_2/6_C d_1/2 p_11/5_B d_1/2 <bass> ' \
                   'p_7/2_F d_1 <bar> <melody> p_11/5_B d_1/2 p_1/6_C d_1/4 p_r d_1/4 <bass> p_7/2_F d_1/2 p_2/4_C ' \
                   'd_1/2 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_10/5_A d_1/4 p_r d_1/4 <bass> p_11/3_B d_1/4 p_r ' \
                   'd_1/4 p_2/3_C d_1/2 <bar> <melody> p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> <melody> p_9/5_G d_1 ' \
                   '<bass> p_2/3_C d_1 <bar> <melody> p_9/5_G d_3/4 p_6/4_F d_1/4 <bass> p_2/3_C d_1/4 p_r d_1/4 ' \
                   'p_9/3_G d_1/4 p_r d_1/4 <bar> <melody> p_4/5_E d_1/4 p_r d_1/4 p_10/5_A d_1/2 <bass> p_9/3_G ' \
                   'd_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> <melody> ' \
                   'p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F d_3/4 p_r d_1/4 <bar> ' \
                   '<melody> p_10/5_A d_1/4 p_r d_1/4 p_11/5_B d_1/2 <bass> p_1/4_C d_1/4 p_r d_1/4 p_11/2_B d_1/2 ' \
                   '<bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1 <bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1 ' \
                   '<bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_2/6_C ' \
                   'd_1/2 <bass> p_11/2_B d_1/2 p_7/2_F d_1/2 <bar> <melody> p_2/6_C d_1 <bass> p_7/2_F d_1 <bar> ' \
                   '<melody> p_2/6_C d_1/2 p_11/5_B d_1/2 <bass> p_7/2_F d_1 <bar> <melody> p_11/5_B d_1/2 p_1/6_C ' \
                   'd_1/4 p_r d_1/4 <bass> p_7/2_F d_3/4 p_r d_1/4 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_9/5_G ' \
                   'd_1/2 <bass> p_11/3_B d_1/4 p_r d_1/4 p_2/3_C d_1/2 <bar> <melody> p_9/5_G d_1 <bass> p_2/3_C d_1 ' \
                   '<bar> <melody> p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> <melody> p_9/5_G d_3/4 p_r d_1/4 <bass> ' \
                   'p_2/3_C d_3/4 p_r d_1/4 <bar> <melody> p_4/5_E d_1/4 p_r d_1/4 p_10/5_A d_1/2 <bass> p_r d_1/2 ' \
                   'p_6/2_F d_1/2 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> <melody> p_10/5_A d_1 <bass> ' \
                   'p_6/2_F d_1 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F d_1/4 p_r d_1/4 p_6/4_F d_1/2 <bar> ' \
                   '<melody> p_10/5_A d_1/4 p_r d_1/4 p_11/5_B d_1/2 <bass> p_1/4_C d_1/4 p_r d_1/4 p_11/2_B d_1/2 ' \
                   '<bar> <melody> p_11/5_B d_1/2 p_1/6_C d_1/4 p_r d_1/4 <bass> p_11/2_B d_1 <bar> <melody> p_11/5_B ' \
                   'd_1 <bass> p_11/2_B d_1 <bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1/4 p_r d_1/4 p_11/3_B ' \
                   'd_1/4 p_r d_1/4 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_2/6_C d_1/2 <bass> p_11/3_B d_1/4 p_r ' \
                   'd_1/4 p_7/2_F d_1/2 <bar> <melody> p_2/6_C d_1 <bass> p_7/2_F d_1 <bar> <melody> p_2/6_C d_1/2 ' \
                   'p_11/5_B d_1/2 <bass> p_7/2_F d_1 <bar> <melody> p_11/5_B d_1/2 p_1/6_C d_1/4 p_r d_1/4 <bass> ' \
                   'p_7/2_F d_1/2 p_2/4_C d_1/2 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_9/5_G d_1/2 <bass> p_11/3_B ' \
                   'd_1/4 p_r d_1/4 p_2/3_C d_1/2 <bar> <melody> p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> <melody> ' \
                   'p_9/5_G d_1 <bass> p_2/3_C d_1 <bar> <melody> p_9/5_G d_3/4 p_6/4_F d_1/4 <bass> p_2/3_C d_1/4 ' \
                   'p_r d_1/4 p_9/3_G d_1/4 p_r d_1/4 <bar> <melody> p_4/5_E d_1/4 p_r d_1/4 p_10/5_A d_1/2 <bass> ' \
                   'p_9/3_G d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> ' \
                   '<melody> p_10/5_A d_1 <bass> p_6/2_F d_1 <bar> <melody> p_10/5_A d_1 <bass> p_6/2_F d_3/4 p_r ' \
                   'd_1/4 <bar> <melody> p_10/5_A d_1/4 p_r d_1/4 p_11/5_B d_1/2 <bass> p_1/4_C d_1/4 p_r d_1/4 ' \
                   'p_11/2_B d_1/2 <bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1/4 p_11/2_B d_1/4 p_11/2_B d_1/2 ' \
                   '<bar> <melody> p_11/5_B d_1 <bass> p_11/2_B d_1/2 p_11/2_B d_1/2 <bar> <melody> p_11/5_B d_1 ' \
                   '<bass> p_11/2_B d_1/4 p_11/2_B d_1/4 p_11/2_B d_1/2 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 ' \
                   'p_11/4_B d_1/2 <bass> <tup> p_11/2_B p_11/2_B p_11/2_B d_1/2 </tup> p_11/2_B d_1/4 p_r d_1/4 ' \
                   '<bar> <melody> p_11/4_B d_1 <bass> p_2/4_C d_1 <bar> <melody> p_11/5_B d_1/4 p_2/6_C d_1/4 ' \
                   'p_6/6_F d_1/4 p_r d_1/4 <bass> p_2/4_C d_1 <bar> <melody> p_2/6_C d_1/4 p_r d_1/4 p_11/6_B d_1/4 ' \
                   'p_r d_1/4 <bass> p_2/4_C d_1/2 p_4/4_E d_1/2 <bar> <melody> p_2/6_C d_1/4 p_r d_1/4 p_1/6_C d_1/4 ' \
                   'p_r d_1/4 <bass> <tup> p_r p_10/3_A p_6/2_F d_1 </tup> <bar> <melody> p_1/4_C d_1 <bass> p_6/2_F ' \
                   'd_1 <bar> <melody> p_10/5_A d_1/4 p_1/6_C d_1/4 p_4/6_E d_1/4 p_r d_1/4 <bass> p_6/2_F d_1 <bar> ' \
                   '<melody> p_1/6_C d_1/4 p_r d_1/4 p_10/6_A d_1/4 p_r d_1/4 <bass> p_6/2_F d_1/2 p_6/2_F d_1/4 p_r ' \
                   'd_1/4 <bar> <melody> p_1/6_C d_1/4 p_7/3_F d_1/4 p_7/4_F d_1/8 p_7/4_F d_3/8 <bass> p_r d_1/2 ' \
                   'p_7/2_F d_1/2 <bar> <melody> p_7/4_F d_1 <bass> p_7/2_F d_1 <bar> <melody> p_7/5_F d_1/4 p_11/5_B ' \
                   'd_1/4 p_2/6_C d_1/4 p_r d_1/4 <bass> p_7/2_F d_1 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_7/6_F ' \
                   'd_1/4 p_r d_1/4 <bass> p_7/2_F d_3/4 p_1/4_C d_1/4 <bar> <melody> p_11/5_B d_1/4 p_6/3_F d_1/4 ' \
                   'p_6/4_F d_1/2 <bass> p_r d_1/4 p_10/3_A d_1/4 p_6/2_F d_1/4 p_6/2_F d_1/4 <bar> <melody> p_6/4_F ' \
                   'd_1/2 p_4/6_E d_1/2 <bass> p_6/2_F d_1 <bar> <melody> p_4/6_E d_1/4 p_r d_1/4 p_2/6_C d_1/2 ' \
                   '<bass> p_6/2_F d_1 <bar> <melody> p_2/6_C d_1/4 p_r d_1/4 p_1/6_C d_1/2 <bass> p_6/2_F d_1/2 ' \
                   'p_4/4_E d_1/2 <bar> <melody> p_1/6_C d_1/2 p_6/4_F d_1/8 p_11/4_B d_1/8 p_11/4_B d_1/4 <bass> ' \
                   'p_4/4_E d_1/2 p_11/2_B d_1/2 <bar> <melody> <tup> p_11/4_B p_11/4_B p_6/3_F d_1 </tup> <bass> ' \
                   'p_11/2_B d_1 <bar> <melody> p_11/5_B d_1/4 p_2/6_C d_1/4 p_6/6_F d_1/4 p_r d_1/4 <bass> p_11/2_B ' \
                   'd_1 <bar> <melody> p_2/6_C d_1/4 p_r d_1/4 p_11/6_B d_1/4 p_r d_1/4 <bass> p_11/2_B d_1/2 p_r ' \
                   'd_1/2 <bar> <melody> p_2/6_C d_1/4 p_r d_1/4 p_1/6_C d_1/4 p_r d_1/4 <bass> <tup> p_r p_6/3_F ' \
                   'p_6/2_F d_1 </tup> <bar> <melody> p_7/4_F d_1 <bass> p_6/2_F d_1 <bar> <melody> p_10/5_A d_1/4 ' \
                   'p_1/6_C d_1/4 p_4/6_E d_1/4 p_6/2_F d_1/4 <bass> p_6/2_F d_3/4 p_r d_1/4 <bar> <melody> p_1/6_C ' \
                   'd_1/4 p_r d_1/4 p_10/6_A d_1/4 p_r d_1/4 <bass> p_6/2_F d_1/2 p_6/2_F d_1/4 p_r d_1/4 <bar> ' \
                   '<melody> p_1/6_C d_1/4 p_7/3_F d_1/4 p_7/4_F d_1/2 <bass> p_r d_1/2 p_7/2_F d_1/2 <bar> <melody> ' \
                   'p_7/4_F d_1 <bass> p_7/2_F d_1 <bar> <melody> p_7/5_F d_1/4 p_11/5_B d_1/4 p_2/6_C d_1/4 p_r ' \
                   'd_1/4 <bass> p_7/2_F d_1 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_7/6_F d_1/4 p_r d_1/4 <bass> ' \
                   'p_7/2_F d_1/4 p_r d_1/4 p_11/3_B d_1/4 p_r d_1/4 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_6/6_F ' \
                   'd_1/2 <bass> p_6/4_F d_1/2 p_6/2_F d_1/2 <bar> <melody> p_5/6_E d_1/4 p_r d_1/4 p_6/6_F d_1/2 ' \
                   '<bass> p_6/2_F d_1 <bar> <melody> p_5/6_E d_1/4 p_r d_1/4 p_6/6_F d_1/2 <bass> p_6/2_F d_1/2 ' \
                   'p_6/2_F d_1/2 <bar> <melody> p_5/6_E d_1/4 p_r d_1/4 p_6/6_F d_1/2 <bass> p_6/2_F d_1/2 p_6/2_F ' \
                   'd_1/2 <bar> <melody> p_5/6_E d_1/4 p_r d_1/4 p_6/5_F d_1/4 p_r d_1/4 <bass> <tup> p_10/3_A ' \
                   'p_11/3_B p_11/2_B d_1 </tup> <bar> <melody> p_11/4_B d_1/4 p_r d_1/4 p_11/4_B d_1/2 <bass> ' \
                   'p_11/2_B d_3/4 p_11/2_B d_1/4 <bar> <melody> p_11/4_B d_3/4 p_r d_1/4 <bass> p_11/2_B d_1 <bar> ' \
                   '<melody> p_11/4_B d_1/4 p_r d_1/4 p_1/5_C d_1/4 p_r d_1/4 <bass> p_11/2_B d_1/4 p_r d_1/4 ' \
                   'p_11/3_B d_1/4 p_r d_1/4 <bar> <melody> p_2/5_C d_1/4 p_r d_1/4 p_1/5_C d_1/4 p_r d_1/4 <bass> ' \
                   'p_r d_1/2 p_6/2_F d_1/2 <bar> <melody> p_1/5_C d_1/4 p_r d_1/4 p_1/5_C d_1/4 p_r d_1/4 <bass> ' \
                   'p_6/2_F d_1 <bar> <melody> p_12/4_B d_1/4 p_r d_1/4 p_1/5_C d_1/2 <bass> p_6/2_F d_1/2 p_6/2_F ' \
                   'd_1/2 <bar> <melody> p_6/4_F d_1/4 p_6/2_F d_1/4 p_1/4_C d_1/4 p_r d_1/4 <bass> p_6/2_F d_1/4 p_r ' \
                   'd_1/4 p_6/2_F d_1/4 p_r d_1/4 <bar> <melody> p_11/4_B d_1/4 p_r d_1/4 p_1/5_C d_1/4 p_r d_1/4 ' \
                   '<bass> p_r d_1/2 p_4/2_E d_1/2 <bar> <melody> p_7/4_F d_1/4 p_r d_1/4 p_7/4_F d_1/2 <bass> ' \
                   'p_4/2_E d_1 <bar> <melody> p_7/4_F d_1/2 p_4/4_E d_1/2 <bass> p_4/2_E d_1 <bar> <melody> p_7/4_F ' \
                   'd_1/4 p_r d_1/4 p_9/4_G d_1/4 p_r d_1/4 <bass> p_4/2_E d_1/4 p_r d_3/4 <bar> <melody> p_11/4_B ' \
                   'd_1/4 p_r d_1/4 p_2/5_C d_1/4 p_r d_1/4 <bass> p_r d_1/2 p_11/2_B d_1/2 <bar> <melody> p_2/5_C ' \
                   'd_1/4 p_r d_1/4 p_2/5_C d_1/4 p_r d_1/4 <bass> p_11/2_B d_1 <bar> <melody> p_1/5_C d_1/4 p_r ' \
                   'd_1/4 p_2/5_C d_1/4 p_r d_1/4 <bass> p_r d_1/4 p_11/3_B d_1/4 p_11/3_B d_1/4 p_r d_1/4 <bar> ' \
                   '<melody> p_6/5_F d_1 <bass> p_11/2_B d_1 <bar> <melody> p_4/5_E d_1/4 p_11/4_B d_1/4 p_6/5_F ' \
                   'd_1/4 p_11/3_B d_1/4 <bass> p_11/2_B d_1/4 p_r d_1/4 p_11/2_B d_1/2 <bar> <melody> p_11/4_B d_1/4 ' \
                   'p_r d_1/4 p_11/4_B d_1/2 <bass> p_11/2_B d_1 <bar> <melody> p_11/4_B d_3/4 p_r d_1/4 <bass> ' \
                   'p_11/2_B d_1 <bar> <melody> p_11/4_B d_1/4 p_r d_1/8 p_2/4_C d_1/8 p_1/5_C d_1/4 p_r d_1/4 <bass> ' \
                   'p_11/2_B d_1/2 p_11/3_B d_1/8 p_r d_3/8 <bar> <melody> p_2/5_C d_1/4 p_r d_1/4 p_6/5_F d_1/4 ' \
                   'p_9/3_G d_1/4 <bass> p_r d_1/2 p_6/2_F d_1/2 <bar> <melody> p_1/5_C d_1/4 p_r d_1/4 p_1/5_C d_1/4 ' \
                   'p_r d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_2/5_C d_1/4 <tup> p_r p_9/3_G p_6/4_F d_1/4 </tup> ' \
                   'p_1/5_C d_1/4 p_r d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_11/4_B d_1/4 p_r d_1/8 p_1/4_C d_1/8 ' \
                   'p_1/5_C d_1/4 p_r d_1/4 <bass> p_6/2_F d_3/4 p_r d_1/4 <bar> <melody> p_11/4_B d_1/4 p_r d_1/4 ' \
                   'p_2/5_C d_1/2 <bass> <tup> p_r p_7/3_F p_4/2_E d_1 </tup> <bar> <melody> p_2/5_C d_1/2 p_7/4_F ' \
                   'd_1/4 p_r d_1/4 <bass> p_4/2_E d_1 <bar> <melody> p_7/4_F d_1/2 p_4/4_E d_1/4 p_r d_1/4 <bass> ' \
                   'p_4/2_E d_3/8 p_4/2_E d_1/8 p_4/2_E d_1/2 <bar> <melody> p_7/4_F d_1/4 p_r d_1/4 p_9/4_G d_1/4 ' \
                   'p_r d_1/4 <bass> p_4/2_E d_1/4 p_r d_3/4 <bar> <melody> p_11/4_B d_1/4 p_11/3_B d_1/4 p_4/5_E ' \
                   'd_1/2 <bass> p_r d_1/2 p_11/2_B d_1/2 <bar> <melody> p_2/5_C d_1 <bass> p_11/2_B d_1 <bar> ' \
                   '<melody> p_1/5_C d_1/4 p_r d_1/4 p_2/5_C d_1/2 <bass> p_11/2_B d_1 <bar> <melody> p_11/4_B d_1/4 ' \
                   'p_r d_1/8 p_11/3_B d_1/8 p_11/4_B d_1/2 <bass> p_11/2_B d_3/4 p_r d_1/8 p_11/3_B d_1/8 <bar> ' \
                   '<melody> p_11/4_B d_1 <bass> p_r d_1/2 p_11/2_B d_1/2 <bar> <melody> p_11/4_B d_1 <bass> p_11/2_B ' \
                   'd_1 <bar> <melody> p_11/5_B d_1/4 p_2/6_C d_1/4 p_6/6_F d_1/4 p_r d_1/4 <bass> p_11/2_B d_1 <bar> ' \
                   '<melody> p_2/6_C d_1/4 p_r d_1/4 p_11/6_B d_1/4 p_r d_1/4 <bass> p_11/2_B d_1/2 p_4/4_E d_1/2 ' \
                   '<bar> <melody> p_2/6_C d_1/4 p_r d_1/4 p_1/6_C d_1/4 p_r d_1/4 <bass> <tup> p_r p_10/3_A p_6/2_F ' \
                   'd_1 </tup> <bar> <melody> p_1/4_C d_1 <bass> p_6/2_F d_1 <bar> <melody> p_10/5_A d_1/4 p_1/6_C ' \
                   'd_1/4 p_4/6_E d_1/4 p_r d_1/4 <bass> p_6/2_F d_1 <bar> <melody> p_1/6_C d_1/4 p_r d_1/4 p_10/6_A ' \
                   'd_1/4 p_r d_1/4 <bass> p_6/2_F d_1/2 p_6/2_F d_1/4 p_r d_1/4 <bar> <melody> p_1/6_C d_1/4 p_7/3_F ' \
                   'd_1/4 p_7/4_F d_1/8 p_7/4_F d_3/8 <bass> p_r d_1/2 p_7/2_F d_1/2 <bar> <melody> p_7/4_F d_1 ' \
                   '<bass> p_7/2_F d_1 <bar> <melody> p_7/5_F d_1/4 p_11/5_B d_1/4 p_2/6_C d_1/4 p_r d_1/4 <bass> ' \
                   'p_7/2_F d_1 <bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_7/6_F d_1/4 p_r d_1/4 <bass> p_7/2_F d_3/4 ' \
                   'p_1/4_C d_1/4 <bar> <melody> p_11/5_B d_1/4 p_6/3_F d_1/4 p_6/4_F d_1/2 <bass> p_r d_1/4 p_10/3_A ' \
                   'd_1/4 p_6/2_F d_1/4 p_6/2_F d_1/4 <bar> <melody> p_6/4_F d_1/2 p_4/6_E d_1/2 <bass> p_6/2_F d_1 ' \
                   '<bar> <melody> p_4/6_E d_1/4 p_r d_1/4 p_2/6_C d_1/2 <bass> p_6/2_F d_1 <bar> <melody> p_2/6_C ' \
                   'd_1/4 p_r d_1/4 p_1/6_C d_1/2 <bass> p_6/2_F d_1/2 p_4/4_E d_1/2 <bar> <melody> p_1/6_C d_1/2 ' \
                   'p_6/4_F d_1/8 p_11/4_B d_1/8 p_11/4_B d_1/4 <bass> p_4/4_E d_1/2 p_11/2_B d_1/2 <bar> <melody> ' \
                   '<tup> p_11/4_B p_11/4_B p_6/3_F d_1 </tup> <bass> p_11/2_B d_1 <bar> <melody> p_11/5_B d_1/4 ' \
                   'p_2/6_C d_1/4 p_6/6_F d_1/4 p_r d_1/4 <bass> p_11/2_B d_1 <bar> <melody> p_2/6_C d_1/4 p_r d_1/4 ' \
                   'p_11/6_B d_1/4 p_r d_1/4 <bass> p_11/2_B d_1/2 p_r d_1/2 <bar> <melody> p_2/6_C d_1/4 p_r d_1/4 ' \
                   'p_1/6_C d_1/4 p_r d_1/4 <bass> <tup> p_r p_6/3_F p_6/2_F d_1 </tup> <bar> <melody> p_7/4_F d_1 ' \
                   '<bass> p_6/2_F d_1 <bar> <melody> p_10/5_A d_1/4 p_1/6_C d_1/4 p_4/6_E d_1/4 p_6/2_F d_1/4 <bass> ' \
                   'p_6/2_F d_3/4 p_r d_1/4 <bar> <melody> p_1/6_C d_1/4 p_r d_1/4 p_10/6_A d_1/4 p_r d_1/4 <bass> ' \
                   'p_6/2_F d_1/2 p_6/2_F d_1/4 p_r d_1/4 <bar> <melody> p_1/6_C d_1/4 p_7/3_F d_1/4 p_7/4_F d_1/2 ' \
                   '<bass> p_r d_1/2 p_7/2_F d_1/2 <bar> <melody> p_7/4_F d_1 <bass> p_7/2_F d_1 <bar> <melody> ' \
                   'p_7/5_F d_1/4 p_11/5_B d_1/4 p_2/6_C d_1/4 p_r d_1/4 <bass> p_7/2_F d_1 <bar> <melody> p_11/5_B ' \
                   'd_1/4 p_r d_1/4 p_7/6_F d_1/4 p_r d_1/4 <bass> p_7/2_F d_1/4 p_r d_1/4 p_11/3_B d_1/4 p_r d_1/4 ' \
                   '<bar> <melody> p_11/5_B d_1/4 p_r d_1/4 p_6/6_F d_1/2 <bass> p_6/4_F d_1/2 p_6/2_F d_1/2 <bar> ' \
                   '<melody> p_5/6_E d_1/4 p_r d_1/4 p_6/6_F d_1/2 <bass> p_6/2_F d_1 <bar> <melody> p_5/6_E d_1/4 ' \
                   'p_r d_1/4 p_6/6_F d_1/2 <bass> p_6/2_F d_1/2 p_6/2_F d_1/2 <bar> <melody> p_5/6_E d_1/4 p_r d_1/4 ' \
                   'p_6/6_F d_1/2 <bass> p_6/2_F d_1/2 p_6/2_F d_1/2 <bar> <melody> p_5/6_E d_1/4 p_6/2_F d_1/4 ' \
                   'p_6/6_F d_1/2 <bass> p_6/2_F d_1/4 p_r d_1/4 p_6/2_F d_1/2 <bar> <melody> p_6/6_F d_1 <bass> ' \
                   'p_6/2_F d_1 <bar> <melody> p_6/6_F d_1 <bass> p_6/2_F d_1 <bar> <melody> p_6/6_F d_1 <bass> ' \
                   'p_6/2_F d_1 <bar> <melody> p_6/6_F d_1 <bass> p_6/2_F d_1 <bar> <melody> p_6/6_F d_1/2 p_r d_1/2 ' \
                   '<bass> p_6/2_F d_1/2 p_r d_1/2 </s>'

gen_broken = 'TimeSig_4/4 Tempo_120 Key_DMajor <bar> <melody> p_7/2_3 d_1 p_2/4_7 d_1/2 p_10/3_5 d_1/2 p_3/2_1 d_1 ' \
             'p_3/4_1 d_1/2 p_10/3_5 d_1/2 <bass> p_7/2_3 d_2 p_3/2_1 d_2 <bar> <melody> p_10/2_5 d_1/2 p_5/3_2 d_1/2 ' \
             'p_2/4_7 d_1/2 p_10/3_5 d_1/2 p_9/3_4 d_1/2 p_10/3_5 d_1/2 p_12/3_6 d_1/2 p_5/3_2 d_1/2 <bass> p_10/2_5 ' \
             'd_2 p_5/2_2 d_2 <bar> <melody> p_7/2_3 d_1 p_2/4_7 d_1/2 p_10/3_5 d_1/2 p_3/3_1 d_1 p_3/4_1 d_1/2 ' \
             'p_10/3_5 d_1/2 <bass> p_7/2_3 d_2 p_3/2_1 d_2 <bar> <melody> p_10/2_5 d_1/2 p_5/3_2 d_1/2 p_2/4_7 d_1/2 ' \
             'p_10/3_5 d_1/2 p_9/3_4 d_1/2 p_10/3_5 d_1/2 p_12/3_6 d_1/2 p_5/3_2 d_1/2 <bass> p_10/2_5 d_2 p_5/2_2 ' \
             'd_2 <bar> <bass> p_7/2_3 d_2 <melody> p_7/2_3 d_1 <bass> p_3/2_1 d_2 <melody> p_2/4_7 d_1/2 p_10/3_5 ' \
             'd_1/2 p_3/3_1 d_1 p_10/3_5 d_1/2 p_3/4_1 d_1/2 <bar> <melody> p_10/2_5 d_1/2 p_5/3_2 d_1/2 <bass> ' \
             'p_10/2_5 d_2 <melody> p_2/4_7 d_1/2 <bass> p_10/2_5 d_2 <melody> p_10/3_5 d_1/2 p_9/3_4 d_1/2 p_10/3_5 ' \
             'd_1/2 p_3/4_1 d_1/2 p_12/3_6 d_1/2 <bar> <bass> p_10/2_5 d_2 <melody> p_2/3_7 d_1/2 <bass> p_10/2_5 d_2 ' \
             '<melody> p_5/3_2 d_1/2 p_5/4_2 d_1/2 p_10/3_5 d_1/2 p_10/3_5 d_1/2 p_5/4_2 d_1/2 p_5/4_2 d_1/2 p_10/3_5 ' \
             'd_1/2 <bar> <melody> p_10/2_5 d_1/2 p_5/3_2 d_1/2 p_2/4_7 d_1/2 p_7/4_3 d_1/2 <bass> p_10/2_5 d_2 ' \
             '<melody> p_3/3_1 d_1/2 <bass> p_10/2_5 d_2 <melody> p_6/3_3 d_1/2 p_3/4_1 d_1/2 p_12/3_6 d_1/2 <bar> ' \
             '<melody> p_2/3_7 d_1/2 <bass> p_10/2_5 d_2 <melody> p_5/3_2 d_1/2 p_10/4_5 d_1/2 <bass> p_10/2_5 d_2 ' \
             '<melody> p_5/4_2 d_1/2 p_2/4_7 d_1/2 p_5/4_2 d_1/2 p_3/4_1 d_1/2 p_12/3_6 d_1/2 <bar> <melody> p_10/3_5 ' \
             'd_1/4 <bass> p_10/2_5 d_2 <melody> p_2/4_7 d_1/4 <bass> p_10/2_5 d_2 <melody> p_5/4_2 d_1/4 p_2/4_7 ' \
             'd_1/4 p_10/3_5 d_1 p_12/3_6 d_1/4 p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_3/4_1 d_1 <bar> <melody> ' \
             'p_2/4_7 d_1/4 p_5/4_2 d_1/4 <bass> p_10/2_5 d_2 <melody> p_2/4_7 d_1/4 <bass> p_10/2_5 d_2 <melody> ' \
             'p_10/3_5 d_1/4 p_8/3_4 d_1 p_12/3_6 d_1/4 p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_3/4_1 d_1 <bar> ' \
             '<bass> p_10/2_5 d_2 <melody> p_2/4_7 d_1/4 <bass> p_10/2_5 d_2 <melody> p_5/4_2 d_1/4 p_2/4_7 d_1/4 ' \
             'p_10/3_5 d_1/4 p_8/3_4 d_1 p_12/3_6 d_1/4 p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_3/4_1 d_1 <bar> ' \
             '<bass> p_10/2_5 d_2 <melody> p_2/4_7 d_1/4 p_5/4_2 d_1/4 <bass> p_10/2_5 d_2 <melody> p_2/4_7 d_1/4 ' \
             'p_10/3_5 d_1/4 p_8/3_4 d_1 p_12/3_6 d_1/4 p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_3/4_1 d_1 <bar> ' \
             '<bass> p_10/2_5 d_2 p_10/2_5 d_2 <melody> p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_10/3_5 d_1/4 ' \
             'p_8/3_4 d_1 p_12/3_6 d_1/4 p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_3/4_1 d_1 <bar> <bass> p_10/2_5 ' \
             'd_2 <melody> p_2/4_7 d_1/4 <bass> p_10/2_5 d_2 <melody> p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_10/3_5 d_1/4 ' \
             'p_8/3_4 d_1 p_12/3_6 d_1/4 p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_3/4_1 d_1 <bar> <melody> p_2/4_7 ' \
             'd_1/4 <bass> p_10/2_5 d_2 p_10/2_5 d_2 <melody> p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_10/3_5 d_1/4 p_8/3_4 d_1 ' \
             'p_12/3_6 d_1/4 p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_3/4_1 d_1 <bar> <bass> p_10/2_5 d_2 p_10/2_5 ' \
             'd_1 p_10/3_5 d_1 <melody> p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_10/3_5 d_1/4 p_8/3_4 d_1 p_12/3_6 ' \
             'd_1/4 p_2/4_7 d_1/4 p_5/4_2 d_1/4 p_2/4_7 d_1/4 p_3/4_1 d_1 <bar> <bass> p_3/3_1 d_2 p_10/2_5 d_2 ' \
             '<melody> p_2/4_7 d_3/4 p_12/3_6 d_1/8 p_2/4_7 d_1/8 p_3/4_1 d_3/4 p_3/4_1 d_1/8 p_5/4_2 d_1/8 p_7/4_3 ' \
             'd_3/4 p_7/4_3 d_1/8 p_8/4_4 d_1/8 p_10/4_5 d_3/4 p_10/4_5 d_1/8 p_12/4_6 d_1/8 <bar> <melody> p_2/5_7 ' \
             'd_3/4 <bass> p_10/2_5 d_2 <melody> p_2/5_7 d_1/2 <bass> p_10/2_5 d_2 <melody> p_2/4_7 d_1/4 p_12/3_6 ' \
             'd_1/8 p_2/4_7 d_1/8 p_3/4_1 d_3/4 p_3/4_1 d_1/8 p_5/4_2 d_1/8 p_7/4_3 d_3/4 p_7/4_3 d_1/8 p_8/4_4 d_1/8 ' \
             '<bar> <melody> p_10/4_5 d_3/4 p_10/4_5 d_1/4 p_12/4_6 d_1/4 <bass> p_10/2_5 d_2 <melody> p_8/4_4 d_1/2 ' \
             '<bass> p_10/2_5 d_2 <melody> p_7/4_3 d_1/8 p_8/4_4 d_1/8 p_10/4_5 d_3/4 p_10/4_5 d_1/8 p_12/4_6 d_1/8 ' \
             'p_2/5_7 d_3/4 p_12/4_6 d_1/8 p_2/5_7 d_1/8 <bar> <bass> p_10/2_5 d_2 <melody> p_3/5_1 d_3/4 <bass> ' \
             'p_10/2_5 d_2 <melody> p_3/5_1 d_1/2 p_7/4_3 d_1/4 p_8/4_4 d_1/4 p_10/4_5 d_3/4 p_10/4_5 d_1/8 p_12/4_6 ' \
             'd_1/8 p_2/5_7 d_3/4 p_12/4_6 d_1/8 p_2/5_7 d_1/8 <bar> <bass> p_10/2_5 d_2 <melody> p_3/5_1 d_1/2 ' \
             '<bass> p_10/2_5 d_2 <melody> p_r d_1/4 p_3/5_1 d_1/4 p_5/5_2 d_3/4 p_3/5_1 d_1/8 p_5/5_2 d_1/8 p_7/5_3 ' \
             'd_1 p_7/5_3 d_3/4 p_7/5_3 d_1/8 p_8/5_4 d_1/8 <bar> <melody> p_10/5_5 d_3/4 <bass> p_10/2_5 d_2 ' \
             'p_10/2_5 d_2 <melody> p_10/5_5 d_1/4 p_12/5_6 d_3/4 p_12/5_6 d_1/4 p_2/6_7 d_3/4 p_2/6_7 d_1/8 p_12/5_6 ' \
             'd_1/8 p_10/5_5 d_3/4 p_10/5_5 d_1/8 p_8/5_4 d_1/8 <bar> <melody> p_2/4_7 d_3/4 <bass> p_10/2_5 d_2 ' \
             '<melody> p_2/4_7 d_1/8 <bass> p_10/2_5 d_2 <melody> p_3/4_1 d_1/8 p_5/4_2 d_3/4 p_5/4_2 d_1/4 p_2/4_7 ' \
             'd_1 p_6/4_3 d_3/4 p_6/4_3 d_1/8 p_5/4_2 d_1/8 <bar> <melody> p_3/4_1 d_3/4 <bass> p_10/2_5 d_2 <melody> ' \
             'p_3/4_1 d_1/8 p_3/4_1 d_1/8 <bass> p_10/2_5 d_1 p_2/3_7 d_1 <melody> p_5/4_2 d_3/4 p_5/4_2 d_1/8 ' \
             'p_5/4_2 d_1/8 p_6/4_3 d_1 p_2/5_7 d_1 <bar> <bass> p_3/3_1 d_1 <melody> p_3/4_1 d_3/4 p_3/4_1 d_1/8 ' \
             '<bass> p_10/2_5 d_1 <melody> p_3/4_1 d_1/8 <bass> p_3/3_1 d_1 <melody> p_2/5_7 d_3/4 <bass> p_10/2_5 ' \
             'd_1 <melody> p_2/5_7 d_1/8 p_10/4_5 d_1/8 p_3/5_1 d_3/4 p_3/5_1 d_1/8 p_7/5_3 d_1/8 p_10/5_5 d_3/4 ' \
             'p_9/5_4 d_1/8 p_10/5_5 d_1/8 <bar> <melody> p_3/6_1 d_3/4 <bass> p_3/3_1 d_2 <melody> p_3/6_1 d_1/8 ' \
             'p_3/6_1 d_1/8 <bass> p_10/2_5 d_2 <melody> p_2/6_7 d_3/4 p_2/6_7 d_1/8 p_10/5_5 d_1/8 p_3/6_1 d_3/4 ' \
             'p_3/6_1 d_1/8 p_12/5_6 d_1/8 p_2/6_7 d_3/4 p_2/6_7 d_1/8 p_2/6_7 d_1/8 <bar> <melody> p_3/6_1 d_3/4 ' \
             'p_3/6_1 d_1/8 p_12/5_5 d_1/8 p_3/6_1 d_3/4 <bass> p_3/3_1 d_2 <melody> p_3/6_1 d_1/8 p_12/5_6 d_1/8 ' \
             'p_2/6_7 d_3/4 p_2/6_7 d_1/8 p_9/5_4 d_1/8 <bass> p_10/2_5 d_2 <melody> p_10/5_5 d_3/4 p_11/5_6 d_1/8 ' \
             'p_10/5_5 d_1/8 <bar> <bass> p_3/3_1 d_1 <melody> p_3/4_1 d_3/4 p_3/4_1 d_1/8 <bass> p_10/2_5 d_1 ' \
             '<melody> p_3/5_1 d_1/8 p_5/5_2 d_3/4 <bass> p_3/3_1 d_1 <melody> p_3/5_1 d_1/8 p_3/5_1 d_1/8 p_7/5_3 ' \
             'd_1 <bass> p_10/2_5 d_1 <melody> p_7/5_3 d_3/4 p_8/5_4 d_1/8 p_10/5_5 d_1/8 <bar> <bass> p_3/3_1 d_2 ' \
             '<melody> p_3/6_1 d_3/4 <bass> p_10/2_5 d_2 <melody> p_3/6_1 d_1/8 p_3/6_1 d_1/8 p_2/6_7 d_3/4 p_2/6_7 ' \
             'd_1/8 p_10/5_5 d_1/8 p_3/6_1 d_3/4 p_3/6_1 d_1/8 p_12/5_6 d_1/8 p_2/6_7 d_3/4 p_3/6_1 d_1/8 p_2/6_7 ' \
             'd_1/8 <bar> <melody> p_3/6_1 d_3/4 p_3/5_1 d_1/8 <bass> p_3/3_1 d_2 <melody> p_3/6_1 d_1/8 p_2/6_7 ' \
             'd_3/4 <bass> p_10/2_5 d_2 <melody> p_2/6_7 d_1/8 p_10/5_5 d_1/8 p_3/6_1 d_3/4 p_3/6_1 d_1/8 p_12/5_6 ' \
             'd_1/8 p_2/6_7 d_3/4 p_2/6_7 d_1/8 p_9/5_4 d_1/8 p_10/5_5 d_3/4 <bar> <bass> p_3/3_1 d_2 <melody> ' \
             'p_3/6_1 d_3/4 <bass> p_10/2_5 d_2 <melody> p_3/6_1 d_1/8 p_10/5_5 d_1/8 p_3/6_1 d_3/4 p_3/6_1 d_1/4 ' \
             'p_2/6_7 d_3/4 p_2/6_7 d_1/8 p_12/5_6 d_1/8 p_10/5_5 d_3/4 p_10/5_5 d_1/8 p_8/5_4 d_1/8 <bar> <melody> ' \
             'p_2/4_7 d_3/4 <bass> p_10/2_5 d_2 <melody> p_2/4_7 d_1/8 p_3/4_1 d_1/8 p_5/4_2 d_3/4 p_5/4_2 d_1/4 ' \
             '<bass> p_10/2_5 d_2 <melody> p_2/4_7 d_1 p_6/4_3 d_3/4 p_6/4_3 d_1/8 p_5/4_2 d_1/8 <bar> <melody> ' \
             'p_3/4_1 d_3/4 p_3/4_1 d_1/8 <bass> p_10/2_5 d_2 <melody> p_3/4_1 d_1/8 <bass> p_10/2_5 d_1 <melody> ' \
             'p_5/4_2 d_3/4 <bass> p_2/3_7 d_1 <melody> p_5/4_2 d_1/8 p_5/4_2 d_1/8 p_6/4_3 d_1 p_2/5_7 d_1 <bar> ' \
             '<bass> p_3/3_1 d_1 p_10/2_5 d_1 p_3/3_1 d_1 <melody> p_3/4_1 d_3/4 <bass> p_10/2_5 d_1 <melody> p_3/4_1 ' \
             'd_1/8 p_3/4_1 d_1/8 p_2/5_7 d_3/4 p_10/5_5 d_1/8 p_5/5_2 d_1/8 p_10/5_5 d_3/4 p_10/5_5 d_1/8 p_7/5_3 ' \
             'd_1/8 p_10/5_5 d_3/4 p_10/5_5 d_1/8 p_8/5_4 d_1/8 <bar> <bass> p_3/3_1 d_2 <melody> p_7/5_3 d_3/4 ' \
             'p_7/5_3 d_1/8 <bass> p_10/2_5 d_2 <melody> p_5/5_2 d_1/8 p_7/5_3 d_1 p_7/5_3 d_3/4 p_7/5_3 d_1/8 ' \
             'p_5/5_2 d_1/8 p_7/5_3 d_1 <bar> <bass> p_3/3_1 d_2 <melody> p_5/5_2 d_3/4 <bass> p_10/2_5 d_2 <melody> ' \
             'p_5/5_2 d_1/8 p_3/5_1 d_1/8 p_5/5_2 d_1/2 p_5/5_2 d_1/4 p_5/5_2 d_1/8 p_3/5_1 d_1/8 p_5/5_2 d_1/2 ' \
             'p_5/5_2 d_1/4 p_5/5_2 d_1/8 p_3/5_1 d_1/8 p_5/5_2 d_1/2 p_5/5_2 d_1/4 p_5/5_2 d_1/8 p_3/5_1 d_1/8 <bar> ' \
             '<bass> p_3/3_1 d_2 p_10/1_5 d_2 <melody> p_7/5_3 d_1/2 p_7/5_3 d_1/4 p_7/5_3 d_1/8 p_5/5_2 d_1/8 ' \
             'p_7/5_3 d_1/2 p_7/5_3 d_1/4 p_7/5_3 d_1/8 p_5/5_2 d_1/8 p_7/5_3 d_1/2 p_7/5_3 d_2 <bar> <melody> ' \
             'p_5/5_2 d_11/4 p_10/5_5 d_1/4 p_10/5_5 d_1 <bass> p_10/2_5 d_2 p_10/2_5 d_2 <bar> <melody> p_3/5_1 ' \
             'd_11/4 <bass> p_3/3_1 d_1 p_3/3_1 d_1 <melody> p_5/5_2 d_1/4 <bass> p_10/2_5 d_1 <melody> p_7/5_3 d_1 ' \
             '<bass> p_10/2_5 d_1 <bar> <bass> p_3/3_1 d_2 <melody> p_3/5_1 d_11/4 p_5/5_2 d_1/4 p_7/5_3 d_1 <bass> ' \
             'p_10/2_5 d_1 p_3/3_1 d_1 <bar> <bass> p_10/2_5 d_1 <melody> p_3/5_1 d_3/4 <bass> p_10/2_5 d_1 <melody> ' \
             'p_3/5_1 d_1/8 <bass> p_3/3_1 d_1 <melody> p_3/5_1 d_1/8 <bass> p_10/2_5 d_1 <melody> p_5/5_2 d_3/4 ' \
             'p_7/5_3 d_1/8 p_5/5_2 d_1/8 p_7/5_3 d_1 p_5/5_2 d_1 <bar> <bass> p_3/3_1 d_2 p_10/2_5 d_2 <melody> ' \
             'p_3/5_1 d_3/4 p_3/5_1 d_1/8 p_5/5_2 d_1/8 p_7/5_3 d_7/4 p_10/5_5 d_1/4 p_10/5_5 d_1 <bar> <melody> ' \
             'p_7/5_3 d_1/2 <bass> p_3/3_1 d_2 <melody> p_7/5_3 d_1/4 p_7/5_3 d_1/8 <bass> p_10/2_5 d_2 <melody> ' \
             'p_5/5_2 d_1/8 p_7/5_3 d_1 p_7/5_3 d_3/4 p_8/5_4 d_1/8 p_7/5_3 d_1/8 p_8/5_4 d_1 <bar> <melody> p_7/5_3 ' \
             'd_3/4 <bass> p_3/3_1 d_2 <melody> p_7/5_3 d_1/8 p_5/5_2 d_1/8 <bass> p_10/2_5 d_2 <melody> p_7/5_3 d_1 ' \
             'p_7/5_3 d_3/4 p_8/5_4 d_1/8 p_7/5_3 d_1/8 p_8/5_4 d_1 <bar> <bass> p_3/3_1 d_2 <melody> p_7/5_3 d_3/4 ' \
             '<bass> p_10/2_5 d_2 <melody> p_7/5_3 d_1/8 p_5/5_2 d_1/8 p_7/5_3 d_1 p_7/5_3 d_3/4 p_7/5_3 d_1/8 ' \
             'p_8/5_4 d_1/8 p_8/5_4 d_1 <bar> <melody> p_7/5_3 d_3/4 p_7/5_3 d_1/8 p_5/5_2 d_1/8 <bass> p_10/2_5 d_2 ' \
             '<melody> p_7/5_3 d_1 p_7/5_3 d_2 <bass> p_3/3_1 d_2 <bar> <melody> p_7/5_3 d_3/4 <bass> p_10/2_5 d_2 ' \
             '<melody> p_7/5_3 d_1/8 <bass> p_10/2_5 d_2 <melody> p_5/5_2 d_1/8 p_7/5_3 d_1 p_7/5_3 d_3/4 p_8/5_4 ' \
             'd_1/8 p_7/5_3 d_1/8 p_8/5_4 d_1 <bar> <melody> p_7/5_3 d_3/4 <bass> p_3/3_1 d_2 <melody> p_7/5_3 d_1/8 ' \
             '<bass> p_10/2_5 d_2 <melody> p_5/5_2 d_1/8 p_7/5_3 d_1 p_7/5_3 d_3/4 p_8/5_4 d_1/8 p_7/5_3 d_1/8 ' \
             'p_8/5_4 d_1 <bar> <bass> p_3/3_1 d_2 <melody> p_7/5_3 d_3/4 p_7/5_3 d_1/8 p_5/5_2 d_1/8 <bass> p_10/2_5 ' \
             'd_2 <melody> p_7/5_3 d_1 p_7/5_3 d_3/4 p_10/5_5 d_1/8 p_8/5_4 d_1/8 p_8/5_4 d_1 <bar> <melody> p_7/5_3 ' \
             'd_3/4 <bass> p_3/3_1 d_2 p_10/2_5 d_2 <melody> p_7/5_3 d_1/8 p_5/5_2 d_1/8 p_7/5_3 d_1 p_7/5_3 d_3/4 ' \
             'p_8/5_4 d_1/8 p_7/5_3 d_1/8 p_8/5_4 d_1 <bar> <melody> p_7/5_3 d_3/4 p_7/5_3 d_1/8 p_5/5_2 d_1/8 <bass> ' \
             'p_3/3_1 d_2 <melody> p_7/5_3 d_1 <bass> p_10/2_5 d_2 <melody> p_7/5_3 d_3/4 p_8/5_4 d_1/8 p_7/5_3 d_1/8 ' \
             'p_8/5_4 d_1 <bar> <bass> p_3/3_1 d_2 p_10/2_5 d_2 <melody> p_7/5_3 d_3/4 p_7/5_3 d_1/8 p_5/5_2 d_1/8 ' \
             'p_7/5_3 d_1 p_7/5_3 d_3/4 p_12/5_6 d_1/8 p_2/6_7 d_1/8 p_3/6_1 d_1 </s> <bass> p_3/3_1 d_2 <melody> ' \
             'p_5/5_2 d_3/4 p_5/5_2 d_1/8 <bass> p_10/2_5 d_2 <melody> p_3/5_1 d_1/8 p_5/5_2 d_1 p_5/5_2 d_1/2 <tup> ' \
             'p_5/5_2 p_3/5_1 p_10/3_5 d_1/2 </tup> p_5/5_2 d_1 <bar> <bass> p_3/3_1 d_2 <melody> p_3/5_1 d_1/2 ' \
             '<bass> p_10/2_5 d_2 <melody> p_3/5_1 d_1/4 p_3/5_1 d_1/8 p_5/5_2 d_1/8 p_7/5_3 d_7/4 p_10/5_5 d_1/4 ' \
             'p_8/5_4 d_1/4 p_10/5_5 d_1/8 p_8/5_4 d_1/8 p_r d_1/8 p_12/5_6 d_1/8 p_10/5_5 d_1/8 p_12/5_6 d_1/8 <bar> ' \
             '<bass> p_3/3_1 d_2 <melody> p_10/5_5 d_3/4 <bass> <tup> p_r p_5/3_2 p_r d_1/8 </tup> p_r d_7/8 p_10/3_5 ' \
             'd_1 <melody> p_10/5_5 d_1/4 p_10/5_5 d_1/4 p_10/5_5 d_1/8 p_12/5_6 d_1/8 p_10/5_5 d_1/4 p_12/5_6 d_1/4 ' \
             'p_10/5_5 d_3/2 p_8/5_4 d_1/4 p_10/5_5 d_1/4 <bar> <bass> p_10/3_5 d_1 <melody> p_12/5_6 d_3/4 p_12/5_6 ' \
             'd_1/4 <bass> p_5/3_2 d_1 <melody> p_12/5_6 d_1/4 <bass> p_10/2_5 d_1 <melody> <tup> p_12/5_6 p_10/5_5 ' \
             'd_1/8 </tup> <bass> <tup> p_r p_10/2_5 p_r d_1/8 </tup> p_r d_3/8 p_3/5_1 d_1/2 <melody> p_10/5_5 d_1/8 ' \
             'p_12/5_6 d_1/4 p_12/5_6 d_1/4 p_10/5_5 d_1 p_10/5_5 d_1/4 p_8/5_4 d_1/4 p_5/5_2 d_1/2 <bar> <melody> ' \
             'p_5/5_2 d_1 <bass> p_10/4_5 d_1 <melody> p_r d_1 <bass> p_r d_1 <bar> <melody> p_3/5_1 d_1 p_7/5_3 ' \
             'd_3/4 p_8/5_4 d_1/4 <bass> p_3/3_1 d_2 p_10/3_5 d_2 <melody> <tup> p_8/5_4 p_7/5_3 p_8/5_4 d_1/2 </tup> ' \
             'p_5/5_2 d_3/2 <bar> <bass> p_10/2_5 d_2 p_3/3_1 d_2 <melody> p_5/5_2 d_1 p_7/5_3 d_1 p_7/5_3 d_3/2 ' \
             'p_8/5_4 d_1/4 p_r d_1/4 <bar> <melody> p_5/5_2 d_3/4 <bass> p_3/3_1 d_2 <melody> p_5/5_2 d_1/4 <bass> ' \
             'p_10/2_5 d_2 <melody> p_7/5_3 d_1 p_7/5_3 d_3/4 p_8/5_4 d_1/8 p_7/5_3 d_1/8 p_8/5_4 d_1 <bar> <bass> ' \
             'p_3/3_1 d_2 p_10/2_5 d_2 <melody> p_7/5_3 d_3/4 p_7/5_3 d_1/8 p_5/5_2 d_1/8 p_7/5_3 d_1 p_7/5_3 d_3/4 ' \
             'p_8/5_4 d_1/8 p_6/5_3 d_1/8 p_8/5_4 d_1 <bar> <bass> p_3/3_1 d_2 <melody> p_7/5_3 d_3/4 <bass> p_10/2_5 ' \
             'd_2 <melody> p_7/5_3 d_1/8 p_5/5_2 d_1/8 p_7/5_3 d_1 p_7/5_3 d_3/4 p_8/5_4 d_1/8 p_10/5_5 d_1/8 p_8/5_4 ' \
             'd_1 <bar> <bass> p_8/2_4 d_2 <melody> p_7/5_3 d_3/4 <tup> p_7/5_3 p_5/5_2 d_1/8 </tup> p_4/5_1 d_1/8 ' \
             'p_5/5_2 d_1 p_5/5_2 d_1 <bass> p_3/3_1 d_2 <melody> p_5/5_2 d_1 <bar> <melody> p_5/5_2 d_1 <tup> ' \
             'p_5/5_2 p_5/5_2 d_1/8 </tup> p_3/5_1 d_3/8 <bass> p_3/3_1 d_2 p_10/2_5 d_2 <melody> p_5/5_2 d_1/4 ' \
             'p_7/5_3 d_1/8 p_5/5_2 d_1/8 p_7/5_3 d_3/2 p_8/5_4 d_1/8 p_10/5_5 d_1/8 <tup> p_10/5_5 p_12/5_6 d_1/8 ' \
             '</tup> p_2/6_7 d_1/8 <bar> <melody> p_3/6_1 d_1 p_7/5_3 d_3/4 <bass> p_3/3_1 d_2 <melody> p_8/5_4 d_1/4 ' \
             '<bass> p_10/2_5 d_2 <melody> <tup> p_8/5_4 p_12/4_6 p_12/4_6 d_1/8 </tup> <tup> p_12/5_6 p_10/5_5 d_1/8 ' \
             '</tup> <tup> p_12/5_6 p_10/5_5 d_1/8 </tup> p_10/5_5 d_1/8 p_8/5_4 d_1/4 p_10/5_5 d_1/4 p_7/5_3 d_1/8 ' \
             'p_r d_1/8 p_r d_1/4 p_r d_1/2 '
