import os
import sys
import ast
import astor
import copy
import unittest
from scalpel.core.mnode import MNode
from scalpel.SSA.const import SSA
src = """
c = 10
a = -1
if c>0:
    a = a+1
else:
    a = 0
total = c+a
"""
mnode = MNode("local")
mnode.source = src
mnode.gen_ast()
ast_node = mnode.ast
cfg = mnode.gen_cfg()
viz_config = cfg.build_visual('svg')
print(viz_config)
viz_config = copy.copy(viz_config)
viz_config.node("1", "#1\n c = 10\n a0 = -1\n if c > 0:")
viz_config.node("2", "#2\n a2 = a1+1")
viz_config.node("4", "#4\n a3 = 0")
viz_config.node("3", "#3\n total = c + φ(a2,a3）")
m_ssa = SSA()
ssa_results, const_dict = m_ssa.compute_SSA(cfg)
print(ssa_results)
