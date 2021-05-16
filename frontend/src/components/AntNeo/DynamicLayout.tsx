import React, { createRef, useEffect, useState } from 'react';
import Graphin from '@antv/graphin';
import { FishEye, Legend, MiniMap, Toolbar, Tooltip } from '@antv/graphin-components';

import type { GraphinData } from '@antv/graphin/es';
import { neoQuery } from '@/utils/neoOperations';
import { AntdTooltip } from './AntdTooltip';
import { dictUnique, arrSubtraction, edgesUnique, normalUnique } from '@/utils/useful';
import { CustomContent } from './ToolbarCustom';
import LayoutSelectorPanel from './LayoutSelectorPanel';
import CypherFunctionalPanel from './CypherFunctionalPanel';
import type { DataNode } from 'rc-tree-select/lib/interface';

const nodeSize = 40;

interface autoComplete {
  label: string;
  options: { value: string; label?: string }[];
}

const defaultLayout = {
  type: 'grid',
  preset: {
    type: 'concentric',
  },
  animation: true,
};

export const DynamicLayout = ({ port, pwd }: { port: string; pwd: string }) => {
  console.log('mount dyn');
  const graphinRef = createRef<Graphin>();

  const [layout, setLayout] = React.useState({ ...defaultLayout, animation: false });
  const [graphData, setGraphData] = useState<GraphinData>({ nodes: [], edges: [] } as GraphinData);
  const [visible, setVisible] = React.useState(false);
  const [layoutPanelVisible, setLayoutPanelVisible] = useState(true);
  const [funcPanelVisible, setFuncPanelVisible] = useState(false);

  useEffect(() => {
    console.log('dyn use effect');
    localStorage.setItem('neo-port', port);
    localStorage.setItem('neo-pwd', pwd);

    // let query = 'MATCH p=()-[r:GeneIndications]->() RETURN p LIMIT 25'
    const query = 'MATCH (n:Herb) RETURN n LIMIT 25';
    neoQuery(query).then((result) => {
      setGraphData(result);
      sessionStorage.setItem('graph', JSON.stringify(result));
    });
  }, []);

  useEffect(() => {
    // @ts-ignore
    const { graph } = graphinRef.current;

    const handleDoubleClick = (evt: { item: any; target: any }) => {
      const { item } = evt; // 被操作的节点 item
      const sub_query = `MATCH r=(s)-->() WHERE ID(s) = ${item.getModel().queryId} RETURN r`;
      neoQuery(sub_query).then((result) => {
        const tmp_graph = JSON.parse(sessionStorage.getItem('graph') as string);
        const res_node = [...tmp_graph.nodes, ...result.nodes];
        const res_edge = [...tmp_graph.edges, ...result.edges];
        const ret = { nodes: dictUnique(res_node, 'queryId'), edges: edgesUnique(res_edge) };
        console.log('new data', tmp_graph, ret);
        setGraphData(ret);
        sessionStorage.setItem('graph', JSON.stringify(ret));
      });
    };

    graph.on('node:dblclick', handleDoubleClick);

    return () => {
      graph.off('node:dblclick', handleDoubleClick);
    };
  }, [graphData, graphinRef]);

  const updateLayout = (previousType: any, type: any, defaultLayoutConfigs: any) => {
    console.log(previousType, type, defaultLayoutConfigs);
    setLayout({ ...defaultLayoutConfigs, type });
  };

  const handleClose = () => {
    setVisible(false);
  };

  const renderNodeOptions = () => {
    const options: autoComplete[] = [];
    graphData.nodes.forEach((node) => {
      const type_id = options.findIndex((r) => node.nodeType === r.label);
      if (type_id === -1) {
        options.push({ label: node.nodeType, options: [{ value: node.s_name }] });
      } else {
        options[type_id].options.push({ value: node.s_name });
      }
    });
    return options;
  };

  const nodeRecurrence = (
    nodeId: string,
    nodeValue: string,
    newNodes: Record<string, string>,
    newEdges: Record<string, string[]>,
  ) => {
    // @ts-ignore
    if (Object.keys(newEdges).findIndex((elem) => elem === nodeId) === -1) {
      return {
        title: newNodes[nodeId],
        value: nodeValue + newNodes[nodeId],
      };
    }
    const tmp: { title: string; value: string; children: any[] } = {
      title: newNodes[nodeId],
      value: nodeValue + newNodes[nodeId],
      children: [],
    };
    newEdges[nodeId].forEach((targetNodeId) => {
      tmp.children.push(
        nodeRecurrence(targetNodeId, `${nodeValue}==>${targetNodeId}`, newNodes, newEdges),
      );
    });
    return tmp;
  };

  const renderTreeOptions = () => {
    const options: DataNode[] = [];
    const newNodes: Record<string, string> = {};
    const newEdges: Record<string, string[]> = {};
    const targetEdges: string[] = [];
    // 构建节点字典表
    graphData.nodes.forEach((node) => {
      newNodes[node.id] = node.s_name;
    });
    // 构建关系字典表
    graphData.edges.forEach((edge) => {
      targetEdges.push(edge.target);
      if (newEdges.hasOwnProperty(edge.source)) newEdges[edge.source].push(edge.target);
      else newEdges[edge.source] = [edge.target];
    });
    // 寻找根节点
    const root = arrSubtraction(Object.keys(newNodes), normalUnique(targetEdges));
    // 组建搜索树
    root.forEach((nodeId) => {
      // @ts-ignore
      options.push(nodeRecurrence(nodeId, nodeId, newNodes, newEdges));
    });
    console.log('tree option ', options);
    return options;
  };

  // const layout = layouts.find(item => item.type === type);
  return (
    <div>
      <Graphin
        data={graphData}
        layout={layout}
        ref={graphinRef}
        // theme={{: ''}}
        style={{ height: '700px', width: '95%' }}
      >
        {/* <LayoutSelector> */}
        <Legend
          bindType="node"
          sortKey="nodeType"
          colorKey="style.keyshape.stroke"
          style={{ right: '10%' }}
        >
          <Legend.Node />
        </Legend>
        {/* <Statistic /> */}
        <LayoutSelectorPanel
          isVisible={layoutPanelVisible}
          setVisible={setLayoutPanelVisible}
          updateLayout={updateLayout}
        />
        <CypherFunctionalPanel
          isVisible={funcPanelVisible}
          setVisible={setFuncPanelVisible}
          nodeOptions={renderNodeOptions()}
          setGraphData={setGraphData}
          treeOptions={renderTreeOptions()}
        />
        {/* </LayoutSelector> */}
        <Tooltip
          bindType="node"
          style={{
            transform: `translate(-${nodeSize / 2}px,-${nodeSize / 2}px)`,
          }}
        >
          <AntdTooltip />
        </Tooltip>
        <Toolbar direction="horizontal" style={{ position: 'absolute', right: '80%' }}>
          <CustomContent
            layoutPanelVisible={layoutPanelVisible}
            setLayoutPanelVisible={setLayoutPanelVisible}
            visible={visible}
            setVisible={setVisible}
            funcPanelVisible={funcPanelVisible}
            setFuncPanelVisible={setFuncPanelVisible}
          />
        </Toolbar>
        <MiniMap visible={true} />
        <FishEye options={{}} visible={visible} handleEscListener={handleClose} />
      </Graphin>
    </div>
  );
};
