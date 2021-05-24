import React, {createRef, useEffect, useState} from 'react';
import Graphin, {GraphinContext} from '@antv/graphin';
import {ContextMenu, FishEye, Legend, MiniMap, Toolbar, Tooltip} from '@antv/graphin-components';

import type {GraphinData} from '@antv/graphin/es';
import {neoQuery} from '@/utils/neoOperations';
import {AntdTooltip} from './AntdTooltip';
import {dictUnique, edgesUnique} from '@/utils/useful';
import {CustomContent} from './ToolbarCustom';
import LayoutSelectorPanel from './LayoutSelectorPanel';
import CypherFunctionalPanel from './CypherFunctionalPanel';
import ActivateRelations from "@antv/graphin/es/behaviors/ActivateRelations";
import {message} from "antd";
import {ExpandAltOutlined, TagFilled} from "@ant-design/icons";

const {Menu} = ContextMenu

const nodeSize = 40;

const defaultLayout = {
  type: 'grid',
  preset: {
    type: 'concentric',
  },
  animation: true,
};

const nodeOptions = [
  {
    key: 'tag',
    icon: <TagFilled/>,
    name: '上卷',
  },
  {
    key: 'expand',
    icon: <ExpandAltOutlined/>,
    name: '下钻',
  },
];

export const DynamicLayout = ({port, pwd}: { port: string; pwd: string }) => {
  const graphinRef = createRef<Graphin>();

  const [layout, setLayout] = React.useState({...defaultLayout, animation: false});
  const [graphData, setGraphData] = useState<GraphinData>({nodes: [], edges: []} as GraphinData);
  const [visible, setVisible] = React.useState(false);
  const [layoutPanelVisible, setLayoutPanelVisible] = useState(true);
  const [funcPanelVisible, setFuncPanelVisible] = useState(false);

  useEffect(() => {
    localStorage.setItem('neo-port', port);
    localStorage.setItem('neo-pwd', pwd);

    const query = 'MATCH (n) RETURN n LIMIT 25';
    neoQuery(query).then((result) => {
      setGraphData(result);
      sessionStorage.setItem('graph', JSON.stringify(result));
    });
  }, []);

  // useEffect(() => {
  //   const {graph} = graphinRef.current;
  //   graph.on('node:dblclick', handleDrillDownClick);
  //   return () => {
  //     graph.off('node:dblclick', handleDrillDownClick);
  //   };
  // }, [graphData, graphinRef]);

  /**
   * 增量渲染节点
   * @param querySentence
   */
  const incrementRender = (querySentence: string) => {
    neoQuery(querySentence).then((result) => {
      const tmp_graph = JSON.parse(sessionStorage.getItem('graph') as string);
      const res_node = [...tmp_graph.nodes, ...result.nodes];
      const res_edge = [...tmp_graph.edges, ...result.edges];
      const ret = {nodes: dictUnique(res_node, 'queryId'), edges: edgesUnique(res_edge)};
      console.log('new data', tmp_graph, ret);
      setGraphData(ret);
      sessionStorage.setItem('graph', JSON.stringify(ret));
    });
  }

  /**
   * 处理下钻的请求
   * @param queryId
   */
  const handleDrillDownClick = (queryId: string) => {
    const sub_query = `MATCH r=(s)-->() WHERE ID(s) = ${queryId} RETURN r`;
    incrementRender(sub_query)
  };

  /**
   * 处理上卷的请求
   * @param queryId
   */
  const handleRollUpClick = (queryId: string) => {
    const sub_query = `MATCH r=()-->(s) WHERE ID(s) = ${queryId} RETURN r`;
    incrementRender(sub_query)
  }

  /**
   * 更新布局
   * @param previousType
   * @param type
   * @param defaultLayoutConfigs
   */
  const updateLayout = (previousType: any, type: any, defaultLayoutConfigs: any) => {
    console.log(previousType, type, defaultLayoutConfigs);
    setLayout({...defaultLayoutConfigs, type});
  };

  /**
   * 右键菜单
   * @param menuItem
   * @param menuData
   */
  const handleNodeClick = (menuItem: any, menuData: any) => {
    if (menuItem.name === '下钻') {
      handleDrillDownClick(menuData.queryId)
    } else if (menuItem.name === '上卷') {
      handleRollUpClick(menuData.queryId)
    } else {
      message.info(`元素：${menuData.id}，动作：${menuItem.name}`);
    }
  }

  /**
   * 画布右键菜单
   * @constructor
   */
  const CanvasMenu = () => {
    const {graph, contextmenu} = React.useContext(GraphinContext);
    const context = contextmenu.canvas;
    const handleDownload = () => {
      graph.downloadFullImage('neo-canvas', 'image/jpeg', {backgroundColor: 'white'});
      context.handleClose();
    };
    const callLayoutPanel = () => {
      setLayoutPanelVisible(!layoutPanelVisible)
      setFuncPanelVisible(true)
      context.handleClose();
    };
    const callCypherPanel = () => {
      setLayoutPanelVisible(true)
      setFuncPanelVisible(!funcPanelVisible)
      context.handleClose();
    };
    const callFishEye = () => {
      setVisible(true)
      context.handleClose();
    }
    return (
      <Menu bindType="canvas">
        <Menu.Item onClick={callLayoutPanel}>可视化布局面板</Menu.Item>
        <Menu.Item onClick={callCypherPanel}>Cypher功能面板</Menu.Item>
        <Menu.Item onClick={callFishEye}>使用鱼眼放大镜</Menu.Item>
        <Menu.Item onClick={handleDownload}>下载画布</Menu.Item>
      </Menu>
    );
  };

  return (
    <div>
      <Graphin
        data={graphData}
        layout={layout}
        ref={graphinRef}
        style={{height: '700px', width: '95%'}}
      >
        <ContextMenu style={{width: '80px'}}>
          <Menu options={nodeOptions} onChange={handleNodeClick} bindType="node"/>
        </ContextMenu>
        <ContextMenu style={{width: '160px'}} bindType="canvas">
          <CanvasMenu/>
        </ContextMenu>
        {/* <LayoutSelector> */}
        <Legend
          bindType="node"
          sortKey="nodeType"
          colorKey="style.keyshape.stroke"
          style={{right: '10%'}}
        >
          <Legend.Node/>
        </Legend>
        <LayoutSelectorPanel
          isVisible={layoutPanelVisible}
          setVisible={setLayoutPanelVisible}
          updateLayout={updateLayout}
        />
        <CypherFunctionalPanel
          isVisible={funcPanelVisible}
          setVisible={setFuncPanelVisible}
          graphData={graphData}
          setGraphData={setGraphData}
        />
        {/* </LayoutSelector> */}
        <Tooltip
          bindType="node"
          style={{
            transform: `translate(-${nodeSize / 2}px,-${nodeSize / 2}px)`,
          }}
        >
          <AntdTooltip/>
        </Tooltip>
        <Toolbar direction="horizontal" style={{position: 'absolute', right: '80%'}}>
          <CustomContent
            layoutPanelVisible={layoutPanelVisible}
            setLayoutPanelVisible={setLayoutPanelVisible}
            visible={visible}
            setVisible={setVisible}
            funcPanelVisible={funcPanelVisible}
            setFuncPanelVisible={setFuncPanelVisible}
          />
        </Toolbar>
        <MiniMap visible={true}/>
        <FishEye options={{}} visible={visible} handleEscListener={() => setVisible(false)}/>
        <ActivateRelations trigger="click"/>
      </Graphin>
    </div>
  );
};
