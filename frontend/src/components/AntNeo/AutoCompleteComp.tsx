import { useCallback, useState } from 'react';
import { neoQuery } from '@/utils/neoOperations';
import { AutoComplete } from 'antd';
import { debounce } from 'lodash';

export const AutoCompleteComp = ({
  nodeOptions,
  setGraphData,
}: {
  nodeOptions: any;
  setGraphData: (x: any) => void;
}) => {
  const [options, setOptions] = useState(nodeOptions);
  const searchHandler = (searchText: string) => {
    setOptions(
      nodeOptions.map((option: { options: any[] }) => ({
        ...option,
        options: option.options.filter((elem) => !elem.value.search(searchText)),
      })),
    );
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
