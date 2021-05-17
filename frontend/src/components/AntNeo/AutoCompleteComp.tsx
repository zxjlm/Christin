import {useCallback, useState} from 'react';
import {neoQuery} from '@/utils/neoOperations';
import {AutoComplete} from 'antd';
import {debounce} from 'lodash';
import type {GraphinData} from "@antv/graphin/es";

interface autoComplete {
  label: string;
  options: { value: string; label?: string }[];
}

export const AutoCompleteComp = ({graphData, setGraphData}: {
  graphData: GraphinData;
  setGraphData: (x: any) => void;
}) => {

  /**
   * 渲染节点
   */
  const renderNodeOptions = () => {
    const sub_options: autoComplete[] = [];
    graphData.nodes.forEach((node) => {
      const type_id = sub_options.findIndex((r) => node.nodeType === r.label);
      if (type_id === -1) {
        sub_options.push({label: node.nodeType, options: [{value: node.s_name}]});
      } else {
        sub_options[type_id].options.push({value: node.s_name});
      }
    });
    return sub_options;
  };

  const allOptions = renderNodeOptions()

  const [options, setOptions] = useState(allOptions);

  const searchHandler = (searchText: string) => {
    setOptions(
      allOptions.map((item: autoComplete) => ({
        ...item,
        options: item.options.filter((elem) => !elem.value.search(searchText)),
      })),
    );
    console.log(searchText)
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const debounceSearch = useCallback(
    debounce((searchText: any) => searchHandler(searchText), 1000),
    [],
  );

  const onSearch = (searchText: string) => {
    debounceSearch(searchText);
  };

  const onSelect = (selectText: string) => {
    neoQuery(`MATCH (n) WHERE n.s_name='${selectText}' RETURN n`).then((result) => {
      setGraphData(result);
      sessionStorage.setItem('graph', JSON.stringify(result));
    });
  };

  return (
    <AutoComplete
      dropdownMatchSelectWidth={500}
      style={{
        width: 250,
        marginTop: 8,
        marginLeft: 20,
      }}
      options={options}
      onSearch={onSearch}
      placeholder={'节点名称'}
      onSelect={onSelect}
    />
  );
};
