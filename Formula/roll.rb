class Roll < Formula
  include Language::Python::Virtualenv

  desc "Personal film roll index"
  homepage "https://github.com/katrinio/roll"
  url "https://github.com/katrinio/roll/archive/refs/tags/v0.7.0.tar.gz"
  sha256 "f4248d7d7429320078aad7274238635d99cf1321fa5d6d8c259a92faca366ac3"
  license "MIT"

  depends_on "python@3.12"

  resource "typer" do
    url "https://files.pythonhosted.org/packages/source/t/typer/typer-0.16.0.tar.gz"
    sha256 "af377ffaee1dbe37ae9440cb4e8f11686ea5ce4e9bae01b84ae7c63b87f1dd3b"
  end

  resource "prompt-toolkit" do
    url "https://files.pythonhosted.org/packages/source/p/prompt_toolkit/prompt_toolkit-3.0.51.tar.gz"
    sha256 "931a162e3b27fc90c86f1b48bb1fb2c528c2761475e57c9c06de13311c7b54ed"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    archive = testpath/"archive"
    system bin/"rl", "init", archive
    assert_predicate archive/".roll", :directory?
    assert_predicate archive/".roll"/"stock.toml", :exist?
  end
end
