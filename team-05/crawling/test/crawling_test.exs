defmodule CrawlingTest do
  use ExUnit.Case
  doctest Crawling

  test "greets the world" do
    assert Crawling.hello() == :world
  end
end
