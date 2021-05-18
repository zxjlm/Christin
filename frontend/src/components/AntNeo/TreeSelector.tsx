import {Button, TreeSelect} from 'antd';
import type {DataNode} from 'rc-tree-select/lib/interface';
import {arrSubtraction, normalUnique} from "@/utils/useful";
import type {GraphinData} from "@antv/graphin/es";
import {useState} from "react";
import {neoQuery} from "@/utils/neoOperations";

const {SHOW_PARENT} = TreeSelect;

export const TreeSelector = ({graphData, setGraphData}: { graphData: GraphinData, setGraphData: (x: any) => void }) => {
  console.log('gd', graphData)
  const [selected, setSelected] = useState<string[]>([]);

  const onChange = (value: any[], labelList: any[]) => {
    const selectedId = labelList.map(item => (graphData.nodes.filter(node => node.s_name === item))).flat()
    setSelected(selectedId.map(item => item.queryId))
  }

  const handleClick = () => {
    console.log(selected.toString())
    neoQuery(`MATCH (n) WHERE id(n) IN [${selected.toString()}] RETURN n`).then((result) => {
      setGraphData(result);
      sessionStorage.setItem('graph', JSON.stringify(result));
    });
  };

  /**
   * 递归构建搜索树的子节点
   * @param nodeId
   * @param nodeValue
   * @param newNodes
   * @param newEdges
   */
  const nodeRecurrence = (
    nodeId: string,
    nodeValue: string,
    newNodes: Record<string, string>,
    newEdges: Record<string, string[]>,
  ) => {
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

  /**
   * 渲染树节点
   */
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
      options.push(nodeRecurrence(nodeId, nodeId, newNodes, newEdges));
    });
    return options;
  };

  return (
    <div>
      <TreeSelect
        treeData={renderTreeOptions()}
        onChange={onChange}
        treeCheckable={true}
        showCheckedStrategy={SHOW_PARENT}
        placeholder={'Please select'}
        allowClear={true}
        style={{
          width: '100%',
        }}
      />
      <Button onClick={handleClick}>确认选择</Button>
    </div>
  );
};
